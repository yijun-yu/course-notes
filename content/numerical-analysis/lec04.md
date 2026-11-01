:::exam 本讲在往年真题里
- **没有直接考"高斯消元 / LU 分解"的大题**（2022–23 到 2025–26 都没有）。但本讲是后面的基础：
  - **对角占优矩阵**（4.5）是 Lec 5 判断 Jacobi / Gauss–Seidel 是否收敛的条件。2023–24 第 4(a) 题要求"交换矩阵的行，把矩阵变成对角占优形式"，用的就是这里的判别法（见「真题精解」）。
  - **解线性方程组**是 Lec 5 迭代法、Lec 8 三次样条（求系数要解三对角方程组）、Lec 9 最小二乘（法方程）的子步骤，考场上手算 $2\times2$、$3\times3$ 时要用到消元。
  - **"用 4 位舍入运算解方程组"** 是常见题型，规则来自 Lec 1，选主元（4.2）是它的标准考点。
- 英文术语：Gaussian elimination、augmented matrix、backward substitution、pivot element、partial pivoting、scaled partial pivoting、LU factorization、permutation matrix、strictly diagonally dominant、positive definite、Cholesky factorization。
:::

图例：**★ 证明**＝考过或很可能考，建议考前自己推一遍；**☆ 证明**＝理解用，考试只用结论。📘＝课件没有、从教材（Burden & Faires）补充；⚠️＝课件笔误或 OCR 错误。

## 4.1 高斯消元与回代 | Gaussian Elimination and Backward Substitution

:::quick
- **什么时候用**：解 $A\mathbf x=\mathbf b$（$A$ 是 $n\times n$ 非奇异矩阵），手算规模通常是 $3\times3$、$4\times4$。
- **增广矩阵**（augmented matrix）：$\tilde A=[A\mid\mathbf b]$。
- **三种行运算**（不改变解）：
  1. $(\lambda E_i)\to E_i$：某行乘非零常数；
  2. $(E_i+\lambda E_j)\to E_i$：某行加上另一行的倍数；
  3. $(E_i)\leftrightarrow(E_j)$：交换两行。
- **消元（forward elimination）**：对 $i=1,\dots,n-1$，用第 $i$ 行消去第 $i$ 列下面的元素：
  $$m_{ji}=\frac{a_{ji}^{(i)}}{a_{ii}^{(i)}},\qquad(E_j-m_{ji}E_i)\to E_j,\qquad j=i+1,\dots,n.$$
- **回代（backward substitution）**：化成上三角后，
  $$x_n=\frac{a_{n,n+1}}{a_{nn}},\qquad x_i=\frac{a_{i,n+1}-\sum_{j=i+1}^na_{ij}x_j}{a_{ii}},\quad i=n-1,\dots,1.$$
- **失败情形**：某个主元 $a_{kk}^{(k)}=0$ 时，乘子 $m_{jk}$ 无法计算。若第 $k$ 列从第 $k$ 行往下找到非零元，就交换两行继续；若这一列往下全是 0，则方程组**没有唯一解**，程序停止。
- **运算量**：消元约 $\dfrac{n^3}3$ 次乘除，每次回代约 $\dfrac{n^2}2$ 次。
- 步骤：
  1. 写增广矩阵；
  2. 逐列消元，**每步把乘子 $m_{ji}$ 记下来**（4.4 的 LU 要用）；
  3. 得到上三角后，从最后一行回代。
:::

#### 算法（课件）

输入 $n$ 和增广矩阵。对 $i=1,\dots,n-1$：找最小的 $p\ge i$ 使 $a_{pi}\ne0$（找不到则输出"无唯一解"）；若 $p\ne i$ 交换 $E_p\leftrightarrow E_i$；对 $j=i+1,\dots,n$ 令 $m_{ji}=a_{ji}/a_{ii}$ 并做 $(E_j-m_{ji}E_i)\to E_j$。若 $a_{nn}=0$ 则无唯一解；否则回代。

:::proof ☆ 主元为 0 且下方全为 0 时没有唯一解
设消元到第 $k$ 步，当前矩阵 $A^{(k)}$ 前 $k-1$ 列已是上三角，且第 $k$ 列从第 $k$ 行起全为 0。则 $A^{(k)}$ 是分块上三角矩阵，其行列式等于前 $k-1$ 个对角元与右下角 $(n-k+1)$ 阶子块行列式的乘积，而这个子块的第一列全为 0，行列式为 0，所以 $\det A^{(k)}=0$。

行运算 2（加倍数）不改变行列式，行运算 1 只乘一个非零常数，行运算 3 只改变符号，所以 $\det A\ne0\iff\det A^{(k)}\ne0$。故 $\det A=0$，$A$ 奇异，方程组没有唯一解。
:::

:::example 例 4.1　课件 Example 1：四阶方程组
$$\begin{aligned}E_1:\ x_1+x_2+3x_4&=4\\E_2:\ 2x_1+x_2-x_3+x_4&=1\\E_3:\ 3x_1-x_2-x_3+2x_4&=-3\\E_4:\ -x_1+2x_2+3x_3-x_4&=4\end{aligned}$$

**增广矩阵**：
$$\left(\begin{array}{cccc|c}1&1&0&3&4\\2&1&-1&1&1\\3&-1&-1&2&-3\\-1&2&3&-1&4\end{array}\right)$$

**第 1 列消元**，乘子 $m_{21}=2$，$m_{31}=3$，$m_{41}=-1$：$(E_2-2E_1)\to E_2$，$(E_3-3E_1)\to E_3$，$(E_4+E_1)\to E_4$：
$$\left(\begin{array}{cccc|c}1&1&0&3&4\\0&-1&-1&-5&-7\\0&-4&-1&-7&-15\\0&3&3&2&8\end{array}\right)$$

