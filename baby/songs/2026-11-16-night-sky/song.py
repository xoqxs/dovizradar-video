"""Song: "Who Is Awake at Night?" (bedtime / night sky). Times in beats."""
BPM = 102
BEAT = 60.0 / BPM

N = {'E4': 64, 'G4': 67, 'A4': 69, 'B4': 71, 'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79}

def L(text, notes):
    syl = text.split('|')
    pitched = [n for n in notes if n[0] != 'r']
    assert len(syl) == len(pitched), (text, len(syl), len(pitched))
    assert abs(sum(n[1] for n in notes) - 8) < 1e-9, text
    return {'syl': syl, 'notes': notes}

Q7 = [('G4',1),('G4',1),('C5',.5),('C5',.5),('E5',.5),('D5',.5),('C5',1),('r',3)]
A8 = [('D5',.5),('D5',.5),('B4',.5),('G4',.5),('B4',1),('D5',.5),('D5',.5),('C5',2),('r',2)]
ACT = [('A4',1),('A4',1),('C5',1),('F5',1),('E5',2),('r',2)]
H7 = [('D5',.5),('D5',.5),('B4',1),('D5',.5),('E5',.5),('D5',.5),('C5',2),('r',2.5)]

V1 = [L('Shh,_|shh,_|who_|is_|in_|the_|sky?', Q7),
      L('The_|round,_|round_|moon,_|so_|big_|and_|bright!', A8),
      L('Glow,_|glow,_|soft_|and_|slow,', ACT),
      L('Hel|lo,_|moon,_|you_|light_|the_|night!', H7)]
V2 = [L('Blink,_|blink,_|who_|is_|shin|ing_|high?', Q7),
      L('A_|lit|tle_|star,_|a_|spark|ly_|light!', A8),
      L('Blink,_|blink,_|on_|and_|off,', ACT),
      L('Hel|lo,_|star,_|you_|wink_|so_|soft!', H7)]
V3 = [L('Hoo,_|hoo,_|who_|is_|in_|the_|tree?', Q7),
      L('An_|owl_|with_|big_|round_|eyes,_|I_|see!', A8),
      L('Hoo,_|hoo,_|hop,_|hop,_|hop,', ACT),
      L('Hel|lo,_|owl,_|what_|a_|big_|hop!', H7)]
V4 = [L('Whoosh,_|whoosh,_|who_|is_|float|ing_|by?', Q7),
      L('A_|sleep|y_|cloud,_|so_|soft_|and_|white!', A8),
      L('Float,_|float,_|slow,_|slow,_|slow,', ACT),
      L('Hel|lo,_|cloud,_|a_|pil|low_|bed!', H7)]
CH = [L('When_|the_|night_|is_|soft_|and_|blue,', [('A4',.5),('C5',.5),('F5',1),('E5',1),('C5',1),('D5',1),('C5',2),('r',1)]),
      L('Friends_|are_|a|wake_|to_|sing_|with_|you!', [('C5',.5),('C5',.5),('A4',1),('C5',.5),('D5',.5),('E5',1),('D5',1),('B4',2),('r',1)]),
      L('Moon_|and_|star_|and_|owl_|and_|cloud,', [('E5',1),('E5',.5),('C5',.5),('A4',1),('C5',1),('F5',1),('E5',2),('r',1)]),
      L('Sing_|it_|qui|et,_|not_|too_|loud!', [('D5',.5),('D5',.5),('B4',1),('G4',1),('D5',1),('B4',1),('C5',2),('r',1)])]
OUT = [L('Good_|night,_|good_|night,_|close_|your_|eyes,', [('E5',1),('E5',1),('C5',1),('A4',1),('C5',1),('D5',1),('E5',1),('r',1)]),
       L('See_|you_|soon,_|my_|night_|time_|friends!', [('G5',1),('E5',1),('C5',1),('E5',1),('D5',1),('B4',1),('C5',2)])]

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
add('v1', 'verse', V1, VERSE_CH, 'moon')
add('v2', 'verse', V2, VERSE_CH, 'star')
add('ch1', 'chorus', CH, CHOR_CH, 'night')
add('v3', 'verse', V3, VERSE_CH, 'owl')
add('v4', 'verse', V4, VERSE_CH, 'cloud')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'night')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'night')
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
