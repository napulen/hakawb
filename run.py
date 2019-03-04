import logging
import numpy as np
import pprint as pp
import mido
import sys
import math

def initLogger():
    logger = logging.getLogger('hakawb')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('hakawb.log', 'w')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

major_keys = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
minor_keys = [k.lower() for k in major_keys]

def get_pc_sets(base, keys):
    pc_sets = {}
    base_harm = base.keys()
    inversions = ['', 'b', 'c', 'd']
    for key in keys:
        for inversion in inversions:
            for harm in base_harm:
                harmstr = '{}:{}{}'.format(key, harm, inversion)
                if inversion == 'd':
                    if harm != 'Gn' and harm != 'Fr' and not '7' in harm:
                        continue
                c = chord.Chord(harmstr)
                logger.debug('{} | {} {} | {} | inversion {} | bass {} | {}'.format(c.harmstr, c.key, 'minor' if c.key.islower() else 'major', c.harm, c.inversion, c.bass, c.pitch_classes))
                pc_set = pc_sets.get(c.pitch_classes, [])
                pc_set.append(c)
                pc_sets[c.pitch_classes] = pc_set
    return pc_sets


def add_pc_sets(a, b):
    c = {}
    c_keys = list(a.keys()) + list(b.keys())
    for pc_set in set(c_keys):
        harms = []
        if pc_set in a:
            harms.extend(a[pc_set])
        if pc_set in b:
            harms.extend(b[pc_set])
        c[pc_set] = harms
    return c

def get_notes_from_midi(midi_file):
    """Returns a list of notes from the note_on events of a MIDI file"""
    mid = mido.MidiFile(midi_file)
    notes = [msg.note for msg in mid
             if msg.type == 'note_on'
             and msg.velocity > 0]
    return notes

def heat_formula(x, alpha):
    return max(-0.5 * (math.tanh(alpha*x - 4) - 1), 0.01)

if __name__ == '__main__':
    input_notes = [60, 64, 67, 59, 62, 65, 67]
    if len(sys.argv) == 2:
        input_notes = get_notes_from_midi(sys.argv[1])
    logger = initLogger()
    # Pre-compute all the chord dictionary
    import chord
    major_pc_sets = get_pc_sets(chord.base_major, major_keys)
    minor_pc_sets = get_pc_sets(chord.base_minor, minor_keys)
    all_pc_sets = add_pc_sets(major_pc_sets, minor_pc_sets)
    # Now parse the input
    bass = 128 # Larger than any midi note number for initialization
    pc_last_active = [3] * 12
    pc_heat = {pc: [] for pc in range(12)}
    alpha = 2
    basses = []
    for note in input_notes[:40]:
        logger.info("Parsing note {}".format(note))
        note_pc = note % 12
        pc_last_active = [x+1 for x in pc_last_active]
        pc_last_active[note_pc] = 0
        pc_current_heat = [heat_formula(x, alpha) for x in pc_last_active]
        for pc, l in pc_heat.items():
            l.append(pc_current_heat[pc])
        if note < bass:
            logger.info("This note became the new bass")
            bass = note
        basses.append(bass)
    for l in pc_heat.values():
        s = ''
        for n in l:
            s += '{:.1f}  '.format(n)
        logger.info(s)
    logger.info('{:<30} {}'.format('Basses', basses))








