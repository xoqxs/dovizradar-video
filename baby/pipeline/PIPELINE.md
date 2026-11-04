# Sing with Tavo – Baby Collective pipeline v2 (owner: Kadir Pars)

Channel: YouTube @Babycollective (UCTmbZBzBjVERcxbOJjsWVeA). English, ages 2–6. Series brand: **Sing with Tavo**.
Schedule (Europe/Istanbul 16:13): **Mon / Wed / Fri** = 1 new song (16:9, ~2:20–2:40) + 1 native vertical Short from it.
**Sunday** = 1 compilation of recent songs (≥ 8:00, aim 9–12 min). Everything PUBLIC, "Made for kids = Yes".
Any other day (manual run) = new song.

## 0. What is FIXED (never change per song)
- Cast (chars.py): **Tavo** – baby fox host, green scarf, yellow pencil case full of crayons (NO backpack, NO blue
  accessories). Friends: **Rosy** (pink crayon, yellow bow), **Rubbo** (eraser, purple sleeve), **Lino** (wooden ruler).
  Every song: Tavo opens his pencil case and the song's "guests" fly out of it.
- Voice: Kokoro **af_heart** for Tavo, always (topic.VOICE = 'af_heart').
- Intro: "Sing with Tavo" logo card + 4-note signature sting (music.py STING) + Tavo saying INTRO_LINE.
- engine.py (16:9 + 9:16 + thumbnail renderer), compile.py, music.py, voice.py, mix.py, chars.py.
  Do NOT rewrite them. Only if something is truly broken: smallest possible fix, note it in baby/gunluk.md.
- Per song you write ONLY two files: **song.py** (lyrics, melody, sections) and **topic.py** (title, themes, guests).
  The files in baby/pipeline are the "Colors in My Lunchbox" example – copy them and replace the content.

## 1. Setup (each run)
```
W=/home/claude/bc; mkdir -p $W && cd $W && cp <repo>/baby/pipeline/*.py .
pip install --break-system-packages -q kokoro-onnx soundfile fonttools scipy
# font (Fredoka Bold, OFL) -> $W/Fredoka-Bold.ttf
mkdir -p /tmp/f && cd /tmp/f && npm pack @fontsource/fredoka@latest >/dev/null && tar xzf *.tgz && \
python3 -c "from fontTools.ttLib import TTFont; f=TTFont('/tmp/f/package/files/fredoka-latin-700-normal.woff'); f.flavor=None; f.save('/home/claude/bc/Fredoka-Bold.ttf')"; cd $W
# voice model (GitHub release, ~350 MB)
mkdir -p /home/claude/tts && cd /home/claude/tts && for f in kokoro-v1.0.onnx voices-v1.0.bin; do [ -f $f ] || curl -sSL -o $f https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f; done; cd $W
```
All commands below run inside $W.

## 2. New song (Mon/Wed/Fri)
### 2a. Topic
One simple concept per song, not used in the last 14 days (baby/gunluk.md): animals + sounds, numbers 1–5 / 6–10,
shapes, body parts, vehicles, weather, days of the week, opposites, feelings, fruits, vegetables, morning routine,
bedtime, brushing teeth, washing hands, sharing, ocean animals, farm animals, bugs, seasons, alphabet chunks (A–E…),
counting down, colors of nature, sizes (big/small), music instruments, kitchen helpers, toys, clothes for weather.

### 2b. song.py
- ORIGINAL lyrics and melody only. Never reuse existing nursery rhymes/songs (lyrics, melodies, hooks, characters).
- Structure: intro (16 beats) → v1 → v2 → chorus → v3 → v4 → chorus×2 → outro (2 lines) → end (8 beats).
  3–5 verses allowed (engine supports up to 5 guests); 4 is best. Each lyric line = 8 beats. BPM 100–118, vary per song.
- `add(name, kind, lines, chords, theme)`: kind ∈ intro/verse/chorus/outro/end; `theme` must be a key of topic.THEMES.
- `L(text, notes)`: syllables split by `|`, `_` after a syllable = space. Syllable count == pitched notes;
  beats per line sum to 8 (asserts check). End lines with 2–3 beats rest. Melody G4–G5 (E4 ok), stepwise, singable;
  chords per 2 beats from C F G Am only.
- Line 3 of each verse (index 2 = ACTION_LINE) is the fun action/sound line ("Pop, pop, yum yum yum") – stars burst there.
- Call-and-response, lots of repetition, simple words. Verse line 1 asks, line 2 answers with the guest.

### 2c. topic.py
- TITLE (≤ 28 chars, catchy), TOPIC, VOICE='af_heart', INTRO_LINE ("Hi friends! It's Tavo! Let's sing about …!"),
  OUTRO_LINE ("Bye bye, friends! See you next time with Tavo!" – may vary slightly), CHORUS_TITLE, OUTRO_TITLE (≤ 18 chars).
- THEMES: pastel gradients (top/bot), strong accent `col`, optional rainbow=True. Must contain 'title', 'end'
  and every theme name used in song.py.
