"""Song: "Tiny Bugs in My Garden" (garden bugs). Times in beats."""
BPM = 106
BEAT = 60.0 / BPM

N = {'E4': 64, 'G4': 67, 'A4': 69, 'B4': 71, 'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79}

def L(text, notes):
    syl = text.split('|')
    pitched = [n for n in notes if n[0] != 'r']
    assert len(syl) == len(pitched), (text, len(syl), len(pitched))
    assert abs(sum(n[1] for n in notes) - 8) < 1e-9, text
    return {'syl': syl, 'notes': notes}

Q8 = [('G4',.5),('G4',.5),('A4',.5),('B4',.5),('C5',.5),('C5',.5),('D5',1),('C5',1),('r',3)]
Q7 = [('G4',1),('G4',1),('A4',.5),('B4',.5),('C5',.5),('B4',.5),('C5',1),('r',3)]
A9 = [('E5',.5),('E5',.5),('D5',.5),('C5',.5),('D5',.5),('C5',.5),('B4',.5),('B4',.5),('C5',2),('r',2)]
A8 = [('E5',.5),('E5',.5),('D5',.5),('C5',.5),('D5',1),('C5',.5),('B4',.5),('C5',2),('r',2)]
ACT = [('E5',1),('E5',1),('G5',1),('G5',1),('G5',2),('r',2)]
H7 = [('D5',.5),('D5',.5),('E5',1),('D5',.5),('C5',.5),('B4',.5),('C5',2),('r',2.5)]
H8 = [('D5',.5),('D5',.5),('E5',.5),('D5',.5),('C5',.5),('B4',.5),('B4',.5),('C5',2),('r',2.5)]

V1 = [L('Buzz,_|buzz,_|who_|is_|in_|the_|flow|ers?', Q8),
      L('A_|lit|tle_|bee,_|so_|fuz|zy_|and_|sweet!', A9),
      L('Buzz,_|buzz,_|round_|and_|round,', ACT),
      L('Hel|lo,_|bee!_|I_|love_|your_|sound!', H7)]
V2 = [L('Tap,_|tap,_|who_|is_|on_|the_|leaf?', Q7),
      L('A_|la|dy|bug_|with_|dots_|so_|neat!', A8),
      L('Crawl,_|crawl,_|up_|and_|down,', ACT),
      L('Hel|lo,_|la|dy|bug,_|on_|the_|ground!', H8)]
V3 = [L('Boing,_|boing,_|who_|is_|in_|the_|grass?', Q7),
      L('A_|crick|et_|jump|ing,_|one,_|two,_|three!', A8),
      L('Hop,_|hop,_|way_|up_|high,', ACT),
      L('Hel|lo,_|crick|et,_|touch_|the_|sky!', H7)]
V4 = [L('Flap,_|flap,_|who_|is_|on_|the_|rose?', Q7),
      L('A_|but|ter|fly,_|as_|bright_|as_|can_|be!', A9),
      L('Flap,_|flap,_|flut|ter_|by,', ACT),
      L('Hel|lo,_|but|ter|fly,_|wav|ing_|hi!', H8)]
CH = [L('In_|the_|gar|den,_|in_|the_|sun,', [('C5',.5),('C5',.5),('A4',1),('C5',1),('F5',1),('E5',1),('D5',2),('r',1)]),
      L('Lit|tle_|bugs_|have_|so_|much_|fun!', [('C5',1),('G4',1),('C5',1),('E5',1),('D5',1),('C5',1),('D5',1),('r',1)]),
      L('Buzz_|and_|crawl_|and_|hop_|and_|fly,', [('A4',1),('A4',.5),('C5',.5),('F5',1),('E5',1),('C5',1),('D5',2),('r',1)]),
      L('Gar|den_|friends,_|say_|hi,_|hi,_|hi!', [('G5',1),('E5',1),('C5',1),('E5',1),('D5',1),('B4',1),('C5',2)])]
OUT = [CH[2],
       L('See_|you_|soon,_|my_|gar|den_|friends!', [('G5',1),('E5',1),('C5',1),('E5',1),('D5',1),('B4',1),('C5',2)])]

VERSE_CH = [['C','C','F','F'], ['G','G','C','C'], ['F','F','C','C'], ['G','G','C','C']]
CHOR_CH = [['F','F','C','C'], ['F','F','G','G'], ['Am','Am','F','F'], ['G','G','C','C']]

SECTIONS = []
t = 0.0
def add(name, kind, lines, chords, theme, beats=None):
    global t
    b = beats if beats is not None else 8 * len(lines)
    SECTIONS.append(dict(name=name, kind=kind, lines=lines, chords=chords, theme=theme, start=t, beats=b))
    t += b

add('intro', 'intro', [], [['C','C','F','F'], ['G','G','C','C']], 'title', 16)
add('v1', 'verse', V1, VERSE_CH, 'bee')
add('v2', 'verse', V2, VERSE_CH, 'ladybug')
add('ch1', 'chorus', CH, CHOR_CH, 'garden')
add('v3', 'verse', V3, VERSE_CH, 'cricket')
add('v4', 'verse', V4, VERSE_CH, 'butterfly')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'garden')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'garden')
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
