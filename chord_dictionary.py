
major_dictionary = {
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
    'Gr': [6, 8, 0, 3]
}


minor_dictionary = {
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
    'Gr': [6, 8, 0, 3]
}