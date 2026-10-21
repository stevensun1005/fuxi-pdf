// Educational adaptation: CC BY-NC-SA 4.0. Provenance: README.md / sources.json.
// Build: typst compile cheatsheet.typ cheatsheet.pdf
#set document(title: "Linear Algebra | English-first one-page reference", author: "fuxi-pdf")
#set page(paper: "us-letter", flipped: true, margin: 3.5mm)
#set text(font: ("Times New Roman", "Liberation Serif", "Microsoft YaHei", "Noto Sans CJK SC"), size: 9pt, lang: "en")
#set par(leading: 1.8pt, spacing: 2pt, justify: false)
#set block(spacing: 3pt)
#let blue = rgb("1648a8")
#let red = rgb("b12626")
#show math.equation: set text(font: ("Cambria Math", "STIX Two Math", "New Computer Modern Math"), fill: blue)
#set math.equation(numbering: none)
#let warn(body) = block(above: 1pt, below: 1pt)[#text(fill: red, size: 8.4pt)[*Watch:* #body]]
#let cn(body) = block(above: 1pt, below: 1pt)[#text(font: ("Microsoft YaHei", "Noto Sans CJK SC"), size: 7.6pt)[*中文提示：*#body]]
#let eq(body) = block(above: 2pt, below: 2pt, body)
#let sec(id, title, source, body) = block(breakable: false, above: 3pt, below: 2pt)[
  #line(length: 100%, stroke: 0.45pt)
  #text(weight: "bold", size: 9.6pt)[#id  #title] #text(size: 6.3pt, fill: rgb("555555"))[#source]
  #parbreak()
  #body
]

#text(weight: "bold", size: 12pt)[LINEAR ALGEBRA · ONE-PAGE REFERENCE] #h(1fr) #text(fill: blue, size: 6.7pt)[MIT OCW · Gilbert Strang · 2011 · Adapted by fuxi-pdf · #link("https://creativecommons.org/licenses/by-nc-sa/4.0/")[CC BY-NC-SA 4.0]]
#parbreak()
#text(size: 7pt)[Scope: MIT 18.06SC, first-half topic selection through determinants and volume; not an official exam scope. No eigenvalues, diagonalization or SVD.]
#parbreak()
#text(size: 7pt)[Real $A in RR^(m times n)$; $r="rank"(A)$; $R="rref"(A)$; $C(A)$=column space; $N(A)$=nullspace; $T$=transpose. Black: explanations / conditions; blue: formulas; red: traps.]

