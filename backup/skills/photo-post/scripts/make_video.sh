#!/bin/bash
# photo-post 動画生成: 写真1〜3枚 → 9:16 Ken Burns + 見出しオーバーレイ + エンドカード mp4
# usage: make_video.sh -o OUT.mp4 -e ENDCARD.png [-t OVERLAY.png] PHOTO1 [PHOTO2 PHOTO3]
set -euo pipefail

FFMPEG=/usr/local/bin/ffmpeg
OUT="" ; ENDCARD="" ; OVERLAY=""
while getopts "o:e:t:" opt; do
  case $opt in
    o) OUT=$OPTARG ;;
    e) ENDCARD=$OPTARG ;;
    t) OVERLAY=$OPTARG ;;
    *) exit 1 ;;
  esac
done
shift $((OPTIND-1))
PHOTOS=("$@")
if [[ -z $OUT || -z $ENDCARD || ${#PHOTOS[@]} -lt 1 || ${#PHOTOS[@]} -gt 3 ]]; then
  echo "usage: make_video.sh -o out.mp4 -e endcard.png [-t overlay.png] photo1 [photo2 photo3]" >&2
  exit 1
fi

# 合計10秒以内に収める（エンドカード2.5秒＋写真尺）。よほどの品質でなければ
# ショート動画は10秒以内が完視聴の限界（2026-07-05草川フィードバック）。
N=${#PHOTOS[@]}
case $N in 1) DUR=6.5 ;; 2) DUR=3.4 ;; *) DUR=2.4 ;; esac
FPS=30
FRAMES=$(echo "$DUR * $FPS / 1" | bc)
FADE_OUT_ST=$(echo "$DUR - 0.5" | bc)
ENDDUR=2.5
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# 各写真セグメント: 2160x3840へカバークロップ→zoompanでスローズーム→1080x1920
BASE="scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${FRAMES}:s=1080x1920:fps=${FPS}"

i=0
for P in "${PHOTOS[@]}"; do
  if [[ $i -eq 0 && -n $OVERLAY ]]; then
    "$FFMPEG" -y -loglevel error -i "$P" -loop 1 -t "$DUR" -i "$OVERLAY" \
      -filter_complex "[0:v]${BASE}[bg];[1:v]format=rgba,fade=t=in:st=0.8:d=0.6:alpha=1[ov];[bg][ov]overlay=0:0:shortest=1,fade=t=out:st=${FADE_OUT_ST}:d=0.5,format=yuv420p" \
      -c:v libx264 -preset medium -crf 20 -r "$FPS" "$TMP/seg${i}.mp4"
  else
    "$FFMPEG" -y -loglevel error -i "$P" \
      -filter_complex "[0:v]${BASE},fade=t=in:st=0:d=0.4,fade=t=out:st=${FADE_OUT_ST}:d=0.5,format=yuv420p" \
      -c:v libx264 -preset medium -crf 20 -r "$FPS" "$TMP/seg${i}.mp4"
  fi
  i=$((i + 1))
done

# エンドカード（既定2.5秒）
"$FFMPEG" -y -loglevel error -loop 1 -t "$ENDDUR" -i "$ENDCARD" \
  -filter_complex "[0:v]scale=1080:1920,fade=t=in:st=0:d=0.4,format=yuv420p" \
  -c:v libx264 -preset medium -crf 20 -r "$FPS" "$TMP/zzz_end.mp4"

# 連結（同一エンコードなので -c copy）
: > "$TMP/list.txt"
for f in "$TMP"/seg*.mp4 "$TMP"/zzz_end.mp4; do
  echo "file '$f'" >> "$TMP/list.txt"
done
"$FFMPEG" -y -loglevel error -f concat -safe 0 -i "$TMP/list.txt" -c copy "$OUT"

/usr/bin/python3 -c "import subprocess,sys; r=subprocess.run(['/usr/local/bin/ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',sys.argv[1]],capture_output=True,text=True); print(f'done: {sys.argv[1]} ({float(r.stdout):.1f}s)')" "$OUT"
