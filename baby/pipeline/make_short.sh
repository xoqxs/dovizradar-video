#!/bin/bash
# usage: make_short.sh LONG.mp4 START_SEC DURATION_SEC "TITLE TEXT" OUT.mp4
# Vertical 1080x1920 Short from the long video: blurred background, video centered, title on top.
set -e
IN="$1"; SS="$2"; DUR="$3"; TITLE="$4"; OUT="$5"
FONT=/home/claude/build/Fredoka-Bold.ttf
TXT=$(printf '%s' "$TITLE" | sed "s/'/\\\\'/g; s/:/\\\\:/g")
ffmpeg -v error -y -ss "$SS" -t "$DUR" -i "$IN" -filter_complex "
[0:v]split[a][b];
[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30,eq=brightness=0.06[bg];
[b]scale=1080:-2[fg];
[bg][fg]overlay=(W-w)/2:(H-h)/2-40,
drawtext=fontfile=$FONT:text='$TXT':fontsize=86:fontcolor=0xD81B60:borderw=10:bordercolor=white:x=(w-text_w)/2:y=330,
drawtext=fontfile=$FONT:text='Sing along!':fontsize=70:fontcolor=0x1E78DC:borderw=8:bordercolor=white:x=(w-text_w)/2:y=1480,
fade=t=in:st=0:d=0.3,fade=t=out:st=$(echo "$DUR-0.6" | bc):d=0.6[v];
[0:a]afade=t=in:st=0:d=0.3,afade=t=out:st=$(echo "$DUR-0.8" | bc):d=0.8[a2]" \
 -map "[v]" -map "[a2]" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -movflags +faststart "$OUT"