**第 2 列消元**，乘子 $m_{32}=\dfrac{-4}{-1}=4$，$m_{42}=\dfrac{3}{-1}=-3$：$(E_3-4E_2)\to E_3$，$(E_4+3E_2)\to E_4$：
$$\left(\begin{array}{cccc|c}1&1&0&3&4\\0&-1&-1&-5&-7\\0&0&3&13&13\\0&0&0&-13&-13\end{array}\right)$$
（第 3 列的乘子 $m_{43}=0$，已是上三角。）

**回代**：
$$\begin{aligned}x_4&=\frac{-13}{-13}=1,\\x_3&=\frac{13-13\cdot1}{3}=0,\\x_2&=\frac{-7+x_3+5x_4}{-1}=\frac{-7+0+5}{-1}=2,\\x_1&=4-x_2-3x_4=4-2-3=-1.\end{aligned}$$
解为 $\mathbf x=(-1,\ 2,\ 0,\ 1)^T$。

**核对**：代回 $E_4$：$-(-1)+2\cdot2+3\cdot0-1=4$ ✓；$E_3$：$3(-1)-2-0+2=-3$ ✓。消元与回代也由程序用精确分数重算。
:::

:::pitfall
- 乘子 $m_{ji}=a_{ji}^{(i)}/a_{ii}^{(i)}$ 用的是**当前**（已被前面步骤修改过的）矩阵里的元素，不是原矩阵。
- 做 $(E_j-m_{ji}E_i)\to E_j$ 时，**整行（包括右端项）**都要一起算。
- 消元时若主元很小（但不为 0），也会出问题，见 4.2。
:::

## 4.2 主元策略 | Pivoting Strategies

:::quick
- **什么时候用**：主元为 0（必须换行），或主元相对其下方元素**很小**（误差被放大），尤其在**有限位（如 4 位）舍入运算**的题目里。
- **为什么要选主元**：主元 $a_{kk}^{(k)}$ 很小时，乘子 $m_{jk}=a_{jk}^{(k)}/a_{kk}^{(k)}$ 很大，之前引入的舍入误差被它放大；回代时又要除以这个小主元，分子上的误差再被放大一次。
- **部分选主元**（partial pivoting）：第 $k$ 步在第 $k$ 列、第 $k$ 行及以下，选绝对值最大的元素作主元，换到第 $k$ 行：
  $$\big\lvert a_{pk}^{(k)}\big\rvert=\max_{k\le i\le n}\big\lvert a_{ik}^{(k)}\big\rvert,\qquad(E_k)\leftrightarrow(E_p).$$
  这样所有乘子满足 $\lvert m_{jk}\rvert\le1$。
- **缩放部分选主元**（scaled partial pivoting，📘 教材）：先给每一行算一个比例因子 $s_i=\max_{1\le j\le n}\lvert a_{ij}\rvert$（在开始时算一次），第 $k$ 步选使
  $$\frac{\lvert a_{pk}^{(k)}\rvert}{s_p}=\max_{k\le i\le n}\frac{\lvert a_{ik}^{(k)}\rvert}{s_i}$$
  的行 $p$ 作主元行，再交换 $E_k\leftrightarrow E_p$。思想：先把每行"最大元素"看成 1 再比较。
- **完全选主元**（maximal / complete pivoting）：在整个剩余子矩阵里选绝对值最大的元素，行、列都可能交换（要记录列交换对应的变量顺序）；稳定但比较代价大。
- 步骤（有限位运算的题）：
  1. 每个输入先舍入到 $k$ 位；
  2. 每一步选主元，换行；
  3. 乘子、乘积、差都**逐步**舍入到 $k$ 位；
  4. 回代也逐步舍入；
  5. 与精确解比较。
:::

:::example 例 4.2　课件：小主元造成的误差（4 位舍入运算）
$$E_1:\ 0.003000\,x_1+59.14\,x_2=59.17,\qquad E_2:\ 5.291\,x_1-6.130\,x_2=46.78.$$
精确解 $x_1=10.00$，$x_2=1.000$。

**(a) 不选主元**。主元 $a_{11}=0.003000$ 很小：
$$m_{21}=\frac{5.291}{0.003000}=1763.67\to1764.$$
$(E_2-m_{21}E_1)\to E_2$：
$$\begin{aligned}a_{22}&=-6.130-1764\times59.14=-6.130-104322.96\ \to\ -6.130-104300\\&=-104306.13\ \to\ -1.043\times10^5,\end{aligned}$$
$$\begin{aligned}b_2&=46.78-1764\times59.17=46.78-104375.88\ \to\ 46.78-104400\\&=-104353.22\ \to\ -1.044\times10^5.\end{aligned}$$
回代：$x_2=\dfrac{-104400}{-104300}=1.00096\to1.001$（已经有一点误差），
$$x_1=\frac{59.17-59.14\times1.001}{0.003000}=\frac{59.17-59.20}{0.003000}=\frac{-0.03000}{0.003000}=-10.00.$$
**$x_1$ 的符号都错了**：$x_2$ 的误差 $0.001$ 被乘上 $\dfrac{59.14}{0.003000}\approx20000$。

**(b) 部分选主元**。第 1 列里 $5.291$ 比 $0.003000$ 大，交换 $E_1\leftrightarrow E_2$：
$$E_1:\ 5.291\,x_1-6.130\,x_2=46.78,\qquad E_2:\ 0.003000\,x_1+59.14\,x_2=59.17.$$
$m_{21}=\dfrac{0.003000}{5.291}=0.0005670$，
$$\begin{aligned}a_{22}&=59.14-0.0005670\times(-6.130)=59.14+0.003476\ \to\ 59.14,\\b_2&=59.17-0.0005670\times46.78=59.17-0.02652\ \to\ 59.14.\end{aligned}$$
$x_2=\dfrac{59.14}{59.14}=1.000$，$x_1=\dfrac{46.78+6.130\times1.000}{5.291}=\dfrac{52.91}{5.291}=10.00$。**两个解都对**。

