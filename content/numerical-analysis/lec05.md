:::exam 本讲在往年真题里（几乎每年一道大题，是全课程真题最密集的一讲）
- **2025–26 第 5 题（10 分）**：(a) 证明 $\dfrac1{\lVert A^{-1}\rVert}\le\lvert\lambda\rvert\le\lVert A\rVert$；(b) 证明 $\lVert A\mathbf x\rVert_2\le\lVert A\rVert_F\lVert\mathbf x\rVert_2$。→ 5.1、5.2
- **2023–24 第 4 题（20 分）**：给方程组，换行成对角占优，Jacobi 迭代两次，Gauss–Seidel 迭代两次，证明 $\rho(M)\le\lVert M\rVert$，求 $\lVert T\rVert_\infty$ 并估计 20 次迭代的误差上界。→ 5.4–5.6
- **2024–25 第 3 题**：Gauss–Seidel、Jacobi 各迭代两次（初值 $(0,0,0,0)^T$），判断是否收敛，若收敛哪个更快。→ 5.4–5.6
- **2022–23 第 3 题**：给方程组，求 Jacobi 和 Gauss–Seidel 的谱半径，判断哪个收敛，写出可收敛的迭代方程。→ 5.6
- **2022–23 第 2 题**：对称矩阵的证明（原题条件丢失）。→ 5.2，见「真题精解」第 5 题。
- **2022–23 填空**："收敛时的条件"，很可能就是 $\rho(T)<1$。→ 5.6
- 英文术语：matrix norm、subordinate / natural / induced norm、Frobenius norm、spectral radius、characteristic polynomial、convergent matrix、Jacobi / Gauss–Seidel iterative method、strictly diagonally dominant、residual vector、condition number、well-conditioned / ill-conditioned。
- **复习顺序建议**：先看每节「速查」框，再做真题精解的第 3、4 题（迭代法的完整流程），最后补 ★ 证明。
:::

图例：**★ 证明**＝考过或很可能考，建议考前自己推一遍；**☆ 证明**＝理解用，考试只用结论。📘＝课件没有、从教材（Burden & Faires）补充；⚠️＝课件笔误或 OCR 错误。

## 5.1 矩阵范数 | Matrix Norms

:::quick
- **什么时候用**：度量矩阵的"大小"；估计 $\lVert A\mathbf x\rVert$；用 $\lVert T\rVert<1$ 判断迭代是否收敛（5.6）；定义条件数（5.7）。
- **矩阵范数**：$n\times n$ 矩阵上的实值函数 $\lVert\cdot\rVert$，对任意矩阵 $A,B$ 和实数 $\alpha$：
  1. $\lVert A\rVert\ge0$；
  2. $\lVert A\rVert=0\iff A=O$；
  3. $\lVert\alpha A\rVert=\lvert\alpha\rvert\lVert A\rVert$；
  4. $\lVert A+B\rVert\le\lVert A\rVert+\lVert B\rVert$；
  5. $\lVert AB\rVert\le\lVert A\rVert\lVert B\rVert$（比向量范数多这一条）。
- **自然（从属 / 诱导）范数**（natural / subordinate / induced norm）：由向量范数 $\lVert\cdot\rVert$ 定义，
  $$\lVert A\rVert=\max_{\lVert\mathbf x\rVert=1}\lVert A\mathbf x\rVert=\sup_{\mathbf x\ne\mathbf 0}\frac{\lVert A\mathbf x\rVert}{\lVert\mathbf x\rVert}.$$
  它是 $A$ 把单位向量"拉伸"的最大倍数。**本课程默认的矩阵范数都是自然范数**。
- **最常用的三个公式**：
  $$\begin{aligned}\lVert A\rVert_\infty&=\max_{1\le i\le n}\sum_{j=1}^n\lvert a_{ij}\rvert\quad(\text{最大行和}),\\\lVert A\rVert_1&=\max_{1\le j\le n}\sum_{i=1}^n\lvert a_{ij}\rvert\quad(\text{最大列和 📘}),\\\lVert A\rVert_2&=\sqrt{\rho(A^TA)}\quad(5.2).\end{aligned}$$
- **Frobenius 范数**：
  $$\lVert A\rVert_F=\Big(\sum_{i=1}^m\sum_{j=1}^n\lvert a_{ij}\rvert^2\Big)^{1/2}.$$
  它是矩阵范数，但**不是**自然范数（$\lVert I\rVert_F=\sqrt n\ne1$，自然范数一定有 $\lVert I\rVert=1$）。📘 $\lVert A\rVert_2\le\lVert A\rVert_F$。
- **两个基本不等式**（自然范数）：
  $$\lVert A\mathbf x\rVert\le\lVert A\rVert\,\lVert\mathbf x\rVert,\qquad\lVert AB\rVert\le\lVert A\rVert\,\lVert B\rVert.$$
- 步骤（求 $\lVert A\rVert_\infty$）：每行取绝对值求和，再取最大。
:::

:::proof ★ $\lVert A\mathbf x\rVert\le\lVert A\rVert\lVert\mathbf x\rVert$ 与 $\lVert AB\rVert\le\lVert A\rVert\lVert B\rVert$
**第一式**：$\mathbf x=\mathbf 0$ 时两边都是 0。$\mathbf x\ne\mathbf 0$ 时，$\mathbf x/\lVert\mathbf x\rVert$ 是单位向量，由定义
$$\Big\lVert A\frac{\mathbf x}{\lVert\mathbf x\rVert}\Big\rVert\le\max_{\lVert\mathbf z\rVert=1}\lVert A\mathbf z\rVert=\lVert A\rVert\ \Rightarrow\ \lVert A\mathbf x\rVert\le\lVert A\rVert\lVert\mathbf x\rVert.$$
**第二式**：对任意 $\mathbf x$，连续两次用第一式，
$$\lVert AB\mathbf x\rVert\le\lVert A\rVert\lVert B\mathbf x\rVert\le\lVert A\rVert\lVert B\rVert\lVert\mathbf x\rVert,$$
所以 $\lVert AB\rVert=\max_{\lVert\mathbf x\rVert=1}\lVert AB\mathbf x\rVert\le\lVert A\rVert\lVert B\rVert$。这也说明自然范数满足矩阵范数的第 5 条。

**考场用法**：第一式几乎是本讲所有不等式的起点（2025–26 第 5(a) 题的两个不等式都从它出发）。
:::

:::proof ★ $\lVert A\rVert_\infty=\max_i\sum_j\lvert a_{ij}\rvert$
记 $S=\max_i\sum_j\lvert a_{ij}\rvert$。

**（$\le$）** 设 $\lVert\mathbf x\rVert_\infty=1$，即 $\lvert x_j\rvert\le1$（$\forall j$），则
$$\lVert A\mathbf x\rVert_\infty=\max_i\Big\lvert\sum_ja_{ij}x_j\Big\rvert\le\max_i\sum_j\lvert a_{ij}\rvert\lvert x_j\rvert\le\max_i\sum_j\lvert a_{ij}\rvert=S,$$
所以 $\lVert A\rVert_\infty\le S$。

**（$\ge$）** 设第 $p$ 行的行和最大：$\sum_j\lvert a_{pj}\rvert=S$。取向量 $\mathbf x$，$x_j=1$（若 $a_{pj}\ge0$），$x_j=-1$（若 $a_{pj}<0$），则 $\lVert\mathbf x\rVert_\infty=1$，且 $a_{pj}x_j=\lvert a_{pj}\rvert$。于是
$$\lVert A\mathbf x\rVert_\infty\ge\Big\lvert\sum_ja_{pj}x_j\Big\rvert=\sum_j\lvert a_{pj}\rvert=S,$$
所以 $\lVert A\rVert_\infty\ge S$。两边合起来 $\lVert A\rVert_\infty=S$。
:::

:::proof ☆ 📘 $\lVert A\rVert_1=\max_j\sum_i\lvert a_{ij}\rvert$
记 $S_1$ 为最大列和。
- **（$\le$）** $\lVert A\mathbf x\rVert_1=\sum_i\big\lvert\sum_ja_{ij}x_j\big\rvert\le\sum_j\lvert x_j\rvert\sum_i\lvert a_{ij}\rvert\le S_1\lVert\mathbf x\rVert_1$。
- **（$\ge$）** 设第 $q$ 列的列和最大，取 $\mathbf x=\mathbf e_q$（$\lVert\mathbf e_q\rVert_1=1$），则 $A\mathbf x$ 是 $A$ 的第 $q$ 列，$\lVert A\mathbf e_q\rVert_1=S_1$。
:::

:::example 例 5.1　各种范数的计算与大小关系
设 $A=\begin{pmatrix}1&2&-1\\0&3&-1\\5&-1&1\end{pmatrix}$（课件例题，只给了题目）。

**行和**：$\lvert1\rvert+\lvert2\rvert+\lvert-1\rvert=4$，$0+3+1=4$，$5+1+1=7$，所以
$$\lVert A\rVert_\infty=\max\{4,4,7\}=7.$$
**📘 列和**：$1+0+5=6$，$2+3+1=6$，$1+1+1=3$，$\lVert A\rVert_1=6$。
**📘 Frobenius**：$\lVert A\rVert_F=\sqrt{1+4+1+0+9+1+25+1+1}=\sqrt{43}\approx6.557$。
**📘 2-范数**：$\lVert A\rVert_2\approx5.282$（算法见 5.2）。谱半径 $\rho(A)=\sqrt7\approx2.646$（特征值 $1,\ 2\pm\sqrt3\,i$，$\lvert2\pm\sqrt3i\rvert=\sqrt7$）。

大小关系：$\rho(A)=2.646\le\lVert A\rVert_2=5.282\le\lVert A\rVert_F=6.557$，且 $\rho(A)\le\lVert A\rVert_1=6$，$\rho(A)\le\lVert A\rVert_\infty=7$ ✓（见 5.2 的 $\rho(A)\le\lVert A\rVert$）。

**课件插图**：$B=\begin{pmatrix}0&-2\\2&0\end{pmatrix}$。对 $\mathbf x=(x_1,x_2)^T$，$B\mathbf x=(-2x_2,\ 2x_1)^T$，把向量旋转 $90^\circ$ 并拉长为 2 倍，所以 $\lVert B\mathbf x\rVert_2=2\lVert\mathbf x\rVert_2$，$\lVert B\rVert_2=2$；$\lVert B\rVert_\infty=\max\{2,2\}=2$。

**核对**：各范数与谱半径由程序用 NumPy 重算。
:::

