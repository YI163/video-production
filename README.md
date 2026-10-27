# video-production

一个可复用的 **Agent Skill**，用于制作 45–90 秒竖屏短视频：素材审计、分镜脚本、视觉包装、字幕、声音、独立审核、技术质检、交付，以及不破坏已批准版本的修改流程。

这是一个**匿名化公开包**：不含成片、源素材、人物、机构名、会话日志、团队记录和本机路径。案例研究是方法复盘，不是逐镜模板。

## 仓库内容

```text
.
├── SKILL.md                    # 触发条件、工作流、失败模式、质量标准
├── references/
│   ├── case-study.md           # 匿名案例：什么做对了、什么退化了
│   ├── workflow.md             # 完整 7 阶段 Workflow
│   ├── modification-protection.md
│   ├── quality-checklist.md
│   ├── tech-recipes.md
│   └── skill-sources.md
├── scripts/
│   ├── check_video.py          # 技术检查器（无第三方依赖）
│   └── contact_sheet.sh        # 1 秒接触表
├── LICENSE                     # MIT（scripts/）
├── LICENSE-DOCS                # CC BY 4.0（文档/方法论）
└── README.md
```

## 安装

Skill 是一个目录，根目录必须有 `SKILL.md`。把本仓库复制到你的 Agent host 使用的 skill 根目录即可。

### DeepSeek Harness 用户级

```bash
git clone https://github.com/YI163/video-production.git
mkdir -p ~/.agents/skills/video-production
rsync -a --exclude .git video-production/ ~/.agents/skills/video-production/
```

### 项目级（DSH 优先级更高）

```bash
git clone https://github.com/YI163/video-production.git
mkdir -p <project>/.dsh/skills/video-production
rsync -a --exclude .git video-production/ <project>/.dsh/skills/video-production/
```

DSH 的 `skill-filesystem` 会监视技能根目录，正常情况下不需要重启。若 Skill 不出现，先用真正的 YAML 解析器检查 frontmatter（见下方“验证”），不要只靠肉眼看。

## 使用

直接用自然语言提出任务即可，例如：

- “剪一个 45–60 秒的竖屏 vlog，配中文字幕。”
- “把这些素材剪成能发的短视频，先做脚本。”
- “给视频加标题、事实卡、片尾卡。”
- “把这段 Log 素材调色，并检查字幕和响度。”
- “修改已批准的版本，但不要破坏原来的整体感。”

Skill 会先判断任务类型：**新制作 / 局部修改 / 全量重做**。如果用户说“把所有素材都换掉”，那是新制作，不是局部修改。

## 依赖

- `ffmpeg`（示例按 ffmpeg 8 写，多数命令 ffmpeg 6+ 可用）。
- Python 3（运行 `scripts/check_video.py`，无第三方包）。
- Pillow（仅当使用包装/字幕生成配方时需要）。
- Whisper（可选，用于逐字稿）。
- 中文字体（如 Hiragino Sans GB、Noto Sans CJK、思源黑体）。

## 设计原则

1. 动手剪辑前，先写“制作宪法”。
2. 素材审计要有时间码和抽帧证据，不靠印象。
3. 脚本必须能直接施工：逐镜源入出、成片时间码、字幕、包装、声音。
4. 视觉系统由素材条件决定（卡片 / 满屏 / 混合）；未经要求不改已批准的系统。
5. 素材、脚本、终审三个 gate 尽量独立。
6. 技术指标要测；检查器通过是必要条件，不是充分条件。
7. 交付要版本化、哈希化；绝不覆盖唯一的已批准版本。

完整流程和检查清单在 `references/`，`SKILL.md` 只保留短正文，细节按需加载。

## 验证

- `SKILL.md` frontmatter 用真正的 YAML 解析器验证通过；`description` 已加引号，避免未转义的 `: ` 让整个 Skill 被静默丢弃。
- `scripts/check_video.py` 在真实 1080×1920 / 30fps 成片上运行通过，返回 `decode_ok: true` 且无 failures。
- `scripts/contact_sheet.sh` 能从同一成片生成 1 秒接触表。
- 公开包不含成片或会话日志，因此不能只靠本仓库复刻原片；案例只保留方法。

## 隐私与匿名

- 不含源素材、成片、人脸、声音、学校/公司名、地点、日期、会话/团队日志、个人路径。
- 案例研究只讲“发生了什么、为什么”，不指认“谁、在哪里”。
- 如果你把它用于真实客户项目，发布素材或可识别人像前必须先取得授权。

## License

- **代码**（`scripts/`）：MIT，见 `LICENSE`。
- **文档、方法论、`SKILL.md`**：CC BY 4.0，见 `LICENSE-DOCS`。

文档署名建议：“video-production skill package”，并附上本仓库链接。
