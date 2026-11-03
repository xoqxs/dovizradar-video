# Baby Collective – daily kids song pipeline (owner: Kadir Pars)

Channel: YouTube @Babycollective (channel id UCTmbZBzBjVERcxbOJjsWVeA). English, ages 2–6. Every day: 1 long song video (16:9, ~2–2.5 min) + 1 Short made from it (9:16, 25–40 s). Both PUBLIC, "Made for kids = Yes".

Reference implementation (first video, 3 Nov 2026: "Colors in My Lunchbox"): song.py, music.py, voice.py, mix.py, render.py, make_short.sh in this folder. Copy them to a work dir and ADAPT; do not just re-render the same song.

## 1. Setup (each run)
```
mkdir -p /home/claude/bc && cd /home/claude/bc && cp <repo>/baby/pipeline/* .
pip install --break-system-packages -q kokoro-onnx soundfile fonttools
# font
mkdir -p f && cd f && npm pack @fontsource/fredoka@latest >/dev/null && tar xzf *.tgz && cd .. && python3 -c "from fontTools.ttLib import TTFont; f=TTFont('f/package/files/fredoka-latin-700-normal.woff'); f.flavor=None; f.save('/home/claude/build/Fredoka-Bold.ttf')"
# voice model (GitHub release, ~350 MB)
mkdir -p /home/claude/tts && cd /home/claude/tts && for f in kokoro-v1.0.onnx voices-v1.0.bin; do [ -f $f ] || curl -sSL -o $f https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f; done
```
Scripts expect to run in /home/claude/build (paths are hard-coded there) – simplest: `mkdir -p /home/claude/build && cp * /home/claude/build/ && cd /home/claude/build`.

## 2. Song (song.py)
- ORIGINAL lyrics only. Never reuse/quote existing nursery rhymes or songs (no "Wheels on the Bus", "Baby Shark", etc. melodies or lyrics).
- Structure stays: intro (16 beats) → verse1 → verse2 → chorus → verse3 → verse4 → chorus×2 → outro (2 lines) → end (8 beats). Each lyric line = 8 beats. BPM 100–118 (vary per day).
- In `L(text, notes)`: syllables separated by `|`, `_` after a syllable = space after it. Number of syllables MUST equal number of pitched notes; note beats per line MUST sum to 8 (the asserts check this). End each line with 2–3 beats rest. Keep melody in G4–G5, C major (or transpose: change N/ROOT/CH consistently), stepwise, singable; chords per 2 beats: C F G Am.
- Teach ONE simple concept per video: colors, animals + sounds, numbers 1–10, shapes, body parts, vehicles, weather, days of week, opposites, feelings, fruits/vegetables, bedtime/morning routine, brushing teeth, sharing, ocean animals, farm animals, bugs, seasons, alphabet chunks (A–F…), counting down. Repeating, call-and-response style, simple words.

## 3. Music → voice → mix
`python3 music.py` (writes music.wav; change instrument mix a bit per day: lead gain, BPM, glock on/off), `python3 voice.py` (Kokoro TTS, chunk-on-note timing; voices to rotate: af_heart, af_bella, af_nicole, am_michael, bf_emma – pick one per video, intro/outro narration text unique each time), `python3 mix.py`.

## 4. Animation (render.py)
- Characters drawn with PIL in the same cute flat style (face() helper: eyes, cheeks, mouth open while voice is active). For a new topic, write new sprite functions (e.g. cow, duck, car, sun, number blocks) – original designs only, no known characters/brands.
- Themes per section (bg gradient colors), big topic word on top, karaoke lyric box with bouncing ball at bottom, collected-items row top right, intro title card with "Baby Collective", end "Bye bye!".
- Before full render: `python3 render.py still <t> x.jpg` at 4–5 busiest moments and LOOK (Read) at them: nothing clipped/overlapping, text readable, correct capitalisation.
- Render: `(python3 render.py 0 2 4 6 8 & python3 render.py 1 3 5 7; wait)`, concat (list of seg_*.mp4, `-c copy`), mux with final_audio.wav (`-c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -movflags +faststart`). For upload size keep ≤ 25 MB (re-encode crf 24 preset medium if larger).
- Thumbnail: `python3 render.py still <intro t≈7> thumb.jpg` (1920x1080 → also save a 1280x720 copy).

## 5. Short
`./make_short.sh LONG.mp4 <chorus start sec> <25–40> "<Short title text>" short.mp4` – pick the most catchy part (usually last chorus). Check one frame.

## 6. Check
ffprobe (1920x1080 / 1080x1920, audio present), 4–5 frames Read, silencedetect for long gaps, total length 1:50–2:40.

## 7. GitHub
Copy long + short + thumbnail to repo `baby/v/` (keep at most 12 files there, delete older ones in baby/v only), `baby/gunluk.md` add line, commit, `git push origin main`, verify raw URL 200:
https://raw.githubusercontent.com/xoqxs/dovizradar-video/main/baby/v/<file>

## 8. YouTube upload – see the scheduled task prompt, step 5 (it is authoritative)
Proven method from the Döviz Radar video tasks: in your own Studio tab, `fetch(RAW_URL)` → Blob → File → DataTransfer into `input[type=file]` → dispatch change (no file picker, no WebRTC needed for YouTube). Title/description: 'ytcp-uploads-dialog #textbox[contenteditable=true]' (1st title, 2nd description) via execCommand insertText, verify textContent. Made for kids: tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_MFK]. #next-button ×3 (2.5 s apart) → tp-yt-paper-radio-button[name=PUBLIC] → #done-button.
CHANNEL: the same Google account owns Döviz Radar (UCETn8pkFCvCHQKpBAKnGXJw); its tasks assume Döviz Radar is the active channel. Switch to Baby Collective via https://www.youtube.com/channel_switcher (wait ~10–20 s, verify Studio URL /channel/UCTmbZBzBjVERcxbOJjsWVeA), upload, and ALWAYS switch back to Döviz Radar at the end (verify https://studio.youtube.com/channel/UCETn8pkFCvCHQKpBAKnGXJw is not "Hata"). The switch can take 10–20 s to reach Studio.

## 9. Titles / description / tags (vary every day, no spam)
- Long title (≤ 70 chars): "<Song name> | <What it teaches> Song for Kids | Baby Collective" (rotate patterns).
- Description: 2–3 sentence unique summary, full lyrics, 3–5 hashtags (#KidsSongs #NurseryRhymes #Learn<Topic> …). No links other than the channel/full song.
- Tags 8–12 relevant.
- Never claim it's by a famous brand; no "Cocomelon/Pinkfong style" words.

## 10. Log
baby/gunluk.md: | date | topic | song title | voice | long link | short link | status |. Do not repeat a topic used in the last 14 days.