:::pitfall
- $\lVert A\rVert_\infty$ 是**行**和的最大值，$\lVert A\rVert_1$ 是**列**和的最大值，别记反（$\infty$ 对应行，$1$ 对应列）。
- 每个元素先取**绝对值**再求和。
- $\lVert A\rVert_F$ **不是**自然范数，不满足 $\lVert I\rVert=1$；但它仍是矩阵范数，满足 $\lVert AB\rVert_F\le\lVert A\rVert_F\lVert B\rVert_F$。
- $\lVert A\rVert_2$ 不是"元素平方和开方"（那是 $\lVert A\rVert_F$），而是 $\sqrt{\rho(A^TA)}$。
:::

## 5.2 特征值、谱半径与谱范数 | Eigenvalues, Spectral Radius and the 2-Norm

:::quick
- **什么时候用**：求 $\rho(A)$（判断迭代收敛、收敛矩阵）；求 $\lVert A\rVert_2$；证明特征值的上下界；对称矩阵的性质。
- **特征值与特征向量**：$A\mathbf x=\lambda\mathbf x$，$\mathbf x\ne\mathbf 0$。等价于 $(A-\lambda I)\mathbf x=\mathbf 0$ 有非零解，即 $\det(A-\lambda I)=0$。
- **特征多项式**（characteristic polynomial）：$p(\lambda)=\det(A-\lambda I)$，是 $n$ 次多项式，至多 $n$ 个根（可能是复数，按重数算）。先求 $\lambda$，再解 $(A-\lambda I)\mathbf x=\mathbf 0$ 求 $\mathbf x$。
- **谱半径**（spectral radius）：
  $$\rho(A)=\max\{\lvert\lambda\rvert:\ \lambda\text{ 是 }A\text{ 的特征值}\},\qquad\lvert\alpha+\beta i\rvert=\sqrt{\alpha^2+\beta^2}.$$
- **两个定理**：
  1. $\lVert A\rVert_2=\sqrt{\rho(A^TA)}$；
  2. $\rho(A)\le\lVert A\rVert$（对**任意**自然范数）。
- **特征值的上下界**：设 $\lambda$ 是 $A$ 的特征值，则 $\lvert\lambda\rvert\le\lVert A\rVert$；若 $A$ 可逆，还有 $\lvert\lambda\rvert\ge\dfrac1{\lVert A^{-1}\rVert}$。
- 📘 **特征值的运算**：$\lambda$ 是 $A$ 的特征值 $\Rightarrow$ $\lambda^k$ 是 $A^k$ 的特征值，$1/\lambda$ 是 $A^{-1}$ 的特征值（$\lambda\ne0$），$\lambda-q$ 是 $A-qI$ 的特征值；特征向量不变。
- 📘 **对称矩阵**（$A=A^T$）：特征值都是实数；不同特征值的特征向量正交；有 $n$ 个标准正交特征向量，$A=QDQ^T$（$Q$ 正交，$D$ 对角）；$\lVert A\rVert_2=\rho(A)$；正定 $\iff$ 特征值全 $>0$。
- 步骤（求 $\lVert A\rVert_2$）：1. 算 $A^TA$；2. 解 $\det(A^TA-\mu I)=0$；3. 取最大的 $\mu$，$\lVert A\rVert_2=\sqrt\mu$。
- 几何意义：$\lambda>1$ 沿该方向拉长，$0<\lambda<1$ 缩短，$\lambda<0$ 还要反向。
:::

:::proof ★ $\rho(A)\le\lVert A\rVert$ 与特征值的上下界
设 $\lambda$ 是 $A$ 的特征值，$\mathbf x$ 是对应特征向量，取 $\lVert\mathbf x\rVert=1$（可以把 $\mathbf x$ 除以它的范数）。则
$$\lvert\lambda\rvert=\lvert\lambda\rvert\lVert\mathbf x\rVert=\lVert\lambda\mathbf x\rVert=\lVert A\mathbf x\rVert\le\lVert A\rVert\lVert\mathbf x\rVert=\lVert A\rVert.$$
对所有特征值取最大：$\rho(A)=\max\lvert\lambda\rvert\le\lVert A\rVert$。这同时是"特征值上界"。

**下界**：若 $A$ 可逆，则 $\lambda\ne0$（否则 $A\mathbf x=\mathbf 0$ 有非零解）。由 $A\mathbf x=\lambda\mathbf x$ 左乘 $A^{-1}$ 得 $\mathbf x=\lambda A^{-1}\mathbf x$，即 $A^{-1}\mathbf x=\lambda^{-1}\mathbf x$，$\lambda^{-1}$ 是 $A^{-1}$ 的特征值。对 $A^{-1}$ 用上界：
$$\frac1{\lvert\lambda\rvert}\le\lVert A^{-1}\rVert\ \Rightarrow\ \lvert\lambda\rvert\ge\frac1{\lVert A^{-1}\rVert}.$$
**说明**：对复特征值 $\lambda$，$\mathbf x$ 是复向量，这里把自然范数按通常方式延拓到 $\mathbb C^n$，结论同样成立。课件和考试都按这个写法即可。

**考场用法**：这就是 2025–26 第 5(a) 题的完整解答（见「真题精解」）。2023–24 第 4(c) 题"证明 $\rho(M)\le\lVert M\rVert$"也是同一段。
:::

:::proof ★ $\lVert A\rVert_2=\sqrt{\rho(A^TA)}$
$A^TA$ 是对称矩阵，所以它有 $n$ 个标准正交的特征向量 $\mathbf u_1,\dots,\mathbf u_n$，对应特征值 $\mu_1,\dots,\mu_n$（实数）。特征值非负，因为
$$\mu_i=\mu_i\mathbf u_i^T\mathbf u_i=\mathbf u_i^TA^TA\mathbf u_i=\lVert A\mathbf u_i\rVert_2^2\ge0.$$
记最大的特征值为 $\mu_{\max}=\rho(A^TA)$。

**（$\le$）** 任取 $\lVert\mathbf x\rVert_2=1$，把 $\mathbf x$ 按正交基展开 $\mathbf x=\sum_ic_i\mathbf u_i$，$\sum_ic_i^2=1$。则
$$\lVert A\mathbf x\rVert_2^2=\mathbf x^TA^TA\mathbf x=\sum_i\mu_ic_i^2\le\mu_{\max}\sum_ic_i^2=\mu_{\max},$$
所以 $\lVert A\rVert_2\le\sqrt{\mu_{\max}}$。

**（$\ge$）** 取 $\mathbf x=\mathbf u_{\max}$（对应 $\mu_{\max}$ 的单位特征向量），$\lVert A\mathbf x\rVert_2^2=\mathbf u_{\max}^TA^TA\mathbf u_{\max}=\mu_{\max}$，所以 $\lVert A\rVert_2\ge\sqrt{\mu_{\max}}$。

合起来 $\lVert A\rVert_2=\sqrt{\rho(A^TA)}$。
:::

:::proof ★ 对称矩阵的 $\lVert A\rVert_2=\rho(A)$
设 $A=A^T$。则 $A^TA=A^2$。$A$ 的特征值 $\lambda_i$ 对应 $A^2$ 的特征值 $\lambda_i^2$，所以 $\rho(A^2)=\max\lambda_i^2=\rho(A)^2$。由上一个定理，
$$\lVert A\rVert_2=\sqrt{\rho(A^TA)}=\sqrt{\rho(A)^2}=\rho(A).$$
:::

:::proof ☆ 📘 实对称矩阵：特征值为实数，不同特征值的特征向量正交
设 $A=A^T$ 是实矩阵。

**特征值是实数**：设 $A\mathbf x=\lambda\mathbf x$，$\mathbf x\in\mathbb C^n$，$\mathbf x\ne\mathbf 0$。左乘 $\bar{\mathbf x}^T$：$\bar{\mathbf x}^TA\mathbf x=\lambda\bar{\mathbf x}^T\mathbf x=\lambda\lVert\mathbf x\rVert^2$。再对这个数取共轭，由 $A$ 实对称：
$$\overline{\bar{\mathbf x}^TA\mathbf x}=\mathbf x^TA\bar{\mathbf x}=(\mathbf x^TA\bar{\mathbf x})^T=\bar{\mathbf x}^TA^T\mathbf x=\bar{\mathbf x}^TA\mathbf x,$$
即 $\bar{\mathbf x}^TA\mathbf x$ 等于它自己的共轭，是实数。所以 $\lambda=\bar{\mathbf x}^TA\mathbf x/\lVert\mathbf x\rVert^2$ 是实数。

**正交性**：设 $A\mathbf x=\lambda\mathbf x$，$A\mathbf y=\mu\mathbf y$，$\lambda\ne\mu$。则
$$\lambda\,\mathbf x^T\mathbf y=(A\mathbf x)^T\mathbf y=\mathbf x^TA^T\mathbf y=\mathbf x^TA\mathbf y=\mu\,\mathbf x^T\mathbf y\ \Rightarrow\ (\lambda-\mu)\,\mathbf x^T\mathbf y=0\ \Rightarrow\ \mathbf x^T\mathbf y=0.$$
:::

:::example 例 5.2　特征值、谱半径、$\lVert A\rVert_2$
**(a)** 课件：证明 $A=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$ 没有实的特征向量（即 $\mathbb R^2$ 中没有 $\mathbf x\ne\mathbf 0$ 使 $A\mathbf x\parallel\mathbf x$）。

$\det(A-\lambda I)=\det\begin{pmatrix}-\lambda&1\\-1&-\lambda\end{pmatrix}=\lambda^2+1=0$，特征值 $\lambda=\pm i$，是复数。对 $\lambda_1=i$：$(A-iI)\mathbf x=\mathbf 0$ 给 $-ix_1+x_2=0$，$x_2=ix_1$，所以特征向量的两个分量一个实一个虚，$\mathbb R^2$ 里没有。几何上 $A$ 是旋转 $90^\circ$。$\rho(A)=\lvert\pm i\rvert=1$。

**(b)** 课件：$A=\begin{pmatrix}2&0&0\\1&1&2\\1&-1&4\end{pmatrix}$，求 $\rho(A)$。

$\det(A-\lambda I)=(2-\lambda)\det\begin{pmatrix}1-\lambda&2\\-1&4-\lambda\end{pmatrix}=(2-\lambda)\big[(1-\lambda)(4-\lambda)+2\big]=(2-\lambda)(\lambda-2)(\lambda-3)$，特征值是 $2,\ 2,\ 3$，$\rho(A)=\max\{2,3\}=3$。

**(c)** 课件：求 $A=\begin{pmatrix}1&1&0\\1&2&1\\-1&1&2\end{pmatrix}$ 的 $\lVert A\rVert_2$。

