---
name: video-production
description: "Plan, edit, grade, subtitle, and quality-check short-form vertical video (vlog, campus/travel, interview, brand story). Use when the user asks to turn raw clips into a 45–90s vertical vlog, add burned-in Chinese subtitles, build title/fact/end cards, grade flat/Log footage, deliver a finished MP4, or revise an already-approved cut without regressing it. Triggers include: 剪 vlog, 竖屏视频, 加字幕, 出成片, 换素材, 调色, 修改视频, 视频复盘, 已批准版本, 保留原版. Do NOT use for long-form film/TV finishing, pure audio editing, 3D animation, or when the user only wants a text plan."
---

# Video Production

## What this skill is for

Turn raw footage into a **finished short vertical video** that someone would actually post: a hook, a clear story, readable burned-in subtitles, intentional packaging, clean audio, and a verified delivery package. It also protects an already-approved cut when the user asks for changes.

The goal is not to copy one successful video's shots or filters. The goal is to reuse the **conditions** that made it good:

1. a written production constitution before editing;
2. timestamped material evidence, not vibes;
3. an executable shot script;
4. a deliberate visual system (layout, typography, safe areas);
5. independent review at the material / script / final gates;
6. objective technical QC;
7. versioned, checksummed delivery.

## When to use

- The user supplies clips and asks for a vlog / short vertical video / campus or travel piece.
- The user asks for burned-in subtitles, titles, fact cards, an end card, or a cover.
- The user asks to grade flat/Log footage or match shots.
- The user asks to revise an approved video: change subtitles, music, opening, packaging, a few shots, or replace footage.
- The user asks why a previous cut was good/bad and wants a reusable process.

## When not to use

- The user only wants a written concept, script, or shot list — no edit.
- Long-form film/TV finishing, color-grading a feature, or complex VFX/3D.
- Pure audio/podcast editing.
- The request is a tiny text-only answer that needs no media inspection.

---

## Step 0 — Classify the job (do this first)

| Class | Signals | Process |
|---|---|---|
| **New production** | new topic, new clips, new deliverable | full workflow |
| **Local patch** | only subtitles, title, a few overlays, one B-roll, volume, music fade | minimal diff + A/B + re-review |
| **Full redo** | replace all/most footage, change layout/aspect/visual system, change grade pipeline, rewrite story | treat as new production; **do not** patch the old timeline |

**Hard rule:** "replace all footage" or "redo it with these new clips" is a **new production**, even if the user calls it a small fix. The old script's source timecodes, framing, subtitles, and B-roll logic no longer hold.

If it is a revision: before touching anything, freeze the approved version (copy + SHA-256). See `references/modification-protection.md`.

---

## Step 1 — Intake and production constitution

Capture only what affects delivery:

- platform / aspect / target duration / language;
- footage paths, Log vs Rec.709, frame rate, audio;
- whether there is a talking-head track, and who speaks;
- music/licensing (CC0/CC BY/user-provided);
- delivery folder/name/overwrite policy;
- what must NOT change.

