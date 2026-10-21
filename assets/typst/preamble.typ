// ══════════════════════════════════════════════════════════════════
//  NovaForge — 通用知识笔记 Typst 模板（共享样式与函数）
//  适用于：考研/考公/专业课/科研/项目/竞赛
//  编译方式：typst compile template.typ
// ══════════════════════════════════════════════════════════════════

// ── 页面设置 ──
#set page(
  paper: "a4",
  margin: (top: 1.4cm, bottom: 1.2cm, left: 1.0cm, right: 1.0cm),
  header: context {
    let ltext = "NovaForge"
    let rtext = "一叶知秋"
    set text(size: 8pt, fill: gray)
    align(left, ltext)
    align(right, rtext)
  },
  footer: context {
    let ctext = counter(page).display()
    set text(size: 8pt, fill: gray)
    align(center, ctext)
  },
  numbering: "1",
)

// ── 全局文本设置 ──
#set text(
  font: ("SimSun", "New Computer Modern"),
  lang: "zh",
  size: 10pt,
)

// ── 数学设置 ──
#set math.equation(numbering: "(1)")

// ── 段落 ──
#set par(first-line-indent: 2em, justify: true)
#show heading.where(level: 1): it => {
  v(0.5em)
  text(size: 1.4em, weight: "bold", fill: title-color, it)
  v(-0.1em)
  line(length: 100%, stroke: 0.8pt + title-color)
  v(0.3em)
}
#show heading.where(level: 2): it => {
  v(0.4em)
  text(size: 1.1em, weight: "bold", fill: sec-color, it)
  v(0.15em)
}
#show heading.where(level: 3): it => {
  v(0.3em)
  text(size: 0.95em, weight: "bold", fill: subsec-color, it)
  v(0.1em)
}

// ── 列表 ──
#set list(marker-indent: 2em, body-indent: 0.5em)

// ── 颜色系统（可按学科自定义）──
// 理科风（深蓝）| 文科风（暗红）| 清新风（墨绿）
#let title-color = rgb("#1a237e")      // 主标题 ← 从这里换色
#let sec-color = rgb("#004d40")        // 节标题
#let subsec-color = rgb("#b71c1c")     // 小节标题
#let emph-color = rgb("#bf360c")       // 强调
#let info-color = rgb("#1565c0")       // 提示
#let warn-color = rgb("#e65100")       // 警告
#let super-color = rgb("#880e4f")      // 超纲/拓展
#let example-color = rgb("#1b5e20")    // 示例
#let section-bg = rgb("#e8eaf6")       // 标题背景
#let light-gray = rgb("#f5f5f5")       // 浅灰
#let hw-color = rgb("#795548")         // 习题
#let learn-color = rgb("#2e7d32")      // 练习

// ── 自定义函数 ──

/// 强调文本（橙红）
#let key(body) = text(fill: emph-color, weight: "bold", body)

/// 拓展/超纲文本（紫红）
#let super(body) = text(fill: super-color, weight: "bold", body)

/// 来源标注（紫色小字）
#let source(body) = text(fill: purple, size: 0.85em, [#body])

/// 原理/公式框
#let formula(body) = {
  v(0.3em)
  align(center, block(
    width: 92%,
    inset: 4pt,
    stroke: title-color,
    fill: white,
    text(fill: title-color, size: 0.9em, body),
  ))
  v(0.2em)
}

/// 提示框
#let infobox(body) = {
  v(0.3em)
  text(fill: info-color, size: 0.9em, [#body])
  v(0.2em)
}

/// 警告
#let warning(body) = {
  v(0.3em)
  text(fill: warn-color, size: 0.9em, weight: "bold", [#body])
  v(0.2em)
}

/// 分隔线
#let sep() = {
  v(0.5em)
  line(length: 100%)
  v(0.5em)
}

/// 知识标题栏（浅蓝灰背景）
#let knowtitle(body) = {
  v(0.3em)
  block(
    width: 100%,
    fill: section-bg,
    inset: (x: 6pt, y: 3pt),
    text(fill: title-color, size: 0.85em, weight: "bold", body),
  )
  v(0.15em)
}

/// 案例/例题环境
#let examenv(title, body) = {
  v(0.4em)
  block(
    inset: (x: 8pt, y: 4pt),
    width: 100%,
    stroke: (left: 3pt + super-color),
    fill: rgb(white),
    [
      #text(fill: super-color, weight: "bold", size: 0.9em)[【案例/例题】#title]
      #v(0.2em)
      #text(fill: info-color, size: 0.9em)[分析：]
      #body
    ]
  )
  v(0.3em)
}

