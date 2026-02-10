# Erdos 1045

The main problem can be found [here](https://www.erdosproblems.com/forum/thread/1045): Let $z_1 \cdots z_n \in \mathbb{C}$ with $|z_i - z_j| \le 2$ for all $i, j$. Consider $\Delta(z_1 \cdots z_n) = \prod_{i \ne j} |z_i - z_j| $. For a given $n$, what is the maximum possible value of $\Delta$? Is $\Delta$ maximized by taking $z_1 \cdots z_n$ to be the vertices of a regular n-gon?

 - $\Delta(z_1 \cdots z_n)$ is invariant under translations $z_i \mapsto z_i + z$, therefore WLOG we can let $z_1 = 0$
 - $\Delta$ is also invariant under rotations about the origin $z_i \mapsto z_i e^{i \theta}$, therefore WLOG we may let $\Re(z_2) = 0$.

Note we can replace $\Delta$ with $$\Delta^2(z_1 \cdots z_n) = \prod_{i \ne j} |z_i - z_j|^2 = \prod_{1 \le i < j \le n} \left( \\\; ( \text{Re}(z_i)-\text{Re}(z_j))^2 \\\; + \\\;(\text{Im}(z_i)-\text{Im}(z_j))^2) \\\;  \right) $$

we attempt to maximize 
```math
\begin{aligned}
\Delta^2 : \mathbb{R}^{2n} &\to \mathbb{R} \\ 
\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{2n-1} \\ x_{2n} \end{bmatrix} &\mapsto \Delta^2( x_1 + x_2i, \cdots, x_{2n-1}+x_{2n}i) 
\end{aligned}
```

## Known Cases
 - $n=4$: 
```math
\begin{aligned}
 z_1 &= (0, 0) \\ 
 z_2 &= (\sqrt{3}, 1) \\ 
 z_3 &= (\sqrt3, -1) \\ 
 z_4 &= (2, 0) 
 \end{aligned}
```
 source: [Quanyu Tang](https://github.com/QuanyuTang/counterexamples-problem-1045/blob/main/Counterexamples_for_Erdos_Problem_1045.pdf)
- $n=5$: maximized by regular pentagon
    
    Proof: Note for a pentagon $z_1 \cdots z_5$, $`\begin{align*}\left( \Delta(z_1 \cdots z_5)\right) ^{1/5} &= \left( \prod \text{sides} \right)^{1/5} \cdot \left( \prod \text{diagonals}\right)^{1/5} \\
    &\ge \left(\frac{1}{5} \sum \text{sides}\right) \cdot \left(\frac{1}{5} \sum \text{diagonals}\right)  && \text{AM-GM}  \end{align*}  `$
    However, $\sum \text{sides}$ and $\sum \text{diagonals} $ of a pentagon are both maximized by the regular pentagon (see [here](https://link.springer.com/article/10.1007/s10898-010-9572-2) for example); since all sides and diagonals are equal, by AM-GM, we have $\ge$ is $=$ in the above inequality
- $n=6$: $` \begin{align*} z_1 &= (-1,0) \\ z_2 &= (1,0) \\ z_3 &= (0, \sqrt3) \\ z_4 &= (0, -(2-\sqrt3)) \\ z_5 &= (\sqrt3-1, 1) \\ z_6 &= (-(\sqrt3-1), 1) \end{align*}`$ source: [Quanyu Tang](https://www.erdosproblems.com/forum/thread/1045)

## Initial Attempts




## Todo
 - find maxima for further $n$ (prove they are at least local minima with e.g. KKT conditions)
 - prove above known cases are global minima with interval arithmetic 

## References / Further Reading
Spamming references for future reading here
- original Erdos problem
    - [Erdos problems site thread](https://www.erdosproblems.com/forum/thread/1045?order=newest): contains main discussion about problem (some discussion about how $\Delta(n)$ behaves as $n \to \infty$)
    - [*Metric properties of polynomials* by Erdos et al](https://users.renyi.hu/~p_erdos/1958-05.pdf): problem stems from this paper
    - [*On metric properties of complex polynomials* by Pommerenke](https://projecteuclid.org/journals/michigan-mathematical-journal/volume-8/issue-2/On-metric-properties-of-complex-polynomials/10.1307/mmj/1028998561.full): shows that $\Delta(n) \le 2^{4(n-1)} n^n$
- related problems
    - [*Using symbolic calculations to determine largest small polygons* by Audet](https://link.springer.com/article/10.1007/s10898-020-00908-w): maximizing area of n-gon with unit diameter
    - [*A Discrete Isoperimetric Problem* by Datta](https://link.springer.com/article/10.1023/A:1004997002327): perimeter of unit diameter n-gon $\le 2n\sin(\pi/2n)$ with equality if $n$ has odd factor
    - [*The small octagon with longest perimeter* by Audet et al](https://www.sciencedirect.com/science/article/pii/S0097316506000537): octagon with unit diameter and longest perimeter; uses interval arithmetic / global optimization
    - [*The small hexagon and heptagon with maximum sum of distances between vertices* by Audet et al](https://link.springer.com/article/10.1007/s10898-010-9572-2): similar to problem above but sum replaced with product, regular n-gon is not maximizer; uses quadratic programming to optimize
 - interval arithmetic
    - [*Rigorous Global Search: Continuous Problems* by Kearfott](https://link.springer.com/book/10.1007/978-1-4757-2495-0): entire book written on using interval arithmetic for nonlinear systems and global optimization
    - [*Enclosure Methods for Multivariate Differentiable Functions and Application to Global Optimization* by Messine et al](https://lib.jucs.org/article/27501/): details interval branch and bound algorithm with Taylor series improvement, also has nice pseudocode
    - [*Formal Verification of Nonlinear Inequalities
with Taylor Interval Approximations* by Hales et al](https://arxiv.org/pdf/1301.1702): use of global optimization/interval arithmetic techniques in computer assisted proof of Kepler conjecture
- general optimization 
    - [free book on optimization algorithms](https://drive.google.com/file/d/1qYjI1igDuBg3x884JKZaCWuJkgdPylHN/view)
    - [paper/tutorial on KKT conditions](https://arxiv.org/pdf/2110.01858)