先算 $A^TA$：
$$A^TA=\begin{pmatrix}1&1&-1\\1&2&1\\0&1&2\end{pmatrix}\begin{pmatrix}1&1&0\\1&2&1\\-1&1&2\end{pmatrix}=\begin{pmatrix}3&2&-1\\2&6&4\\-1&4&5\end{pmatrix}.$$
⚠️ 课件把乘积写成 $\begin{pmatrix}3&2&1\\2&6&4\\-1&4&5\end{pmatrix}$（第 1 行第 3 列的符号错了，它应该和第 3 行第 1 列相同，因为 $A^TA$ 对称），后面的特征多项式用的是对的矩阵。

$$\det(A^TA-\mu I)=-\mu^3+14\mu^2-42\mu=-\mu(\mu^2-14\mu+42)=0\ \Rightarrow\ \mu=0,\ 7\pm\sqrt7.$$
最大是 $7+\sqrt7\approx9.646$，
$$\lVert A\rVert_2=\sqrt{7+\sqrt7}\approx3.106.$$

**核对**：(a)(b) 的特征值、(c) 的 $A^TA$、特征值 $0,\ 4.354,\ 9.646$ 和 $\lVert A\rVert_2=3.1058$ 都由程序重算（NumPy 的 `norm(A,2)` 也给出 $3.1058$）。
:::

:::pitfall
- $\rho(A)$ 是特征值**模**的最大值，复特征值要取模 $\sqrt{\alpha^2+\beta^2}$。
- $\rho(A)$ **不是**任何范数的替代品：$\rho(A)\le\lVert A\rVert$ 是不等式，不一定相等（非对称矩阵常常严格小于）。例如 $A=\begin{pmatrix}0&100\\0&0\end{pmatrix}$ 的 $\rho(A)=0$，但 $\lVert A\rVert=100$。
- 求 $\lVert A\rVert_2$ 要先乘 $A^TA$（不是 $A^2$）；只有 $A$ 对称时才有 $\lVert A\rVert_2=\rho(A)$。
- 手算 $\det(A^TA-\mu I)$ 时先用迹检验：特征值之和 $=\operatorname{tr}(A^TA)=3+6+5=14$，与上面的 $0+(7-\sqrt7)+(7+\sqrt7)=14$ 一致。
:::

## 5.3 收敛矩阵 | Convergent Matrices

:::quick
- **什么时候用**：判断 $A^k\to O$（迭代法 $\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c$ 收敛的核心概念，5.6）。
- **定义**：$n\times n$ 矩阵 $A$ 称为**收敛矩阵**（convergent matrix），若
  $$\lim_{k\to\infty}(A^k)_{ij}=0,\qquad\forall\,i,j.$$
- **五条等价条件**：
  1. $A$ 是收敛矩阵；
  2. 对**某个**自然范数 $\lim_{n\to\infty}\lVert A^n\rVert=0$；
  3. 对**所有**自然范数 $\lim_{n\to\infty}\lVert A^n\rVert=0$；
  4. $\rho(A)<1$；
  5. 对每个 $\mathbf x$，$\lim_{n\to\infty}A^n\mathbf x=\mathbf 0$。
- **最常用的判断**：
  - 判别：$\rho(A)<1$。
  - **快速充分条件**：只要某个自然范数 $\lVert A\rVert<1$（如 $\lVert A\rVert_\infty<1$ 或 $\lVert A\rVert_1<1$），就有 $\rho(A)\le\lVert A\rVert<1$，$A$ 收敛。
  - $\rho(A)\ge1$ 一定不收敛。
- 步骤：先算 $\lVert A\rVert_\infty$、$\lVert A\rVert_1$（快），若 $<1$ 就结束；否则求特征值，看 $\rho(A)$。
:::

:::proof ☆ 为什么 $\rho(A)<1\iff A$ 收敛（主要方向）
**收敛 $\Rightarrow\rho(A)<1$（必要性）**：设 $\lambda$ 是 $A$ 的特征值，$\mathbf x\ne\mathbf 0$ 是特征向量。则 $A^n\mathbf x=\lambda^n\mathbf x$。若 $A$ 收敛，$A^n\mathbf x\to\mathbf 0$，所以 $\lambda^n\to0$，即 $\lvert\lambda\rvert<1$。对所有特征值成立，所以 $\rho(A)<1$。

**$\rho(A)<1\Rightarrow$ 收敛（充分性，$A$ 可对角化的情形）**：$A=SDS^{-1}$，$D=\operatorname{diag}(\lambda_i)$，则 $A^n=SD^nS^{-1}$，而 $D^n=\operatorname{diag}(\lambda_i^n)\to O$（$\lvert\lambda_i\rvert<1$），所以 $A^n\to O$。一般（不可对角化）的矩阵要用 Jordan 标准型，或"对任意 $\varepsilon>0$ 存在自然范数使 $\lVert A\rVert\le\rho(A)+\varepsilon$"这个事实，课件直接引用结论。
:::

:::example 例 5.3　课件例：$A=\begin{pmatrix}\frac12&0\\\frac14&\frac12\end{pmatrix}$ 是收敛矩阵
**用谱半径**：下三角矩阵的特征值就是对角元，$\lambda=\tfrac12,\tfrac12$，$\rho(A)=\tfrac12<1$，收敛。

**用范数（更快）**：$\lVert A\rVert_\infty=\max\{\tfrac12,\ \tfrac14+\tfrac12\}=\tfrac34<1$，由 $\rho(A)\le\lVert A\rVert_\infty<1$，收敛。

**直接验证 $A^k$**：归纳可得
$$A^k=\begin{pmatrix}\big(\tfrac12\big)^k&0\\[2pt]\dfrac{k}{2^{k+1}}&\big(\tfrac12\big)^k\end{pmatrix}.$$
（$k=1$：左下角 $\tfrac14$ ✓；若对 $k$ 成立，则 $A^{k+1}=A^kA$ 的左下角是 $\tfrac k{2^{k+1}}\cdot\tfrac12+\big(\tfrac12\big)^k\cdot\tfrac14=\tfrac{k+1}{2^{k+2}}$ ✓。）所有元素 $\to0$，因为 $\tfrac k{2^{k+1}}\to0$。

| $k$ | 1 | 2 | 5 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|
| $(A^k)_{21}=k/2^{k+1}$ | 0.25 | 0.25 | 0.0781 | 0.00488 | $9.5\times10^{-6}$ | $1.8\times10^{-11}$ |
| $\lVert A^k\rVert_\infty$ | 0.75 | 0.5 | 0.109 | 0.00586 | $1.05\times10^{-5}$ | $1.9\times10^{-11}$ |

**核对**：$A^k$ 的闭式和表中数值由程序直接做矩阵幂验证。
:::

:::pitfall
- 收敛矩阵条件是 $\rho<1$，**不是** $\rho\le1$；$\rho=1$ 的矩阵（如单位矩阵）不收敛。
- $\lVert A\rVert<1$ 是充分条件，不是必要条件：有些矩阵 $\rho(A)<1$ 但 $\lVert A\rVert_\infty>1$（可能要试别的范数或直接算特征值）。
- 例 5.3 里 $\lVert A^k\rVert_\infty$ 虽然前几步不是单调递减得很整齐，但最终 $\to0$；判断收敛看极限，不是看某一步的大小。
:::

## 5.4 Jacobi 迭代 | The Jacobi Iterative Method

:::quick
- **什么时候用**：用迭代法解 $A\mathbf x=\mathbf b$，题目说"用 Jacobi 方法迭代 $k$ 次"。
- **思想**：把 $A\mathbf x=\mathbf b$ 化成等价形式 $\mathbf x=T\mathbf x+\mathbf c$，再迭代 $\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c$。适合**大型稀疏**方程组；小规模时不如直接法（4.1）。
- **分解** $A=D-L-U$：$D$ 是 $A$ 的对角部分；$-L$ 是严格下三角部分，$-U$ 是严格上三角部分（所以 $L$ 的元素是 $-a_{ij}$，$i>j$，$U$ 的元素是 $-a_{ij}$，$i<j$）。
- **矩阵形式**：
  $$\mathbf x^{(k)}=D^{-1}(L+U)\,\mathbf x^{(k-1)}+D^{-1}\mathbf b=T_j\mathbf x^{(k-1)}+\mathbf c_j,\qquad T_j=D^{-1}(L+U),\ \ \mathbf c_j=D^{-1}\mathbf b.$$
- **分量形式**（做题用这个）：
  $$x_i^{(k)}=\frac1{a_{ii}}\Big[b_i-\sum_{j\ne i}a_{ij}x_j^{(k-1)}\Big],\qquad i=1,\dots,n.$$
  第 $k$ 步所有分量都用**上一步**（第 $k-1$ 步）的值，可以"同时"更新。
- 要求 $a_{ii}\ne0$；需要时先**换行**（4.5），并尽量让 $\lvert a_{ii}\rvert$ 大（收敛更快、更容易严格对角占优）。
- **停止准则**：$\dfrac{\lVert\mathbf x^{(k)}-\mathbf x^{(k-1)}\rVert_\infty}{\lVert\mathbf x^{(k)}\rVert_\infty}<\text{TOL}$（课件用 $10^{-3}$）。
- 步骤：
  1. 把第 $i$ 个方程解出 $x_i$；
  2. 取初值 $\mathbf x^{(0)}$（**题目没给就取 $\mathbf 0$**）；
  3. 逐步代入，列表；
  4. 判断收敛（5.6）。
:::

:::example 例 5.4　课件：Jacobi 迭代解四元方程组
$$\begin{aligned}E_1:\ 10x_1-x_2+2x_3&=6\\E_2:\ -x_1+11x_2-x_3+3x_4&=25\\E_3:\ 2x_1-x_2+10x_3-x_4&=-11\\E_4:\ 3x_2-x_3+8x_4&=15\end{aligned}$$
精确解 $\mathbf x=(1,\ 2,\ -1,\ 1)^T$。初值 $\mathbf x^{(0)}=(0,0,0,0)^T$，停止条件 $\dfrac{\lVert\mathbf x^{(k)}-\mathbf x^{(k-1)}\rVert_\infty}{\lVert\mathbf x^{(k)}\rVert_\infty}<10^{-3}$。