#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 9pt,
grid.vline(x: 1, stroke: 0.25pt + rgb("bbbbbb")),
grid.vline(x: 2, stroke: 0.25pt + rgb("bbbbbb")),
grid.vline(x: 3, stroke: 0.25pt + rgb("bbbbbb")),
[
#sec("01", "Systems: three pictures", "[S01 p1–3; S02 p1–4]", [
*Rows:* intersect the equation hyperplanes. *Columns:* combine the columns $a_j$ to obtain $b$. *Matrix:* write both pictures as one equation.
#eq($A x=sum_(j=1)^n x_j a_j=b$)
Solving a system means finding the coefficients of that linear combination. $a_j,b in RR^m$; $x in RR^n$.
])
#sec("02", "Products and transposes", "[S04 p1–3; S05 p1]", [
$A_(m times n) B_(n times k)$ has size $m times k$. The inner dimensions must agree.
#eq($(A B)_(i j)=sum_(ell=1)^n a_(i ell)b_(ell j)$)
Columns of $A B$ combine columns of $A$; rows of $A B$ combine rows of $B$. Outer-product form:
#eq($A B=sum_(ell=1)^n A_(:,ell) B_(ell,:)$)
#eq($(A B)^T=B^T A^T, quad (A B)^(-1)=B^(-1) A^(-1)$)
The inverse rule requires invertible square factors.
#warn[Order reverses. Generally $A B != B A$; $A^T A$ is always symmetric.]
])
#sec("03", "Elimination, permutations, LU", "[S03 p1–3; S05 p1–3; S06 p1]", [
Apply $R_i <- R_i-ell_(i j)R_j$ to both $A$ and $b$. Swap rows for a zero pivot; a rectangular system may have free columns.
#eq($P A=L U, quad L c=P b, quad U x=c$)
$L$: unit lower triangular, storing multipliers. $U$: upper triangular. Without swaps, $P=I$; $P^(-1)=P^T$.
Factor once in $O(n^3)$ for a dense $n times n$ system; each new right-hand side costs $O(n^2)$ to solve.
#eq($mat(2,1;8,7)=mat(1,0;4,1) mat(2,1;0,3)$)
#warn[Permute $b$ too. Check the factorization by multiplying $L U$.]
])
#sec("04", "Invertibility and 2×2 inverse", "[S04 p2–3; S09 p2–3; S19 p2; S21 p1]", [
For an $n times n$ matrix, all are equivalent:
#eq($A^(-1) "exists" <==> r=n <==> N(A)={0}$)
#eq($<==> det A != 0 <==> R=I$)
Equivalently: the columns form a basis of $RR^n$; or $A x=b$ has exactly one solution for *every* $b$.
#eq($[A quad bar.v quad I] -> [I quad bar.v quad A^(-1)]$)
For $a d-b c != 0$:
#eq($mat(a,b;c,d)^(-1)=1/(a d-b c) mat(d,-b;-c,a)$)
Swap the diagonal entries, negate the off-diagonal entries, and divide by the determinant.
])
#sec("05", "Subspaces: the closure test", "[S06 p1–2; S07 p1–2; S12 p1]", [
A subspace contains zero and is closed under addition and multiplication by *every* real scalar:
#eq($u,v in V => alpha u+beta v in V$)
The solutions of $A x=0$ form a subspace. A nonempty solution set of $A x=b != 0$ is an affine translate, not a subspace.
Intersections of subspaces are subspaces. A union of two distinct lines through zero is not closed under addition.
#warn[Containing zero is necessary, not sufficient.]
])
],
[
#sec("06", "RREF, rank and nullspace", "[S08 p1–2; S09 p1–3]", [
Count pivots to obtain $r$. There are $r$ pivot variables and $n-r$ free variables. Set one free variable to 1 and the others to 0; solve for the pivots. These special solutions form a basis of $N(A)$.
#eq($dim N(A)=n-r$)
With pivot columns ordered first:
#eq($R=mat(I,F;0,0), quad Z=mat(-F;I), quad R Z=0$)
*Authored example:* if $R=mat(1,2,0;0,0,1)$, let $x_2=t$; then $x=t(-2,1,0)^T$.
#warn[Restore the original variable order after any column permutation.]
])
#sec("07", "Consistency and solution count", "[S07 p1; S09 p1–3]", [
#eq($A x=b " solvable" <==> b in C(A)$)
Equivalently, $"rank"(A)="rank"([A quad bar.v quad b])$. An augmented row $[0 dots 0 quad bar.v quad d]$ with $d != 0$ means no solution.
If consistent, choose a particular solution $x_p$ by setting the free variables to zero; all solutions are
#eq($x=x_p+z, quad z in N(A)$)
#set table(inset: 1.4pt, stroke: 0.25pt)
#table(columns: (1fr, 1fr), [Rank case], [Solutions for given $b$],
[$r=m=n$], [exactly 1], [$r=n<m$], [0 or 1],
[$r=m<n$], [infinitely many], [$r<m, r<n$], [0 or infinitely many])
#cn[先查是否有解，再查自由变量；相容性取决于 $b$，唯一性取决于 $N(A)$。]
])
#sec("08", "Independence, basis, dimension", "[S10 p1–3]", [
*Independent:* $sum c_j v_j=0$ implies every $c_j=0$. *Span:* all linear combinations fill the target space. *Basis:* independent and spanning. *Dimension:* number of vectors in any basis.
A basis of $C(A)$ uses the pivot columns of the *original* $A$. A basis of the row space uses the nonzero rows of $R$.
#cn[消元后的主元位置用于选原矩阵的列；行变换保留行空间和零空间，但通常改变列空间。]
])
#sec("09", "Four fundamental subspaces", "[S11 p1–3; S15 p1–2; S09 p1]", [
#set table(inset: 2pt, stroke: 0.25pt)
#table(columns: (1.35fr, 0.7fr, 0.7fr), [Subspace], [Ambient], [Dim.],
[$C(A)$], [$RR^m$], [$r$], [$N(A^T)$], [$RR^m$], [$m-r$],
[$C(A^T)$], [$RR^n$], [$r$], [$N(A)$], [$RR^n$], [$n-r$])
#eq($C(A)^perp=N(A^T), quad C(A^T)^perp=N(A)$)
The row space and nullspace are orthogonal complements in $RR^n$; the column space and left nullspace are complements in $RR^m$.
*Consistency test:* $y^T b=0$ for every $y in N(A^T)$.
])
#sec("10", "Matrix spaces and rank one", "[S11 p3; S12 p1–3]", [
Matrices themselves can be vectors: $dim RR^(m times n)=m n$. Symmetric and upper-triangular $n times n$ spaces each have dimension $n(n+1)/2$; diagonal matrices have dimension $n$.
Rank one: $A=u v^T$ for nonzero $u,v$; every column is a multiple of $u$. A fixed-rank collection is generally not a subspace.
#eq($dim(S+T)=dim S+dim T-dim(S inter T)$)
Count independent degrees of freedom, not the number of displayed entries.
])
],
[
#sec("11", "Graphs and network matrices", "[S12 p3; S13 p1–4]", [
Incidence matrix $B$: one row per edge, one column per node. Edge $i -> j$: put $-1$ at $i$, $+1$ at $j$. $B x$ gives potential differences.
For a connected graph with $v$ nodes and $e$ edges:
#eq($"rank"(B)=v-1, quad N(B)="span"{bold(1)}$)
#eq($dim N(B^T)=e-v+1$)
The last quantity counts independent cycles. A tree has $v-1$ edges and no cycles. Kirchhoff's current law with no injected current: $B^T y=0$.
With conductance matrix $D$ and injection $f$:
#eq($d=B x, quad y=D d, quad B^T D B x=f$)
#warn[Nodes index columns; edges index rows.]
])
#sec("12", "Orthogonality and normal equations", "[S15 p1–2; S17 p3]", [
#eq($u perp v <==> u^T v=0, quad norm(u)^2=u^T u$)
Orthogonal subspaces require *every* vector in one to be orthogonal to every vector in the other.
#eq($N(A^T A)=N(A)$)
#eq($z^T A^T A z=norm(A z)^2$)
Hence $A^T A$ is invertible exactly when the columns of $A$ are independent. This condition makes the least-squares coefficient vector unique.
])
#sec("13", "Orthogonal projections", "[S16 p1–2; S17 p1]", [
Onto the line spanned by nonzero $a$:
#eq($p=a (a^T b)/(a^T a), quad P=(a a^T)/(a^T a)$)
Onto $C(A)$ when $A$ has independent columns:
#eq($P=A(A^T A)^(-1) A^T, quad p=P b$)
#eq($P^T=P, quad P^2=P, quad e=(I-P)b$)
$p in C(A)$ and $e perp C(A)$. If $b in C(A)$, then $P b=b$. If $b perp C(A)$, then $P b=0$.
*Authored example:* $a=(1,2)^T$, $b=(3,0)^T$ gives $p=(3/5,6/5)^T$; check $a^T(b-p)=0$.
#warn[Do not use the inverse formula when $A$ is column-rank deficient.]
])
#sec("14", "Least squares and line fitting", "[S16 p3; S17 p1–3]", [
Minimize the residual sum of squares:
#eq($min_x norm(b-A x)^2 => A^T A hat(x)=A^T b$)
For full column rank, $hat(x)=(A^T A)^(-1) A^T b$.
Fit $b_i approx C+D t_i$ using design row $[1,t_i]$. With sample means $mu_t,mu_b$:
#eq($hat(D)=(sum_i (t_i-mu_t)(b_i-mu_b))/(sum_i (t_i-mu_t)^2), quad hat(C)=mu_b-hat(D)mu_t$)
At least two distinct $t_i$ are needed. Source example: $(t,b)=(1,1),(2,2),(3,2)$ gives
#eq($hat(C)=2/3, quad hat(D)=1/2, quad norm(e)^2=1/6$)
#cn[数据图上最小化竖直残差；投影垂直性是在整个观测向量的 $RR^m$ 空间，不是点到拟合线的距离。]
])
#sec("15", "Orthonormal columns", "[S18 p1–3; S15 p1]", [
#eq($q_i^T q_j=cases(1 & i=j, 0 & i != j), quad Q^T Q=I$)
Then $P=Q Q^T$ and the projection coordinates are $hat(x)=Q^T b$. Only for *square* $Q$ do we have $Q^(-1)=Q^T$ and $Q Q^T=I$.
For the orthogonal split $b=p+e$:
#eq($p^T e=0, quad norm(b)^2=norm(p)^2+norm(e)^2$)
#warn[Orthonormal columns do not make a rectangular matrix invertible.]
])
],
[
#sec("16", "Gram–Schmidt and QR", "[S18 p2–3]", [
Start with independent columns $a_1,...,a_n$. Remove earlier projections; normalize the remainder:
#eq($u_j=a_j-sum_(i<j)(q_i^T a_j)q_i, quad q_j=u_j/norm(u_j)$)
#eq($A=Q R, quad R=Q^T A$)
$R$ is upper triangular: $r_(i j)=q_i^T a_j$ for $i<j$, $r_(j j)=norm(u_j)$. Solve least squares via $R hat(x)=Q^T b$.
Source example: $a_1=(1,1,1)^T$, $a_2=(1,0,2)^T$:
#eq($q_1=(1,1,1)^T/sqrt(3), quad q_2=(0,-1,1)^T/sqrt(2)$)
#cn[先减去已保留方向的投影，再归一化；不是把原向量分别除以长度。]
#warn[$u_j=0$ signals dependence; never divide by zero.]
])
#sec("17", "Determinants and elimination", "[S19 p1–3]", [
For square matrices: swap two rows → change sign; scale one row by $c$ → scale the determinant by $c$; add a multiple of another row → no change.
#eq($det I=1, quad det(A B)=det A det B$)
#eq($det A^T=det A, quad det(c A)=c^n det A$)
Dependent rows or columns give determinant zero. If $A$ is invertible, $det A^(-1)=1/(det A)$.
For $P A=L U$ with unit diagonal $L$ and $s$ swaps:
#eq($det A=(-1)^s product_(i=1)^n u_(i i)$)
#warn[Generally $det(A+B) != det A+det B$.]
])
#sec("18", "Cofactors and determinant formulas", "[S20 p1–3]", [
Delete row $i$ and column $j$ to form minor $M_(i j)$:
#eq($C_(i j)=(-1)^(i+j) det M_(i j)$)
#eq($det A=sum_(j=1)^n a_(i j) C_(i j)$)
Expand along a sparse row/column; signs start $+$ at the upper-left. $S_n$: all $n!$ permutations.
#eq($det A=sum_(pi in S_n) "sgn"(pi) product_(i=1)^n a_(i,pi(i))$)
For tridiagonal all-ones bands: $d_n=d_(n-1)-d_(n-2)$, $d_1=1$, $d_2=0$ (source example).
#warn[The 3×3 diagonal shortcut does not extend to 4×4.]
])
#sec("19", "Inverse, Cramer and volume", "[S21 p1–4]", [
Let $C$ be the cofactor matrix. When $det A != 0$:
#eq($A^(-1)=C^T/(det A), quad x_j=(det A_j)/(det A)$)
$A_j$: replace *column* $j$ by $b$. Elimination is usually more efficient.
Column parallelepiped: volume $abs(det A)$. Triangle: half the absolute determinant of its two edges.
*Authored:* edges $(2,0)^T,(1,3)^T$ → parallelogram area 6; triangle area 3.
#warn[Transpose the cofactor matrix. Volume is nonnegative; the sign of the determinant records orientation.]
])
#sec("20", "Exam workflow and checks", "[S14 p1–5 + synthesis]", [
*Solve:* $[A quad bar.v quad b]$ → consistency → $x_p+N(A)$.
*Basis:* name the space → pivots / special solutions → check dimension and independence.
*Fit:* design matrix → normal equations / QR → $A^T e=0$.
*Checks:* $A x=b$; $A z=0$; $Q^T Q=I$; $P^2=P$; determinant sign after swaps.
*Answer cue:* State the rank condition before using an inverse.
#warn[Consistent ≠ unique. Full column rank need not fill $RR^m$.]
])
])
