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
def t1_5(w):  # "Red, red, what is red?"
    return L(f'{w},_|{w.lower()},_|what_|is_|{w.lower()}?', [('G4',1),('G4',1),('A4',.5),('B4',.5),('C5',2),('r',3)])
t3 = [('E5',1),('E5',1),('G5',1),('G5',1),('G5',2),('r',2)]

V1 = [t1_5('Red'),
      L('An_|ap|ple,_|crun|chy,_|round_|and_|red!', [('E5',.5),('E5',.5),('D5',.5),('C5',.5),('D5',1),('C5',.5),('B4',.5),('C5',2),('r',2)]),
      L('Crunch,_|crunch,_|yum_|yum_|yum,', t3),
      L('A_|red_|ap|ple_|in_|my_|tum!', [('D5',.5),('D5',.5),('E5',.5),('D5',.5),('C5',.5),('B4',.5),('C5',2),('r',3)])]
V2 = [L('Yel|low,_|yel|low,_|what_|is_|yel|low?', [('G4',.5),('E4',.5),('G4',.5),('E4',.5),('A4',.5),('B4',.5),('C5',1),('A4',1),('r',3)]),
      L('A_|ba|na|na,_|soft_|and_|mel|low!', [('E5',.5),('E5',.5),('D5',.5),('C5',.5),('D5',1),('C5',.5),('B4',.5),('C5',2),('r',2)]),
      L('Peel,_|peel,_|yum_|yum_|yum,', t3),
      L('A_|yel|low_|ba|na|na_|in_|my_|tum!', [('D5',.5),('D5',.5),('E5',.5),('E5',.5),('D5',.5),('C5',.5),('D5',.5),('B4',.5),('C5',2),('r',2)])]
V3 = [t1_5('Green'),
      L('Ti|ny_|grapes,_|so_|fresh_|and_|clean!', [('E5',.5),('D5',.5),('C5',1),('D5',.5),('D5',1),('B4',.5),('C5',2),('r',2)]),
      L('Pop,_|pop,_|yum_|yum_|yum,', t3),
      L('Green_|grapes_|in_|my_|tum!', [('D5',1),('D5',1),('C5',.5),('B4',.5),('C5',2),('r',3)])]
V4 = [t1_5('Blue'),
      L('Blue|ber|ries,_|one_|and_|two!', [('E5',1),('D5',.5),('C5',.5),('D5',1),('B4',1),('C5',2),('r',2)]),
      L('Munch,_|munch,_|yum_|yum_|yum,', t3),
      L('Blue|ber|ries_|in_|my_|tum!', [('D5',1),('E5',.5),('D5',.5),('C5',.5),('B4',.5),('C5',2),('r',3)])]
CH = [L('Co|lors,_|co|lors,_|all_|a|round,', [('C5',1),('A4',1),('C5',1),('A4',1),('F5',1),('E5',1),('D5',2)]),
      L('Look_|at_|all_|the_|food_|I_|found!', [('C5',1),('G4',1),('C5',1),('E5',1),('D5',1),('C5',1),('D5',2)]),
      L('Red_|and_|yel|low,_|green_|and_|blue,', [('A4',1),('A4',.5),('C5',.5),('F5',1),('E5',1),('C5',1),('D5',2),('r',1)]),
      L('Eat_|your_|co|lors,_|I_|do_|too!', [('G5',1),('E5',1),('C5',1),('E5',1),('D5',1),('B4',1),('C5',2)])]
OUT = [CH[2],
       L('Health|y_|co|lors,_|just_|for_|you!', [('G5',1),('E5',1),('C5',1),('E5',1),('D5',1),('B4',1),('C5',2)])]

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
add('v1', 'verse', V1, VERSE_CH, 'red')
add('v2', 'verse', V2, VERSE_CH, 'yellow')
add('ch1', 'chorus', CH, CHOR_CH, 'rainbow')
add('v3', 'verse', V3, VERSE_CH, 'green')
add('v4', 'verse', V4, VERSE_CH, 'blue')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'rainbow')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'rainbow')
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
