from sympy import *

x, y, t = symbols("x y t")
init_printing(use_unicode=True)
fun = (1 + x**2) * t
fun2 = fun * fun * 10
a = diff(fun, t) - diff(diff(fun, x), x)
b = diff(fun2, t) - diff(diff(fun2, x), x)
print(a)
print(b)
e = solve(diff(fun, x) - diff(fun2, x), x)
# 80*pi^2*(t + 1)^2*(cos(2*pi*x) + 1)*cos(2*pi*x) - 80*pi^2*(t + 1)^2*sin(2*pi*x)^2 + 10*(2*t + 2)*(cos(2*pi*x) + 1)^2
