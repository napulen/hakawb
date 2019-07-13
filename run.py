import logging
import numpy as np
import pprint as pp
import sys
import math
import chord
import pcset
import pitchclass
import chordlabels
import pitch_class_vector
import midi_reverser
import midi_wrapper
import bass

major_keys = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
minor_keys = [k.lower() for k in major_keys]

def initLogger():
    logger = logging.getLogger('hakawb')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('hakawb.log', 'w')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

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

if __name__ == '__main__':
    logger = initLogger()
    if len(sys.argv) != 2:
        logger.error('Usage: {} <input_file>.mid'.format(sys.argv[0]))
        exit()
    # Get the midi messages from a library using the wrapper
    wrapper = midi_wrapper.MidoWrapper(sys.argv[1])
    # Initialize the midi reverser
    midi_rev = midi_reverser.MidiReverser()
    # Pre-compute all the chord dictionary
    major_pc_sets = get_pc_sets(chord.base_major, major_keys)
    minor_pc_sets = get_pc_sets(chord.base_minor, minor_keys)
    pc_sets = instantiate_pc_sets(major_pc_sets, minor_pc_sets)
    # Now parse the input
    # pc_heat_dict = {}
    # pc_set_activations = {pc_set.name: [] for pc_set in pc_sets}
    # max_activations = {}
    # basses = []
    forward = pitch_class_vector.PitchClassVector(decay_damping=0.3, release_damping=0.05, scaling=True)
    bass_model = bass.BassModel()
    for msg in wrapper.midi_messages:
        midi_rev.dispatch(msg)
        forward.dispatch(msg)
        # pc_heat = forward.pc_heat
        # logger.debug(pc_heat)
        # bass_model.dispatch(msg)
        # basses.append(bass_model.bass)
        # max_activation = (0, 'none')
        # for pc_set in pc_sets:
        #     pc_set.compute_activation(pc_heat)
        #     if pc_set.activation > max_activation[0]:
        #         max_activation = (pc_set.activation, pc_set.pc_set)
        #     pc_set_activations[pc_set.name].append('{:.2f}'.format(pc_set.activation))
        # max_activations[forward.t] = max_activation

    # for pc in pc_heat_dict:
    #     logger.info('{}: {}'.format(pc, pc_heat_dict[pc]))
    # logger.info('{:<30} {}'.format('Basses', basses))
    # for name, activation_list in pc_set_activations.items():
    #     logger.info('{:<30} {}'.format(name, activation_list))

    # for pc_activation in max_activations:
    #     logger.info('{}: {} - {}'.format(pc_activation, max_activations[pc_activation], chordlabels.chord_labels[max_activations[pc_activation][1]]))

    # forward_labels = [chordlabels.chord_labels[max_activations[pc_activation][1]] for pc_activation in max_activations]

    # pc_heat_dict = {}
    # pc_set_activations = {pc_set.name: [] for pc_set in pc_sets}
    # max_activations = {}
    backward = pitch_class_vector.PitchClassVector(decay_damping=0.3, release_damping=0.05, scaling=True)
    for msg in midi_rev.output():
        backward.dispatch(msg)
    #     pc_energy = backward.pc_energy
    #     logger.debug(pc_energy)
    #     max_activation = (0, 'none')
    #     for pc_set in pc_sets:
    #         pc_set.compute_activation(pc_heat)
    #         if pc_set.activation > max_activation[0]:
    #             max_activation = (pc_set.activation, pc_set.pc_set)
    #         pc_set_activations[pc_set.name].append('{:.2f}'.format(pc_set.activation))
    #     max_activations[backward.t] = max_activation

    # for pc in pc_heat_dict:
    #     logger.info('{}: {}'.format(pc, pc_heat_dict[pc]))
    # for name, activation_list in pc_set_activations.items():
    #     logger.info('{:<30} {}'.format(name, activation_list))

    # for pc_activation in max_activations:
    #     logger.info('{}: {} - {}'.format(pc_activation, max_activations[pc_activation], chordlabels.chord_labels[max_activations[pc_activation][1]]))

    # backward_labels = [chordlabels.chord_labels[max_activations[pc_activation][1]] for pc_activation in max_activations]
    # backward_labels = list(reversed(backward_labels))

    # for i in range(len(forward_labels)):
    #     print('{:<10}'.format(forward_labels[i]), end='')

    # print()

    # for i in range(len(backward_labels)):
    #     print('{:<10}'.format(backward_labels[i]), end='')