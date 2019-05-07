import logging
import numpy as np
import pprint as pp
import mido
import sys
import math
import chord
import pcset
import pitchclass
import chordlabels
import heat

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

def instantiate_pc_sets(major, minor):
    pc_sets = []
    pc_set_keys = list(major.keys()) + list(minor.keys())
    for pc_set in sorted(set(pc_set_keys)):
        chords = []
        if pc_set in major:
            chords.extend(major[pc_set])
        if pc_set in minor:
            chords.extend(minor[pc_set])
        pc_set_obj = pcset.PitchClassSet(pc_set, chords)
        pc_sets.append(pc_set_obj)
    return pc_sets

# def heat_tanh(x, alpha):
#     return max(-0.5 * (math.tanh(alpha*x - 4) - 1), 0.01)

# def heat_linear(x, alpha):
#     return max(-(x/alpha) + 1, 0.0)

# def heat_exponential(x, alpha):
#     return max(-alpha**x + 2, 0.0)

# def heat_function(x, alpha):
#     return heat_exponential(x, alpha)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        mid = mido.MidiFile(sys.argv[1])
    logger = initLogger()
    # Pre-compute all the chord dictionary
    major_pc_sets = get_pc_sets(chord.base_major, major_keys)
    minor_pc_sets = get_pc_sets(chord.base_minor, minor_keys)
    pc_sets = instantiate_pc_sets(major_pc_sets, minor_pc_sets)
    # Now parse the input
    # bass = 128 # Larger than any midi note number for initialization
    # pc_on = [0] * 12
    # t = 0
    # pc_heat_dict = {}
    # pc_heat_objs = [pitchclass.PitchClass() for x in range(12)]
    # pc_set_activations = {pc_set.name: [] for pc_set in pc_sets}
    # max_activations = {}
    # basses = []

    midi2pcheat = heat.Midi2PitchClassHeat()

    for msg in mid:
        if msg.type != 'note_on' and msg.type != 'note_off':
            continue
        pc_heat = midi2pcheat.parse_midi_event(msg)
        logger.debug(pc_heat)
    for t, val in midi2pcheat.pc_heat_dict.items():
        logger.info('{}: {}'.format(t, val))
    #     if note < bass:
    #         logger.info("This note became the new bass")
    #         bass = note
    #     basses.append(bass)

    #     max_activation = (0, 'none')
    #     for pc_set in pc_sets:
    #         pc_set.compute_activation(pc_current_heat)
    #         if pc_set.activation > max_activation[0]:
    #             max_activation = (pc_set.activation, pc_set.pc_set)
    #         pc_set_activations[pc_set.name].append('{:.2f}'.format
    #         (pc_set.activation))
    #     if note_on:
    #         max_activations[t] = max_activation

    # for pc in pc_heat_dict:
    #     logger.info('{}: {}'.format(pc, pc_heat_dict[pc]))
    # logger.info('{:<30} {}'.format('Basses', basses))
    # for name, activation_list in pc_set_activations.items():
    #     logger.info('{:<30} {}'.format(name, activation_list))

    # for pc_activation in max_activations:
    #     logger.info('{}: {} - {}'.format(pc_activation, max_activations[pc_activation], chordlabels.chord_labels[max_activations[pc_activation][1]]))
