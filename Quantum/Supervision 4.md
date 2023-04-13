# Quantum 4

## 1

### a

$$p_e^5 + 5 p_e^4(1-p_e) + 10 p_e^3(1-p_e)^2$$

### b

$$p_e^7 + 7 p_e^6(1-p_e) + 21 p_e^5(1-p_e)^2 + 35 p_e^4(1-p_e)^3$$

### c

$$\sum_{k=0}^{\frac{n-1}{2}} \binom{n}{k}p_e^{n-k}(1-p_e)^k$$

## 2

$$
XZ
\\
= \begin{bmatrix}
0 & 1 \\ 
1 & 0
\end{bmatrix}
\begin{bmatrix}
1 & 0 \\ 
0 & -1
\end{bmatrix}
\\
= \begin{bmatrix}
0 & 1 \\ 
-1 & 0
\end{bmatrix}
\\
= \begin{bmatrix}
0 & 1 \\ 
-1 & 0
\end{bmatrix}
$$
<br />

$$
ZX
\\
= \begin{bmatrix}
1 & 0 \\ 
0 & -1
\end{bmatrix}
\begin{bmatrix}
0 & 1 \\ 
1 & 0
\end{bmatrix}
\\
= -1\begin{bmatrix}
0 & 1 \\ 
-1 & 0
\end{bmatrix}
\\
= -XZ
$$

## 3

$$
\ket{\phi_0} = (a\ket{0} + b\ket{1}) \bigotimes (c\ket{0} + d\ket{1}) \bigotimes \ket{0}\\
=(a\ket{0} + b\ket{1})\bigotimes(c\ket{00} + d\ket{10}) \\
=ac\ket{000} + ad\ket{010} + bc\ket{100} + bd\ket{110}
$$

$$
\ket{\phi_1} = ac\ket{000} + ad\ket{010} + bc\ket{101} + bd\ket{111}
$$

$$
\ket{\phi_2} = ac\ket{000} + ad\ket{011} + bc\ket{101} + bd\ket{110}
$$

$$\mathbb{P}(0) = (ac)^2 + (bd)^2\\
\mathbb{P}(1) = (ad)^2 + (bc)^2$$

## 4

### a

If all 3 qubits experience a bit flip, then the input to the error correction phase is $\alpha\ket{111} + \beta\ket{000}$, which is indistinguishable from the no-error case (but with $\alpha$ and $\beta$ swapped), and so the final state will also be $\alpha\ket{111} + \beta\ket{000}$.

### b

If the first two qubits experience a flip, they will still have the same value and so the parity is unchanged, so $M_1$ will be 0. The parity of the last 2 bits however will be flipped, and so $M_2$ will be 1. The correction will therefore be $I\bigotimes I \bigotimes X$ and so the final state will be $\alpha\ket{111} + \beta\ket{000}$.

## 5

### a

$$HG = \begin{bmatrix}
1 & 0 & 1 & 0 & 1 & 0 & 1 \\ 
0 & 1 & 1 & 0 & 0 & 1 & 1 \\ 
0 & 0 & 0 & 1 & 1 & 1 & 1 
\end{bmatrix}
\begin{bmatrix}
1 & 1 & 0 & 1 \\
1 & 0 & 1 & 1 \\
1 & 0 & 0 & 0 \\
0 & 1 & 1 & 1 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix} \\
=\begin{bmatrix}
2 & 2 & 0 & 2 \\ 
2 & 0 & 2 & 2 \\ 
0 & 2 & 2 & 2
\end{bmatrix} \\
\equiv \begin{bmatrix}
0 & 0 & 0 & 0 \\ 
0 & 0 & 0 & 0 \\ 
0 & 0 & 0 & 0
\end{bmatrix} \pmod{2}
$$

### b

A bit flip of qubit $i$ of a state $\ket{\phi}$ can be represented by

$$\ket{\phi} + b_i \mod 2$$

where $b_i$ is the $i$<sup>th</sup> column of $I$.

Therefore, the result of the parity check will be

$$H(Gd + b_i) \mod 2 \\
=HGd + Hb_i \mod 2\\
=\begin{bmatrix}
0 \\
0 \\
0
\end{bmatrix} + Hb_i \mod 2 \\
= Hb_i \mod 2$$

| $$i$$ | $$Hb_i \mod 2$$ |
|---|---|
| 1 | $$\begin{bmatrix}1\\0\\0\end{bmatrix}$$ |
| 2 | $$\begin{bmatrix}0\\1\\0\end{bmatrix}$$ |
| 3 | $$\begin{bmatrix}1\\1\\0\end{bmatrix}$$ |
| 4 | $$\begin{bmatrix}0\\0\\1\end{bmatrix}$$ |
| 5 | $$\begin{bmatrix}1\\0\\1\end{bmatrix}$$ |
| 6 | $$\begin{bmatrix}0\\1\\1\end{bmatrix}$$ |
| 7 | $$\begin{bmatrix}1\\1\\1\end{bmatrix}$$ |

