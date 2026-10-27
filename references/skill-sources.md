# Skill sources and format notes

This skill was designed from **public Agent Skills patterns** and an anonymized production retrospective. It was not copied from a personal or local skill template.

## Format

A skill is a directory with a `SKILL.md` at its root. YAML frontmatter requires `name` and `description`; optional folders (`references/`, `scripts/`, `assets/`) follow progressive disclosure:

1. metadata (`name` + `description`) is always visible to the agent;
2. the `SKILL.md` body loads when the skill is selected;
3. references/scripts load only when needed.

**Validate frontmatter with a real YAML parser.** An unquoted `description` containing `: ` (for example `Triggers include: ...`) is invalid YAML; a provider may drop the whole skill silently. Quote the description or use a block scalar (`>-`). A regex or a visual check is not enough.

## DSH filesystem provider (one supported host)

The DeepSeek Harness `skill-filesystem` provider scans, in priority order:

| Rank | Source | Path |
|---|---|---|
| 100 | project `.dsh` | `<projectRoot>/.dsh/skills` |
| 200 | project `.agents` | `<projectRoot>/.agents/skills` |
| 300 | custom | `Config.customSkillDirs` |
| 400 | user DSH | `<dshHome>/skills` |
| 500 | user agents | `<agentsHome>/skills` |

- A skill can be a directory bundle `<name>/SKILL.md` or a flat `<name>.md`; nested `**/SKILL.md` files are not discovered.
- The provider watches the roots, so a fixed skill can appear without an app restart. A malformed skill stays absent until its frontmatter is valid.
- For a project install: copy this directory to `<project>/.dsh/skills/video-production/`. For a user install: copy it to `~/.agents/skills/video-production/`.
- The current case validated loading from a project `.dsh/skills` root; the global copy is a fallback.

## Public Agent Skills references

1. **Anthropic Agent Skills** — https://github.com/anthropics/skills
   - Template: https://github.com/anthropics/skills/blob/main/template/SKILL.md
   - Spec: https://github.com/anthropics/skills/blob/main/spec/agent-skills-spec.md
2. **Anthropic best practices** — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
   - Description quality drives triggering; keep `SKILL.md` concise; push details into references.
3. **Community best-practices compilation** — https://github.com/Dicklesworthstone/meta_skill/blob/main/BEST_PRACTICES_FOR_WRITING_AND_USING_SKILLS_MD_FILES.md
   - Name rules (`[a-z0-9-]`, ≤64 chars), description ≤1024 chars, body <500 lines; scripts for deterministic operations.

## Public video/creative skill examples

1. **muse-creative-skills** — https://github.com/nanbada/muse-creative-skills
   - `video/phone-shot-video/SKILL.md`: purpose → when to use → workflow → QC; concise and trigger-rich.
   - `video/youtube-shorts-growth/SKILL.md`: shorts-specific beats and growth patterns.
2. **refay-skills** — https://github.com/drkhaledalrefay-coder/refay-skills
   - `cinematic/painterly-short-film/SKILL.md`: project setup → assets/identity → scene prompts → continuity → review.

## Design choices borrowed

| Pattern | Source | Use here |
|---|---|---|
| Trigger-rich description | Anthropic best practices | Chinese + English trigger words; explicit “when not to use” |
| Progressive disclosure | Anthropic spec | Short `SKILL.md`; detailed workflow/checklist/tech recipes in references |
| “When to use / when not to” | phone-shot-video | Prevents over-triggering on long-form/VFX/audio-only |
| Project setup → review | painterly-short-film | 7-stage workflow + independent gates |
| Small deterministic scripts | Anthropic best practices | `check_video.py`, `contact_sheet.sh` |

## Maintenance

- If the host changes skill roots/frontmatter, update this file and `SKILL.md` first.
- Add a failure mode only when there is a second independent case; one case is evidence, not a law.
- Keep the package small: no media, no session logs, no credentials, no personal paths.
