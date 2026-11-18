"""Song: "Tidy Up and Count!" (counting 1-4 with toys). Times in beats."""
BPM = 110
BEAT = 60.0 / BPM

N = {'E4': 64, 'G4': 67, 'A4': 69, 'B4': 71, 'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79}

def L(text, notes):
    syl = text.split('|')
    pitched = [n for n in notes if n[0] != 'r']
    assert len(syl) == len(pitched), (text, len(syl), len(pitched))
    assert abs(sum(n[1] for n in notes) - 8) < 1e-9, text
    return {'syl': syl, 'notes': notes}

Q7 = [('E5',1),('E5',1),('C5',.5),('D5',.5),('E5',.5),('D5',.5),('C5',1),('r',3)]
A8 = [('G4',.5),('A4',.5),('C5',.5),('C5',.5),('D5',1),('E5',.5),('D5',.5),('C5',2),('r',2)]
ACT = [('C5',1),('C5',1),('E5',1),('G5',1),('E5',2),('r',2)]
H7 = [('F5',.5),('E5',.5),('D5',1),('C5',.5),('D5',.5),('B4',.5),('C5',2),('r',2.5)]

V1 = [L('Bounce,_|bounce,_|what_|is_|on_|the_|floor?', Q7),
      L('A_|big_|red_|ball,_|so_|round_|and_|fun!', A8),
      L('Bounce,_|bounce,_|in_|the_|box,', ACT),
      L('One,_|one_|toy_|is_|in_|the_|box!', H7)]
V2 = [L('Clack,_|clack,_|what_|is_|on_|the_|rug?', Q7),
      L('A_|lit|tle_|block,_|so_|blue_|and_|square!', A8),
      L('Clack,_|clack,_|in_|the_|box,', ACT),
      L('One,_|two_|toys_|are_|in_|the_|box!', H7)]
V3 = [L('Vroom,_|vroom,_|what_|is_|by_|the_|bed?', Q7),
      L('A_|lit|tle_|car_|that_|goes_|so_|fast!', A8),
      L('Vroom,_|vroom,_|in_|the_|box,', ACT),
      L('One,_|two,_|three_|toys_|in_|the_|box!', H7)]
V4 = [L('Squeak,_|squeak,_|what_|is_|in_|the_|tub?', Q7),
      L('A_|yel|low_|duck_|that_|loves_|to_|float!', A8),
      L('Squeak,_|squeak,_|in_|the_|box,', ACT),
      L('One,_|two,_|three,_|four_|in_|the_|box!', H7)]
CH = [L('Ti|dy_|up,_|ti|dy_|up,_|one,_|two,_|three,', [('C5',.5),('C5',.5),('E5',1),('C5',.5),('C5',.5),('E5',1),('F5',1),('E5',1),('D5',1),('r',1)]),
      L('Ev|ery_|toy_|goes_|home_|with_|me!', [('D5',.5),('D5',.5),('B4',1),('D5',1),('E5',1),('D5',1),('C5',2),('r',1)]),
      L('Ball_|and_|block_|and_|car_|and_|duck,', [('A4',1),('C5',.5),('C5',.5),('F5',1),('F5',1),('E5',1),('C5',2),('r',1)]),
      L('Now_|my_|room_|is_|clean,_|what_|luck!', [('G5',.5),('E5',.5),('D5',1),('B4',1),('D5',1),('D5',1),('C5',2),('r',1)])]
OUT = [L('Ti|dy,_|ti|dy,_|all_|done_|now,', [('E5',1),('D5',1),('E5',1),('C5',1),('D5',1),('E5',1),('C5',1),('r',1)]),
       L('Bye_|bye,_|toys,_|take_|a_|bow!', [('G5',1),('E5',1),('C5',1),('D5',1),('B4',1),('C5',2),('r',1)])]

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
add('v1', 'verse', V1, VERSE_CH, 'ball')
add('v2', 'verse', V2, VERSE_CH, 'block')
add('ch1', 'chorus', CH, CHOR_CH, 'tidy')
add('v3', 'verse', V3, VERSE_CH, 'car')
add('v4', 'verse', V4, VERSE_CH, 'duck')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'tidy')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'tidy')
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