Note that reading from bottom to top, the output of the parity check spells out the index at which the bit flip ocurred, and so this can be used to correct the error.

## 6

$$\ket{\phi_0} = \frac{1}{2\sqrt{2}}\left(\alpha(\ket{000}-\ket{111})(\ket{000}+\ket{111})(\ket{000}+\ket{111}) + \beta(\ket{000}+\ket{111})(\ket{000}-\ket{111})(\ket{000}-\ket{111})\right)$$

$$\ket{\phi_1} = \frac{1}{2\sqrt{2}}\left(\alpha(\ket{000}-\ket{101})(\ket{000}+\ket{101})(\ket{000}+\ket{101}) + \beta(\ket{000}+\ket{101})(\ket{000}-\ket{101})(\ket{000}-\ket{101})\right)$$

$$\ket{\phi_2} = \frac{1}{2\sqrt{2}}\left(\alpha(\ket{000}-\ket{100})(\ket{000}+\ket{100})(\ket{000}+\ket{100}) + \beta(\ket{000}+\ket{100})(\ket{000}-\ket{100})(\ket{000}-\ket{100})\right)$$

$$\ket{\phi_3} = \frac{1}{2\sqrt{2}}\left(\alpha(\ket{+00}-\ket{-00})(\ket{+00}+\ket{-00})(\ket{+00}+\ket{-00}) + \beta(\ket{+00}+\ket{-00})(\ket{+00}-\ket{-00})(\ket{+00}-\ket{-00})\right)$$

$$M_1 = 1\\
M_2 = 0$$

Recovery $= Z\bigotimes I\bigotimes I$

$$\ket{\phi_4} = \frac{1}{2\sqrt{2}}\left(\alpha(\ket{+00}+\ket{-00})(\ket{+00}+\ket{-00})(\ket{+00}+\ket{-00}) + \beta(\ket{+00}-\ket{-00})(\ket{+00}-\ket{-00})(\ket{+00}-\ket{-00})\right)$$

$$\ket{\phi_5} = \frac{1}{2\sqrt{2}}\left(\alpha(\ket{000}+\ket{100})(\ket{000}+\ket{100})(\ket{000}+\ket{100}) + \beta(\ket{000}-\ket{100})(\ket{000}-\ket{100})(\ket{000}-\ket{100})\right)$$

$$\ket{\phi_6} = \frac{1}{2\sqrt{2}}\left(\alpha(\ket{000}+\ket{110})(\ket{000}+\ket{110})(\ket{000}+\ket{110}) + \beta(\ket{000}-\ket{110})(\ket{000}-\ket{110})(\ket{000}-\ket{110})\right)$$

$$\ket{\phi_7} = \frac{1}{2\sqrt{2}}\left(\alpha(\ket{000}+\ket{111})(\ket{000}+\ket{111})(\ket{000}+\ket{111}) + \beta(\ket{000}-\ket{111})(\ket{000}-\ket{111})(\ket{000}-\ket{111})\right)$$

## 8

| Part | Post-Error State | Parity Check Bits | Detected Error | Corrected State |
|---|---|---|---|---|
| a | $$\alpha\ket{1000}+\beta\ket{0111}$$ | 100 | 001 | $$\alpha\ket{0000}+\beta\ket{1111}$$ |
| b | $$\alpha\ket{1100}+\beta\ket{0011}$$ | 010 | Uncertain | N/A |
| c | $$\alpha\ket{1001}+\beta\ket{0110}$$ | 101 | Uncertain | N/A |
| d | $$\alpha\ket{1111}+\beta\ket{0000}$$ | 000 | None | $$\alpha\ket{1111}+\beta\ket{0000}$$ |

## 9

While poor coherence may limit the size or complexity of the problems that can be solved by D-wave, it is unlikely to be a major problem because optimisation problems are less sensitive to coherence errors than other quantum algorithms. Furthermore D-wave has developed techniques such as annealing schedules which are designed to maximise the coherence of the qubits.

## 10

I think that superconducting qubits will come to dominate quantum computing (in particular, more so than trapped-ion qubits) because, at least in the near term, speed will be more important than reliability. For example, with the task of using Shor's algorithm to solve the discrete logarithm problem, the solution provided can be verified using a classical computer, so it is not imperative that the quantum computer be 100% reliable.