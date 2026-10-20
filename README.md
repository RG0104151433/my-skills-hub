# My Skills Hub

> 一个个人 Agent Skills 收藏仓库：自己编写的技能，加上从网上收集、整理和二次编辑的技能，统一按 `SKILL.md` 规范归档。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Skills](https://img.shields.io/badge/skills-42-brightgreen.svg)
![Format](https://img.shields.io/badge/format-SKILL.md-8a2be2.svg)

---

## 这是什么

这里存放我在日常使用 AI 编程助手 / Agent 过程中沉淀下来的技能（Skills）。
技能是一份带 frontmatter 的 Markdown 指令文档，告诉 Agent **在什么场景下、按什么流程、产出什么结果**。
仓库里的内容大致分两类：

| 类型 | 说明 |
| --- | --- |
| **自研** | 从问题出发自己设计、编写和维护的技能，带完整文档、示例与校验脚本 |
| **收集整理** | 来自开源社区（GSAP、Remotion、HyperFrames 等）的技能，按统一格式整理，部分做了本地化适配 |

所有技能都遵循 [Agent Skills](https://agentskills.io/) 的通用约定：目录名与 `name` 字段一致，入口为 `SKILL.md`，可以放进任意支持该规范的 Agent 的 skills 目录中使用。

---

## 仓库结构

```text
my-skills-hub/
├── .gitignore
├── LICENSE
├── README.md                              # 本文件
│
├── algo-implicit-heuristics/              # 【自研】算法认知的隐性启发
│   ├── skills/
│   │   └── algo-implicit-heuristics/
│   │       ├── SKILL.md                   #   技能入口（教学层 + 诊断层 + 执行层）
│   │       └── scripts/check_lesson.py    #   讲稿可机器校验部分
│   ├── docs/                              #   设计、路线图、分析文档
│   ├── examples/                          #   两个完整讲解示例
│   ├── lessons/                           #   真实题目讲义与验证脚本
│   ├── tests/                             #   校验脚本的测试与 fixtures
│   ├── .github/workflows/ci.yml           #   CI
│   ├── CHANGELOG.md / CONTRIBUTING.md / HANDOFF.md
│   ├── LICENSE                            #   该子项目独立 MIT 协议
│   └── README.md
│
└── opencode若干前端绘图技能（原始）/        # 【收集整理】前端 / 动画 / 视频生成技能包
    ├── README-技能安装说明.md              #   安装与权限配置说明
    ├── opencode.json                      #   OpenCode 技能权限配置
    ├── opencode-skills-pack.zip           #   打包版（离线分发用）
    ├── scripts/check_skills.py            #   技能格式批量校验
    └── .opencode/skills/                  #   41 个技能
        ├── gsap-*/                        #   GSAP 动画（8）
        │   ├── gsap-core
        │   ├── gsap-timeline
        │   ├── gsap-scrolltrigger
        │   ├── gsap-plugins
        │   ├── gsap-react
        │   ├── gsap-frameworks
        │   ├── gsap-performance
        │   └── gsap-utils
        ├── remotion-*/                    #   Remotion 视频（13）
        │   ├── remotion-create / remotion-docs / remotion-studio
        │   ├── remotion-best-practices / remotion-render / remotion-upgrade
        │   ├── remotion-captions / remotion-maps / remotion-markup
        │   ├── remotion-multimedia / remotion-interactivity / remotion-saas
        │   └── remotion-to-hyperframes
        ├── hyperframes*/                  #   HyperFrames 视频引擎（9）
        │   ├── hyperframes / hyperframes-core / hyperframes-cli
        │   ├── hyperframes-animation / hyperframes-audio / hyperframes-creative
        │   └── hyperframes-keyframes / hyperframes-registry / hyperframes-studio
        └── 其他创作类技能（11）
            ├── embedded-captions          #   嵌入式字幕 / 动态排版
            ├── faceless-explainer         #   无出镜解说视频
            ├── figma                      #   Figma 内容导入
            ├── general-video              #   通用视频流水线
            ├── media-use                  #   素材（BGM/SFX/图片/配音）解析
            ├── motion-graphics            #   动态图形
            ├── music-to-video             #   音乐可视化
            ├── pr-to-video                #   PR 转视频
            ├── product-launch-video       #   产品发布视频
            ├── slideshow                  #   幻灯片式视频
            └── talking-head-recut         #   口播视频重剪
```

> 目录名 `opencode若干前端绘图技能（原始）` 保留了最初整理时的命名，表示这是一份「原始收集版」技能包。

---

## 技能一览

### 自研：algo-implicit-heuristics

**算法认知的隐性启发** —— 一个平台无关的算法题讲解技能。
它不直接给题解，而是通过并行案例、参数微调和命名渗透，让「这题该想什么」的判断自己长出来；同时用行为信号诊断学习者卡在「前置概念缺失」还是「校准误差」。

- 适用：力扣 / LeetCode 讲题、算法面试准备、把题解改写成概念课
- 不适用：只要代码、报错调试、复杂度推导、API 查询
- 配套：`check_lesson.py` 可校验讲稿结构，CI 已接入

快速开始：

```text
用隐性启发讲讲这道题：<题目描述>
```

详细设计见 [`algo-implicit-heuristics/README.md`](algo-implicit-heuristics/README.md)。

### 收集整理：OpenCode 前端绘图 / 视频技能包

| 来源 | 技能 | 用途 |
| --- | --- | --- |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | `gsap-*` × 8 | GSAP 核心 API、时间线、ScrollTrigger、插件、React 集成与性能 |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | `remotion-*` × 13 | 用 React 创建、渲染、字幕、地图、交互式视频 |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | `hyperframes*` 及创作类技能 | HTML 合成、关键帧、音频、素材、动态图形与成片流水线 |

这些技能按 OpenCode 的 `SKILL.md` 规范整理过：frontmatter 只保留 `name` / `description` / `license` / `compatibility` / `metadata` 等字段，`name` 与目录名一致。

---

## 如何使用

### 方式一：项目级（推荐试用）

把整个仓库或某个技能目录放进项目，或直接在 `opencode若干前端绘图技能（原始）/` 目录内启动 OpenCode，它会从当前目录向上扫描 `.opencode/skills/*/SKILL.md`。

### 方式二：全局安装

把需要的技能复制到 Agent 的全局 skills 目录（不同工具路径略有差异）：

```bash
# OpenCode
mkdir -p ~/.config/opencode/skills
cp -r ".opencode/skills/"* ~/.config/opencode/skills/

# Claude Code / 兼容 Agent Skills 的工具
mkdir -p ~/.claude/skills
cp -r ".opencode/skills/"* ~/.claude/skills/

# 通用 Agent 目录
mkdir -p ~/.agents/skills
cp -r ".opencode/skills/"* ~/.agents/skills/
```

自研技能同理：

```bash
cp -r algo-implicit-heuristics/skills/algo-implicit-heuristics ~/.agents/skills/
```

### 方式三：直接引用

没有 skills 机制的工具，可以把 `SKILL.md` 的内容并入系统提示词，效果基本一致。

### 权限控制

`opencode若干前端绘图技能（原始）/opencode.json` 已给出按技能前缀放行的示例：

```json
{
  "permission": {
    "skill": {
      "gsap-*": "allow",
      "remotion-*": "allow",
      "hyperframes*": "allow"
    }
  }
}
```

把 `allow` 改成 `ask` 可在加载前询问，`deny` 可完全禁用。

更多安装细节见 [`README-技能安装说明.md`](opencode若干前端绘图技能（原始）/README-技能安装说明.md)。

---

## 维护约定

新增技能时，建议保持以下结构：

```text
<skill-name>/
├── SKILL.md          # 必需：frontmatter + 指令正文
├── references/       # 可选：按需加载的参考资料
├── scripts/          # 可选：可执行辅助脚本
└── assets/           # 可选：模板、字体、示例素材
```

- 目录名使用小写短横线（`^[a-z0-9]+(-[a-z0-9]+)*$`），并与 frontmatter 的 `name` 保持一致
- `description` 写清「什么时候用」和「什么时候不用」，这是 Agent 路由的主要依据
- 收集来的技能请保留原作者信息与许可证，二次修改请在 `NOTICE.md` 或技能 README 中说明
- 提交前可运行格式检查：

```bash
# check_skills.py 依赖 PyYAML
python -m pip install pyyaml
python "opencode若干前端绘图技能（原始）/scripts/check_skills.py"
python algo-implicit-heuristics/skills/algo-implicit-heuristics/scripts/check_lesson.py --help
```

---

## 许可证与致谢

本仓库中 **自研部分** 采用 [MIT License](LICENSE)。

**收集整理部分** 的版权归原作者所有，仓库内保留其原始许可证与署名信息：

- GSAP Skills — © GreenSock，MIT
- Remotion Skills — © Remotion，见各技能声明
- HyperFrames 及创作类技能 — © HeyGen，见各技能声明
- `talking-head-recut` — 改编自 [notedit/vtake-skills](https://github.com/notedit/vtake-skills)，MIT，署名见该技能内 [`NOTICE.md`](opencode若干前端绘图技能（原始）/.opencode/skills/talking-head-recut/NOTICE.md)
- `algo-implicit-heuristics` — 本仓库自研，见其独立 [LICENSE](algo-implicit-heuristics/LICENSE)

如果某份内容的使用侵犯了你的权益，欢迎提 Issue，我会尽快处理。

---

## 说明

- 本仓库主要用于个人学习与工作流沉淀，技能质量与适用性请自行评估。
- 部分技能依赖外部 CLI、API Key 或商业服务（如 HeyGen、Remotion 渲染环境），使用前请阅读对应 `SKILL.md` 的安装说明。
- 欢迎 Star、Fork，或通过 Issue / PR 交流。
