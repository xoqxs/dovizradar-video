"""Song structure: lyrics (syllables), melody, chords. Times in beats."""
BPM = 110
BEAT = 60.0 / BPM

N = {'E4': 64, 'G4': 67, 'A4': 69, 'B4': 71, 'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79}

def L(text, notes):
    # text: syllables separated by '|'; '_' marks a space after the syllable
    syl = text.split('|')
    pitched = [n for n in notes if n[0] != 'r']
    assert len(syl) == len(pitched), (text, len(syl), len(pitched))
    assert abs(sum(n[1] for n in notes) - 8) < 1e-9, text
    return {'syl': syl, 'notes': notes}

# verse line types
def ask(w):  # "Beep, beep, who is here?"
    return L(f'{w},_|{w.lower()},_|who_|is_|here?', [('C5',1),('C5',1),('E5',.5),('D5',.5),('C5',2),('r',3)])
ANS = [('G4',.5),('A4',.5),('C5',.5),('D5',.5),('E5',1),('D5',.5),('C5',.5),('D5',2),('r',2)]
t3 = [('E5',1),('C5',1),('E5',1),('E5',1),('G5',2),('r',2)]
def ride(a):
    return L(f'Ride_|a|long_|with_|the_|{a}!', [('G5',1),('E5',.5),('D5',.5),('C5',.5),('D5',.5),('C5',2),('r',3)])

V1 = [ask('Beep'), L('A_|shi|ny_|car_|is_|driv|ing_|near!', ANS),
      L('Beep,_|beep,_|zip_|zip_|zip,', t3), ride('car')]
V2 = [ask('Choo'), L('A_|long_|blue_|train_|is_|chug|ging_|near!', ANS),
      L('Choo,_|choo,_|chug_|chug_|chug,', t3), ride('train')]
V3 = [ask('Toot'), L('A_|sun|ny_|boat_|is_|sail|ing_|near!', ANS),
      L('Toot,_|toot,_|splish_|splish_|splish,', t3), ride('boat')]
V4 = [ask('Zoom'), L('A_|sil|ver_|plane_|is_|fly|ing_|near!', ANS),
      L('Zoom,_|zoom,_|whoosh_|whoosh_|whoosh,', t3), ride('plane')]
CH = [L('Beep_|and_|choo_|and_|toot_|and_|zoom,', [('A4',1),('A4',.5),('C5',.5),('D5',1),('C5',.5),('D5',.5),('E5',2),('r',2)]),
      L('Here_|we_|go,_|make_|some_|room!', [('E5',.5),('E5',.5),('D5',1),('C5',.5),('C5',.5),('D5',2),('r',3)]),
      L('Up_|and_|down_|and_|far_|a|way,', [('F5',1),('E5',.5),('D5',.5),('C5',1),('A4',.5),('C5',.5),('D5',2),('r',2)]),
      L("Let's_|all_|ride_|to|day!", [('G5',1),('E5',1),('D5',1),('B4',1),('C5',2),('r',2)])]
OUT = [CH[2],
       L("Bye_|bye,_|friends,_|let's_|ride_|a|gain!", [('G5',1),('E5',1),('C5',.5),('E5',.5),('D5',1),('B4',1),('C5',2),('r',1)])]

VERSE_CH = [['C','C','C','C'], ['F','F','G','G'], ['C','C','C','C'], ['C','G','C','C']]
CHOR_CH = [['F','F','C','C'], ['C','C','G','G'], ['F','F','G','G'], ['C','G','C','C']]

# sections: (name, kind, lines, chords per line (4 x 2-beat), theme)
SECTIONS = []
t = 0.0
def add(name, kind, lines, chords, theme, beats=None):
    global t
    b = beats if beats is not None else 8 * len(lines)
    SECTIONS.append(dict(name=name, kind=kind, lines=lines, chords=chords, theme=theme, start=t, beats=b))
    t += b

add('intro', 'intro', [], [['C','C','F','F'], ['G','G','C','C']], 'title', 16)
add('v1', 'verse', V1, VERSE_CH, 'car')
add('v2', 'verse', V2, VERSE_CH, 'train')
add('ch1', 'chorus', CH, CHOR_CH, 'road')
add('v3', 'verse', V3, VERSE_CH, 'boat')
add('v4', 'verse', V4, VERSE_CH, 'plane')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'road')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'road')
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
