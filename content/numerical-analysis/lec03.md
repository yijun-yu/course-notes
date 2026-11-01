:::exam 本讲在往年真题里
- **2025–26 第 4 题（10 分）**：给定向量序列 $\mathbf x^{(k)}=(e^{-k}\cos k,\ k\sin(1/k),\ 3+k^{-2})^T$，证明收敛并求极限。→ 3.2。
- **2025–26 第 7 题（10 分）**：非线性方程组，以 $\mathbf x^{(0)}=(0,0)^T$ 为初值做一次牛顿迭代。→ 3.4。⚠️ **这道题在初值处雅可比矩阵奇异**，细节见「真题精解」第 1 题。
- 本讲的向量范数与 Cauchy–Schwarz 不等式是 Lec 5 的基础：2025–26 第 5(b) 题 $\lVert A\mathbf x\rVert_2\le\lVert A\rVert_F\lVert\mathbf x\rVert_2$ 就是用 Cauchy–Schwarz 证的（3.1）。
- 2022–23 到 2024–25 的回忆版里没有出现方程组的题。
- 英文术语：vector norm、$L_1/L_2/L_\infty$ norm、converge with respect to a norm、fixed point of $\mathbf G$、coordinate functions、Jacobian matrix、Newton's method for nonlinear systems、gradient descent / steepest descent、line search。
:::

图例：**★ 证明**＝考过或很可能考，建议考前自己推一遍；**☆ 证明**＝理解用，考试只用结论。📘＝课件没有、从教材（Burden & Faires）补充；⚠️＝课件笔误或 OCR 错误。

## 3.1 向量范数与距离 | Vector Norms and Distance

:::quick
- **什么时候用**：度量向量的"大小"和"误差"；证明迭代收敛时衡量 $\mathbf x^{(k)}-\mathbf p$；Lec 5 以后的矩阵范数都建立在它上面。
- **向量范数**是 $\mathbb R^n\to\mathbb R$ 的函数 $\lVert\cdot\rVert$，满足：
  1. $\lVert\mathbf x\rVert\ge0$；
  2. $\lVert\mathbf x\rVert=0\iff\mathbf x=\mathbf 0$；
  3. $\lVert\alpha\mathbf x\rVert=\lvert\alpha\rvert\lVert\mathbf x\rVert$；
  4. 三角不等式 $\lVert\mathbf x+\mathbf y\rVert\le\lVert\mathbf x\rVert+\lVert\mathbf y\rVert$。
- 三个常用范数（$n=1$ 时都退化成绝对值）：
  $$\lVert\mathbf x\rVert_1=\sum_{i=1}^n\lvert x_i\rvert,\qquad \lVert\mathbf x\rVert_2=\Big(\sum_{i=1}^nx_i^2\Big)^{1/2},\qquad \lVert\mathbf x\rVert_\infty=\max_{1\le i\le n}\lvert x_i\rvert.$$
- **距离**：$\lVert\mathbf x-\mathbf y\rVert_2$、$\lVert\mathbf x-\mathbf y\rVert_\infty$。
- **Cauchy–Schwarz 不等式**：
  $$\Big\lvert\mathbf x^T\mathbf y\Big\rvert=\Big\lvert\sum_{i=1}^nx_iy_i\Big\rvert\le\lVert\mathbf x\rVert_2\lVert\mathbf y\rVert_2.$$
- **范数的等价关系**：
  $$\lVert\mathbf x\rVert_\infty\le\lVert\mathbf x\rVert_2\le\sqrt n\,\lVert\mathbf x\rVert_\infty.$$
  📘 另外 $\lVert\mathbf x\rVert_\infty\le\lVert\mathbf x\rVert_1\le n\lVert\mathbf x\rVert_\infty$，$\lVert\mathbf x\rVert_2\le\lVert\mathbf x\rVert_1\le\sqrt n\lVert\mathbf x\rVert_2$。
- 步骤（证某个函数是范数）：逐条验证 1–4，前三条通常一行，难点是第 4 条，$L_2$ 要借助 Cauchy–Schwarz。
:::

#### 几何图像

满足 $\lVert\mathbf x\rVert_2<1$ 的向量构成单位圆（球）内部，满足 $\lVert\mathbf x\rVert_\infty<1$ 的向量构成单位正方形（立方体）内部。正方形包含圆，这正是 $\lVert\mathbf x\rVert_\infty\le\lVert\mathbf x\rVert_2$ 的几何含义：同一个向量，$\infty$ 范数最小。

:::proof ☆ $L_\infty$ 范数的三角不等式
前三条性质显然。对第 4 条，设 $\mathbf x=(x_i)$，$\mathbf y=(y_i)$：
$$\lVert\mathbf x+\mathbf y\rVert_\infty=\max_i\lvert x_i+y_i\rvert\le\max_i\big(\lvert x_i\rvert+\lvert y_i\rvert\big)\le\max_i\lvert x_i\rvert+\max_i\lvert y_i\rvert=\lVert\mathbf x\rVert_\infty+\lVert\mathbf y\rVert_\infty.$$
第一个 $\le$ 用实数的三角不等式，第二个 $\le$ 是"和的最大值不超过最大值之和"。
:::

:::proof ★ Cauchy–Schwarz 不等式
若 $\mathbf x=\mathbf 0$ 或 $\mathbf y=\mathbf 0$，两边都是 0，结论成立。设 $\mathbf x\neq\mathbf 0$，$\mathbf y\neq\mathbf 0$。对任意实数 $\lambda$，
$$0\le\lVert\mathbf x-\lambda\mathbf y\rVert_2^2=\sum_i(x_i-\lambda y_i)^2=\lVert\mathbf x\rVert_2^2-2\lambda\sum_ix_iy_i+\lambda^2\lVert\mathbf y\rVert_2^2,$$
移项：
$$2\lambda\sum_ix_iy_i\le\lVert\mathbf x\rVert_2^2+\lambda^2\lVert\mathbf y\rVert_2^2.$$
取 $\lambda=\lVert\mathbf x\rVert_2/\lVert\mathbf y\rVert_2>0$，代入得
$$2\frac{\lVert\mathbf x\rVert_2}{\lVert\mathbf y\rVert_2}\sum_ix_iy_i\le\lVert\mathbf x\rVert_2^2+\frac{\lVert\mathbf x\rVert_2^2}{\lVert\mathbf y\rVert_2^2}\lVert\mathbf y\rVert_2^2=2\lVert\mathbf x\rVert_2^2,$$
两边乘以 $\dfrac{\lVert\mathbf y\rVert_2}{2\lVert\mathbf x\rVert_2}>0$：
$$\sum_ix_iy_i\le\lVert\mathbf x\rVert_2\lVert\mathbf y\rVert_2.$$
把 $\mathbf x$ 换成 $-\mathbf x$ 得 $-\sum x_iy_i\le\lVert\mathbf x\rVert_2\lVert\mathbf y\rVert_2$，合起来就是带绝对值的形式。

