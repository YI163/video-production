# Case study: a 45–60s vertical vlog (anonymized)

> This is an anonymized process note, not a shot-for-shot template. The production's footage, people, institution, dates, session logs, and checksums are deliberately not included. No media files are distributed with this skill.

## What was made

A real short vertical vlog, roughly 45–60 seconds, built from a handful of talking-head and B-roll clips. It used burned-in Chinese subtitles, a designed 9:16 canvas, a title, a few fact cards, and an end card. The client approved it before a later revision was requested.

The exact runtime, source names, locations, and file hashes are omitted; they are not needed to reuse the method.

## What made the approved version work

1. **A written production constitution before editing.** Specs, source map, factual baseline, subtitle/safe-area rules, sound targets, red lines. Every collaborator read the same file.
2. **Evidence-based material audit.** Each clip had duration/resolution/fps/codec/color tags, usable in/out points at 0.5s precision, reject reasons, key frames, and a timestamped transcript. The first review still found real range/framing/ASR errors; repair and re-review fixed them.
3. **An executable shot script.** Every shot had source in/out, final in/out, duration, picture treatment, subtitle, packaging, transition, and sound. The durations summed exactly; the voice track was aligned by a fixed offset. The script review found a source-timecode error and pacing/subtitle issues before editing.
4. **A deliberate visual system.** The A-roll used a card layout because the source was low-resolution landscape; a full-bleed crop would have lost too much horizontal context and over-enlarged the image. Titles, subtitles, fact cards, and safe areas were measured, not eyeballed.
5. **Independent gates.** Material, script, and final review were separate from the person doing the edit. Reviewers extracted their own frames and read the SRT. A final pass still found packaging defects; the edit was repaired and re-reviewed.
6. **Technical QC.** Resolution, fps, duration, loudness, true peak, black frames, decode, subtitle burn-in, and safe areas were measured with a checker and sampled frames. A passing checker was necessary, not sufficient.
7. **Delivery discipline.** The final file was stream-copied from the approved master, hashed, and delivered with SRT, cover, a delivery note, and known limitations.

## What went wrong in a later revision

The user asked for a small set of changes, one of which was “replace all footage and grade the new flat footage.” That is a **new production**, not a local patch. The revision:

- changed the approved card layout to a tight full-bleed crop without being asked;
- replaced camera-graded footage with manually graded log footage, without a LUT, reference frame, or independent color check;
- reused overlapping/near-identical B-roll behind consecutive fact cards;
- kept a 2–3 second bridge with no voice, title, or location line, so it read as an unexplained gap;
- dropped shot variety and transitions;
- had no formal independent final review (the reviewer run was stopped);
- was delivered after a technical self-check, not an A/B against the approved cut.

Both versions passed the technical specs. The quality drop was perceptual/structural, not a codec/loudness failure.

## Reusable lessons

- **Study 3–5 high-quality reference vlogs before locking the visual system.** Extract hook/structure/packaging/sound principles; do not copy shots, faces, music, or assets.

- **Classify the job first:** new production / local patch / full redo. “Replace all footage” is a new production.
- **Protect the approved version** before touching anything: copy, hash, read-only, versioned.
- **Do not change an approved visual system** unless the user asks or the new source genuinely cannot support it. If you change it, test headroom/logo/hands and re-review.
- **Fact-card backgrounds must be distinct and calm.** Avoid overlapping source ranges and near-identical pans; slow/freeze a moving background behind text.
- **Every bridge needs a function:** title, voice, location, or narrative beat. A silent, textless banner is a gap.
- **A full footage replacement requires** a new material audit, script, grade, and review; do not patch the old timeline.
- **Technical pass is not an aesthetic pass.** For revisions, compare old and new at the same semantic beats and get an independent verdict.
- **A checker plus a delivery note is not a substitute for judgment.** The most valuable gate is an independent reviewer with evidence.

## What is creative, not mandatory

The hook, card vs full-bleed, shot count, B-roll order, transitions, grade look, music, title voice, and fact-card visual are creative choices. A different source or platform may justify a different answer. Reuse the **verification and protection** parts; leave room for the creative parts.

## Provenance

This note is a retrospective summary written for this skill. The original production media, session logs, team records, and exact checksums are intentionally withheld. No person or institution is identified.
