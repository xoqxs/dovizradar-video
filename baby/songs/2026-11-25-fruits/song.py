"""Song: "Yummy Fruits, Who Is Hiding?" (fruits). Times in beats."""
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

Q7 = [('E5',1),('E5',1),('G5',.5),('F5',.5),('E5',.5),('D5',.5),('E5',1),('r',3)]
A8 = [('C5',.5),('D5',.5),('E5',.5),('F5',.5),('G5',1),('E5',.5),('D5',.5),('C5',2),('r',2)]
ACT = [('G5',1),('G5',1),('E5',1),('F5',1),('G5',2),('r',2)]
H6 = [('A4',.5),('C5',.5),('D5',1),('E5',1),('D5',1),('C5',2),('r',2)]

V1 = [L('Crunch,_|crunch,_|who_|is_|in_|the_|tree?', Q7),
      L('A_|shi|ny,_|red_|ap|ple,_|crunch,_|yum!', A8),
      L('Crunch,_|crunch,_|yum,_|yum,_|yum!', ACT),
      L('In_|my_|pic|nic_|bas|ket!', H6)]
V2 = [L('Peel,_|peel,_|who_|is_|hi|ding_|here?', Q7),
      L('A_|long_|and_|yel|low_|ba|na|na!', A8),
      L('Peel,_|peel,_|yum,_|yum,_|yum!', ACT),
      L('In_|my_|pic|nic_|bas|ket!', H6)]
V3 = [L('Squish,_|squish,_|who_|is_|small_|and_|red?', Q7),
      L('A_|sweet_|and_|jui|cy_|straw|ber|ry!', A8),
      L('Squish,_|squish,_|yum,_|yum,_|yum!', ACT),
      L('In_|my_|pic|nic_|bas|ket!', H6)]
V4 = [L('Munch,_|munch,_|who_|is_|green_|and_|round?', Q7),
      L('A_|soft_|and_|slee|py_|lit|tle_|pear!', A8),
      L('Munch,_|munch,_|yum,_|yum,_|yum!', ACT),
      L('In_|my_|pic|nic_|bas|ket!', H6)]
CH = [L('Ap|ple,_|ba|na|na,_|straw|ber|ry,_|pear,', [('E5',.5),('E5',.5),('G5',.5),('E5',.5),('C5',1),('D5',.5),('E5',.5),('F5',1),('E5',1),('r',2)]),
      L('Yum|my_|fruits_|for_|you_|and_|me!', [('D5',.5),('D5',.5),('E5',1),('F5',.5),('E5',.5),('D5',1),('C5',2),('r',2)]),
      L('On_|the_|farm_|we_|fill_|our_|bas|ket,', [('A4',.5),('C5',.5),('C5',1),('F5',.5),('F5',.5),('E5',1),('D5',.5),('C5',.5),('r',3)]),
      L('Pic|nic_|time,_|hoo|ray,_|hoo|ray!', [('G5',.5),('F5',.5),('E5',1),('D5',.5),('E5',.5),('D5',1),('C5',2),('r',2)])]
OUT = [L('Crunch,_|peel,_|squish_|and_|munch,_|yum,_|yum,_|yum!', [('E5',1),('D5',1),('C5',1),('D5',.5),('E5',.5),('G5',1),('E5',1),('C5',1),('r',1)]),
       L('Bye_|bye,_|friends,_|let\'s_|eat_|and_|play!', [('G5',1),('E5',1),('C5',1),('D5',1),('B4',1),('D5',1),('C5',1),('r',1)])]

VERSE_CH = [['C','C','F','F'], ['G','G','C','C'], ['C','C','G','G'], ['F','G','C','C']]
CHOR_CH = [['C','C','F','F'], ['G','G','C','C'], ['Am','Am','F','F'], ['G','G','C','C']]

# sections: (name, kind, lines, chords per line (4 x 2-beat), theme)
SECTIONS = []
t = 0.0
def add(name, kind, lines, chords, theme, beats=None):
    global t
    b = beats if beats is not None else 8 * len(lines)
    SECTIONS.append(dict(name=name, kind=kind, lines=lines, chords=chords, theme=theme, start=t, beats=b))
    t += b

add('intro', 'intro', [], [['C','C','F','F'], ['G','G','C','C']], 'title', 16)
add('v1', 'verse', V1, VERSE_CH, 'apple')
add('v2', 'verse', V2, VERSE_CH, 'banana')
add('ch1', 'chorus', CH, CHOR_CH, 'fruit')
add('v3', 'verse', V3, VERSE_CH, 'strawberry')
add('v4', 'verse', V4, VERSE_CH, 'pear')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'fruit')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'fruit')
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
