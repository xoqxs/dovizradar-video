"""Song structure: lyrics (syllables), melody, chords. Times in beats."""
BPM = 104
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
def ask(w):  # "Moo, moo, who says moo?"
    return L(f'{w},_|{w.lower()},_|who_|says_|{w.lower()}?', [('G4',1),('G4',1),('A4',.5),('B4',.5),('C5',2),('r',3)])
ANS = [('E5',.5),('E5',.5),('D5',.5),('C5',.5),('D5',1),('C5',.5),('B4',.5),('C5',2),('r',2)]
t3 = [('E5',1),('E5',1),('G5',1),('G5',1),('G5',2),('r',2)]
def hello(a):
    return L(f'Hel|lo,_|{a},_|on_|the_|farm!', [('D5',1),('E5',.5),('D5',.5),('C5',.5),('B4',.5),('C5',2),('r',3)])

V1 = [ask('Moo'), L('A_|big_|brown_|cow_|is_|say|ing_|moo!', ANS),
      L('Moo,_|moo,_|stomp_|stomp_|stomp,', t3), hello('cow')]
V2 = [ask('Quack'), L('A_|lit|tle_|duck_|is_|com|ing_|back!', ANS),
      L('Quack,_|quack,_|splash_|splash_|splash,', t3), hello('duck')]
V3 = [ask('Oink'), L('A_|pink_|pig_|rol|ling_|in_|the_|mud!', ANS),
      L('Oink,_|oink,_|squish_|squish_|squish,', t3), hello('pig')]
V4 = [ask('Baa'), L('A_|fluf|fy_|sheep,_|so_|soft_|and_|white!', ANS),
      L('Baa,_|baa,_|hop_|hop_|hop,', t3), hello('sheep')]
CH = [L('Down_|on_|the_|farm,_|the_|sun_|is_|up,', [('G4',.5),('A4',.5),('C5',1),('E5',1),('D5',.5),('C5',.5),('D5',1),('E5',2),('r',1)]),
      L('Ev|ery|bo|dy_|wakes_|up!', [('E5',.5),('F5',.5),('E5',.5),('D5',.5),('C5',1),('D5',2),('r',3)]),
      L('Moo_|and_|quack_|and_|oink_|and_|baa,', [('A4',1),('A4',.5),('C5',.5),('F5',1),('E5',.5),('D5',.5),('C5',2),('r',2)]),
      L('Sing_|with_|me,_|tra_|la_|la!', [('G5',1),('E5',1),('C5',1),('D5',1),('B4',1),('C5',2),('r',1)])]
OUT = [CH[2],
       L('Bye_|bye,_|farm_|friends,_|tra_|la_|la!', [('G5',1),('E5',1),('C5',.5),('E5',.5),('D5',1),('B4',1),('C5',2),('r',1)])]

VERSE_CH = [['C','C','C','C'], ['F','F','C','C'], ['C','C','F','F'], ['G','G','C','C']]
CHOR_CH = [['F','F','G','G'], ['C','C','G','G'], ['F','F','G','G'], ['C','C','G','C']]

# sections: (name, kind, lines, chords per line (4 x 2-beat), theme)
SECTIONS = []
t = 0.0
def add(name, kind, lines, chords, theme, beats=None):
    global t
    b = beats if beats is not None else 8 * len(lines)
    SECTIONS.append(dict(name=name, kind=kind, lines=lines, chords=chords, theme=theme, start=t, beats=b))
    t += b

add('intro', 'intro', [], [['C','C','F','F'], ['G','G','C','C']], 'title', 16)
add('v1', 'verse', V1, VERSE_CH, 'cow')
add('v2', 'verse', V2, VERSE_CH, 'duck')
add('ch1', 'chorus', CH, CHOR_CH, 'farm')
add('v3', 'verse', V3, VERSE_CH, 'pig')
add('v4', 'verse', V4, VERSE_CH, 'sheep')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'farm')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'farm')
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
