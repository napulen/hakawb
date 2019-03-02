import logging

def initLogger():
    logger = logging.getLogger('hakawb')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return logger

major_keys = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
minor_keys = [k.lower() for k in major_keys]

if __name__ == '__main__':
    logger = initLogger()
    import chord_dictionary as cd
    major = cd.base_major
    major_harm = major.keys()
    for key in major_keys:
        for inversion in ['', 'b', 'c', 'd']:
            for harm in major_harm:
                chord = '{}:{}{}'.format(key, harm, inversion)
                if inversion == 'd':
                    if harm != 'Gn' and harm != 'Fr' and not '7' in harm:
                        continue
                logger.info(chord)


