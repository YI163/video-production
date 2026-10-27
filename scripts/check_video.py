#!/usr/bin/env python3
"""Technical checker for the vertical vlog deliverable.

Usage:
  python3 scripts/check_video.py final.mp4 --width 1080 --height 1920 \
      --min-duration 45 --max-duration 60 --lufs -16 --lufs-tol 2 \
      --max-true-peak -1.0 --max-black 0.5

FFmpeg is found from $FFMPEG, PATH, ./tools/ffmpeg, or /opt/homebrew/bin/ffmpeg.

Exit code 0 = all requested checks pass; 1 = at least one failure.
Prints a JSON report on stdout. No third-party Python packages required.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_ffmpeg():
    env = os.environ.get("FFMPEG")
    if env:
        return env
    which = shutil.which("ffmpeg")
    if which:
        return which
    candidates = [
        os.path.normpath(os.path.join(os.getcwd(), "tools", "ffmpeg")),
        os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "tools", "ffmpeg")),
        os.path.normpath(os.path.join(HERE, "..", "..", "..", "tools", "ffmpeg")),
        os.path.normpath(os.path.join(HERE, "..", "..", "tools", "ffmpeg")),
        "/opt/homebrew/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
    ]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return "ffmpeg"


FFMPEG = _find_ffmpeg()


def run(args, timeout=900):
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True, errors="replace", timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def probe(path):
    code, _, err = run([FFMPEG, "-hide_banner", "-i", path], timeout=120)
    info = {"duration": None, "width": None, "height": None,
            "fps": None, "has_audio": False, "audio": None, "video_codec": None}
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", err)
    if m:
        info["duration"] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    m = re.search(r"Video:\s*([a-z0-9_]+).*?(\d{2,5})x(\d{2,5})", err)
    if m:
        info["video_codec"] = m.group(1)
        info["width"] = int(m.group(2))
        info["height"] = int(m.group(3))
    m = re.search(r"(\d+(?:\.\d+)?)\s+fps", err)
    if m:
        info["fps"] = float(m.group(1))
    m = re.search(r"Audio:\s*(.+)", err)
    if m:
        info["has_audio"] = True
        info["audio"] = m.group(1).strip()[:160]
    return info


def decode_check(path):
    code, _, err = run([FFMPEG, "-v", "error", "-i", path, "-f", "null", "-"], timeout=1200)
    errors = [ln for ln in err.splitlines() if ln.strip()]
    return code == 0 and not errors, errors[:8]


def loudness(path):
    code, _, err = run([FFMPEG, "-hide_banner", "-nostats", "-i", path,
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], timeout=1200)
    start = err.rfind("{")
    end = err.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        data = json.loads(err[start:end + 1])
    except json.JSONDecodeError:
        return None
    out = {}
    for key in ("input_i", "input_tp", "input_lra", "input_thresh"):
        try:
            out[key] = float(data.get(key))
        except (TypeError, ValueError):
            out[key] = None
    return out


def black_segments(path, min_dur=0.30, pix_th=0.10):
    code, _, err = run([FFMPEG, "-hide_banner", "-nostats", "-i", path, "-an",
                        "-vf", "blackdetect=d=%.2f:pix_th=%.2f" % (min_dur, pix_th),
                        "-f", "null", "-"], timeout=1200)
    segs = []
    for m in re.finditer(r"black_start:([\d.]+)\s+black_end:([\d.]+)\s+black_duration:([\d.]+)", err):
        segs.append({"start": float(m.group(1)), "end": float(m.group(2)),
                     "duration": float(m.group(3))})
    return segs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--min-duration", type=float, default=45.0)
    ap.add_argument("--max-duration", type=float, default=60.0)
    ap.add_argument("--lufs", type=float, default=-16.0)
    ap.add_argument("--lufs-tol", type=float, default=2.0)
    ap.add_argument("--max-true-peak", type=float, default=-1.0)
    ap.add_argument("--max-black", type=float, default=0.5,
                    help="longest tolerated black segment in seconds (0 disables)")
    ap.add_argument("--skip-decode", action="store_true")
    ap.add_argument("--skip-loudness", action="store_true")
    args = ap.parse_args()

    failures = []
    if not os.path.isfile(args.file):
        print(json.dumps({"file": args.file, "failures": ["file not found"]}, ensure_ascii=False))
        return 1

    info = probe(args.file)
    if info["width"] != args.width or info["height"] != args.height:
        failures.append("resolution %sx%s != %sx%s" % (info["width"], info["height"],
                                                       args.width, args.height))
    if info["duration"] is None:
        failures.append("duration could not be read")
    elif not (args.min_duration <= info["duration"] <= args.max_duration):
        failures.append("duration %.2fs outside [%.1f, %.1f]" % (info["duration"],
                                                                 args.min_duration,
                                                                 args.max_duration))
    if not info["has_audio"]:
        failures.append("no audio stream")

    report = {"file": args.file, "probe": info}

    if not args.skip_decode:
        ok, errs = decode_check(args.file)
        report["decode_ok"] = ok
        report["decode_errors"] = errs
        if not ok:
            failures.append("decode errors present")

    if info["has_audio"] and not args.skip_loudness:
        loud = loudness(args.file)
        report["loudness"] = loud
        if not loud or loud.get("input_i") is None:
            failures.append("loudness could not be measured")
        else:
            if abs(loud["input_i"] - args.lufs) > args.lufs_tol:
                failures.append("integrated loudness %.1f LUFS outside %.1f±%.1f"
                                % (loud["input_i"], args.lufs, args.lufs_tol))
            if loud.get("input_tp") is not None and loud["input_tp"] > args.max_true_peak:
                failures.append("true peak %.1f dBTP above %.1f"
                                % (loud["input_tp"], args.max_true_peak))

    if args.max_black > 0:
        segs = black_segments(args.file)
        report["black_segments"] = segs
        long_black = [s for s in segs if s["duration"] > args.max_black]
        if long_black:
            failures.append("%d black segment(s) longer than %.1fs"
                            % (len(long_black), args.max_black))

    report["failures"] = failures
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
