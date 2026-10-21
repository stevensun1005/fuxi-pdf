# 原创演示 / Original demonstration

用两张原创幻灯片解释“为什么不能平均局部平均值”，展示同源资料的两种成品。

| 文件 | 内容与纸张 |
| --- | --- |
| [demo-slides.pdf](input/demo-slides.pdf) | 2 张原创宽屏课件 |
| [slide-walkthrough.pdf](output/slide-walkthrough.pdf) | 2 页竖版 A4：每页上方原课件，下方中文精讲 |
| [exam-reference.pdf](output/exam-reference.pdf) | 1 页 Letter：中文解释、反例、英文核心表述及两道短答 |

素材与答案是演示，不是真题。例子独立核算：[2,4] 和 [12] 的局部均值为 3 和 12，直接平均得到 7.5；全局平均为 18/3=6。保存 `(sum,count)` 后再合并与除法可以保留权重。

## 复现

安装仓库根目录的 `requirements-dev.txt`，然后：

```sh
python examples/build_demo.py --font /path/to/chinese-truetype-font.ttf
```

Windows 安装了 Microsoft YaHei 时也可直接运行 `python examples/build_demo.py`。字体需为 ReportLab 支持的 TrueType `.ttf` 或 `.ttc`；字体不随仓库提供。构建器只生成这些固定演示，不负责读取任意课程自动总结。

脚本同时生成 README 中的 PNG 预览以及 `coverage.csv`。用 `python scripts/validate_coverage.py examples/coverage.csv --inventory examples/inventory.json` 检查两张输入页均有对应。
