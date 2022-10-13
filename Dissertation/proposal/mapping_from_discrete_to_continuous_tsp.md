# Definition of the Discrete TSP

Given:

 - A set of points $S$
 - A cost total function $C \subset S \times S \times \mathbb{R}$ with the following property:

     - $\forall A \in S.\;\;\; C(A,A)=0$

Find:

 - A route $Y\in S^n$ where $n \geq |S|$ with the following properties:

     - $\forall A \in S.\;\;\;A \in Y$
     - $\sum_{i=0}^{n-2} C(Y_i, Y_{i+1})$ is minimised

An instance of the discrete TSP can be parameterised by $(S,C)$ and the solution is $Y$.

# Definition of the Continuous TSP

Given:

 - A continuous connected domain $D$
 - A set of points $S' \subseteq D$
 - A continuous cost density total function $f \subset D \times \mathbb{R}$

Find:

 - A contour $Y' \subseteq D$ with the following properties:

     - $\forall A' \in S'.\;\;\;A' \in Y'$
     - $\int_{Y'} f(z)\; dz$ is minimised

An instance of the continuous TSP can be parameterised by $(D,S',f)$ and the solution is $Y'$.

# Mapping from Discrete TSP to Continuous TSP

Below is a rough outline of a proof of the fact that given an instance of the discrete TSP, $(S,C)$, we can determine an instance of the continuous TSP, $(D,S',f)$. Then, given the solution to the continuous instance, $Y'$, we can then determine the solution to the discrete instance, $Y$.

Let $D = \mathbb{R}^n$ where $n=|S|$.

Let $S' = \textrm{the set of unit basis vectors in }D$

Arbitrarily, order the points of $S$ such that $S_i$ is the $i$<sup>th</sup> element of $S$.

Likewise, order the points of $S'$ such that $S'_i$ is the basis vector whose $i$<sup>th</sup> component is 1. 

$\forall d \in D.\;\;\; \textrm{Let }f(d) =$

$$
\begin{cases}
\frac{C(S_i, S_j)}{\sqrt{2}}, & \textrm{if }d\textrm{ is in the }ij\textrm{ plane, in between }S'_i\textrm{ and }S'_j\\ \\
\textrm{arbitrarily large}, & \textrm{otherwise}
\end{cases}
$$

**NOTE**: Since $f$ must be continuous, the *arbitrarily large* value in second case can be continuous and rapidly increasing away from points matching the first case. If the function increases rapidly enough, then the proof will work.

Suppose we find a solution to the continuous TSP instance, $Y'$.

$Y'$ will consist of a connected sequence of straight line segments in axis-aligned planes. Let $Y''$ be that sequence, where $Y''_i$ is the starting point of the $i$<sup>th</sup> line segment.

We can then set $Y_i = S_j$ where $j$ is defined by $Y''_i = S'_j$.

$Y$ will then be a solution to the discrete TSP instance. This solution also preserves costs:

$\sum_{i=0}^{|Y|-2} C(Y_i, Y_{i+1}) = \int_{Y'} f(z)\; dz$
