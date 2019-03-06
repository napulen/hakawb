import logging
import chord

class PitchClassSet:
    all_pcs = {pc for pc in range(12)}
    def __init__(self, pc_set, chords=None):
        self.logger = logging.getLogger('hakawb.PitchClassSet')
        self.pc_set = pc_set
        self.pc_set_prime = PitchClassSet.all_pcs - self.pc_set
        self.strength = 0
        self.relevance = 0
        self.activation = 0
        if chords:
            self.chords = chords
        else:
            self.chords = []

    def add_chords(self, chords):
        if chords:
            self.chords.extend(chords)

    def compute_strength(self, pc_heat):
        pcs = len(self.pc_set)
        strength = []
        for i in self.pc_set:
            strength.append(pc_heat[i])
        self.strength = sum(strength) / pcs
        return self.strength

    def compute_relevance(self, pc_heat):
        pcs_prime = len(self.pc_set_prime)
        relevance = []
        for i in self.pc_set_prime:
            relevance.append(pc_heat[i])
        self.relevance = 1 - (sum(strength) / pcs_prime)
        return self.relevance


    def compute_activation(self, pc_heat):
        compute_strength(pc_heat)
        compute_relevance(pc_heat)
        self.activation = self.strength * self.relevance
        return self.activation