**考场用法（2025–26 第 5(b) 题的核心一步）**：矩阵 $A$ 的第 $i$ 行记作 $\mathbf a_i^T$，则 $(A\mathbf x)_i=\mathbf a_i^T\mathbf x$，由 Cauchy–Schwarz
$$\lvert(A\mathbf x)_i\rvert^2\le\lVert\mathbf a_i\rVert_2^2\lVert\mathbf x\rVert_2^2=\Big(\sum_ja_{ij}^2\Big)\lVert\mathbf x\rVert_2^2.$$
对 $i$ 求和：$\lVert A\mathbf x\rVert_2^2\le\lVert A\rVert_F^2\lVert\mathbf x\rVert_2^2$，开方即得（完整解答见 Lec 5）。
**另一个常见用法**：取 $\mathbf y=(1,1,\dots,1)^T$ 得 $\lVert\mathbf x\rVert_1\le\sqrt n\lVert\mathbf x\rVert_2$。
:::

:::proof ☆ $L_2$ 范数的三角不等式
由 Cauchy–Schwarz，
$$\lVert\mathbf x+\mathbf y\rVert_2^2=\sum_i(x_i+y_i)^2=\lVert\mathbf x\rVert_2^2+2\sum_ix_iy_i+\lVert\mathbf y\rVert_2^2\le\lVert\mathbf x\rVert_2^2+2\lVert\mathbf x\rVert_2\lVert\mathbf y\rVert_2+\lVert\mathbf y\rVert_2^2=\big(\lVert\mathbf x\rVert_2+\lVert\mathbf y\rVert_2\big)^2,$$
两边开方即得 $\lVert\mathbf x+\mathbf y\rVert_2\le\lVert\mathbf x\rVert_2+\lVert\mathbf y\rVert_2$。
:::

:::proof ★ $\lVert\mathbf x\rVert_\infty\le\lVert\mathbf x\rVert_2\le\sqrt n\lVert\mathbf x\rVert_\infty$
设 $\lvert x_j\rvert=\max_i\lvert x_i\rvert=\lVert\mathbf x\rVert_\infty$。

- **左边**：$\lVert\mathbf x\rVert_\infty^2=x_j^2\le\sum_{i=1}^nx_i^2=\lVert\mathbf x\rVert_2^2$（求和里至少包含 $x_j^2$ 这一项），所以 $\lVert\mathbf x\rVert_\infty\le\lVert\mathbf x\rVert_2$。
- **右边**：$\lVert\mathbf x\rVert_2^2=\sum_ix_i^2\le\sum_ix_j^2=nx_j^2=n\lVert\mathbf x\rVert_\infty^2$（每一项都不超过最大项），所以 $\lVert\mathbf x\rVert_2\le\sqrt n\lVert\mathbf x\rVert_\infty$。

**考场用法**：由此，$\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty<\varepsilon\Rightarrow\lVert\mathbf x^{(k)}-\mathbf x\rVert_2<\sqrt n\,\varepsilon$；反过来 $\lVert\cdot\rVert_2<\varepsilon\Rightarrow\lVert\cdot\rVert_\infty<\varepsilon$。这是"在一种范数下收敛 ⇒ 在另一种范数下也收敛"的依据（3.2）。
:::

:::example 例 3.1　算范数并验证不等式
设 $\mathbf v=(1,-2,2)^T$，$\mathbf a=(1,2,-2)^T$，$\mathbf b=(3,-1,2)^T$。

**(a)** $\lVert\mathbf v\rVert_1=1+2+2=5$，$\lVert\mathbf v\rVert_2=\sqrt{1+4+4}=3$，$\lVert\mathbf v\rVert_\infty=2$。
验证 $\lVert\mathbf v\rVert_\infty\le\lVert\mathbf v\rVert_2\le\sqrt3\lVert\mathbf v\rVert_\infty$：$2\le3\le2\sqrt3\approx3.464$ ✓。

**(b)** 验证 Cauchy–Schwarz 与 $L_2$ 三角不等式：
$\mathbf a^T\mathbf b=3-2-4=-3$，$\lVert\mathbf a\rVert_2=3$，$\lVert\mathbf b\rVert_2=\sqrt{14}\approx3.742$，
$$\lvert\mathbf a^T\mathbf b\rvert=3\le3\times3.742=11.225\ \checkmark.$$
$\mathbf a+\mathbf b=(4,1,0)^T$，$\lVert\mathbf a+\mathbf b\rVert_2=\sqrt{17}\approx4.123\le3+3.742=6.742$ ✓。

**核对**：数值由程序重算。
:::

:::pitfall
- $\lVert\mathbf x\rVert_2$ 要开方：$\sqrt{\sum x_i^2}$；漏开方是最常见的错误。
- $\lVert\mathbf x\rVert_\infty$ 是**绝对值**的最大值，不是最大的分量（$\mathbf x=(1,-5)^T$ 时是 5）。
- Cauchy–Schwarz 的左边要加绝对值才总成立（课件写成 $\mathbf x^T\mathbf y\le\cdots$，也对，但用在 $\lvert\cdot\rvert$ 时要补上 $-\mathbf x$ 这一步）。
:::

## 3.2 向量序列的极限 | Convergence of Vector Sequences

:::quick
- **什么时候用**：证明向量序列 $\{\mathbf x^{(k)}\}$ 收敛并求极限（2025–26 第 4 题）；证明迭代法收敛。
- **定义**：$\{\mathbf x^{(k)}\}$ 在范数 $\lVert\cdot\rVert$ 下收敛到 $\mathbf x$：对任意 $\varepsilon>0$，存在 $N_\varepsilon$，使
  $$\lVert\mathbf x^{(k)}-\mathbf x\rVert<\varepsilon,\qquad\forall k\ge N_\varepsilon.$$
- **定理（逐分量判别）**：$\{\mathbf x^{(k)}\}$ 在 $L_\infty$ 范数下收敛到 $\mathbf x$ $\iff$ 每个分量都收敛：
  $$\lim_{k\to\infty}x_i^{(k)}=x_i,\qquad i=1,\dots,n.$$
- 由范数等价（3.1），在 $\mathbb R^n$ 里**一种范数下收敛 $\iff$ 任何范数下收敛**，所以通常直接逐分量求极限。
- 步骤：
  1. 对每个分量单独求 $k\to\infty$ 的极限，得到候选极限 $\mathbf x$；
  2. 每个极限都要有依据（已知极限、夹逼、$\varepsilon$–$N$）；
  3. 写"由逐分量判别定理，$\mathbf x^{(k)}\to\mathbf x$"；
  4. （若要）给出 $\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty$ 的上界说明速度。
- 📘 常用极限：$k\sin\dfrac1k\to1$，$\Big(1+\dfrac1k\Big)^k\to e$，$e^{-k}\cdot(\text{有界量})\to0$，$\dfrac{c}{k^p}\to0$（$p>0$）。
:::

:::proof ★ 逐分量判别定理
**($\Rightarrow$)** 设 $\mathbf x^{(k)}\to\mathbf x$（$L_\infty$ 范数）。对任意 $\varepsilon>0$，存在 $N_\varepsilon$，当 $k\ge N_\varepsilon$ 时
$$\max_{i}\lvert x_i^{(k)}-x_i\rvert=\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty<\varepsilon.$$
最大值小于 $\varepsilon$，所以每个 $\lvert x_i^{(k)}-x_i\rvert<\varepsilon$，即 $\lim_kx_i^{(k)}=x_i$（对每个 $i$）。

