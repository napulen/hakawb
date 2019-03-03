import logging
import pprint as pp
import mido
import sys

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

if __name__ == '__main__':
    input_notes = [60, 62, 64, 65, 67, 69, 71, 60]
    if sys.argv[1]:
        input_notes = get_notes_from_midi(sys.argv[1])
    logger = initLogger()
    # Pre-compute all the chord dictionary
    import chord
    major_pc_sets = get_pc_sets(chord.base_major, major_keys)
    minor_pc_sets = get_pc_sets(chord.base_minor, minor_keys)
    all_pc_sets = add_pc_sets(major_pc_sets, minor_pc_sets)
    # Now parse the input
    bass = 128 # Larger than any midi note number for initialization
    segments = []
    basses = []
    current_segment = []
    current_set = set()
    relevant_sets = all_pc_sets.keys()
    for note in input_notes:
        logger.info("Parsing note {}".format(note))
        note_pc = note % 12
        tmp_segment = current_segment[:]
        tmp_set = current_set
        tmp_segment.append(note)
        tmp_set = tmp_set | {note_pc}
        query_sets = [pc for pc in relevant_sets if tmp_set <= pc]
        logger.info('Possible pitch-class sets: {}'.format(len(query_sets)))
        logger.debug(query_sets)
        if len(query_sets) > 0:
            logger.info('Successfully part of the same segment')
            relevant_sets = query_sets
            current_segment = tmp_segment
            current_set = tmp_set
        else:
            logger.info('This note cannot belong to the same segment')
            # Log everything until this note
            segments.append(current_segment)
            basses.append(bass)
            logger.info('Segments: {}'.format(segments))
            logger.info('Basses: {}'.format(basses))
            # Now start a new segment
            current_segment = [note]
            current_set = {note_pc}
            relevant_sets = all_pc_sets.keys()
            bass = 128
        if note < bass:
            logger.info("This note became the new bass")
            bass = note
        chord_query = []
        for pc_set in relevant_sets:
            chordsobjs = all_pc_sets[pc_set]
            for chord in chordsobjs:
                if (bass % 12) == chord.bass:
                    chord_query.append(chord.harmstr)
        logger.info('Possible chords: {}'.format(len(chord_query)))
        logger.info(chord_query)
    if current_segment:
        segments.append(current_segment)
        basses.append(bass)
    logger.info('Segments: {}'.format(segments))
    logger.info('Basses: {}'.format(basses))









