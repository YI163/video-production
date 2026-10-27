# Quality checklist

Use only the sections relevant to the job; do not skip a section that the brief explicitly cares about.

## 0. Pre-flight

- [ ] Job classified: new / local patch / full redo.
- [ ] If revision: approved frozen (copy + SHA-256), change list written, requested vs unrequested marked.
- [ ] Brief has platform/aspect/duration/language/music/delivery path.
- [ ] Source footage exists, readable, and backed up; originals untouched.
- [ ] Toolchain available: ffmpeg, Python/Pillow, Whisper (if speech), CJK fonts.
- [ ] Disk space for intermediates (roughly 3–5× final size).

## 1. Material audit

- [ ] Duration/resolution/fps/codec/bit depth/color tags recorded for every clip.
- [ ] Log/HLG vs Rec.709 identified; grade plan written.
- [ ] 1s contact sheet + key frames extracted and visually inspected.
- [ ] Usable in/out points (0.5s precision) with reject reasons.
- [ ] Speech clips: timestamped transcript; proper nouns corrected; uncertain words marked.
- [ ] B-roll audio: no ASR hallucination subtitles.
- [ ] Framing/headroom/logo/background/shake/exposure/white balance noted.
- [ ] A-roll vs B-roll vs unusable clearly labeled.
- [ ] Reviewer can reproduce the same frames from the report.

## 2. Script

- [ ] Hook in first 3s (visual + information).
- [ ] 10–16 shots for a 45–60s vlog (adjust to brief; not a law).
- [ ] Every shot: source, source in/out, final in/out, duration, picture, subtitle, packaging, transition, sound.
- [ ] Shot durations sum exactly to target; A-roll audio offset documented and applied.
- [ ] Subtitles use final timecodes; line ≤14 Chinese chars; ≤2 lines; no orphan punctuation.
- [ ] Packaging coordinates/sizes/safe areas specified.
- [ ] Fact cards / end card copy has sources and risk labels.
- [ ] Music/sound plan has levels, fade in/out, licensing.
- [ ] Script review passed; C-2-style timecode errors caught before edit.

## 3. Build — picture

- [ ] All shots rendered at 1080×1920, 30fps, SAR 1:1.
- [ ] A-roll treatment tested: card or full-bleed; no unintended crop of head/logo/hands.
- [ ] No stretching; no black bars unless intentional.
- [ ] Grade: face/white wall/brand color/sky compared across shots; no gray/uncolored section.
- [ ] 10-bit log footage: test `colorlevels` after `format=yuv420p` (ffmpeg 8 can output black on 10-bit).
- [ ] Transitions: hard cuts dominate; dissolves 0.2–0.4s and frame-quantized.
- [ ] No repeated B-roll that reads as a continuity error.
- [ ] Fact-card backgrounds do not fight the panel text (test full opacity/darkening).
- [ ] Fact-card panel does not cut a person at the neck/chest in a distracting way.
- [ ] Approved card layout was not silently replaced by a full-bleed crop; if changed, user asked or the new source genuinely cannot support it, and the change was re-reviewed.
- [ ] Consecutive fact-card backgrounds use distinct source ranges; no 1s+ overlap or near-identical pans; moving backgrounds are slowed/frozen behind text.
- [ ] Every bridge between the last fact card and the end card has a title, voice, location line, or narrative beat; no unexplained 2–3s silent/textless gap.

## 4. Build — subtitles

- [ ] Burned-in and external SRT match cue-by-cue.
- [ ] Text is verbatim or intentionally adapted; no ASR proper-noun errors.
- [ ] Line breaks respect meaning; no word split; ≤14 chars/line.
- [ ] Font 54–60px, white + dark stroke/shadow, readable on light/dark.
- [ ] Bottom margin ≥200px (≥240px safer); not under platform UI.
- [ ] No subtitle over a face/logo/counter/fact-card text.
- [ ] Special claims (“top 3”, rankings) are treated as speaker opinion, not official fact.

## 5. Build — audio

- [ ] Voice clean: high-pass, denoise, compression, no clipping.
- [ ] BGM below voice (12–18dB), ducking or level automation, fade in 1–3s, fade out 2–3s.
- [ ] Ambient B-roll audio muted or ≤−35dB.
- [ ] Overall −16 LUFS ±2; true peak ≤−1dBTP (measure with ebur128/loudnorm, not guess).
- [ ] No click at cut points; voice tail not chopped.
- [ ] Music license/credit recorded (CC BY attribution even if removed from end card).

## 6. Technical QC

- [ ] `check_video.py` exit 0 / failures [].
- [ ] Duration, resolution, fps, frame count match the script.
- [ ] H.264 + AAC, faststart, plays in QuickTime/mobile.
- [ ] 0 black frames (except intentional design); no frozen frames beyond a designed still.
- [ ] A/V duration drift < 50ms.
- [ ] Decode full file with `-f null -` and no errors.
- [ ] SRT UTF-8, 13/13 or full coverage, no BOM issues.

## 7. Visual / editorial review (independent)

- [ ] Full-film 1s contact sheet reviewed.
- [ ] Frame samples at hook / every B-roll / every card / end card.
- [ ] Hook works without sound.
- [ ] Pacing: a visual or informational change every 2–4s; no long dead segment.
- [ ] B-roll matches the spoken content; no mismatched banner/logo.
- [ ] Titles/fact cards/end card hierarchy is readable; no clutter.
- [ ] Color consistency; skin tones natural; no over-saturation.
- [ ] Composition: no accidental crop, no person cut by panel, no logo obscured.
- [ ] Facts: names/numbers/dates/claims checked; sources recorded.
- [ ] Verdict pass/needs_revision with timecoded findings; no self-approval.

## 8. Revision-specific

- [ ] Golden checksum matches before/after.
- [ ] Requested changes only; unrequested parts compared and unchanged.
- [ ] Unchanged shots verified by PSNR/SSIM or frame hash.
- [ ] Subtitles/SRT re-checked after any timing change.
- [ ] Loudness/TP re-checked after any audio change.
- [ ] A/B sheet produced for the user/reviewer.
- [ ] If full redo: new brief/script/review, not a patch.
- [ ] Rollback works; approved not overwritten.

## 9. Delivery

- [ ] Final MP4 + SRT + cover + delivery note + checksums.
- [ ] Delivery note: specs, files, sources, structure, subtitles, music/CC BY, facts, limitations, review verdicts.
- [ ] File names/paths match the user request.
- [ ] Desktop copy permission handled; original project untouched.
- [ ] Golden/master read-only and recoverable.