**($\Leftarrow$)** 设每个分量 $x_i^{(k)}\to x_i$。对给定的 $\varepsilon>0$，对每个 $i$ 存在 $N_{i,\varepsilon}$，使 $k\ge N_{i,\varepsilon}$ 时 $\lvert x_i^{(k)}-x_i\rvert<\varepsilon$。令
$$N_\varepsilon=\max_{1\le i\le n}N_{i,\varepsilon}.$$
$k\ge N_\varepsilon$ 时，所有 $i$ 同时满足 $\lvert x_i^{(k)}-x_i\rvert<\varepsilon$，所以 $\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty<\varepsilon$。

**考场用法**：关键是 $n$ 是有限的，所以可以取有限个 $N_{i,\varepsilon}$ 的最大值。
:::

:::example 例 3.2　课件例：证明 $\mathbf x^{(k)}\to(1,2,0,0)^T$
设 $\mathbf x^{(k)}=\Big(1,\ 2+\dfrac1k,\ \dfrac3{k^2},\ e^{-k}\sin k\Big)^T$，求极限并证明收敛。

**解**：逐分量求极限：
- $x_1^{(k)}=1\to1$；
- $x_2^{(k)}=2+\dfrac1k\to2$；
- $x_3^{(k)}=\dfrac3{k^2}\to0$；
- $x_4^{(k)}=e^{-k}\sin k$，因为 $\lvert e^{-k}\sin k\rvert\le e^{-k}\to0$，由夹逼 $\to0$。

由逐分量判别定理，$\mathbf x^{(k)}\to\mathbf x=(1,2,0,0)^T$（$L_\infty$ 范数）。

**也在 $L_2$ 范数下收敛**：由 $\lVert\cdot\rVert_2\le\sqrt4\,\lVert\cdot\rVert_\infty$，对任意 $\varepsilon>0$，取 $N=N(\varepsilon/2)$，$k\ge N$ 时
$$\lVert\mathbf x^{(k)}-\mathbf x\rVert_2\le2\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty<2\cdot\frac\varepsilon2=\varepsilon.$$

| $k$ | $\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty$ | $\lVert\mathbf x^{(k)}-\mathbf x\rVert_2$ | $2\lVert\cdot\rVert_\infty$ |
|---|---|---|---|
| 1 | 3.0000 | 3.1774 | 6.0000 |
| 2 | 0.7500 | 0.9098 | 1.5000 |
| 5 | 0.2000 | 0.2333 | 0.4000 |
| 10 | 0.1000 | 0.1044 | 0.2000 |
| 100 | 0.0100 | 0.0100 | 0.0200 |

$k\ge3$ 时 $\dfrac3{k^2}\le\dfrac1k$，所以 $\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty=\dfrac1k$。表里每一行都满足 $\lVert\cdot\rVert_\infty\le\lVert\cdot\rVert_2\le2\lVert\cdot\rVert_\infty$ ✓。

**核对**：表中数值由程序计算。
:::

:::pitfall
- 求极限要**每个分量**都有理由，不能只说"显然"。含 $\sin k$、$\cos k$ 的分量，$k\to\infty$ 时它们本身没有极限，必须靠一个趋于 0 的因子（如 $e^{-k}$）夹逼。
- 先猜出极限向量 $\mathbf x$，再证 $\lVert\mathbf x^{(k)}-\mathbf x\rVert\to0$。不能只证 $\lVert\mathbf x^{(k)}\rVert$ 收敛。
- 这个定理是对**有限维**成立的；$n$ 变成无穷时不再成立。
:::

## 3.3 多元不动点迭代 | Fixed Points for Functions of Several Variables

:::quick
- **什么时候用**：把方程组 $\mathbf F(\mathbf x)=\mathbf 0$ 改写成 $\mathbf x=\mathbf G(\mathbf x)$ 后迭代，判断是否收敛、估计误差。
- **方程组**：$f_i(x_1,\dots,x_n)=0$，$i=1,\dots,n$，记成 $\mathbf F(\mathbf x)=\mathbf 0$（$f_i$ 叫坐标函数 coordinate functions）。
- **不动点**：$\mathbf G(\mathbf p)=\mathbf p$。构造方法与 Lec 2 相同：把第 $i$ 个方程解出 $x_i=g_i(\mathbf x)$。
- 设 $D=\{(x_1,\dots,x_n)^T\mid a_i\le x_i\le b_i\}$（"盒子"）。
  - **存在性**：$\mathbf G$ 在 $D$ 上连续，且 $\mathbf G(\mathbf x)\in D$（$\forall\mathbf x\in D$）$\Rightarrow$ $D$ 内有不动点。
  - **收敛定理**：再加上所有 $g_i$ 有连续偏导数，且存在 $K<1$，使
    $$\Big\lvert\frac{\partial g_i(\mathbf x)}{\partial x_j}\Big\rvert\le\frac Kn,\qquad\forall\mathbf x\in D,\ \forall i,j,$$
    则对任意 $\mathbf x^{(0)}\in D$，$\mathbf x^{(k)}=\mathbf G(\mathbf x^{(k-1)})$ 收敛到 $D$ 内唯一的不动点 $\mathbf p$，并且
    $$\lVert\mathbf x^{(k)}-\mathbf p\rVert_\infty\le\frac{K^k}{1-K}\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert_\infty.$$
- **加速**（类似 Lec 5 的 Gauss–Seidel）：算 $x_i^{(k)}$ 时，用刚算出的 $x_1^{(k)},\dots,x_{i-1}^{(k)}$ 代替 $x_1^{(k-1)},\dots,x_{i-1}^{(k-1)}$，通常收敛更快。
- 步骤（用定理判断收敛）：
  1. 取盒子 $D$，验证 $\mathbf G(D)\subseteq D$（逐个 $g_i$ 求值域）；
  2. 求每个 $\lvert\partial g_i/\partial x_j\rvert$ 在 $D$ 上的上界，取 $\max=K/n$，算出 $K$；
  3. 若 $K<1$，引用定理。
- $n=1$ 时 $K/n=K$，退化为 Lec 2 的 $\lvert g'(x)\rvert\le k<1$。
:::

:::proof ☆ 📘 收敛定理的证明思路（课件未证）
**第一步：$\mathbf G$ 是压缩映射。** 取 $\mathbf x,\mathbf y\in D$。$D$ 是盒子，所以线段 $\mathbf y+t(\mathbf x-\mathbf y)$（$0\le t\le1$）在 $D$ 内。对每个 $g_i$ 用一元函数 $\varphi(t)=g_i(\mathbf y+t(\mathbf x-\mathbf y))$ 的中值定理，存在 $\boldsymbol\xi\in D$，
$$g_i(\mathbf x)-g_i(\mathbf y)=\sum_{j=1}^n\frac{\partial g_i}{\partial x_j}(\boldsymbol\xi)(x_j-y_j).$$
所以
$$\lvert g_i(\mathbf x)-g_i(\mathbf y)\rvert\le\sum_{j=1}^n\frac Kn\lvert x_j-y_j\rvert\le n\cdot\frac Kn\lVert\mathbf x-\mathbf y\rVert_\infty=K\lVert\mathbf x-\mathbf y\rVert_\infty.$$
对 $i$ 取最大值：
$$\lVert\mathbf G(\mathbf x)-\mathbf G(\mathbf y)\rVert_\infty\le K\lVert\mathbf x-\mathbf y\rVert_\infty.$$

