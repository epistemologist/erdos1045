from __future__ import annotations
from typing import List, Optional
from mpmath import iv, mpf
from itertools import product, pairwise
from collections import defaultdict
from math import prod
import matplotlib.pyplot as plt
from tqdm import tqdm

iv.dps = 15; mpf.dps = 15
iv.pretty = True

# Monkey patch some utility functions to mpmath interval
iv.mpf.left = lambda self: mpf(self.a)
iv.mpf.right = lambda self: mpf(self.b)
iv.mpf.size = lambda self: self.right() - self.left()

def split_interval(I: iv.mpf) -> List[iv.mpf]:
	# Split interval into two equally divided intervals
	return (
		iv.mpf( [I.a, (I.a + I.b)/2] ),
		iv.mpf( [(I.a + I.b)/2, I.b] )
	) if I.size() > 0 else [I]

iv.mpf.split = lambda self: split_interval(self)
Interval = iv.mpf

class ComplexPolycube:
	# Class to represent subset of C^n represented by product of boxes in C
	# i.e. S = \prod_{i=1^n} S_i
	# where S_i = { u + v i : a_i <= u <= b_i, c_i <= v <= d_i }
	# Let R_i = [a_i, b_i], I_i = [c_i, d_i]
	# We keep an array of [R_1, I_1, ..., R_n, I_n]
	def __init__(self, z: List[Interval]):
		assert len(z) % 2 == 0
		self.n = len(z) // 2
		self.z = z
	def __repr__(self):
		out = []
		for i in range(self.n):
			out.append( f"z{i+1}={self.z[2*i]}+{self.z[2*i+1]}i" )
		return " , ".join( out )
	def to_complex_intervals(self) -> List[iv.mpc]:
		# May be useful, but these do not have many features supported for some reason...
		return [iv.mpc(self.z[2*i], self.z[2*i+1]) for i in range(self.n)]
	def volume(self) -> mpf:
		return prod([ I.size() for I in self.z[3:]]) # First 3 dimensions have size 0 as they are predetermined
	def split(self, dim_idx: List[int]) -> List[ComplexPolycube]:
		new_intervals = []
		for i in range(2*self.n):
			if i in dim_idx:
				new_intervals.append(self.z[i].split())
			else:
				new_intervals.append([ self.z[i] ])
		return [ComplexPolycube(z) for z in product(*new_intervals)]
	def plot(self) -> None:
		#TODO: Implement with matplotlib
		return

def delta(S: ComplexPolycube) -> Optional[Interval]:
	# First check if |z_i - z_j| < 2 for all i != j
	out = Interval([1., 1.])
	Z = S.to_complex_intervals()
	for i in range(len(Z)):
		for j in range(i):
			tmp = Z[i] - Z[j]
			norm = ( tmp.real ** 2 + tmp.imag ** 2  )
			if norm.left() > 4:
				return None
			out *= norm
	return out

def generate_initial_polycube(n):
	return ComplexPolycube(
		[Interval([2,2]) for _ in range(3)] +
		[Interval([0,4]) for _ in range(2*n-3)]
	)

class SearchNode:
	def __init__(
			self,
			c: ComplexPolycube,
			split_idx: int = 3
	):
		self.c = c
		if split_idx < len(c.z):
			self.split_idx = split_idx
		else:
			self.split_idx = 3
		self.delta = delta(c)
	def __repr__(self):
		return repr(self.c)
	def __str__(self):
		return repr(self.c)
	def gen_next_nodes(self) -> List[SearchNode]:
		return [
			SearchNode(
				c=c,
				split_idx=(self.split_idx+1)
			)
			for c in self.c.split([self.split_idx])
		]

def prune_nodes(nodes: List[SearchNode]) -> List[SearchNode]:
	# Given a set of nodes representing a set U \subseteq C^n with delta(x*) \in U
	# This function will return a U' \subseteq U such that delta(x*) \in U'
	nodes_out = []
	delta_sup = 0 # Find maximum of delta over all nodes
	for node in tqdm( nodes ):
		for next_node in node.gen_next_nodes():
			if next_node.delta is not None:
				nodes_out.append(next_node)
				delta_sup = max(delta_sup, next_node.delta.left())
	return list( filter(lambda node: node.delta.right() >= delta_sup, nodes_out) )

def get_volume(nodes: List[SearchNode]) -> float:
	return sum([node.c.volume() for node in nodes])


N = 5
# TOL = mpf("1e-6")
MAX_ITER = 40

volumes = []
lengths = []

search_nodes = [SearchNode( c =  generate_initial_polycube(N) )]
for i in range(MAX_ITER):
	print(f'[+] iteration {i}, vol={get_volume(search_nodes)}, length={len(search_nodes)}')
	volumes.append(get_volume(search_nodes))
	lengths.append(len(search_nodes))
	search_nodes = prune_nodes(search_nodes)

plt.scatter( range(MAX_ITER), lengths ) 
plt.savefig( "lengths3.png" )
plt.clf()
plt.scatter( range(MAX_ITER), volumes ) 
plt.savefig( "volumes3.png" )
plt.clf()
