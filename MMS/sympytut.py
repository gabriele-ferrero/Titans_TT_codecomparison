from sympy import *

x, y, t = symbols("x y t")
init_printing(use_unicode=True)
fun = 2 + cos(2 * pi * x) * cos(2 * pi * y)
a = diff(fun, x) + diff(fun, y)
b = -(diff(a, x) + diff(a, y))
print(b)
print(a)
fun2 = -8 * pi**2 * sin(2 * pi * x) * sin(2 * pi * y) + 8 * pi**2 * cos(
    2 * pi * x
) * cos(2 * pi * y)
c = integrate(integrate(fun2, x, y), x, y)
print(c)
