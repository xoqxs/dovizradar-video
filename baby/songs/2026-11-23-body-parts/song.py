"""Song: "Who Can Move With Me?" (body parts / moving). Times in beats."""
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

Q7 = [('C5',1),('C5',1),('E5',.5),('E5',.5),('G5',.5),('E5',.5),('D5',1),('r',3)]
A8 = [('F5',.5),('F5',.5),('E5',.5),('D5',.5),('E5',1),('D5',.5),('B4',.5),('C5',2),('r',2)]
ACT = [('E5',1),('E5',1),('C5',1),('D5',1),('E5',2),('r',2)]
H6 = [('G5',.5),('E5',.5),('D5',1),('E5',1),('D5',1),('C5',2),('r',2)]

V1 = [L('Clap,_|clap,_|who_|can_|move_|with_|me?', Q7),
      L('Two_|lit|tle_|hands_|that_|clap_|so_|loud!', A8),
      L('Clap,_|clap,_|one,_|two,_|three!', ACT),
      L('Move_|with_|me,_|clap,_|clap,_|clap!', H6)]
V2 = [L('Stomp,_|stomp,_|who_|can_|move_|with_|me?', Q7),
      L('Two_|lit|tle_|feet_|that_|stomp_|the_|floor!', A8),
      L('Stomp,_|stomp,_|one,_|two,_|three!', ACT),
      L('Move_|with_|me,_|stomp,_|stomp,_|stomp!', H6)]
V3 = [L('Sniff,_|sniff,_|who_|can_|move_|with_|me?', Q7),
      L('A_|lit|tle_|nose_|that_|wig|gles_|too!', A8),
      L('Sniff,_|sniff,_|one,_|two,_|three!', ACT),
      L('Move_|with_|me,_|sniff,_|sniff,_|sniff!', H6)]
V4 = [L('Wig|gle,_|who_|can_|move_|with_|me?', Q7),
      L('Two_|lit|tle_|ears_|that_|hear_|a_|song!', A8),
      L('Wig|gle,_|wig|gle,_|wee!', ACT),
      L('Move_|with_|me,_|wig|gle_|ears!', H6)]
CH = [L('Clap_|and_|stomp_|and_|sniff_|and_|wig|gle,', [('E5',1),('E5',.5),('G5',.5),('E5',1),('C5',.5),('D5',.5),('E5',1),('D5',1),('r',2)]),
      L('Ev|ery|bo|dy_|loves_|to_|move!', [('C5',.5),('D5',.5),('E5',.5),('F5',.5),('G5',1),('E5',1),('C5',2),('r',2)]),
      L('In_|my_|room,_|from_|head_|to_|toe,', [('A4',1),('C5',.5),('C5',.5),('F5',1),('F5',.5),('E5',.5),('D5',1),('r',3)]),
      L('Wig|gle,_|wig|gle,_|here_|we_|go!', [('G5',.5),('F5',.5),('E5',.5),('D5',.5),('D5',1),('B4',1),('C5',2),('r',2)])]
OUT = [L('Clap,_|stomp,_|sniff,_|wig|gle,_|what_|a_|day,', [('E5',1),('D5',1),('C5',1),('D5',.5),('E5',.5),('G5',1),('E5',1),('C5',1),('r',1)]),
       L('Bye_|bye,_|friends,_|let\'s_|move_|and_|play!', [('G5',1),('E5',1),('C5',1),('D5',1),('B4',1),('D5',1),('C5',1),('r',1)])]

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
add('v1', 'verse', V1, VERSE_CH, 'hand')
add('v2', 'verse', V2, VERSE_CH, 'foot')
add('ch1', 'chorus', CH, CHOR_CH, 'move')
add('v3', 'verse', V3, VERSE_CH, 'nose')
add('v4', 'verse', V4, VERSE_CH, 'ear')
add('ch2', 'chorus', CH + CH, CHOR_CH + CHOR_CH, 'move')
add('outro', 'outro', OUT, [CHOR_CH[2], CHOR_CH[3]], 'move')
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
