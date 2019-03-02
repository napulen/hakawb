import logging
import pprint as pp

def initLogger():
    logger = logging.getLogger('hakawb')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
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
                logger.info('{} | {} {} | {} | inversion {} | bass {} | {}'.format(c.harmstr, c.key, 'minor' if c.key.islower() else 'major', c.harm, c.inversion, c.bass, c.pitch_classes))
                pc_set = pc_sets.get(c.pitch_classes, [])
                pc_set.append(c.harmstr)
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


if __name__ == '__main__':
    logger = initLogger()
    import chord
    major_pc_sets = get_pc_sets(chord.base_major, major_keys)
    minor_pc_sets = get_pc_sets(chord.base_minor, minor_keys)
    all_pc_sets = add_pc_sets(major_pc_sets, minor_pc_sets)






