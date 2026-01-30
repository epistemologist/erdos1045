import sympy
import torch
from math import sqrt, isclose
from typing import List, Tuple

def delta_with_grad(X: List[float]) -> Tuple[float, List[float]]:
    # Using pytorch to calculate gradient to floating point accuracy
    X_torch = [torch.tensor(
        x,
        dtype=torch.float64,
        requires_grad=True) 
        for x in X
    ]
    def _delta(X: List):
        out = 1
        for i in range(len(X)//2):
            for j in range(i): 
                out *= ( X[2*i]-X[2*j] )**2 + ( X[2*i+1]-X[2*j+1] )**2
        return out
    delta_val = _delta(X_torch)
    delta_val.backward()
    return (
        float(delta_val.detach()),
        [float( i.grad.detach() ) for i in X_torch ]
    )

def verify_kkt(x_opt: List[float]):
    # Phrase this as a constrained optimization problem
    # min -delta(x) \in R^n subject to various constraints g_i(x) <= 0
    # We have n(n+1)/2 constriants for each 1<=i<j<=n:
    # | z_i - z_j | <= 2
    # => | z_i - z_j |^2 = (x[2*i] - x[2*j])^2 + (x[2*i+1] - x[2*j+1])^2 <= 4
    # => (x[2*i] - x[2*j])^2 + (x[2*i+1]-x[2*j+1])^2 - 4 <= 0
    n = len(x_opt)//2
    x = [sympy.symbols(f'x{i}') for i in range(1,len(x_opt)+1)]
    g = []
    for i in range(n):
        for j in range(i):
            g.append((x[2*i] - x[2*j])**2 + (x[2*i+1]-x[2*j+1])**2 - 4)
            
    # We follow https://algorithmsbook.com/optimization/files/optimization.pdf p 187
    f_val, f_grad = delta_with_grad(x_opt)
    mu = [sympy.symbols(f"mu{i}") for i in range(1, len(g)+1)]
    # 1. Feasability
    for i in range(len(g)):
        curr_constraint = g[i]
        # 3. Complementary slackness
        # Here, use floating point comparison
        # if g_i(x) = 0, then mu_i = 0
        if abs( curr_constraint.subs({xi: xval for xi, xval in zip( x,x_opt)}) ) < 1e-12:
            mu[i] = 0
    # 4. Stationarity
    # \grad f(x_opt) + \sum_{i} \mu_i \grad g_i(x_opt) = 0
    summands = [f_grad]
    for i in range(len(g)):
        if mu[i] != 0:
            grad_g_i = [sympy.diff(g[i], xi).subs({xi: xval for xi, xval in zip( x,x_opt)})  for xi in x]
            summands.append([mu[i]*y for y in grad_g_i])
    # [s[i] for s in summands] 
    out = [0 for _ in range(len(summands[0]))]
    for s in summands:
        for i in range(len(s)):
            out[i] += s[i]
    return out


x = [0,0,sqrt(3),1,sqrt(3),-1,2,0]
verify_kkt(x)