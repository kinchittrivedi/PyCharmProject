# Hotel_order_chatbot.py
import os
import re
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------
# Load config & initialize client
# -----------------------
load_dotenv()
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")

client = OpenAI(
    api_key=PERPLEXITY_KEY,
    base_url="https://api.perplexity.ai"
)

# Pinned prompt used for stricter retries when the model drifts
PINNED_SYSTEM_PROMPT = (
    "You are a focused hotel booking assistant. "
    "Only answer questions about hotels, reservations, rooms, amenities, dates, pricing, "
    "and related travel lodging tasks. If the user's input says they don't need help, finish with a short farewell. "
    "Do NOT change topic to unrelated domains (for example: 3D printing, electronics, recipes, etc.). "
    "Be brief and helpful."
)

# -----------------------
# Response parsing helpers
# -----------------------
def extract_content_from_choice(choice, response):
    """Robust extraction of assistant text from a response.choice item."""
    try:
        msg = getattr(choice, "message", None)
    except Exception:
        msg = None

    if msg is None and isinstance(choice, dict):
        msg = choice.get("message")

    if isinstance(msg, dict):
        return msg.get("content") or msg.get("text") or None

    if msg is not None:
        content = getattr(msg, "content", None) or getattr(msg, "text", None)
        if content:
            return content

    if isinstance(choice, dict):
        direct = choice.get("text") or choice.get("content")
        if direct:
            return direct

    direct_attr = getattr(choice, "text", None) or getattr(choice, "content", None)
    if direct_attr:
        return direct_attr

    top_level = getattr(response, "output_text", None)
    if top_level:
        return top_level

    return None