**第 1 步：把每个方程解出对角变量**：
$$\begin{aligned}x_1&=\tfrac1{10}x_2-\tfrac15x_3+\tfrac35,\\x_2&=\tfrac1{11}x_1+\tfrac1{11}x_3-\tfrac3{11}x_4+\tfrac{25}{11},\\x_3&=-\tfrac15x_1+\tfrac1{10}x_2+\tfrac1{10}x_4-\tfrac{11}{10},\\x_4&=-\tfrac38x_2+\tfrac18x_3+\tfrac{15}8.\end{aligned}$$
**第 2 步：$\mathbf x^{(0)}=\mathbf 0$ 代入**：
$$x_1^{(1)}=0.6000,\quad x_2^{(1)}=\tfrac{25}{11}=2.2727,\quad x_3^{(1)}=-1.1000,\quad x_4^{(1)}=\tfrac{15}8=1.8750.$$
**第 3 步：继续**。例如 $x_1^{(2)}=\tfrac1{10}(2.2727)-\tfrac15(-1.1000)+\tfrac35=0.22727+0.22+0.6=1.0473$。

| $k$ | $x_1^{(k)}$ | $x_2^{(k)}$ | $x_3^{(k)}$ | $x_4^{(k)}$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0.6000 | 2.2727 | −1.1000 | 1.8750 |
| 2 | 1.0473 | 1.7159 | −0.8052 | 0.8852 |
| 3 | 0.9326 | 2.0533 | −1.0493 | 1.1309 |
| 4 | 1.0152 | 1.9537 | −0.9681 | 0.9738 |
| 10 | 1.0001 | 1.9998 | −0.9998 | 0.9998 |

**停止**：$k=10$ 时 $\lVert\mathbf x^{(10)}-\mathbf x^{(9)}\rVert_\infty=8.3\times10^{-4}$，$\lVert\mathbf x^{(10)}\rVert_\infty=1.9998$，相对差 $4.2\times10^{-4}<10^{-3}$，实际误差 $\lVert\mathbf x^{(10)}-\mathbf x\rVert_\infty=2.3\times10^{-4}$。

**核对**：迭代由程序重算。⚠️ 课件第 4 行 $x_4^{(4)}$ 写 $0.9739$，精确值 $0.97384$，四舍五入应为 $0.9738$；课件说"$8.0\times10^{-4}/1.9998$"是用 4 位舍入值算的。按精确值，$k=9$ 时相对差已经是 $8.9\times10^{-4}<10^{-3}$，课件在 $k=10$ 停止是教材的写法，不影响结论。
:::

:::pitfall
- Jacobi 每一步**所有分量都用上一步的旧值**，不能把新算出的 $x_1^{(k)}$ 立即用来算 $x_2^{(k)}$（那是 Gauss–Seidel，5.5）。
- 分量公式里是 $b_i-\sum_{j\ne i}a_{ij}x_j$，**除以 $a_{ii}$**；符号别错。
- 不换行直接做，若某个 $a_{ii}=0$ 就无法进行；若不是对角占优，可能不收敛。
- 题目没给初值时取 $\mathbf x^{(0)}=\mathbf 0$，并**写明**这个假设。
:::

## 5.5 Gauss–Seidel 迭代 | The Gauss–Seidel Method

:::quick
- **什么时候用**：题目说"用 Gauss–Seidel 方法迭代 $k$ 次"。
- **思想**：和 Jacobi 一样，但算 $x_i^{(k)}$ 时，**立即使用本轮已经算出的新值** $x_1^{(k)},\dots,x_{i-1}^{(k)}$。
- **分量形式**：
  $$x_i^{(k)}=\frac1{a_{ii}}\Big[b_i-\sum_{j=1}^{i-1}a_{ij}x_j^{(k)}-\sum_{j=i+1}^na_{ij}x_j^{(k-1)}\Big],\qquad i=1,2,\dots,n\ (\text{按顺序}).$$
- **矩阵形式**：$(D-L)\mathbf x^{(k)}=U\mathbf x^{(k-1)}+\mathbf b$，即
  $$\mathbf x^{(k)}=T_g\mathbf x^{(k-1)}+\mathbf c_g,\qquad T_g=(D-L)^{-1}U,\ \ \mathbf c_g=(D-L)^{-1}\mathbf b.$$
- **与 Jacobi 比较**：几乎总是比 Jacobi **更快**（只需要存一份向量，也更省内存），但**不是总是**：存在 Jacobi 收敛而 Gauss–Seidel 不收敛的方程组。
- 步骤：与 Jacobi 相同，区别只是"边算边用新值"，必须**按 $i=1,2,\dots,n$ 的顺序**。
:::

:::example 例 5.5　课件：Gauss–Seidel 解例 5.4 的方程组
写成
$$\begin{aligned}x_1^{(k)}&=\tfrac1{10}x_2^{(k-1)}-\tfrac15x_3^{(k-1)}+\tfrac35,\\x_2^{(k)}&=\tfrac1{11}x_1^{(k)}+\tfrac1{11}x_3^{(k-1)}-\tfrac3{11}x_4^{(k-1)}+\tfrac{25}{11},\\x_3^{(k)}&=-\tfrac15x_1^{(k)}+\tfrac1{10}x_2^{(k)}+\tfrac1{10}x_4^{(k-1)}-\tfrac{11}{10},\\x_4^{(k)}&=-\tfrac38x_2^{(k)}+\tfrac18x_3^{(k)}+\tfrac{15}8.\end{aligned}$$
**第 1 步**（$\mathbf x^{(0)}=\mathbf 0$）：
$$\begin{aligned}x_1^{(1)}&=0.6000,\\x_2^{(1)}&=\tfrac{0.6+25}{11}=2.3273,\\x_3^{(1)}&=\tfrac{-11-2(0.6)+2.3273}{10}=-0.9873,\\x_4^{(1)}&=\tfrac{15-3(2.3273)-0.9873}{8}=0.8789.\end{aligned}$$
（$x_2^{(1)}$ 用的是**新的** $x_1^{(1)}=0.6$，不是 $x_1^{(0)}=0$。）

| $k$ | $x_1^{(k)}$ | $x_2^{(k)}$ | $x_3^{(k)}$ | $x_4^{(k)}$ | 相对差 |
|---|---|---|---|---|---|
| 1 | 0.6000 | 2.3273 | −0.9873 | 0.8789 | 1 |
| 2 | 1.0302 | 2.0369 | −1.0145 | 0.9843 | 0.21 |
| 3 | 1.0066 | 2.0036 | −1.0025 | 0.9984 | 0.017 |
| 4 | 1.0009 | 2.0003 | −1.0003 | 0.9998 | 0.0029 |
| 5 | 1.0001 | 2.0000 | −1.0000 | 1.0000 | $3.9\times10^{-4}$ |

**5 步**就满足 $\dfrac{\lVert\mathbf x^{(k)}-\mathbf x^{(k-1)}\rVert_\infty}{\lVert\mathbf x^{(k)}\rVert_\infty}<10^{-3}$（Jacobi 要 9–10 步）。5 步后的实际误差 $9.1\times10^{-5}$，Jacobi 的 5 步误差是 $2.1\times10^{-2}$。

**核对**：迭代由程序重算。课件 $k=2$ 行的 $x_4^{(2)}=0.9844$，精确值 $0.98434$，应为 $0.9843$。
:::

:::pitfall
- **顺序不能乱**：必须先算 $x_1^{(k)}$，再算 $x_2^{(k)}$（用到新的 $x_1^{(k)}$），依此类推。
- 每个分量里"下标比 $i$ 小"的用新值（上标 $k$），"下标比 $i$ 大"的用旧值（上标 $k-1$）。
- 5.4 与 5.5 的两个矩阵 $T_j,T_g$ 不同，谱半径也不同，不能互相替换（5.6）。
:::

## 5.6 迭代法的收敛性与误差界 | Convergence and Error Bounds

:::quick
- **什么时候用**：判断 Jacobi / Gauss–Seidel（或任何 $\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c$）是否收敛；比较谁更快；估计 $k$ 步后的误差（2023–24 第 4(d) 题）；写出"可收敛的迭代方程"（2022–23 第 3 题）。
- **基本定理**：对任意初值 $\mathbf x^{(0)}\in\mathbb R^n$，$\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c$ 收敛到 $\mathbf x=T\mathbf x+\mathbf c$ 的唯一解 $\iff\rho(T)<1$。
- **充分条件**：某个自然范数 $\lVert T\rVert<1$。此时收敛，并且有**误差界**：
  $$\lVert\mathbf x-\mathbf x^{(k)}\rVert\le\lVert T\rVert^k\lVert\mathbf x^{(0)}-\mathbf x\rVert,\qquad\lVert\mathbf x-\mathbf x^{(k)}\rVert\le\frac{\lVert T\rVert^k}{1-\lVert T\rVert}\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert.$$
  第二个式子**不需要知道精确解**，估计误差用它。
- **Jacobi 与 Gauss–Seidel**：$T_j=D^{-1}(L+U)$，$T_g=(D-L)^{-1}U$。若 $\rho(T_j)<1$（或 $\rho(T_g)<1$），对应迭代收敛到 $A\mathbf x=\mathbf b$ 的解。
- **严格对角占优** $\Rightarrow$ Jacobi 和 Gauss–Seidel **都**对任意初值收敛。
- **快慢比较**：$\rho(T)$ 越小，渐近收敛越快（误差大约每步乘以 $\rho(T)$）。
- **Stein–Rosenberg 定理**：若 $a_{ij}\le0$（$i\ne j$）且 $a_{ii}>0$，则下面四种情形**恰有一种**成立：
  1. $0\le\rho(T_g)<\rho(T_j)<1$（都收敛，GS 更快）；
  2. $1<\rho(T_j)<\rho(T_g)$（都发散，GS 发散更快）；
  3. $\rho(T_j)=\rho(T_g)=0$；
  4. $\rho(T_j)=\rho(T_g)=1$。
- 步骤（判断收敛、比较快慢，写迭代方程）：
  1. 写出 $D,\ L,\ U$（$A=D-L-U$）；
  2. $T_j=D^{-1}(L+U)$，$T_g=(D-L)^{-1}U$，以及 $\mathbf c_j,\mathbf c_g$；
  3. 求谱半径：$T_j$ 用 $\det(\lambda D-(L+U))=0$，$T_g$ 用 $\det(\lambda(D-L)-U)=0$（避免求逆）；
  4. $\rho<1$ 的那个收敛，写出 $\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c$；
  5. 两个都收敛时，比较 $\rho$。
  
  **捷径**：若 $A$ 严格对角占优，直接说"两个都收敛"。
:::

