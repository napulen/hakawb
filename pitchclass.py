import logging
import math

class PitchClass:
    def __init__(self):
        self.logger = logging.getLogger('hakawb.PitchClass')
        self.logger.info('Creating new pitch class')
        self.heat = 0
        self.internal_t = 128
        self.delta_t = 0
        self.note_on = False
        self.heat_function = self.release

    def attack(self, alpha=3):
        #return max(-self.internal_t/4.0 + 1.0, 0.5)
        return max(-(math.tanh(alpha*self.internal_t - 3) - 1) / 2.0, 0.5)

    def release(self, alpha=3):
        #return max(-self.internal_t/2.0 + 0.5, 0.0)
        return max(-(math.tanh(alpha*self.internal_t) - 1) / 2.0, 0.0)

    def update(self, delta_t, note_on):
        if self.note_on != note_on:
            self.note_on = note_on
            self.heat_function = self.attack if note_on else self.release
            self.internal_t = 0
        else:
            self.internal_t += delta_t
        self.heat = self.heat_function()
