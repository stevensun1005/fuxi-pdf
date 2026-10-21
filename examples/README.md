# 真实公开课件演示 / Real lecture demonstration

来源：**Katrina LaCurts，MIT OpenCourseWare，6.033 Computer System Engineering，Spring 2018，Lecture 14: Fault Tolerance: Reliability via Replication**。

本演示选取原课件 **第 11-13 页**，分别讲 RAID 1、RAID 4 与 RAID 5。选页构成一个连贯的小节；不声称覆盖整份 15 页课件。出处、选页范围和下载文件 SHA-256 见 [source.json](source.json)；中文与英文讲解源稿见 [demo-content.json](demo-content.json)。

| 文件 | 内容与纸张 |
| --- | --- |
| [demo-slides.pdf](input/demo-slides.pdf) | 3 张完整原页，保留原图、署名和原页码 |
| [slide-walkthrough.pdf](output/slide-walkthrough.pdf) | 3 页 A4 宽度竖版长页：原课件在上，下方用编号、代码框、表格与提示框精讲，带逐页书签 |
| [exam-reference.pdf](output/exam-reference.pdf) | 3 页 Letter：中文机制与例子，英文核心表述及每页两道短答；末页有比较表 |

原课件来自 [官方资源页](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/mit6_033s18lec14/)。演示讲解、补充例子和英文短答由本项目编写，不是官方答案或真题。预览使用成品第 2 页（RAID 4）。

RAID 4 的自编 XOR 例子独立核算：`10 XOR 11 = 01`；丢失第二块后，`10 XOR 01 = 11`。三种方案的 N 均指原始数据需要的等容量盘数，C 为单盘容量；RAID 1 用 2N 块盘，RAID 4/5 用 N+1 块盘，三者可用容量约为 N×C。

## 复现

安装仓库根目录的 `requirements-dev.txt`，然后：

```sh
python examples/build_demo.py --font /path/to/chinese-truetype-font.ttf
```

脚本默认使用仓库中的真实课件节选，重建两册、README 预览与覆盖台账，不访问网络。Windows 安装 Microsoft YaHei 时可省略 `--font`。字体需为 ReportLab 支持的 TrueType `.ttf` 或 `.ttc`，不随仓库提供。代码优先使用系统已有的 Consolas 或 DejaVu Sans Mono，中文注释使用中文字体回退。

精讲用约 11.5 pt 正文、灰底等宽代码块、字段/状态表格与浅青提示框，按内容增加页高，保持一张原课件与完整讲解同页，适合屏幕阅读。它不是标准 A4 打印页；考场册仍使用固定 Letter 纸张。详细风格见 [逐页排版规范](../references/walkthrough-style.md)。

如需从官方 PDF 重新提取三张原页，下载 [完整课件](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/8eb16d3628bbd77ee7e8471b9871ec09_MIT6_033S18lec14.pdf)，再指定：

```sh
python examples/build_demo.py --source-pdf /path/to/MIT6_033S18lec14.pdf --font /path/to/chinese-truetype-font.ttf
```

构建器先核对源文件哈希，防止版本变化后静默选错页。它是固定演示构建器，不负责自动总结任意课程。

```sh
python scripts/validate_coverage.py examples/coverage.csv --inventory examples/inventory.json
```

台账的 `page_or_slide` 为节选内的第 1-3 页；`citation` 与 `notes` 明确映射到原课件第 11-13 页。该验证只证明三页节选有去向，不证明整讲覆盖。

## 许可

真实课件节选、演示讲解、派生 PDF 和其 PNG 预览采用 [CC BY-NC-SA 4.0](../licenses/MIT-OCW-demo-LICENSE.md)。技能与构建代码仍采用根目录 MIT 许可。

打印考场册：Letter，100% 实际大小，每面一页；单面 3 张，双面 2 张、沿长边翻转。这只是演示设置，是否允许携带及页数限制以实际考试规定为准。