Write a short `00-production-spec.md` (or reuse the project's existing one) with:

- specs and red lines;
- factual baseline (what may appear on screen; what is only a speaker's opinion);
- visual grammar: card vs full-bleed, title, subtitles, fact cards, end card, safe areas;
- sound plan;
- review gates.

**Do not skip this because the job looks small.** The spec is what lets a reviewer say "this violates the agreed system" instead of arguing taste.

---

## Step 2 — Material audit (evidence, not impressions)

For every clip record:

- duration / resolution / fps / codec / bit depth / color tags;
- content and action by timestamp;
- usable in/out points (0.5s precision) and reject reasons;
- framing, headroom, logo/background, shake, exposure, white balance;
- audio: speech vs ambience; if speech, a timestamped transcript;
- Log/HLG or Rec.709; if flat, plan the grade.

Use 1s contact sheets + key frames; use Whisper for a first transcript, then correct proper nouns with context. **Do not subtitle B-roll ambience that Whisper hallucinated.**

Output: a material report with frames and timecodes, not just prose. A reviewer must be able to re-extract the same frames.

---

## Step 3 — Visual system and shot script

### 3.1 Choose the A-roll treatment from the source

- **Card layout** for low-res landscape (e.g. 960×720) or when the environment/logo matters: a 4:3/16:9 card on a designed 1080×1920 canvas; avoids 2.67× upscale.
- **Full-bleed** for native vertical or 4K landscape with enough headroom: test the crop before committing.
- **Hybrid** when both face and context matter.

Do not change an already-approved layout unless the user asks or the new source genuinely cannot support it. If you do change it, treat it as a design change and re-review.

### 3.2 Write a shot table, not a mood board

Every shot needs: source, source in/out, final in/out, duration, picture treatment, subtitle, packaging, transition, sound. Sum the durations; align the voice track by a fixed offset; use final-timecode subtitles.

Include:

- a hook in the first 3s;
- a visual/information change every 2–4s;
- B-roll that covers weak A-roll sections;
- fact cards / end card copy with sources and risk labels;
- a music/sound plan.

Review the script before editing. A wrong source timecode is cheap to fix here, expensive later.

---

## Step 4 — Build

- Render each shot separately; concatenate/xfade in a second pass. Avoid one giant filter graph.
- Grade Log footage with a LUT or a tested manual chain; compare face / white wall / brand color across shots.
- Generate overlays (title, fact cards, end card, subtitles) as full-canvas RGBA PNGs with Pillow; test them on real frames.
- Keep subtitles in the bottom safe area (bottom margin ≥200px; 240px is safer), ≤14 Chinese characters per line, ≤2 lines.
- Mix voice first, then BGM under it (12–18dB below voice), fade in/out 1–3s, loudnorm to about −16 LUFS, true peak ≤ −1dBTP.
- Keep all scripts, overlays, audio, and intermediate shots versioned.

Useful checks and recipes: `references/tech-recipes.md`.

---

## Step 5 — Review gates (do not self-approve)

Three independent gates:

1. **Material gate** — does the research match the frames/audio? Are usable ranges real? Are ASR errors corrected? Are B/C/D unbilled ambience left alone?
2. **Script gate** — can it be edited exactly as written? Do source in/out points exist? Do subtitles match the transcript and fit? Is the total duration exact? Is the hook real?
3. **Final gate** — full-film frame sampling + SRT read + audio check + factual check. Technical QC (resolution, fps, duration, loudness, true peak, black frames, decode, burn-in) is separate and cannot replace the visual/subtitle review.

Each finding needs: timecode, symptom, fix, severity (blocker/high/medium/low). A pass requires no blocker/high; medium should be fixed or explicitly accepted; low can ship with a note.

If a review fails, repair and re-review the affected area. Do not deliver on "the checker passes".

---

## Step 6 — Deliver

- Final MP4: 1080×1920, 30fps, H.264 High, AAC 48k stereo, faststart.
- SRT with the same cues as the burn-in; cover 1080×1920.
- `交付说明.md`: specs, files, sources, structure, subtitles, music/CC BY, factual sources, known limitations, review verdicts.
- SHA-256/MD5 manifest; keep the approved version/master read-only.
- Confirm QuickTime/mobile playback.

---

## Step 7 — Revisions

Follow `references/modification-protection.md`. The short version:

1. freeze the approved version;
2. list exactly what the user asked to change;
3. treat everything else as "must preserve";
4. use the smallest patch that works;
5. if re-generation is unavoidable, declare the risk and re-run the full review;
6. A/B compare old vs new at the same semantic beats;
7. never overwrite the only good version;
8. if the new version fails, roll back and keep the old one.

---

## Quality bar (defaults; adjust to the brief)

| Item | Default |
|---|---|
| Canvas / fps | 1080×1920 / 30fps |
| Duration | 45–60s for a vlog; 15–30s for a hook-led short |
| Video | H.264 High, yuv420p, CRF ~18, faststart |
| Audio | AAC 48k stereo, ~192kbps |
| Loudness | −16 LUFS ±2, true peak ≤ −1dBTP |
| Black frames | none except intentional design |
| Subtitles | burned-in + SRT; bottom margin ≥200px; ≤14 chars/line |
| Music | voice-first; BGM 12–18dB under voice; fade in/out |
| Delivery | MP4 + SRT + cover + delivery note + checksums |

These are defaults, not laws. If the platform or brief requires something else, write it in the spec.

---

## Common failure modes (from a real revision)

- **Do not change an approved visual system unless asked.** An approved cut used a 4:3 card for low-res landscape; a later revision replaced it with a full-bleed 4K crop, and the reviewer complained that the landscape footage had simply been cropped. If the source is landscape and the approved look was a card, keep the card unless the user asks for a redesign; if changing, test headroom/logo/hands and review.
- **Fact-card backgrounds must be distinct and calm.** Do not reuse overlapping source ranges or two near-identical pans behind consecutive cards; slow/freeze the background if the camera moves. A moving, duplicated background reads as “two almost identical shots” and “the camera sweeps too fast”.
- **Every bridge segment needs a function.** A 2–3s shot between the last fact card and the end card must carry a title, a voice, a location line, or a narrative beat. A silent, textless banner reads as an unexplained gap; shorten it or give it a role.
- **A full footage replacement is a new production.** Do not patch the old timeline; re-audit material, re-script, re-grade, and re-review. “Small fix” language does not change the scope.
- **Technical pass is not an aesthetic pass.** A checker can prove 1080×1920/0 black frames/decode OK; it cannot prove the cut looks good. For revisions, A/B against the approved cut and get an independent verdict.

## Creative latitude

Standardize the **verification**; leave the **creative** open:

- concept, hook, narrative order;
- card vs full-bleed vs hybrid;
- shot count, B-roll order, transitions;
- grade look (natural / warm / filmic);
- music genre, title voice, fact-card visual.

Do not turn one approved cut into a template. The reusable asset is the process and the review discipline, not the exact fonts, shots, or music.

---

## References

- `references/case-study.md` — an anonymized case study: what worked, what regressed, and why.
- `references/workflow.md` — full 7-stage workflow with artifacts and gates.
- `references/modification-protection.md` — versioning, minimal diff, A/B, rollback.
- `references/quality-checklist.md` — pre-flight, technical, visual, subtitle, audio, delivery checklists.
- `references/tech-recipes.md` — ffmpeg/Pillow/Whisper/loudness recipes and known pitfalls.
- `references/skill-sources.md` — public Agent Skills and video-skill examples this skill learned from (Anthropic Agent Skills, muse-creative-skills, refay-skills) plus DSH discovery notes.
- `scripts/check_video.py` — reusable technical checker.
- `scripts/contact_sheet.sh` — quick 1s contact sheet.

## Quick start

```bash
# discover tools
FF=$(command -v ffmpeg || echo tools/ffmpeg)
$FF -hide_banner -i clip.mp4 2>&1 | grep -E 'Duration|Stream'

# 1s contact sheet (5 columns)
$FF -hide_banner -loglevel error -i clip.mp4 \
  -vf "fps=1,scale=320:-1,tile=5x6:padding=4:margin=4" \
  -frames:v 1 contact.jpg

# technical check after export
python3 scripts/check_video.py final.mp4 --width 1080 --height 1920 \
  --min-duration 45 --max-duration 60 --lufs -16 --lufs-tol 2 \
  --max-true-peak -1.0 --max-black 0.5
```

If the user has an approved version, **stop and read `references/modification-protection.md` before running anything that writes to the deliverable.**
