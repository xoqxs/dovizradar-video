"""Song structure: lyrics (syllables), melody, chords. Times in beats."""
BPM = 108
BEAT = 60.0 / BPM

N = {'E4': 64, 'G4': 67, 'A4': 69, 'B4': 71, 'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79}

def L(text, notes):
    # text: syllables separated by '|'; '_' marks a space after the syllable
    syl = text.split('|')
    pitched = [n for n in notes if n[0] != 'r']
    assert len(syl) == len(pitched), (text, len(syl), len(pitched))
    assert abs(sum(n[1] for n in notes) - 8) < 1e-9, text
    return {'syl': syl, 'notes': notes}

# verse line types (original melody)
ASK = [('G4',.5),('C5',.5),('G4',.5),('C5',.5),('D5',.5),('E5',.5),('D5',.5),('D5',1.5),('r',3)]
ANS = [('E5',.5),('E5',.5),('D5',.5),('C5',.5),('D5',.5),('E5',.5),('D5',.5),('C5',2),('r',2.5)]
ACT = [('C5',1),('E5',1),('G5',1),('E5',1),('G5',2),('r',2)]
END = [('D5',.5),('D5',.5),('E5',.5),('D5',.5),('C5',.5),('B4',.5),('A4',.5),('C5',2),('r',2.5)]
def ask(): return L('Look_|up,_|look_|up,_|what_|do_|you_|see?', ASK)

V1 = [ask(), L('The_|sun_|is_|shi|ning_|down_|on_|me!', ANS),
      L('Shine,_|shine,_|warm_|warm_|warm,', ACT), L('A_|sun|ny_|day_|to_|keep_|me_|warm!', END)]
V2 = [ask(), L('The_|rain_|is_|fal|ling,_|one_|two_|three!', ANS),
      L('Drip,_|drop,_|splash_|splash_|splash,', ACT), L("A_|rain|y_|day,_|let's_|jump_|and_|splash!", END)]
V3 = [ask(), L('The_|wind_|is_|blow|ing_|past_|a_|tree!', ANS),
      L('Whoosh,_|whoosh,_|blow_|blow_|blow,', ACT), L('A_|win|dy_|day,_|a|way_|we_|go!', END)]
V4 = [ask(), L('The_|snow_|is_|soft_|for_|you_|and_|me!', ANS),
      L('Cold,_|cold,_|snow_|snow_|snow,', ACT), L('A_|snow|y_|day,_|the_|cold_|winds_|blow!', END)]
HI = [('G5',1),('E5',1),('G5',1),('E5',1),('D5',1),('D5',1),('C5',2)]
CH = [L('Sun_|and_|rain_|and_|wind_|and_|snow,', [('E5',1),('C5',1),('F5',1),('D5',1),('G5',1),('E5',1),('D5',2)]),
      L('Look_|out|side,_|and_|off_|we_|go!', [('C5',1),('D5',1),('E5',1),('C5',1),('D5',1),('B4',1),('C5',2)]),
      L('Ev|ery_|day_|the_|sky_|is_|new,', [('A4',1),('C5',1),('D5',1),('E5',1),('F5',1),('E5',1),('D5',1),('r',1)]),
      L('Hel|lo,_|sky!_|I_|see_|you_|too!', HI)]
OUT = [CH[2], L('Hel|lo,_|sky!_|Good|bye_|to_|you!', HI)]

VERSE_CH = [['C','G','G','C'], ['C','G','C','C'], ['C','C','C','C'], ['G','F','C','C']]
CHOR_CH = [['C','F','C','G'], ['C','C','G','C'], ['Am','C','F','G'], ['C','C','G','C']]

# sections: (name, kind, lines, chords per line (4 x 2-beat), theme)
SECTIONS = []
t = 0.0
def add(name, kind, lines, chords, theme, beats=None):
    global t
    b = beats if beats is not None else 8 * len(lines)
    SECTIONS.append(dict(name=name, kind=kind, lines=lines, chords=chords, theme=theme, start=t, beats=b))
    t += b

add('intro', 'intro', [], [['C','C','F','F'], ['G','G','C','C']], 'title', 16)
add('v1', 'verse', V1, VERSE_CH, 'sunny')
add('v2', 'verse', V2, VERSE_CH, 'rainy')
add('ch1', 'chorus', CH, CHOR_CH, 'sky')
add('v3', 'verse', V3, VERSE_CH, 'windy')
add('v4', 'verse', V4, VERSE_CH, 'snowy')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'sky')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'sky')
add('end', 'end', [], [['C','C','C','C']], 'end', 8)
TOTAL_BEATS = t

def events():
    """Yield melody notes (start_beat, dur, midi, section, line_idx, syl_idx) and chords (start, dur, name)."""
    notes, chords = [], []
    for s in SECTIONS:
        for li, line in enumerate(s['lines']):
            b = s['start'] + 8 * li
            si = 0
            for p, d in line['notes']:
                if p != 'r':
                    notes.append((b, d, N[p], s['name'], li, si)); si += 1
                b += d
        nl = max(1, len(s['lines'])) if s['lines'] else s['beats'] // 8
        for li in range(int(s['beats'] // 8)):
            cl = s['chords'][li % len(s['chords'])]
            for k, c in enumerate(cl):
                chords.append((s['start'] + 8 * li + 2 * k, 2, c))
    return notes, chords
