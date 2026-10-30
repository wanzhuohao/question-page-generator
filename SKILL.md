---
name: question-page-generator
description: 根据题目图片自动识别题型，生成自包含的 HTML 网页，同时支持打印版本和在线练习版本。适用于数学、语文、英语等任何教育练习题。触发场景：用户上传题目图片、要求「把题目变成网页」「生成练习页」「做题页面」「出个练习」。
---

# Question Page Generator

给一张题目图片，自动识别题型，生成一个自包含的 HTML 网页，同时提供「打印版本」和「在线练习版本」。

## 工作流程

### 1. 接收题目图片

用户以图片上传或提供本地路径的方式给出题目。

### 2. 识别题型

使用图像理解工具识别图片，提问聚焦于：题目内容、结构、答案、交互方式。识别完成后整理为结构化数据。参考 [references/question-types.md](references/question-types.md) 中的识别模式，但不限于其中列出的类型。

### 3. 生成 HTML 页面

使用 [assets/template.html](assets/template.html) 作为基础模板，将识别到的题目数据写入 `QUESTION_DATA` 对象。

**渲染决策逻辑**（数据驱动，不依赖固定题型名）：

| 数据特征 | 渲染方式 | 适用场景 |
|----------|----------|----------|
| `choices` 字段 | 按钮选择 | 选择题、比大小、填运算符、看拼音写汉字、英语单词 |
| `type` 为 shape 类 | 图形布局 | 百数表、三角形填数、方形填数 |
| `grid` 字段 | 网格输入 | 图形填数 |
| `expr` 字段 | 文本输入 | 算式、填空、乘法填空、找规律、连加连减、表内乘法、同数连加、括号混合、竖式 |
| `prompt` 字段 | 文本输入 | 应用题、问答题 |
| 均不匹配 | 通用文本 | 退化模式 |

文本渲染基于字段优先级（`prompt` → `expr` → `pinyin`/`char` → `word` → `upper` → `top` → 兜底）。

**打印模式**（参考 uniapp 数学口算打印页）：

- 头部显示标题、姓名/班级/分数、题目个数
- 纯计算题且题量 ≥ 6 时自动使用 3 列网格排版
- 「查看答案」按钮点击后显示参考答案区域
- 「打印试卷」按钮调用 `window.print()`

**图形渲染框架**：

模板内置 `renderShape()` 函数，支持 grid / triangle / square 三种布局渲染器。这些题型的 `expr` 字段是 JSON 字符串，包含布局信息。识别图片时整理为 JSON 结构，模板自动渲染。

新增布局类型时，在 `renderShape()` 中添加一个新的渲染分支即可，无需重写模板。

### 4. 发布为 Artifact

用当前环境的 Artifact 发布工具交付 HTML 文件。

## 脚本说明

### `scripts/generate_test_pages.py`

用样例数据生成测试 HTML 页面，验证模板渲染。覆盖 19 个题型（加法、减法、比大小、填运算符、填空、乘法填空、找规律、连加连减、表内乘法、同数连加、括号混合、竖式、百数表、三角形、方形、看拼音写汉字、英语单词、应用题）。

```powershell
python -X utf8 scripts/generate_test_pages.py
```

输出到 `scripts/test-output/`，每个题型一个 HTML 文件。

### `scripts/verify_render.js`

用 Node.js 验证模板渲染逻辑（文本渲染、图形渲染、答案规范化）。

```powershell
node scripts/verify_render.js
```

## 注意事项

- 图片理解结果可能不准确，识别后应向用户确认题型和内容
- 生成的 HTML 文件应通过浏览器实际打开验证后发布
- 打印模式使用 `@media print` 规则，打印时自动隐藏交互控件和操作按钮
- 不需要预先知道题型，一切从图片识别出发
