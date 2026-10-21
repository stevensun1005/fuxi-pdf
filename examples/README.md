# MIT 6.033 第14讲 · 完整双册示例

另有独立的 [单页紧凑数学示例](compact-math/README.md)：线性代数近半学期主题，四栏三色；下文保留计算机系统全讲精讲与不限页详细考场册示例。

来源：**Katrina LaCurts，MIT OpenCourseWare，6.033 Computer System Engineering，Spring 2018，Lecture 14: Fault Tolerance: Reliability via Replication**。

覆盖整讲原第 **1-15 页**，以及 [官方配套提纲](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/pages/week-8/lecture-14-outline/) 中用于解释标题页的内容。包括封面、错误画面、转场页、正文、总结和许可页，不只截取 RAID 小节。

| 文件 | 内容 |
| --- | --- |
| [demo-slides.pdf](input/demo-slides.pdf) | 15 页全讲公开适配版；原第 9 页厂商图改为明确标注的文字示意 |
| [slide-walkthrough.pdf](output/slide-walkthrough.pdf) | 15 页中文精讲；原页在上，编号、代码框、表格与提示框在下；保留全部原页关联 |
| [exam-reference.pdf](output/exam-reference.pdf) | 10 页标准 Letter cheatsheet；中文解释与推导后接英文表述及 14 道自编短答，含目录、英文索引和原页定位 |
| [demo-content.json](demo-content.json) | 每一页的中文讲解和结构化排版内容 |
| [exam-content.json](exam-content.json) | 7 个考点的中英内容及代码/表格 |
| [source.json](source.json) | 作者、网址、原文件哈希、全部页码与第 9 页替换说明 |
| [build-report.json](build-report.json) | 实际成品页数、目录定位与预览页 |

学习册用 A4 页宽与可变页高，正文约 11.5 pt，保证原页和完整讲解同页，适合屏幕阅读。它不是标准 A4 打印稿。Cheatsheet 用固定 Letter 纸张与约 10.5 pt 正文，支持自然续页，中文和英文都使用正常正文字体；代码与计算步骤使用等宽框。

README 预览为精讲原第 12 页（RAID 4）与 cheatsheet 第 3 页（可用性）。

## 七个考点

1. C01：故障模型、识别、检测与限制、处理方式。
2. C02：MTTF、MTTR、可用性公式、单位与手算。
3. C03：磁盘失效、MTBF 的群体统计含义与年龄相关风险。
4. C04：RAID 1 镜像、容量与容错边界。
5. C05：RAID 4、XOR 恢复、专用校验盘瓶颈。
6. C06：RAID 5、分布校验与未改变的单盘容错等级。
7. C07：成本和性能取舍、相关故障、简洁英文回答的组织。

讲解、补充例子和短答是本项目的教育改编，不是真题或官方答案。原页 7、8、10 等标题页会明确说明细节来自官方提纲。提纲中的可用性例子按给定数字复算为 `43200/43210 = 0.99976857`；提纲写的 `.9997` 是粗略记法，保留四位小数应为 `.9998`。

## 原图与公开适配

原第 9 页的 Seagate 厂商规格图明确排除在 OCW 的开放许可外。公开版用独立生成的文字页保留该位置与统计教学内容，不嵌入被排除的图片。其余 14 页保留原图；需要查看未经修改的原件时，使用 [官方完整 PDF](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/8eb16d3628bbd77ee7e8471b9871ec09_MIT6_033S18lec14.pdf)。

## 复现

安装根目录的 `requirements-dev.txt` 后运行：

```sh
python examples/build_demo.py --font /path/to/chinese-truetype-font.ttf
```

默认使用仓库中的 15 页公开适配版，离线重建两册、目录、索引、预览与覆盖报告。Windows 已安装 Microsoft YaHei 时可省略 `--font`。字体需为 ReportLab 支持的 TrueType `.ttf` 或 `.ttc`；代码优先使用系统已有的 Consolas 或 DejaVu Sans Mono，中文注释使用中文字体回退，字体文件不随仓库分发。

如从下载的原文件重新生成公开适配版，运行：

```sh
python examples/build_demo.py --source-pdf /path/to/MIT6_033S18lec14.pdf --font /path/to/chinese-truetype-font.ttf
```

构建器先核对源文件哈希，再生成完整顺序并替换第 9 页。它是固定课程示例构建器，不是自动总结任意课程的 CLI。

```sh
python scripts/validate_coverage.py examples/coverage.csv --inventory examples/inventory.json
```

台账按原第 1-15 页登记：14 页记为 covered，原第 15 页作为许可/出处页记为 administrative 并说明理由；逐页精讲仍保留它。每行同时定位学习册与考场册的概念编号和实际印刷页码。

## 打印与许可

Cheatsheet：Letter，100% 实际大小，每面一页；单面 10 张，双面 5 张，沿长边翻转。是否允许携带及页数限制以实际考试规定为准。

课程公开适配版、讲解、派生 PDF 和预览采用 [CC BY-NC-SA 4.0](../licenses/MIT-OCW-demo-LICENSE.md)；技能与构建代码仍采用 MIT 许可。
