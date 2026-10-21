# 紧凑型数学 Cheatsheet：线性代数前半段

[单页 PDF](cheatsheet.pdf) · [可编辑 Typst 源稿](cheatsheet.typ) · [英文为主预览](preview-english.png) · [来源清单](sources.json) · [逐页覆盖台账](coverage.csv) · [核验记录](validation.md)

此示例已明确选择一页、英文为主；新的制作任务若未明确语言偏好，skill 会先问，不直接照搬此示例。与仓库中 10 页的计算机系统详细考场册分开，这份示例展示真正的**一页紧凑公式纸**：Letter 横向、四栏、四周 3.5 mm 边距、黑蓝红三色、20 个检索小节，英文标题、定义、条件、步骤与答题提示优先，仅在相容性、选基、最小二乘几何和 Gram–Schmidt 处补 4 段中文短注。英文正文 9 pt、中文短注 7.6 pt，公式是真正的数学排版；没有底部页脚、封面、独立目录或额外背面。必要署名与许可保留在页顶，打印说明放在本文件。

## 真实课程与范围

来源是 **MIT OpenCourseWare 18.06SC Linear Algebra, Fall 2011，Gilbert Strang** 的公开 lecture summaries。按[官方资源索引](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/resource-index/)的顺序，选 Unit I 全部 14 份摘要（含 overview 和 Exam 1 review），以及 Unit II 前 7 份，截止 *Cramer's Rule, Inverse Matrix and Volume*。共 **21 份、85 个 PDF 页面**，其中 21 页是课程署名/许可页。

这是“接近半学期主题范围”的演示，不按日历周数精确对半，也不是官方期中考试范围。行列式性质讲义开头明确以课程中点作为过渡；本示例纳入紧接其后的展开与体积两讲以形成完整模块。未覆盖特征值、对角化、微分方程矩阵法、SVD 等后续专题。

新增内容包括二阶逆矩阵、外积乘法、LU 成本与算例、零空间算例、四种秩情形对照、相容性约束、网络电导方程、投影算例、一般直线拟合公式、正交分解、QR 原例及行列式排列通式。

单页保留：方程视角、矩阵乘法与逆、消元和 LU、子空间、RREF、秩与解、基与维数、四个基本子空间、矩阵空间、图与网络、正交、投影、最小二乘、Gram–Schmidt/QR、行列式与体积。省略完整证明、多数原例、复习题逐题解答、small-world 距离问题等细节；**来源逐页有记录，不等于每页所有内容都印在一页内**。

## 来源定位与许可

PDF 内 `[S08 p1–2]` 指 `sources.json` 的 S08 摘要第 1–2 个 PDF 页面，均从 1 开始。台账将每个源页指向成品小节，记录压缩与省略。原始讲义不重复打包进仓库；清单提供官方资源页、直接下载 URL、页数与 SHA-256，可重新获取并核对。

资料由本项目独立压缩、翻译、重组及校正，不是官方答案，不代表 MIT 认可，也不声明该课程允许考试携带资料。来源与本目录的讲解、Typst 稿、PDF 和 PNG 按 [CC BY-NC-SA 4.0](../../licenses/MIT-OCW-math-LICENSE.md) 分发；不包含用户的私人 STAT337 原件或内容。

## 重新生成

可使用 Typst CLI：

```sh
typst compile examples/compact-math/cheatsheet.typ examples/compact-math/cheatsheet.pdf
```

或 Python binding（本次使用 `typst==0.15.0`）：

```sh
python -m pip install typst==0.15.0
python -c "import typst; typst.compile('examples/compact-math/cheatsheet.typ', output='examples/compact-math/cheatsheet.pdf')"
```

本次英文使用 Windows 的 Times New Roman，中文短注使用 Microsoft YaHei，数学使用 Cambria Math；字体嵌入 PDF、字体文件不随仓库分发。源稿也列出 Liberation Serif、Noto Sans CJK SC、STIX Two Math / New Computer Modern Math 作为回退；需在宿主安装对应字体。更换字体或 Typst 版本后重新检查**恰好一页、上下标、中文、换栏与溢出**，不能把旧预览当成新编译结果。

台账校验：

```sh
python scripts/validate_coverage.py examples/compact-math/coverage.csv --inventory examples/compact-math/inventory.json
```

打印选择 **Letter、横向、100% 实际大小、每面 1 页**。本文件只有一个打印面；不要用打印机的“多页合一”再次缩小。已做数字渲染与尺寸检查，未进行实体打印测试。