**第二步：唯一性、收敛、误差界**，与 Lec 2 完全相同，只是把绝对值换成 $\lVert\cdot\rVert_\infty$：
- 若 $\mathbf p,\mathbf q$ 都是不动点：$\lVert\mathbf p-\mathbf q\rVert_\infty=\lVert\mathbf G(\mathbf p)-\mathbf G(\mathbf q)\rVert_\infty\le K\lVert\mathbf p-\mathbf q\rVert_\infty$，$K<1$ 只能 $\mathbf p=\mathbf q$。
- $\lVert\mathbf x^{(k)}-\mathbf p\rVert_\infty=\lVert\mathbf G(\mathbf x^{(k-1)})-\mathbf G(\mathbf p)\rVert_\infty\le K^k\lVert\mathbf x^{(0)}-\mathbf p\rVert_\infty\to0$。
- 误差界：$\lVert\mathbf x^{(k+1)}-\mathbf x^{(k)}\rVert_\infty\le K^k\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert_\infty$，对 $m>k$ 用三角不等式把 $\lVert\mathbf x^{(m)}-\mathbf x^{(k)}\rVert$ 拆成相邻项之和，令 $m\to\infty$，得 $\dfrac{K^k}{1-K}\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert_\infty$。

**存在性**的证明是 Lec 2 中"令 $h(x)=g(x)-x$ 用介值定理"的高维推广（Brouwer 不动点定理），本课程只引用结论。
:::

:::example 例 3.3　课件例：用不动点迭代解三元方程组
$$\begin{aligned}3x_1-\cos(x_2x_3)-\tfrac12&=0,\\ x_1^2-81(x_2+0.1)^2+\sin x_3+1.06&=0,\\ e^{-x_1x_2}+20x_3+\tfrac{10\pi-3}{3}&=0.\end{aligned}$$

**改写**：把第 $i$ 个方程解出 $x_i$：
$$g_1=\tfrac13\cos(x_2x_3)+\tfrac16,\qquad g_2=\tfrac19\sqrt{x_1^2+\sin x_3+1.06}-0.1,\qquad g_3=-\tfrac1{20}e^{-x_1x_2}-\tfrac{10\pi-3}{60}.$$

**验证定理条件**（取 $D=[-1,1]^3$）：

1. **映入自身**。$\lvert x_2x_3\rvert\le1$，所以 $\cos(x_2x_3)\in[\cos1,1]$，$g_1\in[0.3468,\,0.5]$。$x_1^2+\sin x_3+1.06\in[\,1.06-\sin1,\ 1+\sin1+1.06\,]=[0.2185,\,2.9015]$，所以 $g_2\in[-0.0481,\,0.0893]$。$e^{-x_1x_2}\in[e^{-1},e]$，$g_3\in[-0.6095,\,-0.4920]$。三个区间都在 $[-1,1]$ 内。
2. **偏导数界**（$g_1,g_2,g_3$ 关于自己的变量的偏导为 0）：
   $$\Big\lvert\frac{\partial g_1}{\partial x_2}\Big\rvert=\frac{\lvert x_3\sin(x_2x_3)\rvert}3\le\frac{\sin1}3\approx0.2805,\qquad\Big\lvert\frac{\partial g_1}{\partial x_3}\Big\rvert\le\frac{\sin1}3,$$
   $$\Big\lvert\frac{\partial g_2}{\partial x_1}\Big\rvert=\frac{\lvert x_1\rvert}{9\sqrt{x_1^2+\sin x_3+1.06}}\le\frac1{9\sqrt{0.2185}}<0.238,\qquad\Big\lvert\frac{\partial g_2}{\partial x_3}\Big\rvert=\frac{\lvert\cos x_3\rvert}{18\sqrt{\cdots}}<0.119,$$
   $$\Big\lvert\frac{\partial g_3}{\partial x_1}\Big\rvert=\frac{\lvert x_2\rvert e^{-x_1x_2}}{20}\le\frac e{20}<0.14,\qquad\Big\lvert\frac{\partial g_3}{\partial x_2}\Big\rvert<0.14.$$
   所有偏导数的绝对值 $\le\dfrac{\sin1}{3}$，取 $K/3=\dfrac{\sin1}3$，即 $K=\sin1\approx0.8415<1$。
3. 由定理，在 $D$ 内有唯一不动点，迭代对任意 $\mathbf x^{(0)}\in D$ 收敛。

**第一步手算**（$\mathbf x^{(0)}=(0.1,\,0.1,\,-0.1)^T$，同时更新）：
$$x_1^{(1)}=\tfrac13\cos(-0.01)+\tfrac16=0.333317+0.166667=0.499983,$$
$$x_2^{(1)}=\tfrac19\sqrt{0.01+\sin(-0.1)+1.06}-0.1=\tfrac19\sqrt{0.970167}-0.1=0.109441-0.1=0.009441,$$
$$x_3^{(1)}=-\tfrac1{20}e^{-0.01}-\tfrac{10\pi-3}{60}=-0.049503-0.473599=-0.523101.$$

**迭代结果**（课件表，同时更新）：

| $k$ | $x_1^{(k)}$ | $x_2^{(k)}$ | $x_3^{(k)}$ | $\lVert\mathbf x^{(k)}-\mathbf x^{(k-1)}\rVert_\infty$ |
|---|---|---|---|---|
| 0 | 0.10000000 | 0.10000000 | −0.10000000 | |
| 1 | 0.49998333 | 0.00944115 | −0.52310127 | 0.423 |
| 2 | 0.49999593 | 0.00002557 | −0.52336331 | $9.4\times10^{-3}$ |
| 3 | 0.50000000 | 0.00001234 | −0.52359814 | $2.3\times10^{-4}$ |
| 4 | 0.50000000 | 0.00000003 | −0.52359847 | $1.2\times10^{-5}$ |
| 5 | 0.50000000 | 0.00000002 | −0.52359877 | $3.1\times10^{-7}$ |

**加速版**（用最新分量，Gauss–Seidel 式）：

| $k$ | $x_1^{(k)}$ | $x_2^{(k)}$ | $x_3^{(k)}$ | $\lVert\mathbf x^{(k)}-\mathbf x^{(k-1)}\rVert_\infty$ |
|---|---|---|---|---|
| 1 | 0.49998333 | 0.02222979 | −0.52304613 | 0.423 |
| 2 | 0.49997747 | 0.00002815 | −0.52359807 | $2.2\times10^{-2}$ |
| 3 | 0.50000000 | 0.00000004 | −0.52359877 | $2.8\times10^{-5}$ |
| 4 | 0.50000000 | 0.00000000 | −0.52359877 | $3.8\times10^{-8}$ |

4 步就达到同时更新 5 步的精度。精确解是 $\mathbf p=(0.5,\ 0,\ -\pi/6)^T$，$-\pi/6=-0.5235988$ ✓（代入：$g_1=\tfrac13+\tfrac16=0.5$，$g_2=\tfrac19\sqrt{0.25-0.5+1.06}-0.1=\tfrac19\times0.9-0.1=0$，$g_3=-\tfrac1{20}-\tfrac{10\pi-3}{60}=-\tfrac\pi6$）。