:::proof ★ 引理：$\rho(T)<1\Rightarrow(I-T)^{-1}=\sum_{j=0}^\infty T^j$
**$I-T$ 可逆**：若 $\lambda$ 是 $T$ 的特征值（$T\mathbf x=\lambda\mathbf x$），则 $(I-T)\mathbf x=(1-\lambda)\mathbf x$，所以 $1-\lambda$ 是 $I-T$ 的特征值。$\lvert\lambda\rvert\le\rho(T)<1$，所以 $\lambda\ne1$，$I-T$ 没有零特征值，可逆。

**级数**：令 $S_m=I+T+\cdots+T^m$，则
$$(I-T)S_m=(I+T+\cdots+T^m)-(T+T^2+\cdots+T^{m+1})=I-T^{m+1}.$$
因为 $\rho(T)<1$，$T$ 是收敛矩阵（5.3），$T^{m+1}\to O$，所以 $(I-T)\lim_{m\to\infty}S_m=I$，即 $(I-T)^{-1}=\lim S_m=\sum_{j=0}^\infty T^j$。
:::

:::proof ★ 基本定理：$\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c$ 收敛 $\iff\rho(T)<1$
**（$\Leftarrow$）** 设 $\rho(T)<1$。反复代入：
$$\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c=T^2\mathbf x^{(k-2)}+(T+I)\mathbf c=\cdots=T^k\mathbf x^{(0)}+(T^{k-1}+\cdots+T+I)\mathbf c.$$
$T$ 是收敛矩阵，$T^k\mathbf x^{(0)}\to\mathbf 0$；由引理，$\sum_{j=0}^{k-1}T^j\to(I-T)^{-1}$。所以
$$\lim_{k\to\infty}\mathbf x^{(k)}=(I-T)^{-1}\mathbf c=:\mathbf x,\qquad\text{且 }\mathbf x=T\mathbf x+\mathbf c.$$
**（$\Rightarrow$）** 设对任意 $\mathbf x^{(0)}$ 都收敛到 $\mathbf x=T\mathbf x+\mathbf c$ 的解。任取 $\mathbf z\in\mathbb R^n$，令 $\mathbf x^{(0)}=\mathbf x-\mathbf z$。由 $\mathbf x=T\mathbf x+\mathbf c$ 减去 $\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c$：
$$\mathbf x-\mathbf x^{(k)}=T(\mathbf x-\mathbf x^{(k-1)})=\cdots=T^k(\mathbf x-\mathbf x^{(0)})=T^k\mathbf z.$$
因为 $\mathbf x^{(k)}\to\mathbf x$，所以 $T^k\mathbf z\to\mathbf 0$。$\mathbf z$ 任意，由 5.3 的等价条件（5），$T$ 是收敛矩阵，$\rho(T)<1$。

**考场用法**：这是"$\rho(T)<1$ 是充要条件"的来历，也解释了为什么 2022–23 填空"收敛时的条件"答 $\rho(T)<1$。
:::

:::proof ★ 误差界（推论）
设 $\lVert T\rVert<1$（某个自然范数）。因为 $\rho(T)\le\lVert T\rVert<1$，迭代收敛到 $\mathbf x$。

**第一式**：由 $\mathbf x-\mathbf x^{(k)}=T(\mathbf x-\mathbf x^{(k-1)})$，反复代入得 $\mathbf x-\mathbf x^{(k)}=T^k(\mathbf x-\mathbf x^{(0)})$，所以
$$\lVert\mathbf x-\mathbf x^{(k)}\rVert\le\lVert T\rVert^k\lVert\mathbf x-\mathbf x^{(0)}\rVert.$$
**第二式**：相邻两项之差满足 $\mathbf x^{(m+1)}-\mathbf x^{(m)}=T(\mathbf x^{(m)}-\mathbf x^{(m-1)})=\cdots=T^m(\mathbf x^{(1)}-\mathbf x^{(0)})$。因为 $\mathbf x^{(M)}\to\mathbf x$，
$$\mathbf x-\mathbf x^{(k)}=\sum_{m=k}^\infty\big(\mathbf x^{(m+1)}-\mathbf x^{(m)}\big),$$
取范数并用三角不等式：
$$\lVert\mathbf x-\mathbf x^{(k)}\rVert\le\sum_{m=k}^\infty\lVert T\rVert^m\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert=\frac{\lVert T\rVert^k}{1-\lVert T\rVert}\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert.$$
**考场用法**：2023–24 第 4(d) 题直接代入第二式。
:::

:::proof ★ 严格对角占优 $\Rightarrow$ Jacobi 收敛
严格对角占优：$\lvert a_{ii}\rvert>\sum_{j\ne i}\lvert a_{ij}\rvert$。$T_j=D^{-1}(L+U)$ 的第 $i$ 行是 $\big(-a_{ij}/a_{ii}\big)_{j\ne i}$，对角元为 0。所以
$$\lVert T_j\rVert_\infty=\max_i\sum_{j\ne i}\frac{\lvert a_{ij}\rvert}{\lvert a_{ii}\rvert}<1.$$
由 5.6 的充分条件，Jacobi 对任意初值收敛。
:::

:::proof ☆ 📘 严格对角占优 $\Rightarrow$ Gauss–Seidel 收敛
只需证 $\rho(T_g)<1$。设 $\lambda$ 是 $T_g$ 的特征值，$\mathbf x\ne\mathbf 0$ 是特征向量，$T_g\mathbf x=\lambda\mathbf x$，即 $U\mathbf x=\lambda(D-L)\mathbf x$。写出第 $i$ 个分量（$L,U$ 的元素是 $-a_{ij}$）：
$$\lambda\Big(a_{ii}x_i+\sum_{j<i}a_{ij}x_j\Big)=-\sum_{j>i}a_{ij}x_j.$$
取 $i$ 使 $\lvert x_i\rvert=\lVert\mathbf x\rVert_\infty>0$，于是 $\lvert x_j\rvert\le\lvert x_i\rvert$（$\forall j$）。对括号里的量用三角不等式的反向形式：
$$\Big\lvert a_{ii}x_i+\sum_{j<i}a_{ij}x_j\Big\rvert\ge\lvert a_{ii}\rvert\lvert x_i\rvert-\sum_{j<i}\lvert a_{ij}\rvert\lvert x_j\rvert\ge\Big(\lvert a_{ii}\rvert-\sum_{j<i}\lvert a_{ij}\rvert\Big)\lvert x_i\rvert.$$
等式右边取绝对值，$\bigl\lvert\sum_{j>i}a_{ij}x_j\bigr\rvert\le\sum_{j>i}\lvert a_{ij}\rvert\lvert x_i\rvert$。合起来并除以 $\lvert x_i\rvert$：
$$\lvert\lambda\rvert\Big(\lvert a_{ii}\rvert-\sum_{j<i}\lvert a_{ij}\rvert\Big)\le\sum_{j>i}\lvert a_{ij}\rvert.$$
由严格对角占优，括号 $\lvert a_{ii}\rvert-\sum_{j<i}\lvert a_{ij}\rvert>\sum_{j>i}\lvert a_{ij}\rvert\ge0$。若 $\lvert\lambda\rvert\ge1$，则左边 $\ge\lvert a_{ii}\rvert-\sum_{j<i}\lvert a_{ij}\rvert>\sum_{j>i}\lvert a_{ij}\rvert$ = 右边，矛盾。所以 $\lvert\lambda\rvert<1$，$\rho(T_g)<1$。
:::

:::proof ☆ Jacobi 的极限确实是 $A\mathbf x=\mathbf b$ 的解（课件的说明）
若 Jacobi 序列收敛到 $\mathbf x$，则 $\mathbf x=D^{-1}(L+U)\mathbf x+D^{-1}\mathbf b$，两边乘 $D$：$D\mathbf x=(L+U)\mathbf x+\mathbf b$，即 $(D-L-U)\mathbf x=\mathbf b$。因为 $D-L-U=A$，所以 $A\mathbf x=\mathbf b$。Gauss–Seidel 同理。
:::

:::example 例 5.6　判断收敛、估计误差（例 5.4 的方程组）
**严格对角占优**：$10>1+2$，$11>1+1+3$，$10>2+1+1$，$8>3+1$，所以 Jacobi 和 Gauss–Seidel **都收敛**。

**谱半径**（程序求特征值）：$\rho(T_j)=0.4264$，$\rho(T_g)=0.0898$。两个都 $<1$，且 $\rho(T_g)<\rho(T_j)$，**Gauss–Seidel 更快**。与例 5.4、5.5 一致：误差每步大约乘 $0.43$（Jacobi）和 $0.09$（GS），Gauss–Seidel 5 步的精度（误差 $9\times10^{-5}$），Jacobi 要约 12 步才能达到（12 步误差 $4.1\times10^{-5}$）。

**用范数估计 Jacobi 的误差**：$T_j$ 的行绝对值和是 $\tfrac{3}{10},\ \tfrac5{11},\ \tfrac4{10},\ \tfrac48$，所以 $\lVert T_j\rVert_\infty=\tfrac12$。由 $\mathbf x^{(1)}=(0.6,\ 2.2727,\ -1.1,\ 1.875)^T$，$\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert_\infty=2.2727$，
$$\lVert\mathbf x-\mathbf x^{(10)}\rVert_\infty\le\frac{(1/2)^{10}}{1-1/2}\times2.2727=4.4\times10^{-3}.$$
实际误差是 $2.3\times10^{-4}$，界是**保守**的（它只用了 $\lVert T_j\rVert_\infty=0.5$，而真正的收敛因子 $\rho(T_j)=0.43$）。

**核对**：$\rho(T_j)$、$\rho(T_g)$、$\lVert T_j\rVert_\infty$ 与实际误差由程序计算。
:::

:::pitfall
- 求 $\rho(T)$ 要用 $T$ 的特征值，不是 $A$ 的；$A$ 的特征值与迭代收敛无关。
- 同一个方程组，**换行之后** $T_j,T_g$ 都会变（2023–24 第 4 题要先换行再求 $T$）。
- 严格对角占优只是**充分**条件：不满足时不能断定发散，要去求 $\rho(T)$。
- 比较快慢看 $\rho(T)$，**不是** $\lVert T\rVert_\infty$。$\lVert T\rVert_\infty<1$ 只是保证收敛并给出（偏大的）误差界。
- 误差界的 $\mathbf x^{(1)}-\mathbf x^{(0)}$ 用的是**前两步**，不需要精确解。
- Stein–Rosenberg 只适用于 $a_{ij}\le0$（$i\ne j$）、$a_{ii}>0$；2023–24 第 4 题的矩阵非对角元是 $+1$，**不适用**。
:::

## 5.7 残差与条件数 | Residuals and Condition Numbers