**核对**：用 50 位精度的十进制数逐步模拟 4 位舍入，(a) 得 $x_2=1.001$、$x_1=-10.00$，(b) 得 $x_2=1.000$、$x_1=10.00$，与课件一致。
:::

:::example 例 4.3　部分选主元也会失败：缩放选主元
把例 4.2 的第一个方程两边乘以 $10^4$：
$$E_1:\ 30.00\,x_1+591400\,x_2=591700,\qquad E_2:\ 5.291\,x_1-6.130\,x_2=46.78.$$
解不变，但**部分选主元**现在看到第 1 列里 $30.00>5.291$，**不换行**，$m_{21}=0.1764$：
$$\begin{aligned}a_{22}&=-6.130-0.1764\times591400\ \to\ -1.043\times10^5,\\b_2&=46.78-0.1764\times591700\ \to\ -1.044\times10^5,\end{aligned}$$
重复了例 4.2(a) 的错误：$x_2=1.001$，
$$x_1=\frac{591700-591400\times1.001}{30.00}=\frac{591700-592000}{30.00}=-10.00.$$

**缩放部分选主元**：比例因子 $s_1=591400$，$s_2=6.130$。比较
$$\frac{\lvert a_{11}\rvert}{s_1}=\frac{30.00}{591400}=5.07\times10^{-5},\qquad\frac{\lvert a_{21}\rvert}{s_2}=\frac{5.291}{6.130}=0.863.$$
第 2 行的比值大，选它作主元行，交换 $E_1\leftrightarrow E_2$。$m_{21}=\dfrac{30.00}{5.291}=5.670$，
$$\begin{aligned}a_{22}&=591400-5.670\times(-6.130)=591400+34.76\ \to\ 5.914\times10^5,\\b_2&=591700-5.670\times46.78\ \to\ 5.914\times10^5,\end{aligned}$$
$x_2=\dfrac{591400}{591400}=1.000$，$x_1=\dfrac{46.78+6.130}{5.291}=10.00$ ✓。

**核对**：同样用程序逐步舍入模拟，与课件结论一致。
:::

:::pitfall
- 选主元只在**该列从当前行往下**找，不能把已处理完的行换回来。
- 有限位运算题里，**乘积和差每一步都要先舍入**再继续，不能算出精确值再一次性舍入。
- 部分选主元不总是够用（例 4.3）。比例因子 $s_i$ 是在**原矩阵**上整行取最大绝对值，开始时算一次。
- 课件对缩放选主元只讲了思想（"让每行最大元素相对大小为 1"），具体比值公式来自教材。
:::

## 4.3 求逆矩阵 | Computing the Matrix Inverse

:::quick
- **什么时候用**：题目要求 $A^{-1}$。**如果只是解 $A\mathbf x=\mathbf b$，不要求逆**，直接消元更省（求逆约需 $n^3$ 次乘除，是解一个方程组的 3 倍）。
- **方法**：对 $[A\mid I]$ 做行运算，把左半部分化成 $I$，右半部分就是 $A^{-1}$：
  $$[A\mid I]\ \xrightarrow{\text{行运算}}\ [I\mid A^{-1}].$$
- 步骤：
  1. 写 $[A\mid I]$；
  2. 先化成上三角（同 4.1，需要时选主元）；
  3. 每行除以主元，再自下而上消去主元上方的元素（Gauss–Jordan）；
  4. 读出右半部分，**用 $AA^{-1}=I$ 验算**。
- $A$ 奇异（$\det A=0$）时，左半部分化不成 $I$。
:::

:::proof ☆ 为什么 $[A\mid I]\to[I\mid A^{-1}]$
每一种行运算等价于左乘一个初等矩阵。设把 $A$ 化成 $I$ 的所有行运算的乘积是矩阵 $E$，则 $EA=I$，所以 $E=A^{-1}$。同样的行运算作用在右半部分的 $I$ 上，得到 $EI=E=A^{-1}$。
:::

:::example 例 4.4　课件：求 $3\times3$ 矩阵 $A$ 的逆
设 $A=\begin{pmatrix}1&2&-1\\2&1&0\\-1&1&2\end{pmatrix}$。

**$[A\mid I]$**：
$$\left(\begin{array}{ccc|ccc}1&2&-1&1&0&0\\2&1&0&0&1&0\\-1&1&2&0&0&1\end{array}\right)$$

**化上三角**：$(R_2-2R_1)$，$(R_3+R_1)$，再 $(R_3+R_2)$：
$$\left(\begin{array}{ccc|ccc}1&2&-1&1&0&0\\0&-3&2&-2&1&0\\0&0&3&-1&1&1\end{array}\right)$$

**向上消元**：$R_3\div3$，得第三行 $(0,0,1\mid-\tfrac13,\tfrac13,\tfrac13)$；$R_2-2R_3$ 后除以 $-3$，得第二行 $(0,1,0\mid\tfrac49,-\tfrac19,\tfrac29)$；$R_1-2R_2+R_3$，得第一行 $(1,0,0\mid-\tfrac29,\tfrac59,-\tfrac19)$。所以
$$A^{-1}=\frac19\begin{pmatrix}-2&5&-1\\4&-1&2\\-3&3&3\end{pmatrix}.$$

**验算**：$AA^{-1}$ 的第一行：$\dfrac19\big[1(-2)+2(4)-1(-3),\ 1(5)+2(-1)-1(3),\ 1(-1)+2(2)-1(3)\big]=\dfrac19[9,0,0]=(1,0,0)$ ✓。

**核对**：$\det A=-9$（所以分母是 9），程序用精确分数和 NumPy 都验证了 $A^{-1}$ 和 $AA^{-1}=I$。课件只给了题目，答案是我算的。
:::

