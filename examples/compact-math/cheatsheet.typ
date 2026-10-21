// Educational adaptation: CC BY-NC-SA 4.0. Sources and changes: README.md.
// Build: typst compile cheatsheet.typ cheatsheet.pdf
#set document(title: "Linear Algebra | 单页紧凑速查", author: "fuxi-pdf")
#set page(paper: "us-letter", flipped: true, margin: 3.5mm)
#set text(font: ("Microsoft YaHei", "Noto Sans CJK SC", "DejaVu Sans"), size: 8.7pt, lang: "zh")
#set par(leading: 2pt, spacing: 2.5pt, justify: false)
#set block(spacing: 3pt)
#let blue = rgb("1648a8")
#let red = rgb("b12626")
#show math.equation: set text(font: ("Cambria Math", "STIX Two Math", "New Computer Modern Math"), fill: blue)
#set math.equation(numbering: none)
#let en(body) = block(above: 2pt, below: 1pt)[#text(fill: blue, size: 8.6pt)[*EN* #body]]
#let warn(body) = block(above: 1pt, below: 1pt)[#text(fill: red, size: 8.2pt)[*注意* #body]]
#let eq(body) = block(above: 2.5pt, below: 2.5pt, body)
#let sec(id, title, source, body) = block(breakable: false, above: 3pt, below: 2pt)[
  #line(length: 100%, stroke: 0.45pt)
  #text(weight: "bold", size: 9.3pt)[#id  #title] #text(size: 6.3pt, fill: rgb("555555"))[#source]
  #parbreak()
  #body
]

#text(weight: "bold", size: 11pt)[线性代数 · 紧凑单页速查] #h(1fr) #text(fill: blue, size: 6.7pt)[MIT OCW · Gilbert Strang · 2011 · 改编 fuxi-pdf · #link("https://creativecommons.org/licenses/by-nc-sa/4.0/")[CC BY-NC-SA 4.0]]
#parbreak()
#text(size: 7pt)[范围：MIT 18.06SC (2011)，几何、消元、子空间、正交与最小二乘、行列式。约半学期主题；不含特征值及后续内容。]
#parbreak()
#text(size: 6.7pt)[符号：实矩阵 $A in RR^(m times n)$，$r = "rank"(A)$，$R = "rref"(A)$；$C$=列空间，$N$=零空间；$T$=转置。黑=中文/条件，蓝=公式/英文，红=易错。]
#v(1pt)

