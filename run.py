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

major_pc_sets = {}

if __name__ == '__main__':
    logger = initLogger()
    import chord
    major = chord.base_major
    major_harm = major.keys()
    for key in major_keys:
        for inversion in ['', 'b', 'c', 'd']:
            for harm in major_harm:
                chordstr = '{}:{}{}'.format(key, harm, inversion)
                if inversion == 'd':
                    if harm != 'Gn' and harm != 'Fr' and not '7' in harm:
                        continue
                c = chord.Chord(chordstr)
                logger.info('{} | {} {} | {} | inversion {} | bass {} | {}'.format(c.harmstr, c.key, 'minor' if c.key.islower() else 'major', c.harm, c.inversion, c.bass, c.pitch_classes))
                pc_set = major_pc_sets.get(c.pitch_classes, [])
                pc_set.append(c.harmstr)
                major_pc_sets[c.pitch_classes] = pc_set
    pp.pprint(major_pc_sets)