def get_reply(messages, model="sonar-pro"):
    """
    Send messages to the LLM and return the assistant reply text.
    This function is safe to call from a background thread.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
    except Exception as e:
        return f"[Error calling model: {e}]"

    try:
        first_choice = response.choices[0]
    except Exception:
        return f"[Unexpected response shape — see console for raw response: {response}]"

    content = extract_content_from_choice(first_choice, response)
    if content is None:
        print("Raw response for debugging:", response)
        return "[Could not extract model reply — see console]"

    return content

# -----------------------
# Goodbye / short-no detectors
# -----------------------
GOODBYE_REGEX = re.compile(
    r"^(?:bye|goodbye|see you|see ya|thanks(?:\s*(?:,)?\s*(?:that's it|that'?s all)?)?|thank you(?: very much)?|no thanks|no thank you|that's all|that's it|i'm good|i am good|all good|never mind|no need|i'm done|i am done|done|stop|cancel|abort|no support needed|no support|no)$",
    re.IGNORECASE,
)

def is_goodbye(text: str) -> bool:
    """Conservative test whether the text indicates the user or assistant wants to end the session."""
    if not text:
        return False
    t = text.strip()
    if GOODBYE_REGEX.match(t):
        return True

    short_threshold = 40
    lower = t.lower()
    tokens = ["thanks", "thank you", "no thanks", "that's all", "thats all", "that's it", "thats it",
              "i'm good", "i am good", "done", "never mind", "no need", "no", "nope", "nah"]
    if len(t) <= short_threshold and not t.endswith("?"):
        for tok in tokens:
            if tok in lower:
                return True

    if re.search(r"\b(don't need|do not need|not needed|no longer need)\b", lower):
        return True

    return False

def short_no_following_question(user_text: str, last_assistant_text: str) -> bool:
    """
    If user says a short 'no' right after assistant asked a question, treat as goodbye.
    """
    if not user_text:
        return False
    ut = user_text.strip().lower()
    if ut not in {"no", "nah", "nope", "n"}:
        return False
    if not last_assistant_text:
        return True
    if last_assistant_text.strip().endswith("?"):
        return True
    if re.search(r"\b(would you|do you want|should i|want me to|shall i|is that|confirm)\b", last_assistant_text, re.IGNORECASE):
        return True
    return False

# -----------------------
# Off-topic detection and retry logic
# -----------------------
HOTEL_KEYWORDS = {"hotel", "room", "booking", "book", "check-in", "checkin", "check out", "check-out", "reservation", "amenity", "suite", "rate", "night", "nights", "guest", "guests", "stay", "accommodation", "mumbai", "andheri", "andheri east"}
OFFTOPIC_KEYWORDS = {"3d", "3-d", "printing", "printer", "filament", "support material", "supports", "brim", "raft", "slicer", "prusaslicer", "cura", "layer height"}

def is_off_topic(text: str) -> bool:
    """Heuristic: returns True if reply seems about an unrelated domain and lacks hotel tokens."""
    if not text:
        return False
    lower = text.lower()
    found_off = any(tok in lower for tok in OFFTOPIC_KEYWORDS)
    found_hotel = any(tok in lower for tok in HOTEL_KEYWORDS)
    return found_off and not found_hotel

# -----------------------
# GUI Application
# -----------------------
class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("Hotel Booking Chatbot (Perplexity)")
        root.geometry("700x520")

        # Conversation display (scrollable)
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Frame for input and button
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill=tk.X, padx=8, pady=(0,8))

        self.entry = tk.Entry(bottom_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,8))
        self.entry.bind("<Return>", self.on_send_pressed)

        self.send_btn = tk.Button(bottom_frame, text="Send", width=12, command=self.on_send_pressed)
        self.send_btn.pack(side=tk.RIGHT)

        # Conversation state (list of role/content dicts)
        self.messages = [
            {"role": "system", "content": PINNED_SYSTEM_PROMPT}
        ]

        # If key missing, show a warning popup once
        if not PERPLEXITY_KEY:
            messagebox.showwarning("API key missing", "PERPLEXITY_API_KEY not found in .env. The app will not be able to call the model.")

        # Greet the user (and store greeting in history)
        initial_greet = "Hello — I can help you book hotels. Tell me what you need (e.g., dates, location)."
        self.append_message("assistant", initial_greet)
        self.messages.append({"role": "assistant", "content": initial_greet})

        # track whether the conversation has ended (to disable input)
        self.ended = False
        self.lock = threading.Lock()  # guard for shutdown

    def append_message(self, role, text):
        """Append a message to the chat display (main-thread UI update)."""
        self.chat_display.configure(state=tk.NORMAL)
        if role == "user":
            self.chat_display.insert(tk.END, f"You: {text}\n\n")
        else:
            self.chat_display.insert(tk.END, f"AI: {text}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state=tk.DISABLED)

    def set_input_state(self, enabled: bool):
        """Enable/disable user input controls."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.entry.configure(state=state)
        self.send_btn.configure(state=state)
        if enabled:
            self.entry.focus_set()

    # -----------------------
    # Graceful end session helper
    # -----------------------
    def _end_session(self, *, close_window: bool = True, farewell_shown: bool = True):
        """
        End the conversation safely on the main thread.
        - close_window=True will destroy the GUI after a short delay so the user sees the farewell.
        """
        with self.lock:
            if getattr(self, "ended", False):
                return
            self.ended = True

        # Disable input immediately
        self.set_input_state(False)

        if close_window:
            def do_destroy():
                try:
                    self.root.update_idletasks()
                    self.root.destroy()
                except Exception:
                    try:
                        self.root.quit()
                    except Exception:
                        pass
            # small delay so farewell is visible
            self.root.after(700, do_destroy)

    # -----------------------
    # Send button / enter handler
    # -----------------------
    def on_send_pressed(self, event=None):
        if self.ended:
            return "break"

        user_text = self.entry.get().strip()
        if not user_text:
            return "break"

        # Clear entry immediately
        self.entry.delete(0, tk.END)

        # Local goodbye detection (end deterministically without API call)
        last_assistant = self.messages[-1]["content"] if self.messages and self.messages[-1]["role"] == "assistant" else ""
        if is_goodbye(user_text) or short_no_following_question(user_text, last_assistant):
            farewell_text = "Okay — I'm glad I could help. If you need anything later, just ask. Goodbye!"
            self.append_message("assistant", farewell_text)
            self.messages.append({"role": "assistant", "content": farewell_text})
            # schedule safe end on the main thread (shows farewell briefly, then closes)
            self.root.after(0, lambda: self._end_session(close_window=True, farewell_shown=True))
            return "break"

        # Normal flow: display user's message and send to model
        self.append_message("user", user_text)
        self.messages.append({"role": "user", "content": user_text})

        # show typing placeholder and disable input while waiting
        self.append_message("assistant", "[AI is typing...]")
        self.set_input_state(False)

        # Start background thread to call API
        threading.Thread(target=self._background_get_reply, daemon=True).start()
        return "break"

    # -----------------------
    # Background API call
    # -----------------------
    def _background_get_reply(self):
        # Call model with current conversation
        try:
            reply = get_reply(self.messages)
        except Exception as e:
            reply = f"[Error during get_reply: {e}]"

        # If the assistant reply seems off-topic, retry once with very strict system prompt
        if is_off_topic(reply):
            print("Detected off-topic reply; retrying with pinned strict system prompt...")
            last_user = None
            for m in reversed(self.messages):
                if m["role"] == "user":
                    last_user = m
                    break
            retry_messages = [
                {"role": "system", "content": PINNED_SYSTEM_PROMPT},
            ]
            if last_user:
                retry_messages.append(last_user)
            try:
                retry_reply = get_reply(retry_messages)
            except Exception as e:
                retry_reply = f"[Retry error: {e}]"
            if not is_off_topic(retry_reply):
                reply = retry_reply
            else:
                print("Retry also off-topic. Suppressing out-of-domain content.")
                reply = "Sorry — I misunderstood earlier. I'm a hotel booking assistant; I can help with hotel reservations, dates, locations, rooms, and amenities. Do you still need help with a booking?"

        # Update UI on main thread
        self.root.after(0, self._finish_reply, reply)

    # -----------------------
    # Finish reply (UI update on main thread)
    # -----------------------
    def _finish_reply(self, reply_text):
        # Remove the "[AI is typing...]" placeholder
        self.chat_display.configure(state=tk.NORMAL)
        content = self.chat_display.get("1.0", tk.END).rstrip()
        if content.endswith("AI: [AI is typing...]"):
            content = content[: -len("AI: [AI is typing...]")].rstrip()
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.insert(tk.END, content + "\n\n")
        self.chat_display.configure(state=tk.DISABLED)

        # Show assistant's real reply
        self.append_message("assistant", reply_text)

        # Add to full message history
        self.messages.append({"role": "assistant", "content": reply_text})

        # End if assistant itself gives a clear farewell
        if is_goodbye(reply_text) or re.search(r"\b(bye|goodbye|see you|take care|farewell)\b", reply_text, re.IGNORECASE):
            # schedule safe end on the main thread so destroy happens from main loop
            self.root.after(0, lambda: self._end_session(close_window=True, farewell_shown=True))
            return

        # Otherwise continue normally
        self.set_input_state(True)

# -----------------------
# Entry point
# -----------------------
def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