/// 练习/复盘环境（绿色标签）
#let pracenv(title, body) = {
  v(0.4em)
  block(
    inset: (x: 8pt, y: 4pt),
    width: 100%,
    stroke: (left: 3pt + learn-color),
    [
      #text(fill: learn-color, weight: "bold", size: 0.9em)[【练习/复盘】#title]
      #v(0.2em)
      #text(fill: gray, size: 0.9em)[解答：]
      #body
    ]
  )
  v(0.3em)
}

/// 课后作业环境（棕色，解答见附录）
#let hwenv(title, body) = {
  v(0.4em)
  block(
    inset: (x: 8pt, y: 4pt),
    width: 100%,
    stroke: (left: 3pt + hw-color),
    [
      #text(fill: hw-color, weight: "bold", size: 0.9em)[【作业】#title]
      #v(0.2em)
      #text(fill: gray, size: 0.85em)[（解答见附录）]
      #body
    ]
  )
  v(0.3em)
}

/// 方法速通
#let method-box(body) = {
  v(0.2em)
  text(fill: emph-color, weight: "bold")[方法速通：]
  body
  v(0.15em)
}

// ── 期末复习模式专用命令 ──

/// 年份标签（竞赛用 4 位完整年份）
#let yearlabel(year, note: "") = {
  let suffix = if note != "" { note } else { "" }
  text(fill: super-color, size: 0.85em)[#year 年 #suffix]
}

/// 练习留白提示
#let seeans() = text(fill: gray, size: 0.85em)[（答案见末节）]

/// 答案条目
#let answer(num, body) = {
  v(0.4em)
  text(fill: example-color, weight: "bold", size: 0.95em)[答案 #num：]
  body
}

// ── 考研模式专用命令 ──

/// 考研真题标注
#let exam(year, uni, code, num) = {
  text(fill: super-color, size: 0.85em)[#uni · #code · #year · 第#num题]
}

// ── 科研模式专用命令 ──

/// 文献标题
#let lithead(body) = {
  v(0.3em)
  text(fill: title-color, size: 0.9em, weight: "bold", body)
  v(0.15em)
}

/// 文献信息表
#let paperinfo(title, author, venue, year) = {
  table(
    columns: (auto, auto),
    inset: 4pt,
    [标题], [---],
    [作者], [---],
    [刊源], [---],
    [年份], [---],
  )
}

// ── 封面函数 ──

/// 生成封面
#let cover(subject, subtitle: "", description: "", refs: (), author: "一叶知秋", field: "", module: "", version: "1.0", date: "") = {
  align(center, [
    #v(3em)
    #text(size: 1.8em, weight: "bold", fill: title-color)[#subject]
    #if subtitle != "" [ #v(0.2em) #text(size: 1.3em, weight: "bold", fill: title-color)[#subtitle] ]
    #if description != "" [ #v(0.2em) #text(size: 0.95em, fill: gray, weight: "bold")[#description] ]
    #v(0.8em)
    #for ref in refs [
      #text(size: 0.85em, fill: gray)[#ref] \
    ]
    #v(0.2em)
    #text(size: 0.85em, fill: gray)[#author \ #field \ #module]
    #v(0.6em)
    #text(size: 0.95em, fill: title-color, weight: "bold")[版本：#version]
    #if date != "" [ #v(0.1em) #text(size: 0.8em, fill: gray)[最后修订：#date] ]
    #v(2em)
  ])
}

// ── 使用说明结构 ──

/// 生成"如何使用"说明
#let usage-guide() = {
  heading(level: 1, outlined: false)[如何使用这份笔记]
  这份笔记的目标是 **帮你建立系统的知识体系**：
  - **搭配学习**：配合教材/课程使用，先理解再巩固
  - **独立使用**：完整覆盖核心知识点，独立查阅
  - **复习冲刺**：方法总结 + 典型例题 + 速查表，快速回顾

  #text(fill: emph-color, weight: "bold")[每节结构：]
  + **概念引入** — 先建立直觉
  + **核心原理** — 公式/原理框突出
  + **方法技巧** — 实操技巧浓缩
  + **典型示例** — 经典案例搭桥
  + **真题/实战** — 真实题目/项目
  + **巩固练习** — 复盘训练
  + **专题总结** — 末章归纳核心题型/模式
}

// ── 范围说明 ──

/// 生成范围说明表格
#let scope-table(data) = {
  heading(level: 1, outlined: false)[范围说明]
  table(
    columns: (auto, auto),
    fill: (light-gray, white),
    stroke: 0.5pt,
    [模块], [覆盖内容],
    ..data,
  )
}