#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 9pt,
grid.vline(x: 1, stroke: 0.25pt + rgb("bbbbbb")),
grid.vline(x: 2, stroke: 0.25pt + rgb("bbbbbb")),
grid.vline(x: 3, stroke: 0.25pt + rgb("bbbbbb")),
[
#sec("01", "方程的三种视角", "[S01 p1–3; S02 p1–4]", [
行：方程超平面的交点。列：用各列线性组合拼出 $b$。矩阵：同一个问题的紧凑记法。
#eq($A x = sum_(j=1)^n x_j a_j = b$)
#en[Solving $A x=b$ means expressing $b$ as a linear combination of the columns of $A$.]
#warn[列向量在 $RR^m$；系数 $x$ 在 $RR^n$。]
])
#sec("02", "矩阵乘法 / 转置", "[S04 p1–3; S05 p1]", [
$A_(m times n) B_(n times k)$ 才可乘；结果 $m times k$。右乘逐列组合，左乘逐行组合。
#eq($(A B)_(i j)=sum_(ell=1)^n a_(i ell)b_(ell j)$)
外积视角：$A B=sum_(ell=1)^n A_(:,ell) B_(ell,:)$，每项是“列×行”的矩阵。
#eq($(A B)^T=B^T A^T, quad (A B)^(-1)=B^(-1) A^(-1)$)
逆乘积式要求两者均为可逆方阵。
#en[Order reverses under transpose or inversion.]
#warn[通常 $A B != B A$；$A^T A$ 总对称。]
])
#sec("03", "消元 / 置换 / LU", "[S03 p1–3; S05 p1–3; S06 p1]", [
$R_i <- R_i - ell_(i j) R_j$，同时更新右端 $b$。主元为零先找可交换行；矩形阵可跳过无主元列。
#eq($P A=L U, quad L c=P b, quad U x=c$)
$L$ 单位下三角，$U$ 上三角；无换行时 $P=I$。$L$ 记录消元倍数。置换阵 $P^(-1)=P^T$。
方阵分解成本 $O(n^3)$；每个新 $b$ 的两次三角求解为 $O(n^2)$。[S05 p2]
原例的分解，可直接相乘自检：
#eq($mat(2,1;8,7)=mat(1,0;4,1) mat(2,1;0,3)$)
#en[Factor once, then use forward and back substitution for each right-hand side.]
#warn[换行后不能忘记对 $b$ 同步置换。]
])
#sec("04", "逆矩阵与可逆判据", "[S04 p2–3; S09 p2–3; S19 p2; S21 p1]", [
仅对 $n times n$ 方阵，下列等价：
#eq($A^(-1) "exists" <==> r=n <==> N(A)={0}$)
#eq($<==> det A != 0 <==> R=I$)
也等价于：对每个 $b$，$A x=b$ 恰有一解；列向量构成 $RR^n$ 的基。
#eq($[A quad bar.v quad I] -> [I quad bar.v quad A^(-1)]$)
二阶速算（$a d-b c != 0$）：
#eq($mat(a,b;c,d)^(-1)=1/(a d-b c) mat(d,-b;-c,a)$)
#en[An invertible square matrix has a pivot in every row and every column.]
])
#sec("05", "子空间检查", "[S06 p1–2; S07 p1–2]", [
非空集合 $V$ 是子空间：含零向量，且对加法与任意实数倍封闭；可合写为
#eq($u,v in V => alpha u+beta v in V$)
齐次方程解集是子空间；$A x=b != 0$ 的非空解集是平移后的仿射集，不是子空间。
反例：两条不同的过原点直线的并集通常不对加法封闭；两个子空间的交集总是子空间。[S12 p1]
#en[It contains zero and is closed under all linear combinations.]
#warn[过原点只是必要条件，不足以证明封闭。]
])
],
[
#sec("06", "RREF、秩与零空间", "[S08 p1–2; S09 p1–3]", [
数主元得 $r$；主元变量 $r$ 个，自由变量 $n-r$ 个。逐次设一个自由变量为 1、其余为 0，回解主元变量得特殊解。
#eq($dim N(A)=n-r$)
将主元列排在前面时，可写
#eq($R=mat(I,F;0,0), quad Z=mat(-F;I), quad R Z=0$)
自编例：$R=mat(1,2,0;0,0,1)$，自由变量 $x_2=t$，故 $x=t(-2,1,0)^T$。
#en[The special solutions form a basis for the nullspace.]
#warn[若换过列，解向量要恢复原变量顺序。]
])
#sec("07", "解存在吗？有几个？", "[S07 p1; S09 p1–3]", [
#eq($A x=b " solvable" <==> b in C(A)$)
等价于 $"rank"(A)="rank"([A quad bar.v quad b])$；增广消元若出现 $[0 dots 0 quad bar.v quad d]$ 且 $d != 0$ 就无解。
有解时：$r=n$ 唯一；$r<n$ 无穷多。
#eq($x=x_p+z, quad z in N(A)$)
$x_p$ 可令自由变量为零求出。$r=m$ 表示对所有 $b$ 均有解；不保证唯一。
#set table(inset: 1.4pt, stroke: 0.25pt)
#table(columns: (1fr, 1fr), [秩情形], [给定 $b$ 的解数],
[$r=m=n$], [恰好 1], [$r=n<m$], [0 或 1],
[$r=m<n$], [无穷多], [$r<m, r<n$], [0 或无穷多])
#en[Consistency depends on $b$; uniqueness depends on $N(A)$.]
])
#sec("08", "线性无关、基、维数", "[S10 p1–3]", [
无关：$sum c_j v_j=0$ 只能有全零系数。张成：所有线性组合等于目标空间。*基=无关+张成*；维数=任一基的向量个数。
$C(A)$ 的基：取 *原矩阵* 中与主元位置对应的列。行空间的基：取 $R$ 的非零行。
#en[The pivot columns of the original matrix form a basis for its column space.]
#warn[行消元保持行空间和零空间，通常改变列空间。]
])
#sec("09", "四个基本子空间", "[S11 p1–3; S15 p1–2]", [
#set table(inset: 2pt, stroke: 0.25pt)
#table(columns: (1.3fr, 0.7fr, 0.7fr), [空间], [所在], [维数],
[$C(A)$], [$RR^m$], [$r$],
[$N(A^T)$], [$RR^m$], [$m-r$],
[$C(A^T)$], [$RR^n$], [$r$],
[$N(A)$], [$RR^n$], [$n-r$])
#eq($C(A)^perp=N(A^T), quad C(A^T)^perp=N(A)$)
相容的另一判据：对所有 $y in N(A^T)$，$y^T b=0$；左零空间给出右端必须满足的约束。[S09 p1]
#en[Each nullspace is the orthogonal complement of the corresponding row space.]
])
#sec("10", "矩阵空间 / 秩一", "[S11 p3; S12 p1–3]", [
矩阵也可当向量：$dim RR^(m times n)=m n$；对称/上三角 $n times n$ 阵各 $n(n+1)/2$ 维；对角阵 $n$ 维。
秩一阵 $A=u v^T$，其中 $u,v$ 非零；列均为 $u$ 的倍数。固定秩集合一般不是子空间。
#eq($dim(S+T)=dim S+dim T-dim(S inter T)$)
#en[A basis counts independent degrees of freedom.]
])
],
[
#sec("11", "图、网络与关联矩阵", "[S12 p3; S13 p1–4]", [
$B$ 每行一条边、每列一个节点；边 $i -> j$ 的行在 $i$ 为 $-1$，$j$ 为 $+1$。$B x$ 给节点势差。
连通图 $v$ 节点、$e$ 边：
#eq($"rank"(B)=v-1, quad N(B)="span"{bold(1)}$)
#eq($dim N(B^T)=e-v+1$)
末式数独立回路；树有 $v-1$ 条边、无回路。$B^T y=0$ 是无外源时的节点流量守恒。
有电源注入 $f$、边电导矩阵 $D$ 时：势差 $d=B x$，电流 $y=D d$，联立得 $B^T D B x=f$。[S13 p4]
#en[Cycle flows lie in the left nullspace.]
])
#sec("12", "正交与最小二乘条件", "[S15 p1–2; S17 p3]", [
#eq($u perp v <==> u^T v=0, quad norm(u)^2=u^T u$)
正交子空间要求 *每对* 向量内积为零，不只是两个平面“看起来垂直”。
#eq($N(A^T A)=N(A)$)
#eq($z^T A^T A z=norm(A z)^2$)
因此 $A^T A$ 可逆当且仅当 $A$ 列满秩。
#en[Independent columns make the least-squares coefficient vector unique.]
])
#sec("13", "投影：从向量到子空间", "[S16 p1–2; S17 p1]", [
投影到非零 $a$ 张成的直线：
#eq($p=a (a^T b)/(a^T a), quad P=(a a^T)/(a^T a)$)
投影到 $C(A)$（$A$ 列满秩）：
#eq($P=A(A^T A)^(-1) A^T, quad p=P b$)
#eq($P^T=P, quad P^2=P, quad e=(I-P)b$)
$p in C(A)$，$e perp C(A)$；若 $b in C(A)$，则 $P b=b$。
自编例：$a=(1,2)^T,b=(3,0)^T$，$p=(3/5,6/5)^T$；查 $a^T(b-p)=0$。
#en[The residual is orthogonal to the target subspace.]
#warn[秩不足时，不能直接使用上述逆矩阵式。]
])
#sec("14", "最小二乘与直线拟合", "[S16 p3; S17 p1–3]", [
最小化残差平方和，不要求原方程有解：
#eq($min_x norm(b-A x)^2 => A^T A hat(x)=A^T b$)
列满秩时 $hat(x)=(A^T A)^(-1) A^T b$。拟合 $b_i approx C+D t_i$：设计阵第 $i$ 行是 $[1, t_i]$。
原例 $(t,b)=(1,1),(2,2),(3,2)$：
#eq($hat(C)=2/3, quad hat(D)=1/2, quad norm(e)^2=1/6$)
从法方程推得：
#eq($hat(D)=(sum_i (t_i-mu_t)(b_i-mu_b))/(sum_i (t_i-mu_t)^2), quad hat(C)=mu_b-hat(D)mu_t$)
$mu_t,mu_b$ 为样本均值；至少两个不同 $t_i$ 才能确定斜率。
#en[This minimizes squared vertical residuals in the data plot.]
#warn[投影几何发生在观测向量空间 $RR^m$。]
])
#sec("15", "正交归一基 / Q", "[S18 p1–3]", [
#eq($q_i^T q_j=cases(1 & i=j, 0 & i != j), quad Q^T Q=I$)
矩形 $Q$ 列正交归一时，$P=Q Q^T$；投影坐标 $hat(x)=Q^T b$。只有 $Q$ 为方阵时，才有 $Q^(-1)=Q^T$、$Q Q^T=I$。
正交分解 $b=p+e$：$p^T e=0$，故 $norm(b)^2=norm(p)^2+norm(e)^2$。[S15 p1]
#en[Orthonormal columns simplify projection; a rectangular $Q$ need not be invertible.]
])
],
[
#sec("16", "Gram–Schmidt / QR", "[S18 p2–3]", [
输入无关列 $a_1,...,a_n$；依次减掉已有方向的投影，再归一化：
#eq($u_j=a_j-sum_(i<j)(q_i^T a_j)q_i, quad q_j=u_j/norm(u_j)$)
#eq($A=Q R, quad R=Q^T A$)
$R$ 上三角，$r_(i j)=q_i^T a_j$（$i<j$），$r_(j j)=norm(u_j)$。满列秩最小二乘：解 $R hat(x)=Q^T b$。
原例 $a_1=(1,1,1)^T,a_2=(1,0,2)^T$：$q_1=(1,1,1)^T/sqrt(3)$，$q_2=(0,-1,1)^T/sqrt(2)$。[S18 p3]
#en[Subtract projections, normalize, and preserve the span.]
#warn[$u_j=0$ 表示依赖，不能除以零。]
])
#sec("17", "行列式性质与消元", "[S19 p1–3]", [
仅对方阵。换两行变号；某行乘 $c$，行列式乘 $c$；某行加另一行倍数，行列式不变。
#eq($det I=1, quad det(A B)=det A det B$)
#eq($det A^T=det A, quad det(c A)=c^n det A$)
行（列）相关则 $det A=0$；可逆时 $det A^(-1)=1/(det A)$。
若 $P A=L U$，$L$ 对角为 1、共换行 $s$ 次：
#eq($det A=(-1)^s product_(i=1)^n u_(i i)$)
#en[Track row swaps, then multiply the diagonal entries of the triangular matrix.]
#warn[一般 $det(A+B) != det A+det B$。]
])
#sec("18", "余子式 / 展开 / 递推", "[S20 p1–3]", [
删第 $i$ 行、第 $j$ 列得 $M_(i j)$；代数余子式
#eq($C_(i j)=(-1)^(i+j) det M_(i j)$)
#eq($det A=sum_(j=1)^n a_(i j) C_(i j)$)
排列通式（$S_n$ 为全部 $n!$ 个排列）：
#eq($det A=sum_(pi in S_n) "sgn"(pi) product_(i=1)^n a_(i,pi(i))$)
选零最多的行或列展开；符号棋盘从左上角 $+$ 开始。三对角全 1 原例：$d_n=d_(n-1)-d_(n-2)$，$d_1=1,d_2=0$。
#en[Expand along any one row or column, using the matching cofactors.]
#warn[三阶对角线口诀不能推广到四阶。]
])
#sec("19", "逆、Cramer 与体积", "[S21 p1–4]", [
$C$ 为代数余子式矩阵；若 $det A != 0$：
#eq($A^(-1)=C^T/(det A), quad x_j=(det A_j)/(det A)$)
$A_j$ 是将 $A$ 的第 $j$ *列* 换成 $b$。
列向量构成的平行多面体体积为 $abs(det A)$；三角形面积为两边组成行列式绝对值的一半。
自编例：边向量 $(2,0)^T,(1,3)^T$ 的平行四边形面积 $abs(2 times 3-0 times 1)=6$，三角形为 3。
#en[The absolute determinant gives volume; its sign records orientation.]
#warn[逆矩阵要转置余子式阵；体积不能为负。]
])
#sec("20", "答题路径 / 快速自检", "[S14 p1–5 + synthesis]", [
*求解*：增广消元→查相容→特解+零空间。*求基*：先认空间→主元/特殊解→核对维数。*拟合*：列出设计阵→法方程或 QR→查 $A^T e=0$。
*自检*：$A x=b$？$A z=0$？$Q^T Q=I$？$P^2=P$？行列式换行符号与单位正确？
#en[State the rank or independence condition before using an inverse formula.]
#warn[相容≠唯一；列满秩≠列空间填满 $RR^m$。]
])
])