**核对**：两张表、值域和偏导数界都由程序重算（偏导数在 $81^3$ 个网格点上取最大值，最大为 $0.2805=\sin1/3$）。定理给出的误差界 $\dfrac{K^k}{1-K}\lVert\mathbf x^{(1)}-\mathbf x^{(0)}\rVert_\infty$ 很保守（$K=0.84$ 收缩得很慢），实际收敛远比它快。
:::

:::pitfall
- 条件是 $\lvert\partial g_i/\partial x_j\rvert\le K/n$，**$n$ 在分母上**；只验证 $\le K<1$ 不够。
- 同一个方程组可以改写成很多种 $\mathbf G$，有的收敛有的不收敛（和 Lec 2 一样）；定理只是充分条件。
- 验证映入自身时，要对每个分量分别求值域，别漏掉 $g_i$ 里的根号、指数在盒子边界处的值。
:::

## 3.4 牛顿法解非线性方程组 | Newton's Method for Nonlinear Systems

:::quick
- **什么时候用**：给定 $\mathbf F(\mathbf x)=\mathbf 0$ 和初值，要求"用牛顿法迭代 $k$ 次"（2025–26 第 7 题）。
- **雅可比矩阵**（Jacobian matrix）$J(\mathbf x)$，第 $i$ 行第 $j$ 列是 $\dfrac{\partial f_i}{\partial x_j}(\mathbf x)$：
  $$J(\mathbf x)=\begin{pmatrix}\dfrac{\partial f_1}{\partial x_1}&\cdots&\dfrac{\partial f_1}{\partial x_n}\\ \vdots&&\vdots\\ \dfrac{\partial f_n}{\partial x_1}&\cdots&\dfrac{\partial f_n}{\partial x_n}\end{pmatrix}.$$
- **牛顿迭代**：
  $$\mathbf x^{(k)}=\mathbf x^{(k-1)}-J(\mathbf x^{(k-1)})^{-1}\mathbf F(\mathbf x^{(k-1)}).$$
- **实际计算（不求逆）**：每步分两小步：
  1. 解线性方程组 $J(\mathbf x^{(k-1)})\,\mathbf y=-\mathbf F(\mathbf x^{(k-1)})$（Lec 4 的高斯消元）；
  2. $\mathbf x^{(k)}=\mathbf x^{(k-1)}+\mathbf y$。
- 停止准则：$\lVert\mathbf y\rVert<\text{TOL}$。
- **收敛**：初值足够接近解，且 $J(\mathbf p)$ 可逆时，**二阶收敛**。
- 优点：快；缺点：每步要算并分解 $J$；需要好的初值；$J(\mathbf x^{(k-1)})$ **必须可逆**（$\det J\neq0$）。
- 步骤：
  1. 写出 $\mathbf F$ 和 $J$（逐个求偏导，三角函数用弧度）；
  2. **先检查 $\det J(\mathbf x^{(0)})\neq0$**；
  3. 代入 $\mathbf x^{(0)}$ 算 $\mathbf F$ 和 $J$；
  4. 解 $J\mathbf y=-\mathbf F$；
  5. $\mathbf x^{(1)}=\mathbf x^{(0)}+\mathbf y$，重复。
- $n=1$ 时 $J=f'$，退化为 Lec 2 的 $p_n=p_{n-1}-f(p_{n-1})/f'(p_{n-1})$。
:::

:::proof ★ 牛顿法的推导（线性化）
在 $\mathbf x^{(k-1)}$ 附近把 $\mathbf F$ 做一阶展开：
$$\mathbf F(\mathbf x)\approx\mathbf F(\mathbf x^{(k-1)})+J(\mathbf x^{(k-1)})\big(\mathbf x-\mathbf x^{(k-1)}\big).$$
令右边等于 $\mathbf 0$，解出 $\mathbf x$（这就是 $\mathbf x^{(k)}$）：
$$J(\mathbf x^{(k-1)})\big(\mathbf x^{(k)}-\mathbf x^{(k-1)}\big)=-\mathbf F(\mathbf x^{(k-1)}),$$
即 $\mathbf y=\mathbf x^{(k)}-\mathbf x^{(k-1)}$ 满足 $J\mathbf y=-\mathbf F$。几何上，是用切"平面"代替曲面，取切平面与零点的交点。

**考场用法**：问"推导牛顿法"就写这几行。上面这个线性方程组能解的前提是 $J$ 可逆，所以 $\det J\neq0$ 是方法能执行的前提条件。
:::

:::proof ☆ 为什么用雅可比矩阵（课件的不动点推导）
把一元情形 $g(x)=x-\phi(x)f(x)$ 推广：令
$$\mathbf G(\mathbf x)=\mathbf x-A(\mathbf x)^{-1}\mathbf F(\mathbf x),$$
其中矩阵 $A(\mathbf x)$ 待定。记 $A(\mathbf x)^{-1}=\big(b_{ij}(\mathbf x)\big)$，则 $g_i(\mathbf x)=x_i-\sum_jb_{ij}(\mathbf x)f_j(\mathbf x)$，
$$\frac{\partial g_i}{\partial x_k}=\delta_{ik}-\sum_{j=1}^n\Big(b_{ij}\frac{\partial f_j}{\partial x_k}+\frac{\partial b_{ij}}{\partial x_k}f_j\Big),\qquad\delta_{ik}=\begin{cases}1,&i=k\\0,&i\neq k.\end{cases}$$
⚠️ 课件把第一项写成 $\partial f_i/\partial x_k$，应为 $\partial f_j/\partial x_k$（对 $j$ 求和）。

要二阶收敛，需要在解 $\mathbf p$ 处所有 $\dfrac{\partial g_i}{\partial x_k}(\mathbf p)=0$。因为 $f_j(\mathbf p)=0$，第二项消失，条件变成
$$\sum_jb_{ij}(\mathbf p)\frac{\partial f_j}{\partial x_k}(\mathbf p)=\delta_{ik}\ \Longleftrightarrow\ A(\mathbf p)^{-1}J(\mathbf p)=I\ \Longleftrightarrow\ A(\mathbf p)=J(\mathbf p).$$
最自然的选择是对所有 $\mathbf x$ 取 $A(\mathbf x)=J(\mathbf x)$，这就是牛顿法。
:::

:::proof ☆ 📘 二阶收敛（课件定理）
设 $\mathbf G$ 满足：在 $\mathbf p$ 的邻域 $N_\delta$ 内，$g_i$ 的一、二阶偏导数连续，$\big\lvert\partial^2g_i/\partial x_j\partial x_k\big\rvert\le M$，并且 $\dfrac{\partial g_i}{\partial x_k}(\mathbf p)=0$（对所有 $i,k$）。则 $\mathbf x^{(0)}$ 足够接近 $\mathbf p$ 时二阶收敛，且
$$\lVert\mathbf x^{(k)}-\mathbf p\rVert_\infty\le\frac{n^2M}2\lVert\mathbf x^{(k-1)}-\mathbf p\rVert_\infty^2.$$

