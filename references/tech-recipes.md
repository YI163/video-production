# Tech recipes and pitfalls

These are the commands that worked in a real production (ffmpeg 8.0, macOS arm64). Paths are examples; discover tools first.

## Tool discovery

```bash
FF="${FFMPEG:-$(command -v ffmpeg || echo tools/ffmpeg)}"
PY="${PYTHON:-python3}"
$FF -hide_banner -version | head -3
$FF -hide_banner -encoders 2>/dev/null | grep -E 'libx264|aac'
```

There may be **no ffprobe** in a static ffmpeg build. Read metadata with `ffmpeg -i` and parse stderr:

```bash
$FF -hide_banner -i clip.mp4 2>&1 | grep -E 'Duration|Stream|color|transfer|primaries'
```

## Contact sheets and key frames

```bash
# 1s sheet, 5 columns
$FF -hide_banner -loglevel error -i clip.mp4 \
  -vf "fps=1,scale=320:-1,tile=5x6:padding=4:margin=4" \
  -frames:v 1 contact.jpg -y

# a frame at t seconds (fast seek before -i)
$FF -hide_banner -loglevel error -ss 8.0 -i clip.mp4 -frames:v 1 f8.jpg -y
```

For 4K HEVC, `-ss` before `-i` is fast; if the first frame looks black/odd, seek with `-ss` after `-i` (slower, accurate).

## Whisper transcript

```bash
# 16k mono
$FF -hide_banner -loglevel error -i clip.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav -y

# whisper.cpp (example)
tools/asr/whisper.cpp-1.5.4/main -m tools/asr/ggml-base.bin \
  -f audio.wav -l zh -t 8 -bs 5 -bo 5 -ml 12 -osrt -otxt -ojf -of transcript
```

- `-ml 12` splits long lines; timestamps can be coarse.
- For better proper nouns/word timing, cross-check with a stronger model if available; otherwise correct with context.
- Do **not** subtitle low-level B-roll noise: Whisper hallucinates repeated phrases.

## A-roll: card vs full-bleed

### Card (low-res landscape)

```bash
# 960x720 -> 1080x810 card on a blurred 1080x1920 background
$FF -hide_banner -loglevel error -i 4x3.mp4 -filter_complex "
[0:v]split=2[bg][fg];
[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
     gblur=sigma=30,colorlevels=rimax=0.70:gimax=0.70:bimax=0.70[b];
[fg]scale=1080:810:flags=lanczos,format=yuv420p,eq=contrast=1.03:saturation=1.04[fgc];
[b][fgc]overlay=(W-w)/2:555[out]" -map "[out]" ...
```

Use `format=yuv420p` before `colorlevels`/`eq` if the source is 10-bit; see pitfall below.

### Full-bleed crop (4K landscape -> 9:16)

```bash
# 3840x2160: keep 1215x2160 window around the subject, then scale to 1080x1920
$FF -hide_banner -loglevel error -ss 6.0 -t 4.0 -i 4k.mp4 \
  -vf "fps=30,crop=1215:2160:1300:0,scale=1080:1920:flags=lanczos,format=yuv420p,..." \
  -an -c:v libx264 -preset veryfast -crf 14 -r 30 -frames:v 120 shot.mp4 -y
```

**Test the crop at the first/middle/last second**: headroom, hands, logo, suitcase. Do not assume the center crop is right.

## Pitfall: 10-bit + colorlevels = black

On this machine, ffmpeg 8 with 10-bit HEVC and `colorlevels=...` produced **black frames**. Fix:

```bash
-vf "fps=30,scale=1080:1920,format=yuv420p,colorlevels=rimin=0.07:...:bimax=0.93,eq=...,unsharp=lx=5:ly=5:la=0.35"
```

Convert to 8-bit **before** the grade; keep the source 10-bit for the rest if possible. Always extract a frame after the first render to verify it isn't black.

## Manual D-Log M-ish grade (no LUT)

Example that worked as a starting point (tune per shot):

```bash
colorlevels=rimin=0.07:gimin=0.07:bimin=0.07:rimax=0.93:gimax=0.93:bimax=0.93,
eq=contrast=1.12:saturation=1.30:gamma=0.96,
vibrance=intensity=0.15,
colorbalance=rs=0.015:gs=0.0:bs=-0.01,
unsharp=lx=5:ly=5:la=0.35
```

Compare a face, a white wall, a brand color, and sky before/after. If a LUT is available, prefer it; if not, keep the grade conservative and consistent.

## Overlay PNGs with ffmpeg

```bash
$FF -hide_banner -loglevel error -y -i base.mp4 \
  -loop 1 -i overlay.png \
  -filter_complex "[0:v][1:v]overlay=0:0:enable='between(t,1.0,3.8)'[v]" \
  -map "[v]" -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p -r 30 -t 49.0 out.mp4
```

