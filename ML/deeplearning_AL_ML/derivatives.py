from sympy import symbols, diff

J = (3)**2
J_epsilon = (3 + 0.001)**2
k = (J_epsilon - J)/0.001    # difference divided by epsilon
print(f"J = {J}, J_epsilon = {J_epsilon}, dJ_dw ~= k = {k:0.6f} ")

J = (3)**2
J_epsilon = (3 + 0.000000001)**2
k = (J_epsilon - J)/0.000000001
print(f"J = {J}, J_epsilon = {J_epsilon}, dJ_dw ~= k = {k} ")

J, w = symbols('J, w')
J=w**2
dJ_dw = diff(J,w)
print(dJ_dw)

print(dJ_dw.subs([(w,2)]))    # derivative at the point w = 2

J=w**3
dJ_dw = diff(J,w)
print(dJ_dw)

print(dJ_dw.subs([(w,2)]))

J = (2)**3
J_epsilon = (2+0.001)**3
k = (J_epsilon - J)/0.001
print(f"J = {J}, J_epsilon = {J_epsilon}, dJ_dw ~= k = {k} ")

J= 1/w
dJ_dw = diff(J,w)
print(dJ_dw)

print(dJ_dw.subs([(w,2)]))

J = 1/2
J_epsilon = 1/(2+0.001)
k = (J_epsilon - J)/0.001
print(f"J = {J}, J_epsilon = {J_epsilon}, dJ_dw ~= k = {k} ")


