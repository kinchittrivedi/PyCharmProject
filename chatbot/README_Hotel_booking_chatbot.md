# Hotel_order_chatbot (Perplexity GUI)

A simple desktop chatbot (Tkinter) that uses Perplexity's OpenAI-compatible API to help users with hotel bookings. The GUI supports conversational history, off-topic suppression, automatic goodbye detection (both user and assistant), and a graceful shutdown when the session ends.

---

## Prerequisites

- **Python 3.9+** (3.10 or 3.11 recommended)
- A Perplexity API key (you must have a Perplexity Pro or otherwise valid key)
- Required Python packages (install via `pip`):
  ```bash
  pip install openai python-dotenv
  ```

**Notes**
- The code uses the `openai` Python SDK but points the client to Perplexity's OpenAI-compatible base URL (`https://api.perplexity.ai`).
- The GUI is built with Tkinter (bundled with standard Python on most platforms).

---

## Files

- `Hotel_order_chatbot.py` — Full program (GUI + all helper functions).
- `.env` — Local environment file with `PERPLEXITY_API_KEY`.

---

## Setup

1. Create a `.env` file in the project root:

   ```
   PERPLEXITY_API_KEY=pxyz-...your-key-here...
   ```

2. Install packages:

   ```
   pip install openai python-dotenv
   ```

3. Run the program:

   ```
   python Hotel_order_chatbot.py
   ```

---

## Function Reference

### extract_content_from_choice
Extracts assistant text robustly across SDK formats.

### get_reply
Sends conversation to Perplexity and returns assistant reply.

### is_goodbye
Detects if the user or assistant message indicates conversation end.

### short_no_following_question
Treats a short “no” after a direct assistant question as goodbye.

### is_off_topic
Detects unrelated domains (e.g., 3D printing) and triggers retry logic.

### ChatApp (Tkinter GUI)
Handles UI, message history, threading, reply handling, shutdown, and off-topic suppression.

---

## Sample Interaction

### Normal
```
AI: Hello — I can help you book hotels.
You: Need a hotel in Andheri East.
AI: Sure — how many guests?
```

### Goodbye
```
You: no thanks
AI: Okay — Goodbye!
```

### Off-topic suppression
```
You: need a hotel in mumbai
AI: [Hallucinated text suppressed]
AI: Sorry — I'm a hotel booking assistant...
```

---

## Troubleshooting

- Missing key → create `.env`
- API error → check key and network
- Off-topic → safe fallback message shown

---

## Enhancements you can add
- New Chat button  
- Save conversation  
- Dark mode/theme  
- Streaming output  