:::quick
- **什么时候用**：评价近似解 $\tilde{\mathbf x}$ 的好坏；判断方程组是否病态；估计解对数据扰动的敏感性。
- **残差向量**（residual vector）：$\mathbf r=\mathbf b-A\tilde{\mathbf x}$。
- **条件数**（condition number）：$K(A)=\lVert A\rVert\,\lVert A^{-1}\rVert$。$K(A)\ge1$；$K(A)$ 接近 1 称**良态**（well-conditioned），$K(A)$ 很大称**病态**（ill-conditioned）。
- **误差界**：设 $\tilde{\mathbf x}$ 是近似解，$\mathbf r$ 是它的残差（任意自然范数）：
  $$\lVert\mathbf x-\tilde{\mathbf x}\rVert\le\lVert\mathbf r\rVert\,\lVert A^{-1}\rVert,\qquad\frac{\lVert\mathbf x-\tilde{\mathbf x}\rVert}{\lVert\mathbf x\rVert}\le K(A)\frac{\lVert\mathbf r\rVert}{\lVert\mathbf b\rVert}\quad(\mathbf x\ne\mathbf 0,\ \mathbf b\ne\mathbf 0).$$
- 📘 **扰动定理**：若 $A$ 可逆，$\lVert\delta A\rVert\le\dfrac1{\lVert A^{-1}\rVert}$，$\tilde{\mathbf x}$ 是 $(A+\delta A)\tilde{\mathbf x}=\mathbf b+\delta\mathbf b$ 的解，则
  $$\frac{\lVert\mathbf x-\tilde{\mathbf x}\rVert}{\lVert\mathbf x\rVert}\le\frac{K(A)\lVert A\rVert}{\lVert A\rVert-K(A)\lVert\delta A\rVert}\Big(\frac{\lVert\delta\mathbf b\rVert}{\lVert\mathbf b\rVert}+\frac{\lVert\delta A\rVert}{\lVert A\rVert}\Big).$$
- **含义**：$A$ 良态时，$A,\mathbf b$ 的小变化只引起解的小变化；$A$ 病态时，**残差很小也不能保证近似解很准**，数据的小变化可能使解大变。
- 步骤（算 $K_\infty(A)$）：1. 求 $A^{-1}$（2×2 用公式）；2. 分别算 $\lVert A\rVert_\infty,\lVert A^{-1}\rVert_\infty$（最大行和）；3. 相乘。
:::

:::proof ★ 残差误差界
由 $\mathbf r=\mathbf b-A\tilde{\mathbf x}=A\mathbf x-A\tilde{\mathbf x}$ 和 $A$ 可逆，$\mathbf x-\tilde{\mathbf x}=A^{-1}\mathbf r$。所以
$$\lVert\mathbf x-\tilde{\mathbf x}\rVert=\lVert A^{-1}\mathbf r\rVert\le\lVert A^{-1}\rVert\lVert\mathbf r\rVert.$$
又 $\mathbf b=A\mathbf x$，$\lVert\mathbf b\rVert\le\lVert A\rVert\lVert\mathbf x\rVert$，即 $\dfrac1{\lVert\mathbf x\rVert}\le\dfrac{\lVert A\rVert}{\lVert\mathbf b\rVert}$。于是
$$\frac{\lVert\mathbf x-\tilde{\mathbf x}\rVert}{\lVert\mathbf x\rVert}\le\lVert A\rVert\lVert A^{-1}\rVert\frac{\lVert\mathbf r\rVert}{\lVert\mathbf b\rVert}=K(A)\frac{\lVert\mathbf r\rVert}{\lVert\mathbf b\rVert}.$$
:::

:::proof ☆ $K(A)\ge1$
对自然范数 $\lVert I\rVert=1$，所以 $1=\lVert I\rVert=\lVert AA^{-1}\rVert\le\lVert A\rVert\lVert A^{-1}\rVert=K(A)$。
:::

:::example 例 5.7　📘 小残差、大误差：病态方程组
$$\begin{cases}x_1+2x_2=3\\1.0001x_1+2x_2=3.0001\end{cases}\qquad A=\begin{pmatrix}1&2\\1.0001&2\end{pmatrix},\ \mathbf b=\begin{pmatrix}3\\3.0001\end{pmatrix},$$
精确解 $\mathbf x=(1,1)^T$。取近似解 $\tilde{\mathbf x}=(3,0)^T$。

**残差**：$A\tilde{\mathbf x}=(3,\ 3.0003)^T$，$\mathbf r=\mathbf b-A\tilde{\mathbf x}=(0,\ -0.0002)^T$，$\lVert\mathbf r\rVert_\infty=0.0002$——很小。
**实际误差**：$\lVert\mathbf x-\tilde{\mathbf x}\rVert_\infty=\lVert(-2,1)^T\rVert_\infty=2$——很大。

**条件数**：$\det A=2-2.0002=-0.0002$，
$$A^{-1}=\frac1{-0.0002}\begin{pmatrix}2&-2\\-1.0001&1\end{pmatrix}=\begin{pmatrix}-10000&10000\\5000.5&-5000\end{pmatrix}.$$
$\lVert A\rVert_\infty=\max\{3,\ 3.0001\}=3.0001$，$\lVert A^{-1}\rVert_\infty=\max\{20000,\ 10000.5\}=20000$，
$$K_\infty(A)=3.0001\times20000\approx60002.$$
**验证误差界**：
$$\lVert\mathbf x-\tilde{\mathbf x}\rVert_\infty=2\le\lVert\mathbf r\rVert_\infty\lVert A^{-1}\rVert_\infty=0.0002\times20000=4\ \checkmark,$$
$$\frac{2}{1}=2\le K(A)\frac{\lVert\mathbf r\rVert_\infty}{\lVert\mathbf b\rVert_\infty}=60002\times\frac{0.0002}{3.0001}=4.0\ \checkmark.$$
**结论**：$K\approx6\times10^4$，是严重病态；残差 $2\times10^{-4}$ 对应的误差可以大到 2。

**核对**：$A^{-1}$、$K_\infty$、误差界与实际误差由程序重算。例子来自教材 Burden & Faires §7.5，课件只讲了定义和定理。
:::

:::pitfall
- 条件数和**范数选择**有关（$K_\infty\ne K_2$），题目说用哪个范数就算哪个。
- 小残差不一定意味着小误差——病态时尤其如此；这是 5.7 最重要的一点。
- 误差界是**上界**，实际误差常常小很多（例 5.7 里实际误差 2，界 4）。
- 求 $K(A)$ 要算 $A^{-1}$，高维时代价大，考试里一般只有 $2\times2$ 或 $3\times3$。
:::

## 真题精解 | Past Exam Problems

说明：2025–26 是原卷；2022–23 到 2024–25 是同学回忆版，题干和数据常有缺失，缺的地方我写明了怎么处理。本讲的真题放在最后，因为它们都是综合用到 5.1–5.7。

:::problem 真题 1 · 2025–26 第 5(a) 题（5 分）· 特征值的上下界
#### 题目
Let $A\in\mathbb R^{n\times n}$ be an invertible matrix, and let $\lambda$ be any eigenvalue of $A$. Prove that for any subordinate matrix norm $\lVert\cdot\rVert$, the following inequality holds:
$$\frac1{\lVert A^{-1}\rVert}\le\lvert\lambda\rvert\le\lVert A\rVert.$$

#### 思路
对应 5.2 的"特征值上下界"。两个不等式都从 $\lVert A\mathbf x\rVert\le\lVert A\rVert\lVert\mathbf x\rVert$ 出发：右边直接用，左边对 $A^{-1}$ 再用一次。

#### 解
设 $\mathbf x\ne\mathbf 0$ 是 $\lambda$ 对应的特征向量：$A\mathbf x=\lambda\mathbf x$。

**右边（$\lvert\lambda\rvert\le\lVert A\rVert$）**：两边取范数，用从属范数的性质 $\lVert A\mathbf x\rVert\le\lVert A\rVert\lVert\mathbf x\rVert$：
$$\lvert\lambda\rvert\lVert\mathbf x\rVert=\lVert\lambda\mathbf x\rVert=\lVert A\mathbf x\rVert\le\lVert A\rVert\lVert\mathbf x\rVert.$$
除以 $\lVert\mathbf x\rVert>0$ 得 $\lvert\lambda\rvert\le\lVert A\rVert$。

**左边（$\lvert\lambda\rvert\ge1/\lVert A^{-1}\rVert$）**：$A$ 可逆，所以 $\lambda\ne0$（若 $\lambda=0$，$A\mathbf x=\mathbf 0$ 有非零解，与 $A$ 可逆矛盾）。由 $A\mathbf x=\lambda\mathbf x$ 左乘 $A^{-1}$：
$$\mathbf x=\lambda A^{-1}\mathbf x\ \Rightarrow\ A^{-1}\mathbf x=\frac1\lambda\mathbf x.$$
对这个等式取范数：
$$\frac1{\lvert\lambda\rvert}\lVert\mathbf x\rVert=\lVert A^{-1}\mathbf x\rVert\le\lVert A^{-1}\rVert\lVert\mathbf x\rVert\ \Rightarrow\ \frac1{\lvert\lambda\rvert}\le\lVert A^{-1}\rVert\ \Rightarrow\ \lvert\lambda\rvert\ge\frac1{\lVert A^{-1}\rVert}.$$
（$\lVert A^{-1}\rVert>0$，因为 $A^{-1}\ne O$。）

两边合起来：$\dfrac1{\lVert A^{-1}\rVert}\le\lvert\lambda\rvert\le\lVert A\rVert$。$\blacksquare$

#### 核对
例 5.1 的 $A$（特征值 $1,\ 2\pm\sqrt3i$，模分别是 $1,\ \sqrt7,\ \sqrt7$）：$\lVert A\rVert_\infty=7$，$\lVert A^{-1}\rVert_\infty=4.1429$，$1/\lVert A^{-1}\rVert_\infty=0.2414$，所以
$$0.2414=\frac1{\lVert A^{-1}\rVert_\infty}\le\lvert\lambda\rvert\in\{1,\ 2.646\}\le\lVert A\rVert_\infty=7\ \checkmark.$$
换成 2-范数：$1/\lVert A^{-1}\rVert_2=0.3424\le\lvert\lambda\rvert\le\lVert A\rVert_2=5.2824$，同样成立。数值由程序计算。

