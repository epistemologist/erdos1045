import symengine # Wrapper around sympy written in C++ for faster symbol manipulation
import sympy

from sympy import I, re, im
# Given n, generate \Delta^2(n) as a symbolic expression in (x_1, x_2, \cdots, x_{2n-1}, x_{2n})
def Delta(n):
	X = [ symengine.var(f'X{i}') for i in range(1, 2*n+1)]
	out = 1
	for i in range(n):
		for j in range(i):
			zi_real = X[2*i]; zj_real = X[2*j]
			zi_imag = X[2*i+1]; zj_imag = X[2*j+1]
			out *= (zi_real - zj_real)**2 + (zi_imag - zj_imag)**2
	return (X, symengine.expand( out ) )


def verify_optimum(n, optimum):
	X, delta_expr = Delta(n)
	X_opt = sum([[re(z), im(z)] for z in optimum], [])
	gradient = [
		sympy.diff(delta_expr, xi).subs({Xi: Xi_val for Xi, Xi_val in zip(X, X_opt)})
		for xi in X
	]
	hessian_matrix = sympy.Matrix( [
		[sympy.diff(delta_expr, X[i], X[j]).subs({Xi: Xi_val for Xi, Xi_val in zip(X, X_opt)}) for j in range(len(X))]
		for i in range(len(X))
	])
	return X, gradient, hessian_matrix

# Some code for n=3 case
X, delta_expr = Delta(3)
x1, x2, x3 = sympy.symbols("x1 x2 x3")
# Reparametrize - rotate and translate to set (X1, X2), (X3, X4), (X5, X6) -> (0,0), (0,x1), (x2, x3)
delta_expr = delta_expr.subs({i:j for i,j in zip(X, [0,0,0, x1, x2, x3])})
# Verify that equilateral triangle maximizes Delta(n) in this case
# i.e. x1,x2,x3 = 2,sqrt(3), 1

print(delta_expr)
