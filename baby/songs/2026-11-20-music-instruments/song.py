"""Song: "Boom, Ding, Who Can Play?" (music instruments). Times in beats."""
BPM = 106
BEAT = 60.0 / BPM

N = {'E4': 64, 'G4': 67, 'A4': 69, 'B4': 71, 'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79}

def L(text, notes):
    # text: syllables separated by '|'; '_' marks a space after the syllable
    syl = text.split('|')
    pitched = [n for n in notes if n[0] != 'r']
    assert len(syl) == len(pitched), (text, len(syl), len(pitched))
    assert abs(sum(n[1] for n in notes) - 8) < 1e-9, text
    return {'syl': syl, 'notes': notes}

Q7 = [('G4',1),('G4',1),('C5',.5),('C5',.5),('E5',.5),('D5',.5),('C5',1),('r',3)]
A8 = [('E5',.5),('E5',.5),('D5',.5),('C5',.5),('D5',1),('C5',.5),('A4',.5),('G4',2),('r',2)]
ACT = [('G4',1),('G4',1),('C5',1),('E5',1),('G5',2),('r',2)]
H6 = [('F5',.5),('E5',.5),('D5',1),('C5',1),('B4',1),('C5',2),('r',2)]

V1 = [L('Boom,_|boom,_|who_|is_|in_|the_|band?', Q7),
      L('A_|big_|round_|drum_|that_|makes_|a_|beat!', A8),
      L('Boom,_|boom,_|tap_|your_|feet,', ACT),
      L('Come_|and_|play,_|boom,_|boom,_|boom!', H6)]
V2 = [L('Toot,_|toot,_|who_|is_|in_|the_|band?', Q7),
      L('A_|shi|ny_|trum|pet,_|hear_|it_|blow!', A8),
      L('Toot,_|toot,_|puff_|your_|cheeks,', ACT),
      L('Come_|and_|play,_|toot,_|toot,_|toot!', H6)]
V3 = [L('Ding,_|ding,_|who_|is_|in_|the_|band?', Q7),
      L('A_|xy|lo|phone_|with_|rain|bow_|keys!', A8),
      L('Ding,_|ding,_|up_|we_|go,', ACT),
      L('Come_|and_|play,_|ding,_|ding,_|ding!', H6)]
V4 = [L('Shake,_|shake,_|who_|is_|in_|the_|band?', Q7),
      L('Ma|ra|cas,_|shake_|them_|high_|and_|low!', A8),
      L('Shake,_|shake,_|side_|to_|side,', ACT),
      L('Come_|and_|play,_|shake,_|shake,_|shake!', H6)]
CH = [L('Boom_|and_|toot_|and_|ding_|and_|shake,', [('C5',1),('C5',1),('E5',1),('E5',1),('G5',1),('E5',1),('D5',1),('r',1)]),
      L('What_|a_|hap|py_|sound_|we_|make!', [('D5',.5),('D5',.5),('B4',1),('D5',1),('E5',1),('D5',1),('C5',2),('r',1)]),
      L('In_|the_|park_|we_|play_|all_|day,', [('A4',1),('C5',.5),('C5',.5),('F5',1),('F5',1),('E5',1),('C5',2),('r',1)]),
      L('Come_|on,_|ev|ery|bo|dy,_|play!', [('G5',.5),('E5',.5),('D5',1),('B4',.5),('C5',.5),('D5',1),('C5',2),('r',2)])]
OUT = [L('Boom,_|toot,_|ding,_|shake,_|what_|a_|band,', [('E5',1),('D5',1),('E5',1),('C5',1),('D5',1),('E5',1),('C5',1),('r',1)]),
       L('Bye_|bye,_|friends,_|give_|a_|hand!', [('G5',1),('E5',1),('C5',1),('D5',1),('B4',1),('C5',2),('r',1)])]

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
add('v1', 'verse', V1, VERSE_CH, 'drum')
add('v2', 'verse', V2, VERSE_CH, 'trumpet')
add('ch1', 'chorus', CH, CHOR_CH, 'band')
add('v3', 'verse', V3, VERSE_CH, 'xylo')
add('v4', 'verse', V4, VERSE_CH, 'maracas')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'band')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'band')
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
