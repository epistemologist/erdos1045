# Code from https://github.com/karpathy/micrograd/blob/master/micrograd/engine.py
# Rewritten to work with intervals

from mpmath import iv, mpf

iv.dps = 15; mpf.dps = 15

Interval = iv.mpf

class Value:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = Interval([ 0, 0 ] )
        # internal variables used for autograd graph construction
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op # the op that produced this node, for graphviz / debugging / etc

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward

        return out

    def backward(self):
        # topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self): # -self
        return self * Interval([-1, -1])
    
    def __radd__(self, other): # other + self
        return self + other

    def __sub__(self, other): # self - other
        return self + (-other)
    def __rsub__(self, other): # other - self
        return other + (-self)

    def __rmul__(self, other): # other * self
        return self * other
    def __truediv__(self, other): # self / other
        return self * other**-1
    def __rtruediv__(self, other): # other / self
        return other * self**-1

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"

from typing import List
from math import sqrt
import sympy


def make_interval(x: float) -> Interval:
    return Interval([x-1e-9, x+1e-9])

def delta(X: List[Interval]):
    z = [Value(make_interval(x)) for x in X]
    out = Value(Interval([1,1]))
    for i in range(len(X)//2):
        for j in range(i): 
            out *= (z[2*i]-z[2*j])**2 + (z[2*i+1]-z[2*j+1])**2
    out.backward()
    return (out, z)

z_opt = [0,0,sqrt(3),1,sqrt(3),-1,2,0]

z = [sympy.symbols(f"z{i}") for i in range(8)]

d = 1
for i in range(4):
    for j in range(i):
        d *= (z[2*i]-z[2*j])**2 + (z[2*i+1]-z[2*j+1])**2
grad = [sympy.diff(d, zi).evalf(
    subs = {zj: z_val for zj, z_val in zip(z, z_opt)}
) for zi in z]

