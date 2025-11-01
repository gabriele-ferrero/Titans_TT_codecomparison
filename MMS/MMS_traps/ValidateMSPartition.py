from sympy import *

x, y, t = symbols("x y t")
init_printing(use_unicode=True)
fun =( 1+cos(2*pi*x) *cos(2*pi*y) )*t
fun2 = fun * 10
a = diff(fun, t) - diff(diff(diff(diff(fun, x), x),y),y)
b = diff(fun2, t) - diff(diff(fun2, x), x)
print(a)
print(b)
e = solve(diff(fun, x) - diff(fun2, x), x)
# 80*pi^2*(t + 1)^2*(cos(2*pi*x) + 1)*cos(2*pi*x) - 80*pi^2*(t + 1)^2*sin(2*pi*x)^2 + 10*(2*t + 2)*(cos(2*pi*x) + 1)^2