:::pitfall
- 行运算要同时作用在**整行**（左右两半）。
- 没有化到 $[I\mid\cdot]$ 之前，右半部分不是逆；务必验算 $AA^{-1}=I$，第一行第一列就能发现大多数算错。
:::

## 4.4 LU 分解 | LU Factorization

:::quick
- **什么时候用**：同一个 $A$ 要解**多个**右端项 $\mathbf b$；或题目要求写出 $L,U$。
- **分解**：$A=LU$，$L$ 是**单位下三角**矩阵（对角线为 1），$U$ 是上三角矩阵。
- **怎么得到**：$U$ = 高斯消元得到的上三角矩阵；$L$ 的第 $j$ 行第 $i$ 列（$j>i$）就是消元时的乘子 $m_{ji}$：
  $$U=\begin{pmatrix}a_{11}^{(1)}&a_{12}^{(1)}&\cdots&a_{1n}^{(1)}\\&a_{22}^{(2)}&\cdots&\vdots\\&&\ddots&\vdots\\&&&a_{nn}^{(n)}\end{pmatrix},\qquad L=\begin{pmatrix}1&&&\\m_{21}&1&&\\\vdots&\ddots&\ddots&\\m_{n1}&\cdots&m_{n,n-1}&1\end{pmatrix}.$$
- **条件**：消元过程中**不需要换行**（所有主元 $a_{ii}^{(i)}\ne0$）。
- **解方程组** $A\mathbf x=\mathbf b$：
  1. 解 $L\mathbf y=\mathbf b$（**前代** forward substitution）；
  2. 解 $U\mathbf x=\mathbf y$（**回代**）。
  
  分解一次约 $\dfrac{n^3}3$ 次乘除，之后每个 $\mathbf b$ 只要 $O(n^2)$。
- **需要换行时**（📘）：$PA=LU$，$P$ 是置换矩阵（permutation matrix，由单位矩阵 $I$ 重排行得到）。此时解 $A\mathbf x=\mathbf b$ 改成：先算 $P\mathbf b$，解 $L\mathbf y=P\mathbf b$，再解 $U\mathbf x=\mathbf y$。
- 步骤：消元并记下乘子 → 拼 $L$、$U$ → 验证 $LU=A$ → 前代、回代。
:::

#### 置换矩阵

$n\times n$ 置换矩阵 $P$ 是把单位矩阵 $I_n$ 的行重排得到的。$PA$ 就是把 $A$ 的行按同样方式重排。例：
$$P=\begin{pmatrix}1&0&0\\0&0&1\\0&1&0\end{pmatrix},\qquad PA=\begin{pmatrix}a_{11}&a_{12}&a_{13}\\a_{31}&a_{32}&a_{33}\\a_{21}&a_{22}&a_{23}\end{pmatrix}.$$
$P$ 把第 2、3 行互换。置换矩阵可逆，$P^{-1}=P^T$。

:::proof ★ 乘子构成 $L$，$A=LU$
设消元不需要换行。第 $k$ 步用高斯变换矩阵 $M^{(k)}$ 表示：把第 $k$ 行的 $-m_{jk}$ 倍加到第 $j$ 行（$j>k$），
$$M^{(k)}=I-N_k,\qquad N_k=\sum_{j>k}m_{jk}\,\mathbf e_j\mathbf e_k^T,$$
其中 $\mathbf e_j$ 是第 $j$ 个单位向量。$n-1$ 步以后得到上三角矩阵
$$U=M^{(n-1)}\cdots M^{(2)}M^{(1)}A.$$

**第一步：$M^{(k)}$ 的逆。** 记 $\mathbf c_k=\sum_{j>k}m_{jk}\mathbf e_j$（前 $k$ 个分量为 0），则 $N_k=\mathbf c_k\mathbf e_k^T$，
$$N_k^2=\mathbf c_k(\mathbf e_k^T\mathbf c_k)\mathbf e_k^T=0\qquad(\text{因为 }\mathbf c_k\text{ 的第 }k\text{ 个分量是 }0).$$
所以 $(I-N_k)(I+N_k)=I-N_k^2=I$，即 $L^{(k)}:=(M^{(k)})^{-1}=I+N_k$（对应课件里 $\big[M^{(k)}\big]^{-1}$ 的样子：第 $k$ 列下方是 $+m_{jk}$）。

**第二步：乘积。** 对 $a<b$：
$$N_aN_b=\mathbf c_a(\mathbf e_a^T\mathbf c_b)\mathbf e_b^T=0,$$
因为 $\mathbf c_b$ 的前 $b$ 个分量是 0，而 $a<b$，所以 $\mathbf e_a^T\mathbf c_b=0$。因此
$$L^{(1)}L^{(2)}\cdots L^{(n-1)}=(I+N_1)(I+N_2)\cdots(I+N_{n-1})=I+N_1+N_2+\cdots+N_{n-1}=:L,$$
（展开后所有含 $N_aN_b$（$a<b$）的交叉项都是 0。）$L$ 恰好是单位下三角矩阵，第 $k$ 列下方放着 $m_{jk}$。

**第三步：**
$$A=\big(M^{(1)}\big)^{-1}\big(M^{(2)}\big)^{-1}\cdots\big(M^{(n-1)}\big)^{-1}U=L^{(1)}L^{(2)}\cdots L^{(n-1)}U=LU.$$

**考场用法**：这就是"为什么 $L$ 里直接填乘子（符号为正）"的理由。做题时不需要重新乘矩阵，直接填。
:::