- Full-canvas 1080×1920 RGBA PNGs with Pillow are easier to control than libass.
- Subtitles strip 1080×130, overlay at `y=1480`; text glyph top ~1494.
- Fact-card panels: alpha 245–250; test that background text doesn't bleed through.
- Multiple overlays: chain `overlay` with `enable='between(t,a,b)'`; avoid one giant command if debugging.

## Concat and xfade

```bash
# hard-cut concat
printf "file '%s'\n" "$PWD"/shots/s*.mp4 > list.txt
$FF -hide_banner -loglevel error -y -f concat -safe 0 -i list.txt -c copy base.mp4

# xfade example (frame-quantized)
$FF -hide_banner -loglevel error -y -i a.mp4 -i b.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.267:offset=29.767[v]" \
  -map "[v]" ...
```

For 30fps, quantize dissolve durations to integer frames (8/6/8/12 frames = 0.267/0.200/0.267/0.400s). Asymmetric overlaps cause timestamp drift.

## Subtitle PNG with Pillow

```python
from PIL import Image, ImageDraw, ImageFont
W,H = 1080,1920
f = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 54, index=2)
strip = Image.new("RGBA",(W,130),(0,0,0,0))
d = ImageDraw.Draw(strip)
text = "这是一段示例字幕，"
tw = f.getlength(text)
d.text(((W-tw)/2, 14), text, font=f, fill=(255,255,255,255),
       stroke_width=7, stroke_fill=(0,0,0,255))
strip.save("sub_02.png")
```

`Hiragino Sans GB.ttc` index 2 = W6; `STHeiti Medium.ttc` index 1 = Heiti SC. Test CJK rendering early.

## Audio: voice + BGM + fades + loudness

```bash
# voice: denoise/compress, normalize to a working level
$FF -hide_banner -loglevel error -y -ss 2.72 -t 26.2 -i talking-head.mp4 -vn \
  -af "highpass=f=90,afftdn=nf=-25,acompressor=threshold=0.12:ratio=2:attack=8:release=180,loudnorm=I=-18:TP=-2:LRA=11" \
  -ar 48000 -ac 2 voice.wav

# BGM: low level, fade in/out
$FF -hide_banner -loglevel error -y -i bgm.mp3 -t 48.8 \
  -af "loudnorm=I=-31:TP=-2:LRA=11,afade=t=in:st=0:d=1.5,afade=t=out:st=45.8:d=3.0" \
  -ar 48000 -ac 2 bgm.wav

# delay voice to its final start (e.g. 4.0s), pad to video length
$FF -hide_banner -loglevel error -y -i voice.wav \
  -af "adelay=4000|4000,apad=whole_dur=48.8,atrim=0:48.8" -ar 48000 -ac 2 voice_pad.wav

# mix; final loudness target
$FF -hide_banner -loglevel error -y -i voice_pad.wav -i bgm.wav \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first,alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[a]" -ar 48000 -ac 2 mix.wav

# if one-pass loudnorm undershoots, do a two-pass pass with measured_* values
```

Mux without re-encoding video:

```bash
$FF -hide_banner -loglevel error -y -i video.mp4 -i mix.wav \
  -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart final.mp4
```

Measure with `ebur128`:

```bash
$FF -hide_banner -nostats -i final.mp4 -af "ebur128=peak=true" -f null - 2>&1 | grep -A4 'Integrated loudness'
```

## Technical checker

```bash
$PY scripts/check_video.py final.mp4 --width 1080 --height 1920 \
  --min-duration 45 --max-duration 60 --lufs -16 --lufs-tol 2 \
  --max-true-peak -1.0 --max-black 0.5
```

It parses `ffmpeg -i`, decodes the full file, measures loudness with `loudnorm`, detects black segments, and exits non-zero on failure. No external Python packages.

## Common pitfalls

- **`ffprobe` missing**: use `ffmpeg -i`; don't assume a full ffmpeg build has ffprobe.
- **10-bit + colorlevels black**: add `format=yuv420p` before grade; verify first frame.
- **59.94fps source**: `fps=30` first; count frames exactly; `trim=end_frame=N`.
- **AAC true peak**: measure after AAC encode; the WAV may pass but MP4 may overshoot.
- **Subtitle safe area**: 200px is a minimum; platform UI can cover more; 240–280px is safer.
- **Fact card text bleed**: translucent panel + bright poster = competing text; increase alpha or change background.
- **4K crop**: 1215×2160 is only 31.6% of width; check headroom/logo/hands at multiple times.
- **CJK fonts**: use system TTC with explicit `index`; test before building all overlays.
- **Long filter graphs**: render per shot; one failure shouldn't require a 20-input rerun.
- **Overwriting**: never write the final deliverable path until the latest version passes; keep approved.

## Delivery sanity

```bash
md5 final.mp4
$FF -hide_banner -i final.mp4 2>&1 | grep -E 'Duration|Stream'
mdls -name kMDItemDurationSeconds -name kMDItemPixelWidth -name kMDItemPixelHeight final.mp4
```

On macOS, `mdls` confirms QuickTime-visible duration/dimensions. Keep `faststart` (`moov` before `mdat`) for web/mobile playback.
