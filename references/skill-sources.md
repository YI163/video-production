# Skill sources and host notes

This skill is designed from **public Agent Skills patterns** and an anonymized production retrospective. It is not tied to a single agent host.

## Format

A skill is a directory with a `SKILL.md` at its root. YAML frontmatter requires `name` and `description`; optional folders (`references/`, `scripts/`, `assets/`) follow progressive disclosure:

1. metadata (`name` + `description`) is always visible to the agent;
2. the `SKILL.md` body loads when the skill is selected;
3. references/scripts load only when needed.

Only portable frontmatter fields are used (`name`, `description`). There are no host-specific keys, tool names, or install hooks in the skill body.

**Validate frontmatter with a real YAML parser.** An unquoted `description` containing `: ` (for example `Triggers include: ...`) is invalid YAML; a provider may drop the whole skill silently. Quote the description or use a block scalar (`>-`). A regex or a visual check is not enough.

## Where to install (host examples)

The only host-specific part is the skills directory. Copy the whole `video-production/` folder into the root your host reads.

| Host | Personal / user root | Project root |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` |
| DeepSeek Harness (DSH) | `~/.agents/skills/` | `<project>/.dsh/skills/` |
| Other Agent Skills host | consult host docs | consult host docs |

- The skill directory must be directly under the root: `<root>/video-production/SKILL.md`.
- Nested `**/SKILL.md` bundles are not discovered by every host; keep the skill at the top level.
- Some hosts auto-select skills from the description; others require you to point the agent at `SKILL.md`. Both are fine; the workflow is plain Markdown.
- Some hosts do not execute `scripts/` automatically. If shell/Python execution is available, run the scripts explicitly; otherwise use the Markdown checklists and recipes.

## Tested behavior

- **DSH:** the skill was loaded and the YAML frontmatter was validated in a real session.
- **Claude Code / other hosts:** the package follows the Agent Skills `SKILL.md` convention, but automatic triggering and script execution were not individually tested here. If your host differs, fall back to “read `SKILL.md` and follow it”.
- The scripts themselves are plain Python/Bash and are not tied to any host.

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
| Progressive disclosure | Anthropic spec | Short `SKILL.md`; details in references |
| “When to use / when not to” | phone-shot-video | Prevents over-triggering on long-form/VFX/audio-only |
| Project setup → review | painterly-short-film | 7-stage workflow + independent gates |
| Small deterministic scripts | Anthropic best practices | `check_video.py`, `contact_sheet.sh` |

## Maintenance

- Keep the body portable: no host-specific tool names or paths; put install paths in this file/README only.
- If a host changes its skill roots/frontmatter, update this file, not the workflow.
- Add a failure mode only when there is a second independent case; one case is evidence, not a law.
- Keep the package small: no media, no session logs, no credentials, no personal paths.