:::proof ☆ $LU$ 分解（$L$ 单位下三角时）是唯一的
设 $A=L_1U_1=L_2U_2$，$L_i$ 单位下三角，$U_i$ 上三角且可逆（$A$ 非奇异）。左乘 $L_2^{-1}$、右乘 $U_1^{-1}$：
$$L_2^{-1}L_1=U_2U_1^{-1}.$$
左边是单位下三角，右边是上三角，两边只能是对角矩阵，而左边对角线全为 1，所以两边都等于 $I$，即 $L_1=L_2$，$U_1=U_2$。

这说明手算时不管用什么消元顺序，只要不换行，得到的 $L,U$ 都一样，可以用 $LU=A$ 直接验证。
:::

:::example 例 4.5　课件 Example 2：4×4 矩阵的 LU 分解并解方程组
$$A=\begin{pmatrix}1&1&0&3\\2&1&-1&1\\3&-1&-1&2\\-1&2&3&-1\end{pmatrix}$$

**(a) 分解**。就是例 4.1 的消元，乘子 $m_{21}=2,\ m_{31}=3,\ m_{41}=-1,\ m_{32}=4,\ m_{42}=-3,\ m_{43}=0$，得
$$A=\underbrace{\begin{pmatrix}1&0&0&0\\2&1&0&0\\3&4&1&0\\-1&-3&0&1\end{pmatrix}}_{L}\underbrace{\begin{pmatrix}1&1&0&3\\0&-1&-1&-5\\0&0&3&13\\0&0&0&-13\end{pmatrix}}_{U}.$$
验证 $LU$ 的第 4 行：$(-1)\cdot[1,1,0,3]+(-3)\cdot[0,-1,-1,-5]+0+1\cdot[0,0,0,-13]=[-1,\,-1+3,\,3,\,-3+15-13]=[-1,2,3,-1]$ ✓。

**(b) 解 $A\mathbf x=\mathbf b$，$\mathbf b=(8,7,14,-7)^T$**（即课件的方程组 $x_1+x_2+3x_4=8$，$2x_1+x_2-x_3+x_4=7$，$3x_1-x_2-x_3+2x_4=14$，$-x_1+2x_2+3x_3-x_4=-7$）：

**前代** $L\mathbf y=\mathbf b$：
$$\begin{aligned}y_1&=8,\\y_2&=7-2y_1=-9,\\y_3&=14-3y_1-4y_2=14-24+36=26,\\y_4&=-7+y_1+3y_2=-7+8-27=-26.\end{aligned}$$
**回代** $U\mathbf x=\mathbf y$：
$$\begin{aligned}x_4&=\frac{-26}{-13}=2,\\x_3&=\frac{26-13\cdot2}3=0,\\x_2&=\frac{-9+x_3+5x_4}{-1}=\frac{-9+0+10}{-1}=-1,\\x_1&=8-x_2-3x_4=8+1-6=3.\end{aligned}$$
解为 $\mathbf x=(3,\,-1,\,0,\,2)^T$。

⚠️ 课件 (a) 部分写的右端项是 $\mathbf b=(1,1,-3,4)^T$，与 (b) 实际用的 $(8,7,14,-7)^T$ 不一致。例 4.1 的右端项是 $(4,1,-3,4)^T$，$(1,1,-3,4)$ 应是它的 OCR 错误。

**核对**：程序验证 $LU=A$，且 $A\mathbf x=\mathbf b$ 的残差为 0。同一个 $L,U$ 也可以用来解例 4.1 的 $\mathbf b=(4,1,-3,4)^T$：前代得 $\mathbf y=(4,-7,13,-13)^T$，回代得 $(-1,2,0,1)^T$ ✓。
:::

:::example 例 4.6　📘 需要换行的情形：$PA=LU$
$$A=\begin{pmatrix}0&2&1\\1&1&1\\2&1&0\end{pmatrix}.$$
$a_{11}=0$，必须换行。**部分选主元**：

1. 第 1 列最大是第 3 行的 $2$，交换 $R_1\leftrightarrow R_3$，行顺序变成 $(3,2,1)$：$\begin{pmatrix}2&1&0\\1&1&1\\0&2&1\end{pmatrix}$。乘子 $m_{21}=\tfrac12$，$m_{31}=0$：第 2 行变成 $(0,\tfrac12,1)$。
2. 第 2 列（第 2 行起）比较 $\lvert\tfrac12\rvert$ 与 $\lvert2\rvert$，选 $2$，交换第 2、3 行，行顺序变成 $(3,1,2)$：$\begin{pmatrix}2&1&0\\0&2&1\\0&\tfrac12&1\end{pmatrix}$，乘子 $\tfrac{1/2}{2}=\tfrac14$，第 3 行变成 $(0,0,\tfrac34)$。

交换行的同时，已算出的乘子也跟着换位置（$m_{21}=\frac12$ 现在属于第 3 行）。结果：
$$P=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix},\quad L=\begin{pmatrix}1&0&0\\0&1&0\\\tfrac12&\tfrac14&1\end{pmatrix},\quad U=\begin{pmatrix}2&1&0\\0&2&1\\0&0&\tfrac34\end{pmatrix}.$$
（$P$ 的第 $i$ 行是 $I$ 的第"最终排在第 $i$ 位的原行号"行：最终顺序是原第 3、1、2 行。）

**解 $A\mathbf x=\mathbf b$，$\mathbf b=(7,6,4)^T$**：$P\mathbf b=(4,7,6)^T$。
前代 $L\mathbf y=P\mathbf b$：$y_1=4$，$y_2=7$，$y_3=6-\tfrac12\cdot4-\tfrac14\cdot7=2.25$。
回代 $U\mathbf x=\mathbf y$：$x_3=\dfrac{2.25}{0.75}=3$，$x_2=\dfrac{7-3}{2}=2$，$x_1=\dfrac{4-2}{2}=1$。解为 $(1,2,3)^T$。

**核对**：程序验证 $PA=LU$，且 $A(1,2,3)^T=(7,6,4)^T$ ✓。
:::

