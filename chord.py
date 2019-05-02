import logging

pitch_classes = ['c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'ab', 'a', 'bb', 'b']

base_major = {
    # Diatonic major triads
    'I':    [0, 4, 7],
    'ii':   [2, 5, 9],
    'iii':  [4, 7, 11],
    'IV':   [5, 9, 0],
    'V':    [7, 11, 2],
    'vi':   [9, 0, 4],
    'viio': [11, 2, 5],
    # Diatonic major sevenths
    'IM7':   [0, 4, 7, 11],
    'ii7':   [2, 5, 9, 0],
    'iii7':  [4, 7, 11, 2],
    'IVM7':  [5, 9, 0, 4],
    'V7':    [7, 11, 2, 5],
    'vi7':   [9, 0, 4, 7],
    'viio7': [11, 2, 5, 9],
    # Chromatic alterations
    'N':  [1, 5, 8],
    'Lt': [6, 8, 0],
    'Fr': [6, 8, 0, 2],
    'Gn': [6, 8, 0, 3]
}

base_minor = {
    # Diatonic natural minor triads
    'i': [0, 3, 7],
    'iio': [2, 5, 8],
    'III': [3, 7, 10],
    'iv': [5, 8, 0],
    'v': [7, 10, 2],
    'VI': [8, 0, 3],
    '-VII': [10, 2, 5],
    # Diatonic harmonic minor triads
    '#III': [3, 7, 11],
    'V': [7, 11, 2],
    'viio': [11, 2, 5],
    # Diatonic melodic minor triads
    'ii': [2, 5, 9],
    'IV': [5, 9, 0],
    '#vio': [9, 0, 3],
    # Diatonic natural minor sevenths
    'i7': [0, 3, 7, 10],
    'iio7': [2, 5, 8, 0],
    'IIIM7': [3, 7, 10, 2],
    'iv7': [5, 8, 0, 3],
    'v7': [7, 10, 2, 5],
    'VIM7': [8, 0, 3, 7],
    '-VII7': [10, 2, 5, 8],
    # Diatonic harmonic minor sevenths
    'iM7': [0, 3, 7, 11],
    '+IIIM7': [3, 7, 11, 2],
    'V7': [7, 11, 2, 5],
    'viioD7': [11, 2, 5, 8],
    # Diatonic melodic minor sevenths
    'ii7': [2, 5, 9, 0],
    'IV7': [5, 9, 0, 3],
    '#vio7': [9, 0, 3, 7],
    'viio7': [11, 2, 5, 9],
    # Chromatic alterations
    'N': [1, 5, 8],
    'Lt': [6, 8, 0],
    'Fr': [6, 8, 0, 2],
    'Gn': [6, 8, 0, 3]
}

class Chord:
    def __init__(self, harmstr):
        self.logger = logging.getLogger('hakawb.Chord')
        self.logger.debug('Instantiating chord {}...'.format(harmstr))
        split = harmstr.split(':')
        # Expecting chords in the form Key:Harm, e.g., C:Vc
        if len(split) == 2:
            key, harm = split
            self.logger.debug('Key:{}, harm:{}'.format(key, harm))
        else:
            key = 'C'
            harm = split[0]
            self.logger.warn('No key provided, assuming C')
            self.logger.debug('harm:{}'.format(harm))
        # All lower-case harm strings mean minor mode
        base_chords = base_minor if key.islower() else base_major
        key_offset = pitch_classes.index(key.lower())
        inversion = 0
        rootpos, firstinv, _ = harm.rpartition('b')
        if firstinv:
            self.logger.debug('Chord is in 1st inversion')
            harm = rootpos
            inversionY = 1
        else:
            rootpos, secinv, _ = harm.rpartition('c')
            if secinv:
                self.logger.debug('Chord is in 2nd inversion')
                harm = rootpos
                inversion = 2
            else:
                rootpos, thirdinv, _ = harm.rpartition('d')
                if thirdinv:
                    self.logger.debug('Chord is in 3rd inversion')
                    harm = rootpos
                    inversion = 3
        pc_list = base_chords[harm]
        self.logger.debug('Base pitch classes: {}'.format(pc_list))
        pc_list = [(x + key_offset) % 12 for x in pc_list]
        self.logger.debug('Base pitch classes in the right key: {}'.format(pc_list))
        self.harmstr = harmstr
        self.harm = harm
        self.key = key
        self.inversion = inversion
        self.pitch_classes = frozenset(pc_list)
        self.bass = pc_list[inversion]