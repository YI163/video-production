# video-production

A reusable **Agent Skill** for producing short-form vertical video: material audit, shot script, visual packaging, subtitles, audio, independent review, technical QC, delivery, and version-safe revisions.

This is an **anonymized public package**. It contains no footage, no people, no institution names, no session logs, no team records, and no personal filesystem paths. The included case study is a process note, not a shot-for-shot template.

## What is inside

```text
.
├── SKILL.md                    # trigger, workflow, failure modes, quality bar
├── references/
│   ├── case-study.md           # anonymized: what worked, what regressed
│   ├── workflow.md             # full 7-stage workflow
│   ├── modification-protection.md
│   ├── quality-checklist.md
│   ├── tech-recipes.md
│   └── skill-sources.md
├── scripts/
│   ├── check_video.py          # technical checker (no third-party deps)
│   └── contact_sheet.sh        # quick 1s contact sheet
├── LICENSE                     # MIT for scripts
├── LICENSE-DOCS                # CC BY 4.0 for documentation/methodology
└── README.md
```

## Install

The skill is a directory with a `SKILL.md` at its root. Copy it into a skill root used by your agent host.

For a DeepSeek Harness user install:

```bash
git clone <this-repo> video-production
mkdir -p ~/.agents/skills/video-production
rsync -a --exclude .git video-production/ ~/.agents/skills/video-production/
```

For a project-local install (higher priority in DSH):

```bash
mkdir -p <project>/.dsh/skills/video-production
rsync -a --exclude .git video-production/ <project>/.dsh/skills/video-production/
```

The DSH `skill-filesystem` provider watches its roots, so a valid skill should appear without restarting. If it does not, validate the YAML frontmatter with a real parser (see below).

## Use

Ask naturally; the description triggers on tasks such as:

- “剪一个 45–60 秒的竖屏 vlog，配中文字幕”
- “把这些素材剪成能发的短视频，先做脚本”
- “给视频加标题、事实卡、片尾卡”
- “把这段 Log 素材调色，并检查字幕/响度”
- “修改已批准的版本，但不要破坏原来的整体感”

The skill starts by classifying the job: **new production / local patch / full redo**. If the user says “replace all footage”, that is a new production, not a patch.

## Requirements

- `ffmpeg` (the recipes assume ffmpeg 8; most commands work on 6+).
- Python 3 for `scripts/check_video.py`; no third-party packages.
- Pillow only if you use the overlay/subtitle recipes.
- Whisper (optional) for transcripts.
- CJK fonts for Chinese subtitles (e.g. Hiragino Sans GB, Noto Sans CJK, Source Han Sans).

## Design principles

1. Write a production constitution before editing.
2. Audit material with timestamps and frames, not impressions.
3. Turn the script into an executable shot table.
4. Choose the visual system from the source (card vs full-bleed vs hybrid); do not change an approved system unless asked.
5. Keep material, script, and final review independent.
6. Measure technical specs; a checker is necessary, not sufficient.
7. Version and hash the delivery; never overwrite the only approved version.

The full workflow and checklists are in `references/`; the skill body stays short and loads details on demand.

## Validation

- `SKILL.md` frontmatter parses with a real YAML parser (the `description` is quoted; an unquoted `: ` can silently drop the skill).
- `scripts/check_video.py` was run against a real 1080×1920 30 fps export; it returned `decode_ok: true` and no failures.
- `scripts/contact_sheet.sh` generated a 1s contact sheet from the same export.
- No production media or session logs are included, so the case study cannot be re-cut from this repository alone.

## Privacy / anonymization

- No source clips, no golden video, no faces, no voices, no school/company names, no locations, no dates, no session/team logs, no personal paths.
- The case study describes **what** happened and **why**, not **who/where**.
- If you adapt this for a real client, get consent before publishing footage or identifiable stills.

## License

- **Code** (`scripts/`): MIT — see `LICENSE`.
- **Documentation, methodology, and `SKILL.md`**: CC BY 4.0 — see `LICENSE-DOCS`.

Attribution for the docs: “video-production skill package” with a link to this repository.
