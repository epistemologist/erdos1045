from scipy.optimize import differential_evolution
from typing import List
from math import inf
from sys import argv
from time import time

import matplotlib.pyplot as plt
import numpy as np

def gen_erdos_problem(n):
    def delta(X: List[float]) -> float:
        """
        # X represents list of complex numbers
        # [Re(z1), Im(z1), ..., Re(zn), Im(zn)]
        # We want to maximize Delta(z_1 ... z_n) = prod_{i != j} |z_i - z_j|
        # For ease of calculation, we instead calculate Delta^2
        """
        out = 1.
        # First check if | zi - zj | < 2 for all i, j
        for i in range(n):
            for j in range(n):
                if (X[2*i]-X[2*j])**2 + (X[2*i+1]-X[2*j+1])**2 > 4:
                    return inf
        for i in range(n):
            for j in range(i):
                # out *= | zi - zj |^2
                zi_real = X[2*i]; zj_real = X[2*j]
                zi_imag = X[2*i+1]; zj_imag = X[2*j+1]
                tmp_real = zi_real - zj_real; tmp_imag = zi_imag - zj_imag
                out *= tmp_real * tmp_real + tmp_imag * tmp_imag
        return -out # Note that scipy minimizes, so return negative
    return delta

X = []
Y = []

N = int(argv[1])
START_TIME = time()

def callback(intermediate_result):
    global N, X, Y, START_TIME
    res = intermediate_result
    X.append(res.nit); Y.append(res.fun)
    if res.nit % 1 == 0:
        print(f"[+] N: {N} - time_elapsed: {time()-START_TIME}, iter: {res.nit}, fun: {res.fun}")

delta = gen_erdos_problem(N)
res = differential_evolution(
    delta,
    bounds=[(2,2) for _ in range(3)] + [(0,4) for _ in range(2*N-3)],
    maxiter=100_000,
    popsize=1000,
    rng=0,
    callback=callback,
)
# Plot the value of Delta over optimization
#plt.plot( X, [ -y for y in Y ] )
#plt.show()
# Unpack the values of z
z = [re+im*1j for re, im in zip( res.x[0::2], res.x[1::2] ) ]
# Print the maximizing value of z
# print(f"[!] f_max = {-res.fun} @ z = {z}")
# Plot z in the complex plane
plt.axis('equal')
plt.scatter([i.real for i in z], [i.imag for i in z],s=200)
plt.savefig(f"./plots/{N}.png")
with open(f"./maxima/{N}.txt", 'w') as f:
    for i in z:
        f.write(str(i)+"\n")