#### 变形
- 这个不等式说明：所有特征值落在圆环 $\dfrac1{\lVert A^{-1}\rVert}\le\lvert z\rvert\le\lVert A\rVert$ 内。
- 它蕴含 $K(A)=\lVert A\rVert\lVert A^{-1}\rVert\ge\dfrac{\lvert\lambda_{\max}\rvert}{\lvert\lambda_{\min}\rvert}\ge1$（5.7）。
- 复特征值的情形：把范数自然延拓到 $\mathbb C^n$，证明完全一样；课件和考试按实向量写即可。
:::

:::problem 真题 2 · 2025–26 第 5(b) 题（5 分）· $\lVert A\mathbf x\rVert_2\le\lVert A\rVert_F\lVert\mathbf x\rVert_2$
#### 题目
Let $A\in\mathbb R^{m\times n}$ and $\mathbf x\in\mathbb R^n$. Prove the inequality relating the vector 2-norm and the matrix Frobenius norm:
$$\lVert A\mathbf x\rVert_2\le\lVert A\rVert_F\lVert\mathbf x\rVert_2.$$
(Recall that the Frobenius norm is defined as $\lVert A\rVert_F=\big(\sum_{i=1}^m\sum_{j=1}^n\lvert a_{ij}\rvert^2\big)^{1/2}$.)

#### 思路
对应 3.1 的 Cauchy–Schwarz 不等式。$A\mathbf x$ 的每个分量是 $A$ 的一行与 $\mathbf x$ 的内积，对每个分量用一次 Cauchy–Schwarz，再把 $m$ 个分量加起来。

#### 解
记 $A$ 的第 $i$ 行为 $\mathbf a_i^T=(a_{i1},\dots,a_{in})$，则 $(A\mathbf x)_i=\mathbf a_i^T\mathbf x=\sum_{j=1}^na_{ij}x_j$。

**第一步**：对每个 $i$ 用 Cauchy–Schwarz $\lvert\mathbf u^T\mathbf v\rvert\le\lVert\mathbf u\rVert_2\lVert\mathbf v\rVert_2$：
$$\lvert(A\mathbf x)_i\rvert^2=\Big\lvert\sum_ja_{ij}x_j\Big\rvert^2\le\Big(\sum_ja_{ij}^2\Big)\Big(\sum_jx_j^2\Big)=\Big(\sum_ja_{ij}^2\Big)\lVert\mathbf x\rVert_2^2.$$
**第二步**：对 $i=1,\dots,m$ 求和：
$$\lVert A\mathbf x\rVert_2^2=\sum_{i=1}^m\lvert(A\mathbf x)_i\rvert^2\le\Big(\sum_{i=1}^m\sum_{j=1}^na_{ij}^2\Big)\lVert\mathbf x\rVert_2^2=\lVert A\rVert_F^2\lVert\mathbf x\rVert_2^2.$$
**第三步**：两边开平方（都非负）：
$$\lVert A\mathbf x\rVert_2\le\lVert A\rVert_F\lVert\mathbf x\rVert_2.\ \blacksquare$$

#### 核对
例 5.1 的 $A$，取 $\mathbf x=(1,1,1)^T$：$A\mathbf x=(2,\ 2,\ 5)^T$，$\lVert A\mathbf x\rVert_2=\sqrt{33}=5.745$；$\lVert A\rVert_F\lVert\mathbf x\rVert_2=6.557\times\sqrt3=11.357$，$5.745\le11.357$ ✓。

#### 变形
- 对所有 $\mathbf x\ne\mathbf 0$ 取最大：$\lVert A\rVert_2=\max_{\lVert\mathbf x\rVert_2=1}\lVert A\mathbf x\rVert_2\le\lVert A\rVert_F$，即 $\lVert A\rVert_2\le\lVert A\rVert_F$（5.1 里提到的那个不等式）。
- 若题目让你比较等号何时成立：当 $A$ 的秩为 1（$A=\mathbf u\mathbf v^T$）时 $\lVert A\rVert_2=\lVert A\rVert_F$。
:::

:::problem 真题 3 · 2023–24 第 4 题（20 分）· 换行、Jacobi、Gauss–Seidel、证明、误差界
#### 题目（回忆版）
$$x_1+x_2+3x_3=5,\qquad x_1+3x_2+x_3=2,\qquad3x_1+x_2+x_3=-4.$$
(a) 交换矩阵的行，把矩阵变成使雅可比（Jacobi）方法一定收敛的形式（即对角占优矩阵），并用雅可比方法迭代两次。
(b) 用高斯–赛德尔（Gauss–Seidel）方法迭代两次。
(c) 证明 $\rho(M)\le\lVert M\rVert$。
(d) 求 (a) 中雅可比方法 $\mathbf x=T\mathbf x+\mathbf c$ 中 $T$ 的无穷范数，并根据其值，估计 20 次迭代的误差上界。

（回忆版没有写初值，取 $\mathbf x^{(0)}=\mathbf 0$。原作者提醒"数据可能有误"，下面按所记数据作答，精确解为 $(-2.3,\ 0.7,\ 2.2)^T$。）

#### 思路
(a) 4.5 的对角占优判别 + 换行，再用 5.4 的分量公式。(b) 5.5。(c) 5.2 的 ★ 证明。(d) $T_j$ 的 $\infty$ 范数（最大行和），代入 5.6 的第二个误差界。

#### 解
**(a) 换行 + Jacobi**。系数矩阵第 1 行 $\lvert1\rvert<1+3$、第 3 行 $\lvert1\rvert<3+1$ 不满足对角占优。交换第 1、3 行：
$$\begin{cases}3x_1+x_2+x_3=-4\\x_1+3x_2+x_3=2\\x_1+x_2+3x_3=5\end{cases}\qquad\text{每行 }3>1+1=2,\ \text{严格对角占优，Jacobi 对任意初值收敛。}$$
**Jacobi 迭代式**：
$$x_1^{(k)}=\frac{-4-x_2^{(k-1)}-x_3^{(k-1)}}3,\quad x_2^{(k)}=\frac{2-x_1^{(k-1)}-x_3^{(k-1)}}3,\quad x_3^{(k)}=\frac{5-x_1^{(k-1)}-x_2^{(k-1)}}3.$$
$\mathbf x^{(0)}=\mathbf 0$：
$$\mathbf x^{(1)}=\Big(-\tfrac43,\ \tfrac23,\ \tfrac53\Big)^T\approx(-1.3333,\ 0.6667,\ 1.6667)^T,$$
$$\begin{aligned}x_1^{(2)}&=\frac{-4-0.6667-1.6667}3=-2.1111,\\x_2^{(2)}&=\frac{2+1.3333-1.6667}3=0.5556,\\x_3^{(2)}&=\frac{5+1.3333-0.6667}3=1.8889.\end{aligned}$$
$\mathbf x^{(2)}\approx(-2.1111,\ 0.5556,\ 1.8889)^T$。

**(b) Gauss–Seidel**（对同一个换行后的方程组，用最新值）：
$$x_1^{(k)}=\frac{-4-x_2^{(k-1)}-x_3^{(k-1)}}3,\quad x_2^{(k)}=\frac{2-x_1^{(k)}-x_3^{(k-1)}}3,\quad x_3^{(k)}=\frac{5-x_1^{(k)}-x_2^{(k)}}3.$$
第 1 步：$x_1^{(1)}=-\tfrac43$；$x_2^{(1)}=\dfrac{2+\frac43-0}3=\tfrac{10}9\approx1.1111$；$x_3^{(1)}=\dfrac{5+\frac43-\frac{10}9}3=\tfrac{47}{27}\approx1.7407$。
第 2 步：
$$x_1^{(2)}=\frac{-4-\frac{10}9-\frac{47}{27}}3=-\frac{185}{81}\approx-2.2840,\qquad x_2^{(2)}=\frac{2+\frac{185}{81}-\frac{47}{27}}3=\frac{206}{243}\approx0.8477,$$
$$x_3^{(2)}=\frac{5+\frac{185}{81}-\frac{206}{243}}3=\frac{1564}{729}\approx2.1454.$$
$\mathbf x^{(2)}\approx(-2.2840,\ 0.8477,\ 2.1454)^T$，按 $\infty$ 范数，GS 的误差 $\lVert\mathbf x^{(2)}-\mathbf x\rVert_\infty=0.148$，Jacobi 的是 $0.311$（Jacobi 的 $\mathbf x^{(2)}=(-2.1111,\ 0.5556,\ 1.8889)^T$），GS 整体更接近 $(-2.3,\ 0.7,\ 2.2)^T$。

**(c) 证明 $\rho(M)\le\lVert M\rVert$**（自然范数）：设 $\lambda$ 是 $M$ 的任一特征值，$\mathbf x$ 是对应特征向量，$\lVert\mathbf x\rVert=1$。则
$$\lvert\lambda\rvert=\lvert\lambda\rvert\lVert\mathbf x\rVert=\lVert\lambda\mathbf x\rVert=\lVert M\mathbf x\rVert\le\lVert M\rVert\lVert\mathbf x\rVert=\lVert M\rVert.$$
对所有特征值取最大：$\rho(M)=\max\lvert\lambda\rvert\le\lVert M\rVert$。$\blacksquare$

**(d) $\lVert T\rVert_\infty$ 与误差界**。Jacobi 的 $T=D^{-1}(L+U)$，$D=3I$，$L+U$ 是全 1 矩阵去掉对角线，
$$T=-\frac13\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad\mathbf c=\Big(-\tfrac43,\ \tfrac23,\ \tfrac53\Big)^T.$$
$T$ 每行绝对值之和都是 $\tfrac13+\tfrac13=\tfrac23$，所以
$$\lVert T\rVert_\infty=\frac23<1.$$
由 5.6 的误差界（$\mathbf x^{(1)}=\mathbf c$，$\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert_\infty=\tfrac53$）：
$$\lVert\mathbf x-\mathbf x^{(20)}\rVert_\infty\le\frac{\lVert T\rVert_\infty^{20}}{1-\lVert T\rVert_\infty}\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert_\infty=\frac{(2/3)^{20}}{1/3}\times\frac53=5\Big(\frac23\Big)^{20}\approx5\times3.007\times10^{-4}\approx1.5\times10^{-3}.$$

#### 核对
程序：换行后精确解 $(-2.3,\ 0.7,\ 2.2)$；Jacobi $\mathbf x^{(1)},\mathbf x^{(2)}$、Gauss–Seidel $\mathbf x^{(1)},\mathbf x^{(2)}$ 与上面一致；$\lVert T_j\rVert_\infty=0.6667$；误差界 $1.50\times10^{-3}$，Jacobi 20 步的**实际误差**是 $6.0\times10^{-5}$，界保守约 25 倍。