:::pitfall
- $L$ 的对角线是 1，乘子放在对角线**下方**，符号为正（消元时减掉 $m_{ji}E_i$，所以 $L$ 里是 $+m_{ji}$）。
- $L$、$U$ 要先验证 $LU=A$ 再用。
- 换行时，$L$ 里已有的乘子也要**一起换行**（只换 $L$ 的前 $k-1$ 列的那几行），否则 $PA\ne LU$。
- $A=LU$ 这种单位下三角的形式叫 Doolittle 分解；也有 $U$ 单位对角的 Crout 分解（📘），考试以课件的 Doolittle 为准。
:::

## 4.5 对角占优与正定矩阵 | Diagonally Dominant and Positive Definite Matrices

:::quick
- **什么时候用**：判断消元是否**不用换行**、是否稳定；Lec 5 判断 Jacobi / Gauss–Seidel 是否收敛；用 Cholesky 解对称正定方程组。
- **对角占优**（diagonally dominant）：每一行
  $$\lvert a_{ii}\rvert\ge\sum_{j\ne i}\lvert a_{ij}\rvert.$$
  **严格对角占优**（strictly diagonally dominant）：每一行都是 $>$。
- **定理**：严格对角占优矩阵**非奇异**，并且对 $A\mathbf x=\mathbf b$ 做高斯消元不需要换行，数值上对舍入误差稳定。
- **正定**（positive definite）：$A$ **对称**且对所有 $\mathbf x\ne\mathbf 0$ 有 $\mathbf x^TA\mathbf x>0$。
- **正定矩阵的必要条件**（快速排除用）：
  1. $A$ 可逆；
  2. $a_{ii}>0$（对角元为正）；
  3. $\max_{k,j}\lvert a_{kj}\rvert\le\max_i a_{ii}$；
  4. $(a_{ij})^2<a_{ii}a_{jj}$（$i\ne j$）。
- **判别**：对称矩阵 $A$ 正定 $\iff$ 高斯消元**不换行**时所有主元都 $>0$。
- **分解**：$A$ 正定 $\iff$ $A=LDL^T$（$L$ 单位下三角，$D$ 是对角元为正的对角矩阵）$\iff$ $A=\tilde L\tilde L^T$（Cholesky 分解，$\tilde L$ 下三角，对角元可取正）。其中 $D=\operatorname{diag}(\text{主元})$，$\tilde L=L\,D^{1/2}$。
- 步骤（判断 $A$ 是否正定）：先看是否对称，再看对角元是否 $>0$、$a_{ij}^2<a_{ii}a_{jj}$（任何一条不满足就不是），最后做消元看主元是否都 $>0$。
:::

:::proof ★ 严格对角占优矩阵非奇异
设 $A$ 严格对角占优。反证：假设 $A\mathbf x=\mathbf 0$ 有非零解 $\mathbf x$。取下标 $i$ 使 $\lvert x_i\rvert=\max_j\lvert x_j\rvert>0$。第 $i$ 个方程是 $\sum_ja_{ij}x_j=0$，即 $a_{ii}x_i=-\sum_{j\ne i}a_{ij}x_j$，所以
$$\lvert a_{ii}\rvert\lvert x_i\rvert\le\sum_{j\ne i}\lvert a_{ij}\rvert\lvert x_j\rvert\le\Big(\sum_{j\ne i}\lvert a_{ij}\rvert\Big)\lvert x_i\rvert<\lvert a_{ii}\rvert\lvert x_i\rvert,$$
最后一个 $<$ 用的是严格对角占优和 $\lvert x_i\rvert>0$。得到 $\lvert a_{ii}\rvert\lvert x_i\rvert<\lvert a_{ii}\rvert\lvert x_i\rvert$，矛盾。所以 $A\mathbf x=\mathbf 0$ 只有零解，$A$ 非奇异。
:::

:::proof ☆ 📘 严格对角占优 ⟹ 消元不需要换行
只需证明：对 $A$ 做一步消元，右下角 $(n-1)\times(n-1)$ 子矩阵仍严格对角占优（且主元 $a_{11}\ne0$，因为严格对角占优时 $\lvert a_{11}\rvert>\sum_{j\ge2}\lvert a_{1j}\rvert\ge0$）。

消元后右下角元素为 $b_{ij}=a_{ij}-\dfrac{a_{i1}a_{1j}}{a_{11}}$（$i,j\ge2$）。对第 $i$ 行，利用第 1 行、第 $i$ 行的严格对角占优：
$$\sum_{j\ge2,\,j\ne i}\lvert b_{ij}\rvert\le\sum_{j\ge2,\,j\ne i}\lvert a_{ij}\rvert+\frac{\lvert a_{i1}\rvert}{\lvert a_{11}\rvert}\sum_{j\ge2,\,j\ne i}\lvert a_{1j}\rvert<\big(\lvert a_{ii}\rvert-\lvert a_{i1}\rvert\big)+\frac{\lvert a_{i1}\rvert}{\lvert a_{11}\rvert}\big(\lvert a_{11}\rvert-\lvert a_{1i}\rvert\big)=\lvert a_{ii}\rvert-\frac{\lvert a_{i1}\rvert\lvert a_{1i}\rvert}{\lvert a_{11}\rvert}\le\lvert b_{ii}\rvert.$$
最后一步用 $\lvert b_{ii}\rvert=\Big\lvert a_{ii}-\dfrac{a_{i1}a_{1i}}{a_{11}}\Big\rvert\ge\lvert a_{ii}\rvert-\dfrac{\lvert a_{i1}\rvert\lvert a_{1i}\rvert}{\lvert a_{11}\rvert}$。所以子矩阵仍严格对角占优，下一步的主元也不为 0，归纳可知所有主元都非零，不需要换行。
:::