**证明思路**：把 $g_i$ 在 $\mathbf p$ 处做带二阶余项的 Taylor 展开：
$$g_i(\mathbf x)=g_i(\mathbf p)+\sum_k\frac{\partial g_i}{\partial x_k}(\mathbf p)(x_k-p_k)+\frac12\sum_{j,k}\frac{\partial^2g_i}{\partial x_j\partial x_k}(\boldsymbol\xi)(x_j-p_j)(x_k-p_k).$$
一阶项因 $\partial g_i/\partial x_k(\mathbf p)=0$ 全部消失，$g_i(\mathbf p)=p_i$。二阶项共 $n^2$ 项，每项绝对值 $\le M\lVert\mathbf x-\mathbf p\rVert_\infty^2$，所以
$$\lvert g_i(\mathbf x)-p_i\rvert\le\frac{n^2M}2\lVert\mathbf x-\mathbf p\rVert_\infty^2.$$
取 $\mathbf x=\mathbf x^{(k-1)}$，$g_i(\mathbf x^{(k-1)})=x_i^{(k)}$，对 $i$ 取最大值即得。
:::

:::example 例 3.4　课件例：牛顿法解三元方程组（同 3.3 的方程组，$\mathbf x^{(0)}=(0.1,0.1,-0.1)^T$）
$$f_1=3x_1-\cos(x_2x_3)-\tfrac12,\quad f_2=x_1^2-81(x_2+0.1)^2+\sin x_3+1.06,\quad f_3=e^{-x_1x_2}+20x_3+\tfrac{10\pi-3}3.$$

**雅可比矩阵**：
$$J(\mathbf x)=\begin{pmatrix}3&x_3\sin(x_2x_3)&x_2\sin(x_2x_3)\\ 2x_1&-162(x_2+0.1)&\cos x_3\\ -x_2e^{-x_1x_2}&-x_1e^{-x_1x_2}&20\end{pmatrix}.$$

**第一步**（$\mathbf x^{(0)}=(0.1,0.1,-0.1)^T$）：
$$\mathbf F(\mathbf x^{(0)})=\begin{pmatrix}0.3-0.99995-0.5\\0.01-3.24-0.099833+1.06\\0.990050-2+9.471976\end{pmatrix}=\begin{pmatrix}-1.19995\\-2.26983\\8.46203\end{pmatrix},\qquad J(\mathbf x^{(0)})=\begin{pmatrix}3&0.001&-0.001\\0.2&-32.4&0.995004\\-0.099005&-0.099005&20\end{pmatrix}.$$
解 $J\mathbf y=-\mathbf F$（高斯消元）：
$$\mathbf y=(0.399870,\ -0.080533,\ -0.421520)^T,\qquad\mathbf x^{(1)}=\mathbf x^{(0)}+\mathbf y=(0.499870,\ 0.019467,\ -0.521520)^T.$$

**迭代结果**（60 位精度重算）：

| $k$ | $x_1^{(k)}$ | $x_2^{(k)}$ | $x_3^{(k)}$ | $\lVert\mathbf x^{(k)}-\mathbf x^{(k-1)}\rVert_\infty$ |
|---|---|---|---|---|
| 0 | 0.1000000000 | 0.1000000000 | −0.1000000000 | |
| 1 | 0.4998696729 | 0.0194668485 | −0.5215204719 | $4.215\times10^{-1}$ |
| 2 | 0.5000142402 | 0.0015885914 | −0.5235569643 | $1.788\times10^{-2}$ |
| 3 | 0.5000001135 | 0.0000124448 | −0.5235984501 | $1.576\times10^{-3}$ |
| 4 | 0.5000000000 | 0.0000000008 | −0.5235987756 | $1.244\times10^{-5}$ |
| 5 | 0.5000000000 | 0.0000000000 | −0.5235987756 | $7.758\times10^{-10}$ |

**二阶收敛的体现**：$x_2$ 的误差依次是 $1.9\times10^{-2},\,1.6\times10^{-3},\,1.2\times10^{-5},\,7.8\times10^{-10},\,3\times10^{-18}$，比值 $\dfrac{e_{k+1}}{e_k^2}\approx4.9,\,5.0,\,5.0$，趋于常数；每步有效位数大约翻倍。对比 3.3：同一个方程组，不动点迭代 5 步误差在 $10^{-7}$，牛顿法 5 步在 $10^{-18}$。

⚠️ 课件表第 3 行 $x_1^{(3)}=0.5000000113$ 应为 $0.5000001135$，第 4–5 行 $x_2$ 的小量级也与精确值略有出入（$8.5\times10^{-10}$ vs $7.8\times10^{-10}$ 等），应是教材 10 位舍入造成的，不影响结论。

**核对**：用 60 位精度独立重算，并用双精度 NumPy 交叉检验，结果一致。
:::

:::pitfall
- **$\det J(\mathbf x^{(0)})=0$ 时牛顿法无法执行**，$J\mathbf y=-\mathbf F$ 没有唯一解。做题第一件事就是检查它（见真题精解第 1 题）。
- $J$ 的行是方程、列是变量：第 $i$ 行第 $j$ 列是 $\partial f_i/\partial x_j$，写反了就是转置。
- 每一步都要用**新点**重新计算 $J$。只在初值处算一次 $J$ 是"简化牛顿法"，只有线性收敛。
- 不要真的去求 $J^{-1}$，解线性方程组更省、更准。
- 方程组较大时每步代价大（求偏导、解 $n\times n$ 方程组），这是它的缺点。
:::

## 3.5 梯度下降 | Gradient Descent (Steepest Descent)

:::quick
- **什么时候用**：初值不好、牛顿法不收敛时，用它先把初值"拉"到解附近；或需要一个稳健（但慢）的方法。
- **思路**：把"解方程组"变成"求函数最小值"。令
  $$g(\mathbf x)=\sum_{i=1}^nf_i(\mathbf x)^2=\lVert\mathbf F(\mathbf x)\rVert_2^2,$$
  $g\ge0$，且 $g(\mathbf x)=0\iff\mathbf F(\mathbf x)=\mathbf 0$。所以**方程组的解就是 $g$ 的最小点**。
- **梯度**：
  $$\nabla g(\mathbf x)=\Big(\frac{\partial g}{\partial x_1},\dots,\frac{\partial g}{\partial x_n}\Big)^T=2J(\mathbf x)^T\mathbf F(\mathbf x).$$
- **迭代**：$\mathbf x^{(k)}=\mathbf x^{(k-1)}-\alpha\,\nabla g(\mathbf x^{(k-1)})$，$\alpha>0$ 是步长（step size）。
- **步长选择**（教材算法 10.3 的线搜索 line search）：沿方向 $-\nabla g$ 找使 $g$ 最小的 $\alpha$，用三个点的二次插值近似。
- **收敛**：只有**线性**收敛，但对初值要求低，通常即使初值很差也能收敛（到 $g$ 的某个局部最小点）。
- **与牛顿法对比**：

| | 牛顿法 | 梯度下降 |
|---|---|---|
| 求的是 | 根 $\mathbf F(\mathbf x)=\mathbf 0$ | 局部最小点 $g(\mathbf x)=\lVert\mathbf F\rVert_2^2$ |
| 收敛速度 | 二阶 | 线性 |
| 对初值 | 要求高 | 要求低 |
| 每步代价 | 解 $n\times n$ 线性方程组 | 算梯度、一维线搜索 |
| $J$ 奇异时 | 无法执行 | 仍可执行 |