#### 变形
- 若 (d) 问"估计"，写 $\lesssim1.5\times10^{-3}$，并说明这是由 $\lVert T\rVert_\infty=2/3$ 得到的**上界**，实际误差更小。
- 如果用另一个界 $\lVert T\rVert^{20}\lVert\mathbf x^{(0)}-\mathbf x\rVert_\infty=(2/3)^{20}\times2.3=6.9\times10^{-4}$，需要知道精确解，一般不用。
- 没给初值时一定写明"取 $\mathbf x^{(0)}=\mathbf 0$"。
:::

:::problem 真题 4 · 2022–23 第 3 题 / 2024–25 第 3 题 · 谱半径与收敛速度的比较
#### 题目（回忆版，数据丢失）
- 2022–23 第 3 题：给定了一个方程组，求解 Jacobi 和 Gauss–Seidel 迭代方法的谱半径，判断哪个方法可以收敛，写出可收敛的迭代方程。
- 2024–25 第 3 题：Gauss–Seidel 求线性方程组的解迭代两次；Jacobi 迭代两次（初值都是 $(0,0,0,0)^T$）；是否收敛，如果收敛哪个方法收敛更快。

这两道题的方程组都没有记下来。下面用**两个有数据的方程组**把题型做一遍：先用真题 3 的 $3\times3$ 方程组（手算谱半径的完整过程），再用 5.4 的 $4\times4$ 方程组（与 2024–25 同样是 4 元、初值 $\mathbf 0$）。

#### 思路
按 5.6 的步骤：写 $D,L,U$ → $T_j,T_g$ → 用 $\det(\lambda D-(L+U))=0$、$\det(\lambda(D-L)-U)=0$ 求谱半径 → 判断收敛 → 写迭代方程。

#### 解 A：$3\times3$（真题 3 换行后的方程组）
$$A=\begin{pmatrix}3&1&1\\1&3&1\\1&1&3\end{pmatrix},\quad D=3I,\quad L=-\begin{pmatrix}0&0&0\\1&0&0\\1&1&0\end{pmatrix},\quad U=-\begin{pmatrix}0&1&1\\0&0&1\\0&0&0\end{pmatrix}.$$
**Jacobi**：$T_j=D^{-1}(L+U)=-\tfrac13\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix}$。特征方程
$$\det(\lambda D-(L+U))=\det\begin{pmatrix}3\lambda&1&1\\1&3\lambda&1\\1&1&3\lambda\end{pmatrix}=27\lambda^3-9\lambda+2=(3\lambda-1)^2(3\lambda+2)=0,$$
特征值 $\tfrac13,\ \tfrac13,\ -\tfrac23$，
$$\rho(T_j)=\frac23<1.$$
**Gauss–Seidel**：$D-L=\begin{pmatrix}3&0&0\\1&3&0\\1&1&3\end{pmatrix}$，$U=\begin{pmatrix}0&-1&-1\\0&0&-1\\0&0&0\end{pmatrix}$。特征方程
$$\det(\lambda(D-L)-U)=\det\begin{pmatrix}3\lambda&1&1\\\lambda&3\lambda&1\\\lambda&\lambda&3\lambda\end{pmatrix}=27\lambda^3-8\lambda^2+\lambda=\lambda(27\lambda^2-8\lambda+1)=0,$$
特征值 $\lambda=0,\ \dfrac{4\pm\sqrt{11}\,i}{27}$，模 $\sqrt{\dfrac{16+11}{27^2}}=\dfrac1{\sqrt{27}}$，
$$\rho(T_g)=\frac1{3\sqrt3}\approx0.1925<1.$$
**结论**：两个都收敛（也可由严格对角占优直接得到）；$\rho(T_g)=0.19<\rho(T_j)=0.67$，**Gauss–Seidel 收敛更快**，误差每步约乘 $0.19$（Jacobi 乘 $0.67$）。

**可收敛的迭代方程**（Gauss–Seidel 的矩阵形式 $\mathbf x^{(k)}=T_g\mathbf x^{(k-1)}+\mathbf c_g$）：
$$T_g=(D-L)^{-1}U=\begin{pmatrix}0&-\tfrac13&-\tfrac13\\0&\tfrac19&-\tfrac29\\0&\tfrac2{27}&\tfrac5{27}\end{pmatrix},\qquad\mathbf c_g=(D-L)^{-1}\mathbf b=\Big(-\tfrac43,\ \tfrac{10}9,\ \tfrac{47}{27}\Big)^T.$$
Jacobi 的则是 $T_j$ 与 $\mathbf c_j=(-\tfrac43,\ \tfrac23,\ \tfrac53)^T$。

**实际误差对比**（真题 3 的程序结果，$\lVert\cdot\rVert_\infty$）：

| $k$ | Jacobi | Gauss–Seidel |
|---|---|---|
| 5 | $3.7\times10^{-2}$ | $1.8\times10^{-3}$ |
| 10 | $3.5\times10^{-3}$ | $3.7\times10^{-7}$ |
| 20 | $6.0\times10^{-5}$ | $1.9\times10^{-14}$ |

#### 解 B：$4\times4$（5.4 的方程组，初值 $\mathbf 0$，各迭代两次）
- **Gauss–Seidel**（例 5.5）：$\mathbf x^{(1)}=(0.6000,\ 2.3273,\ -0.9873,\ 0.8789)^T$，$\mathbf x^{(2)}=(1.0302,\ 2.0369,\ -1.0145,\ 0.9843)^T$。
- **Jacobi**（例 5.4）：$\mathbf x^{(1)}=(0.6000,\ 2.2727,\ -1.1000,\ 1.8750)^T$，$\mathbf x^{(2)}=(1.0473,\ 1.7159,\ -0.8052,\ 0.8852)^T$。
- **是否收敛**：严格对角占优 $\Rightarrow$ 两者都收敛；$\rho(T_j)=0.4264$，$\rho(T_g)=0.0898$，**Gauss–Seidel 更快**（例 5.6）。

#### 核对
$T_j,T_g$ 的特征值由程序独立求出，与手算的特征方程一致：$T_j$ 的特征值 $\tfrac13,\tfrac13,-\tfrac23$，$T_g$ 的特征值 $0,\ 0.1481\pm0.1228i$（即 $\tfrac{4\pm\sqrt{11}i}{27}$）。

#### 变形
- 若题目的 $A$ 不是对角占优：必须用谱半径判断，可能出现 Jacobi 收敛而 GS 不收敛（反之亦然）；只有满足 Stein–Rosenberg 条件（$a_{ij}\le0$，$a_{ii}>0$）时才能断定"同时收敛时 GS 更快"。
- "写出可收敛的迭代方程"就是写出 $\mathbf x^{(k)}=T\mathbf x^{(k-1)}+\mathbf c$ 的具体 $T$ 和 $\mathbf c$（或分量形式），并说明 $\rho(T)<1$。
:::

:::problem 真题 5 · 2022–23 第 2 题 · 对称矩阵的证明（题干丢失）
#### 题目（回忆版）
"对于对称矩阵，证明……"——后面的结论没有记下来。

对称矩阵最常考的是下面几条，每一条的证明都很短。我不知道原题是哪条，**把四条全部证出来**，考场上遇到哪条就用哪条。

#### 解
设 $A$ 是 $n\times n$ 实对称矩阵（$A=A^T$）。

**(1) 特征值都是实数。**（5.2 的 ☆ 证明）设 $A\mathbf x=\lambda\mathbf x$，$\mathbf x\in\mathbb C^n$，$\mathbf x\ne\mathbf 0$。则 $\bar{\mathbf x}^TA\mathbf x=\lambda\lVert\mathbf x\rVert^2$。对这个数取共轭，由 $A$ 实对称：
$$\overline{\bar{\mathbf x}^TA\mathbf x}=\mathbf x^TA\bar{\mathbf x}=\bar{\mathbf x}^TA^T\mathbf x=\bar{\mathbf x}^TA\mathbf x,$$
所以 $\bar{\mathbf x}^TA\mathbf x$ 是实数，$\lambda=\bar{\mathbf x}^TA\mathbf x/\lVert\mathbf x\rVert^2$ 是实数。

**(2) 不同特征值的特征向量正交。** 设 $A\mathbf x=\lambda\mathbf x$，$A\mathbf y=\mu\mathbf y$，$\lambda\ne\mu$：
$$\lambda\,\mathbf x^T\mathbf y=(A\mathbf x)^T\mathbf y=\mathbf x^TA\mathbf y=\mu\,\mathbf x^T\mathbf y\ \Rightarrow\ (\lambda-\mu)\,\mathbf x^T\mathbf y=0\ \Rightarrow\ \mathbf x^T\mathbf y=0.$$
**(3) $\lVert A\rVert_2=\rho(A)$。** $A^TA=A^2$，$A^2$ 的特征值是 $\lambda_i^2$，所以 $\rho(A^TA)=\rho(A)^2$，
$$\lVert A\rVert_2=\sqrt{\rho(A^TA)}=\rho(A).$$
**(4) 对称矩阵正定 $\iff$ 特征值全为正。** 由 $A=QDQ^T$（$Q$ 正交，$D=\operatorname{diag}(\lambda_i)$）。令 $\mathbf y=Q^T\mathbf x$（$\mathbf x\ne\mathbf 0\iff\mathbf y\ne\mathbf 0$），
$$\mathbf x^TA\mathbf x=\mathbf y^TD\mathbf y=\sum_i\lambda_iy_i^2.$$
若所有 $\lambda_i>0$，则对 $\mathbf y\ne\mathbf 0$ 上式 $>0$，$A$ 正定；反过来若某个 $\lambda_k\le0$，取 $\mathbf y=\mathbf e_k$，得 $\mathbf x^TA\mathbf x=\lambda_k\le0$，$A$ 不正定。

#### 核对
例 $A=\begin{pmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{pmatrix}$（4.5 例 4.8 的 $C$）：特征值 $2-\sqrt2,\ 2,\ 2+\sqrt2$（程序求得 $0.586,\ 2,\ 3.414$），全为实数且为正，$\lVert A\rVert_2=\rho(A)=2+\sqrt2=3.414$，与 (1)(3)(4) 一致；$\lVert A\rVert_\infty=4>\rho(A)$，说明不同范数给出不同大小。

#### 变形
- 若原题是"证明对称矩阵的特征值为实数"，写 (1)；"证明 $\lVert A\rVert_2=\rho(A)$"，写 (3)（引用 5.2 的 $\lVert A\rVert_2=\sqrt{\rho(A^TA)}$）。
- 若原题要求的是 Lec 4 的内容（对称正定矩阵有 $LL^T$ 分解），见 4.5 的 ☆ 证明。
:::