:::proof ☆ 正定矩阵的性质 (1)–(4)
设 $A$ 正定。
1. **可逆**：若 $A\mathbf x=\mathbf 0$，则 $\mathbf x^TA\mathbf x=0$，由正定得 $\mathbf x=\mathbf 0$，所以只有零解。
2. **$a_{ii}>0$**：取 $\mathbf x=\mathbf e_i$，$\mathbf x^TA\mathbf x=a_{ii}>0$。
4. **$a_{ij}^2<a_{ii}a_{jj}$**（先证第 4 条）：取 $\mathbf x=t\mathbf e_i+\mathbf e_j$（$i\ne j$，$t$ 任意实数），
   $$\mathbf x^TA\mathbf x=a_{ii}t^2+2a_{ij}t+a_{jj}>0\quad(\forall t),$$
   这个关于 $t$ 的二次函数恒正，判别式小于 0：$4a_{ij}^2-4a_{ii}a_{jj}<0$。
3. **最大元在对角线上**：由第 4 条，$\lvert a_{kj}\rvert<\sqrt{a_{kk}a_{jj}}\le\max_ia_{ii}$（$k\ne j$）；对角元本身显然 $\le\max_ia_{ii}$。
:::

:::proof ☆ 📘 $A=LDL^T$ 与 Cholesky 分解
设 $A$ 对称正定。由"消元不换行时主元全为正"，$A=LU$（$L$ 单位下三角）。由 $A=A^T$：
$$LU=U^TL^T\ \Rightarrow\ U(L^T)^{-1}=L^{-1}U^T.$$
左边是上三角矩阵（上三角乘上三角），右边是下三角矩阵，所以两边相等的矩阵必是对角矩阵 $D$。于是 $U=DL^T$，
$$A=LDL^T,$$
并且 $D$ 的对角元就是 $U$ 的对角元，即各步主元，全为正。令 $D^{1/2}=\operatorname{diag}(\sqrt{d_i})$，$\tilde L=LD^{1/2}$，则 $\tilde L\tilde L^T=LD^{1/2}D^{1/2}L^T=LDL^T=A$。

反过来，若 $A=\tilde L\tilde L^T$ 且 $\tilde L$ 可逆，则 $A$ 对称，且 $\mathbf x^TA\mathbf x=\lVert\tilde L^T\mathbf x\rVert_2^2>0$（$\mathbf x\ne\mathbf 0$），所以 $A$ 正定。
:::

:::example 例 4.7　对角占优的判断与换行
**(a)** $A=\begin{pmatrix}7&2&0\\3&5&-1\\0&5&-6\end{pmatrix}$：每行比较 $\lvert a_{ii}\rvert$ 与其余元素绝对值之和：$7>2$，$5>3+1=4$，$6>0+5=5$，**严格对角占优**，所以非奇异，高斯消元不需要换行。

**(b)** $B=\begin{pmatrix}6&4&-3\\4&-2&0\\-3&0&1\end{pmatrix}$：第 1 行 $6<4+3=7$，**不是**对角占优（第 2 行 $2<4$、第 3 行 $1<3$ 也不满足）。

**(c)** 对角占优与换行：方程组
$$x_1+x_2+3x_3=5,\qquad x_1+3x_2+x_3=2,\qquad3x_1+x_2+x_3=-4.$$
系数矩阵 $A=\begin{pmatrix}1&1&3\\1&3&1\\3&1&1\end{pmatrix}$：第 1 行 $1<4$，第 3 行 $1<4$，只有第 2 行 $3>2$，不是对角占优。**交换第 1、3 行**：
$$A'=\begin{pmatrix}3&1&1\\1&3&1\\1&1&3\end{pmatrix},\quad\mathbf b'=(-4,\ 2,\ 5)^T.$$
每行 $3>1+1=2$，**严格对角占优**。解（程序精确求得）为 $\mathbf x=(-2.3,\ 0.7,\ 2.2)^T$。

**核对**：(a)(b)(c) 的行和比较由程序算出；(c) 代回：$3(-2.3)+0.7+2.2=-4$ ✓，$-2.3+3(0.7)+2.2=2$ ✓，$-2.3+0.7+3(2.2)=5$ ✓。
:::

:::example 例 4.8　📘 正定性判断、$LDL^T$ 与 Cholesky 分解
$$A=\begin{pmatrix}4&-1&1\\-1&4.25&2.75\\1&2.75&3.5\end{pmatrix}.$$
**判断**：$A$ 对称；$a_{ii}>0$；做高斯消元（不换行），乘子 $m_{21}=-0.25$，$m_{31}=0.25$，第 2 步乘子 $m_{32}=\dfrac{2.75+0.25}{4.25-0.25}=\dfrac{3}{4}$，主元依次为 $4,\ 4,\ 1$，**全为正**，所以 $A$ 正定。

**$LDL^T$**：
$$L=\begin{pmatrix}1&0&0\\-0.25&1&0\\0.25&0.75&1\end{pmatrix},\qquad D=\operatorname{diag}(4,\ 4,\ 1).$$
**Cholesky**：$\tilde L=LD^{1/2}=L\operatorname{diag}(2,2,1)$，
$$\tilde L=\begin{pmatrix}2&0&0\\-0.5&2&0\\0.5&1.5&1\end{pmatrix},\qquad\tilde L\tilde L^T=A.$$
验证 $(\tilde L\tilde L^T)_{32}=0.5\cdot(-0.5)+1.5\cdot2+0=-0.25+3=2.75$ ✓。

**解 $A\mathbf x=\mathbf b$，$\mathbf b=(5,\ 15.75,\ 17)^T$**：