- 步骤：算 $g$ 和 $\nabla g=2J^T\mathbf F$ → 选 $\alpha$ → $\mathbf x\leftarrow\mathbf x-\alpha\nabla g$，重复，直到 $g$ 足够小。
:::

:::proof ☆ $\nabla g=2J^T\mathbf F$
$g=\sum_if_i^2$，对 $x_k$ 求偏导：
$$\frac{\partial g}{\partial x_k}=\sum_{i=1}^n2f_i\frac{\partial f_i}{\partial x_k}=2\sum_iJ_{ik}f_i=2\big(J^T\mathbf F\big)_k.$$
:::

:::proof ☆ 📘 为什么沿 $-\nabla g$ 方向下降最快
沿单位方向 $\mathbf u$（$\lVert\mathbf u\rVert_2=1$）的方向导数是 $D_{\mathbf u}g=\nabla g^T\mathbf u$。由 Cauchy–Schwarz（3.1），
$$-\lVert\nabla g\rVert_2\le\nabla g^T\mathbf u\le\lVert\nabla g\rVert_2,$$
左边的等号当且仅当 $\mathbf u=-\nabla g/\lVert\nabla g\rVert_2$ 时取到。所以 $-\nabla g$ 方向是 $g$ 下降最快的方向。只要 $\nabla g\neq\mathbf 0$，沿这个方向走足够短的一步，$g$ 一定减小。
:::

:::example 例 3.5　梯度下降
**(a)** 📘 手算一步：用 2025–26 第 7 题的方程组（牛顿法在这个初值处失败，见真题精解），$\mathbf F=(5x_1^2-x_2^2,\ x_2-0.25(\sin x_1+\cos x_2))^T$，$\mathbf x^{(0)}=(0,0)^T$。

$\mathbf F(\mathbf x^{(0)})=(0,\,-0.25)^T$，$J(\mathbf x^{(0)})=\begin{pmatrix}0&0\\-0.25&1\end{pmatrix}$（奇异），$g(\mathbf x^{(0)})=0^2+0.25^2=0.0625$。
$$J^T\mathbf F=\begin{pmatrix}0&-0.25\\0&1\end{pmatrix}\begin{pmatrix}0\\-0.25\end{pmatrix}=\begin{pmatrix}0.0625\\-0.25\end{pmatrix},\qquad\nabla g=2J^T\mathbf F=(0.125,\,-0.5)^T.$$
步长不同，结果不同：

| $\alpha$ | $\mathbf x^{(1)}=\mathbf x^{(0)}-\alpha\nabla g$ | $g(\mathbf x^{(1)})$ |
|---|---|---|
| 0.5 | $(-0.0625,\ 0.25)^T$ | 0.00239 |
| 1 | $(-0.125,\ 0.5)^T$ | 0.12674 |
| 2 | $(-0.25,\ 1)^T$ | 1.33157 |

$\alpha=0.5$ 时 $g$ 从 $0.0625$ 降到 $0.0024$；$\alpha\ge1$ 时 $g$ 反而变大，说明步长太大会"越过"最小点。**这就是线搜索的作用。**

**(b)** 课件例：同 3.3 的方程组，$\mathbf x^{(0)}=(0,0,0)^T$，$g(\mathbf x^{(0)})=111.975$，用线搜索选 $\alpha$：

| $k$ | $x_1^{(k)}$ | $x_2^{(k)}$ | $x_3^{(k)}$ | $g(\mathbf x^{(k)})$ |
|---|---|---|---|---|
| 1 | 0.011218 | 0.010096 | −0.522741 | 2.327617 |
| 2 | 0.137860 | −0.205453 | −0.522059 | 1.27406 |
| 3 | 0.266959 | 0.005511 | −0.558494 | 1.06813 |
| 4 | 0.272734 | −0.008118 | −0.522006 | 0.468309 |
| 5 | 0.308689 | −0.020403 | −0.533112 | 0.381087 |
| 6 | 0.314308 | −0.014705 | −0.520923 | 0.318837 |
| 7 | 0.324267 | −0.008525 | −0.528431 | 0.287024 |

（课件表从 $k=2$ 开始列出。）第 1 步就把 $g$ 从 112 降到 2.3，但之后下降很慢，7 步后 $x_1=0.324$，离解 $0.5$ 还远——**线性收敛**。实用做法：先用梯度下降走几步拿到较好的初值，再切换到牛顿法。

**核对**：(a) 的表和 (b) 的表都由程序重算（(b) 按教材算法 10.3 实现线搜索，与课件 $k=2\ldots7$ 的数值逐位一致）。
:::

:::pitfall
- 梯度下降收敛到的是 $g$ 的**局部最小点**，不一定是方程组的解：必须检查 $g$ 是否接近 0。若停在 $g>0$ 的点，说明陷入了局部最小。
- 步长不能太大（例 3.5(a)），课件写的"$\alpha$ 是步长"只是公式，实际要用线搜索或回溯减半来选。
- $\nabla g=2J^T\mathbf F$ 里有因子 2 和转置，别漏。
:::

## 真题精解 | Past Exam Problems

说明：本讲相关真题只有 2025–26 的两道（原卷）。

:::problem 真题 1 · 2025–26 第 7 题（10 分）· 牛顿法解方程组一次迭代
#### 题目
Given the system of nonlinear equations:
$$\begin{cases}5x_1^2-x_2^2=0\\ x_2-0.25(\sin x_1+\cos x_2)=0\end{cases}$$
Perform one iteration of Newton's method starting with the initial guess $\mathbf x^{(0)}=(0,0)^T$ to find $\mathbf x^{(1)}$.

#### 思路
对应 3.4。先写 $\mathbf F$ 和 $J$，再按步骤第 2 条检查 $\det J(\mathbf x^{(0)})$。

#### 解
$$\mathbf F(\mathbf x)=\begin{pmatrix}5x_1^2-x_2^2\\ x_2-0.25(\sin x_1+\cos x_2)\end{pmatrix},\qquad J(\mathbf x)=\begin{pmatrix}10x_1&-2x_2\\-0.25\cos x_1&1+0.25\sin x_2\end{pmatrix}.$$
代入 $\mathbf x^{(0)}=(0,0)^T$：
$$\mathbf F(\mathbf x^{(0)})=\begin{pmatrix}0\\0-0.25(0+1)\end{pmatrix}=\begin{pmatrix}0\\-0.25\end{pmatrix},\qquad J(\mathbf x^{(0)})=\begin{pmatrix}0&0\\-0.25&1\end{pmatrix}.$$
**$J(\mathbf x^{(0)})$ 的第一行全是 0，$\det J(\mathbf x^{(0)})=0$，矩阵奇异**，$J^{-1}$ 不存在。牛顿方程 $J\mathbf y=-\mathbf F$ 写开是
$$\begin{cases}0\cdot y_1+0\cdot y_2=0\\-0.25\,y_1+y_2=0.25\end{cases}$$
第一个方程恒成立，第二个方程只给出一个约束：
$$y_2=0.25+0.25\,y_1,\qquad y_1\text{ 任意}.$$
方程组有**无穷多个解** $\mathbf y=(t,\ 0.25+0.25t)^T$，所以 $\mathbf x^{(1)}=\mathbf x^{(0)}+\mathbf y$ **不能唯一确定**：标准牛顿法在 $\mathbf x^{(0)}=(0,0)^T$ 处无法执行。