- VERSES: one dict per verse section in order: guest (key of GUESTS), word (BIG word, ≤ 9 letters, CAPS), theme.
- GUESTS: one sprite function per verse, signature `f(mouth_open=False, blink=False, size=440)`, drawn on an 880 px
  canvas with `canvas(S)`, `face(d, cx, cy, s, mouth_open, blink)`, `finish(im, size)` so they match Tavo's flat cute style.
  Simple bold shapes, 2–4 colours, a face on every guest. Original designs only – no known characters, brands, logos.
- THUMB = dict(lines=[2 short lines of the title], theme='title').

### 2d. Build
```
python3 -c "import song, topic"                      # asserts pass
python3 music.py && python3 voice.py && python3 mix.py   # music.wav, voice.wav, voice_env.npy, final_audio.wav
python3 engine.py chorus_starts                      # e.g. "ch1: 43.64s (17.5s long)" / "ch2: 96.00s (34.9s long)"
# LOOK before rendering (Read each jpg): intro ~5 s, a verse word moment, a chorus, the end – in h AND v
python3 engine.py still h 5.5 a.jpg ; python3 engine.py still v 5.5 b.jpg   (+ 3–4 more times)
python3 engine.py render                             # -> video_h.mp4 (~2.5 min)
python3 engine.py final  bc-YYYY-MM-DD-<slug>.mp4    # loudnorm -14 LUFS, auto-compress ≤ 24 MB
python3 engine.py short  <ch2 start> <25–40> bc-YYYY-MM-DD-<slug>-short.mp4   # native 1080x1920
python3 engine.py thumb  bc-YYYY-MM-DD-<slug>-kapak.jpg                           # 1280x720
```
Short window: start and length of the LAST chorus as printed by chorus_starts (ch2, ~30–38 s; if it is longer than 40 s use its first 4 lines = 32 beats).
Check: ffprobe sizes (1920x1080 / 1080x1920, audio present), duration 2:00–2:50, `silencedetect=n=-40dB:d=3`
finds no gap after 0:10, Read 3–4 frames of each file + the thumbnail.

### 2e. Save the song source
Copy song.py and topic.py to `baby/songs/YYYY-MM-DD-<slug>/` (small text files – kept forever; old songs can be
re-rendered from them for compilations).

## 3. Sunday compilation
1. Songs: the newest Tavo songs in baby/gunluk.md (status "yayınlandı", not compilations), newest first, until the
   total is ≥ 8:30 (normally 4 songs; max 6). Prefer songs not used in last Sunday's compilation, but repeating 1–2 is fine.
2. For each song: if `baby/v/<file>.mp4` exists use it; otherwise re-render it from `baby/songs/<date-slug>/`
   (copy song.py + topic.py into a fresh copy of $W, run 2d up to `final`). The example song in baby/pipeline
   ("Colors in My Lunchbox") is also a valid source. Old pre-Tavo videos (e.g. "Hello, Little Shapes") only if
   still short of 8:00.
3. `python3 compile.py bc-YYYY-MM-DD-mix.mp4 "<Comp title>" song1.mp4 "Title 1" song2.mp4 "Title 2" …`
   (exit code 2 = shorter than 8:00 → add a song). Output ≤ 48 MB; chapters in `<out>.chapters.txt`.
4. `python3 compile.py --thumb bc-YYYY-MM-DD-mix-kapak.jpg "<Comp title>" <minutes>`
5. Title e.g. "Sing with Tavo Song Mix | Colors, Shapes & More | 10 Min Kids Songs" (≤ 70, vary weekly).
   Description: 2 unique sentences + the chapters list exactly as written (first line 0:00) + 3–5 hashtags.
   No Short on Sunday.

## 4. GitHub (repo xoqxs/dovizradar-video, work ONLY under baby/)
- Upload files go to `baby/v/`, commit + `git push origin main`, verify each raw URL returns 200:
  https://raw.githubusercontent.com/xoqxs/dovizradar-video/main/baby/v/<file>
- Retention (keeps the repo small): after a successful YouTube upload, delete that run's Short and thumbnail from
  baby/v in the log commit. Keep long song mp4s for 14 days (for Sundays), then delete them (source stays in
  baby/songs). Delete the compilation mp4 + thumbnail right after it is published. Never touch files outside baby/.

## 5. YouTube upload – the scheduled task prompt is authoritative (channel switch → upload → switch BACK to Döviz Radar).

## 6. Titles / descriptions / tags (unique every time, no spam)
- Song title (≤ 70): "<Song name> | <What it teaches> Song for Kids | Sing with Tavo" – rotate patterns, e.g.
  "Learn Farm Animals with Tavo | Moo Moo Song for Toddlers".
- Description: 2–3 unique sentences (what children learn, Tavo and friends), full lyrics, 3–5 hashtags
  (#KidsSongs #NurseryRhymes #SingWithTavo #Learn<Topic> …). Short: first line "Full song: <long video link>".
- Tags 8–12 relevant (sing with tavo, kids songs, toddler learning, <topic> song …).
- Never mention other brands/channels (no "Cocomelon/Pinkfong/Super Simple style").

## 7. Log – baby/gunluk.md
| date | topic | song title | voice | long link | short link | status |  (compilation: topic "derleme", short "–").