先解 $\tilde L\mathbf y=\mathbf b$（前代）：
$$\begin{aligned}y_1&=\frac52=2.5,\\y_2&=\frac{15.75+0.5\cdot2.5}{2}=8.5,\\y_3&=17-0.5\cdot2.5-1.5\cdot8.5=3.\end{aligned}$$
再解 $\tilde L^T\mathbf x=\mathbf y$（回代）：
$$\begin{aligned}x_3&=3,\\x_2&=\frac{8.5-1.5\cdot3}{2}=2,\\x_1&=\frac{2.5+0.5\cdot2-0.5\cdot3}{2}=1.\end{aligned}$$
解为 $(1,2,3)^T$。

**反例**：$B=\begin{pmatrix}2&3\\3&1\end{pmatrix}$：$a_{12}^2=9>a_{11}a_{22}=2$，违反性质 4，**不是**正定；消元的第 2 个主元是 $1-\dfrac92=-3.5<0$，同样说明。

**另一个例子**：$C=\begin{pmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{pmatrix}$ 的主元是 $2,\ \tfrac32,\ \tfrac43$，全为正，所以正定；但它**不是严格对角占优**（第 2 行 $2=1+1$），说明正定与对角占优是两个不同的条件。

**核对**：$LDL^T$、$\tilde L$ 与 NumPy 的 `cholesky` 一致，$A$ 的特征值 $0.526,\ 4.569,\ 6.654$ 全为正；解 $(1,2,3)^T$ 代回成立。课件只给了定理，例题是 📘 教材例子，数值我重算过。
:::

:::pitfall
- 对角占优看的是**每一行**：$\lvert a_{ii}\rvert$ 与"**同一行**其余元素的绝对值之和"比，不是和列比。
- 正定的前提是**对称**；不对称的矩阵没有"正定"这个说法（课件的定义里包含对称）。
- 严格对角占优是消元不换行的**充分**条件，不是必要条件。
- 主元全正是"对称矩阵正定"的判据，**不对称矩阵**不能用。
- 用 Cholesky 之前要先确认正定（主元全为正），否则会出现负数开方。
:::

## 真题精解 | Past Exam Problems

说明：本讲没有直接对应的真题；只有 2023–24 第 4 题里一步要用到本讲的"对角占优"判别。这道题的其余三问属于 Lec 5，完整解答放在 Lec 5 的真题精解里，这里只做第 (a) 问的"换行"部分。该题是回忆版，原作者提醒"数据可能有误"，下面按所记数据作答。

:::problem 真题 1 · 2023–24 第 4(a) 题 · 换行使矩阵严格对角占优
#### 题目（回忆版，只列用到本讲的部分）
$$x_1+x_2+3x_3=5,\qquad x_1+3x_2+x_3=2,\qquad3x_1+x_2+x_3=-4.$$
(a) 交换矩阵的行，把矩阵变成使雅可比（Jacobi）方法一定收敛的形式（即对角占优矩阵），并用雅可比方法迭代两次。

#### 思路
对应 4.5。Jacobi 方法收敛的一个充分条件是系数矩阵**严格对角占优**（Lec 5）。所以先逐行检查，再通过换行把每行最大的元素放到对角线上。

#### 解
系数矩阵和右端项：
$$A=\begin{pmatrix}1&1&3\\1&3&1\\3&1&1\end{pmatrix},\qquad\mathbf b=(5,\ 2,\ -4)^T.$$
逐行比较：第 1 行 $\lvert1\rvert<1+3$，第 2 行 $\lvert3\rvert>1+1$，第 3 行 $\lvert1\rvert<3+1$。**第 1、3 行不满足**。

每一行的最大元素：第 1 行是 $a_{13}=3$（要放到第 3 列位置），第 3 行是 $a_{31}=3$（要放到第 1 列位置）。所以把**第 1 行与第 3 行互换**：
$$\begin{cases}3x_1+x_2+x_3=-4\\x_1+3x_2+x_3=2\\x_1+x_2+3x_3=5\end{cases}\qquad A'=\begin{pmatrix}3&1&1\\1&3&1\\1&1&3\end{pmatrix}.$$
每行 $3>1+1=2$，**严格对角占优**，Jacobi 方法对任意初值收敛（Lec 5 的定理）。

**Jacobi 迭代**（初值题目没给，取 $\mathbf x^{(0)}=\mathbf 0$）：
$$x_1^{(k)}=\frac{-4-x_2^{(k-1)}-x_3^{(k-1)}}3,\quad x_2^{(k)}=\frac{2-x_1^{(k-1)}-x_3^{(k-1)}}3,\quad x_3^{(k)}=\frac{5-x_1^{(k-1)}-x_2^{(k-1)}}3.$$
第 1 次：$\mathbf x^{(1)}=\big(-\tfrac43,\ \tfrac23,\ \tfrac53\big)^T\approx(-1.3333,\ 0.6667,\ 1.6667)^T$。
第 2 次：
$$x_1^{(2)}=\frac{-4-0.6667-1.6667}3=-2.1111,\quad x_2^{(2)}=\frac{2+1.3333-1.6667}3=0.5556,\quad x_3^{(2)}=\frac{5+1.3333-0.6667}3=1.8889.$$
$\mathbf x^{(2)}\approx(-2.1111,\ 0.5556,\ 1.8889)^T$。精确解是 $(-2.3,\ 0.7,\ 2.2)^T$，两步之后已经在接近。

#### 核对
程序精确求解 $A'\mathbf x=\mathbf b'$ 得 $(-2.3,\ 0.7,\ 2.2)$；Jacobi 两步由程序重算与上面一致。

#### 变形
- 这个例子里只有这一种排列能让每行的最大元素落在对角线上（第 3 行放到第 1 位，第 1 行放到第 3 位，第 2 行不动），所以换法是确定的。
- 第 (b)(c)(d) 问（Gauss–Seidel 迭代、证明 $\rho(M)\le\lVert M\rVert$、求 $T_j$ 的 $\infty$ 范数并估计 20 次迭代的误差上界）见 Lec 5。
:::