**如果一定要给出一个数（取最小范数解）**：$\mathbf y$ 取满足约束、长度最短的点，即从原点到直线 $-0.25y_1+y_2=0.25$ 的垂足：
$$\mathbf y=\frac{0.25}{1.0625}(-0.25,\ 1)^T=\Big(-\frac1{17},\ \frac4{17}\Big)^T,\qquad\mathbf x^{(1)}=\Big(-\frac1{17},\ \frac4{17}\Big)^T\approx(-0.0588,\ 0.2353)^T.$$
这一点处 $J$ 可逆（$\det J=-0.74$），之后牛顿法正常进行并收敛：

| $k$ | $x_1^{(k)}$ | $x_2^{(k)}$ | $\lVert\mathbf y\rVert_\infty$ |
|---|---|---|---|
| 1 | −0.058824 | 0.235294 | （取最小范数解）|
| 2 | −0.108884 | 0.216988 | $5.0\times10^{-2}$ |
| 3 | −0.098640 | 0.219387 | $1.0\times10^{-2}$ |
| 4 | −0.098164 | 0.219500 | $4.8\times10^{-4}$ |
| 5 | −0.098163 | 0.219500 | $1.0\times10^{-6}$ |

收敛到方程组的一个解 $(-0.098163,\ 0.219500)^T$。方程组共有两个实数解，另一个是 $(0.121242,\ 0.271105)^T$。

#### 核对
程序算得 $\det J(\mathbf x^{(0)})=0$，矩阵秩为 1；$J\mathbf y=-\mathbf F$ 的通解如上，最小范数解 $(-1/17,\,4/17)$ 与伪逆（`lstsq`）结果一致。**这一点说明 $\mathbf x^{(0)}=(0,0)^T$ 是个"坏初值"**：从 $(10^{-3},0)^T$ 出发第一步是 $\mathbf y=(-0.0005,\ 0.2501)^T$，从 $(0,10^{-3})^T$ 出发却是 $(-0.998,\ -0.0005)^T$，初值的微小变化导致完全不同的步子。

#### 变形与说明
- **答题写法**：把 $\mathbf F$、$J$、代入值、$\det J=0$、牛顿方程的无穷多解都写出来，明确指出标准牛顿法此处无法确定 $\mathbf x^{(1)}$，再给出最小范数解作为补充。**出题人的标准答案我没有，不确定评分时要的是"指出奇异"还是别的写法，建议和老师给的答案核对。**
- **如果初值换成 $(0.1,\,0.1)^T$**（$J$ 可逆，可以演示完整一步）：
  $$\mathbf F=\begin{pmatrix}5(0.01)-0.01\\0.1-0.25(\sin0.1+\cos0.1)\end{pmatrix}=\begin{pmatrix}0.04\\-0.173709\end{pmatrix},\qquad J=\begin{pmatrix}1&-0.2\\-0.248751&1.024958\end{pmatrix},$$
  $\det J=1.024958-0.049750=0.975208$。解 $J\mathbf y=-\mathbf F=(-0.04,\ 0.173709)^T$（Cramer 法则）：
  $$y_1=\frac{-0.04(1.024958)-(-0.2)(0.173709)}{0.975208}=-0.006416,\qquad y_2=\frac{1\cdot0.173709-(-0.248751)(-0.04)}{0.975208}=0.167923,$$
  $\mathbf x^{(1)}=(0.093584,\ 0.267922)^T$。继续迭代：$(0.125954,\,0.272216)\to(0.121339,\,0.271128)\to(0.121242,\,0.271105)$，收敛到另一个解 $(0.121242,\ 0.271105)^T$。
- 3.5 的梯度下降在 $(0,0)^T$ 处仍可执行（例 3.5(a)），可以用它先走一步再换牛顿法。
:::

:::problem 真题 2 · 2025–26 第 4 题（10 分）· 向量序列的收敛与极限
#### 题目
Let the iterative sequence be defined by $\mathbf x^{(k)}=\big(e^{-k}\cos(k),\ k\sin(1/k),\ 3+k^{-2}\big)^T$. Prove this sequence is convergent and determine the limit as $k\to\infty$.

#### 思路
对应 3.2。逐分量求极限，每个分量写出依据，再引用逐分量判别定理。

#### 解
**第一分量**：$\lvert e^{-k}\cos k\rvert\le e^{-k}$，而 $e^{-k}\to0$，由夹逼，$e^{-k}\cos k\to0$。

**第二分量**：令 $t=1/k\to0^+$，
$$k\sin\frac1k=\frac{\sin t}t\to1\quad(t\to0^+)\quad\text{（重要极限）}.$$
（或直接估计：当 $t>0$ 时 $t-\tfrac{t^3}6\le\sin t\le t$，所以 $1-\dfrac1{6k^2}\le k\sin\dfrac1k\le1$，夹逼得极限 $1$。）

**第三分量**：$3+k^{-2}\to3+0=3$。

**结论**：每个分量都收敛，由逐分量判别定理，$\{\mathbf x^{(k)}\}$ 在 $L_\infty$ 范数下收敛，因而在任何范数下收敛，
$$\lim_{k\to\infty}\mathbf x^{(k)}=(0,\ 1,\ 3)^T.$$

#### 核对
| $k$ | $x_1^{(k)}$ | $x_2^{(k)}$ | $x_3^{(k)}$ | $\lVert\mathbf x^{(k)}-(0,1,3)^T\rVert_\infty$ |
|---|---|---|---|---|
| 1 | 0.198766 | 0.841471 | 4.000000 | 1.000 |
| 2 | −0.056319 | 0.958851 | 3.250000 | 0.250 |
| 5 | 0.001911 | 0.993347 | 3.040000 | 0.040 |
| 10 | −0.000038 | 0.998334 | 3.010000 | 0.010 |
| 100 | ≈0 | 0.999983 | 3.000100 | 0.0001 |

距离随 $k$ 减小，趋势符合 $(0,1,3)^T$。

#### 变形
- **直接证 $\varepsilon$–$N$（更严格）**：$\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty=\max\Big\{e^{-k}\lvert\cos k\rvert,\ \Big\lvert k\sin\dfrac1k-1\Big\rvert,\ \dfrac1{k^2}\Big\}\le\max\Big\{e^{-k},\ \dfrac1{6k^2},\ \dfrac1{k^2}\Big\}\le\dfrac1{k^2}$。最后一步用 $e^k\ge1+k+\dfrac{k^2}2+\dfrac{k^3}6\ge k^2$（$k\ge1$）。所以对任意 $\varepsilon>0$，取 $N>1/\sqrt\varepsilon$，$k\ge N$ 时 $\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty<\varepsilon$。表中最后一列恰好等于 $1/k^2$，说明这个界是紧的。
- 若题目问"收敛速度"：$\lVert\mathbf x^{(k)}-\mathbf x\rVert_\infty=O(1/k^2)$，对应 Lec 1 的多项式收敛速度，$p=2$。
- 若题目要求"在 $L_2$ 范数下也收敛"：由 $\lVert\cdot\rVert_2\le\sqrt3\lVert\cdot\rVert_\infty$ 直接得 $\lVert\mathbf x^{(k)}-\mathbf x\rVert_2\le\sqrt3/k^2\to0$。
:::
