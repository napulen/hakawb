import logging
import math

class NoteAttack:
    def __init__(self, decay_damping=0.8, release_damping=0.1):
        self.logger = logging.getLogger('hakawb.NoteAttack')
        self.logger.info('new NoteAttack() <- decay_damping={}, release_damping={}'.format(decay_damping, release_damping))
        self.energy = 1.0
        self.internal_t = 0
        self.offset = 0
        self.decay_damping = decay_damping
        self.release_damping = release_damping
        self.damping = self.decay_damping

    def attack(self):
        self.logger.debug('attack()')
        self.damping = self.decay_damping
        self.offset = 0
        self.internal_t = 0
        self.energy = 1.0

    def release(self):
        self.logger.debug('release()')
        self.damping = self.release_damping
        self.offset = math.log10(self.energy) / math.log10(self.release_damping)
        self.internal_t = 0

    def update_energy(self, delta_t):
        self.internal_t += delta_t
        self.energy = self.damping ** (self.internal_t + self.offset)


class PitchClassVector:
    def __init__(self, scaling=False, decay_damping=0.8, release_damping=0.1, reverse=False):
        self.logger = logging.getLogger('hakawb.PitchClassVector')
        self.logger.info('Creating PitchClassVector object')
        self.noteattacks_dict = {}
        self.energythreshold = 0.001
        self.pc_energy = []
        self.output = []
        self.reversed = reverse
        self.scaling = scaling
        self.t = 0
        self.dt = 0
        self.decay_damping = decay_damping
        self.release_damping = release_damping


    def get_midi_event_id(self, msg):
        # The idea is that a related note_on and note_off
        # events should generate the same midi_event_id
        return 'note_{}_channel_{}_pc_{}'.format(msg.note, msg.channel, msg.note % 12)

    def get_pitchclass_from_note_id(self, note_id):
        return int(note_id.split('_')[-1])

    def iterate_over_noteattacks(self):
        self.pc_energy = [0.0] * 12
        damped_notes = []
        for note_id, noteattack in self.noteattacks_dict.items():
            noteattack.update_energy(self.dt)
            note_pc = self.get_pitchclass_from_note_id(note_id)
            if noteattack.energy < self.energythreshold:
                self.logger.debug("Energy in {} is negligible. Removing".format(note_id))
                damped_notes.append(note_id)
            else:
                self.pc_energy[note_pc] += noteattack.energy
                self.logger.debug('{}: {}'.format(note_id, noteattack.energy))
        # Remove the notes that stopped sounding
        [self.noteattacks_dict.pop(n) for n in damped_notes]

    def energy_non_linearity(self, energy):
        if energy >= 1:
            return (energy-1) / math.sqrt((energy-1)**2 + 1) + 1
        else:
            return energy

    def scaling_pitchclass_energy(self):
        self.logger.debug(self.pc_energy)
        self.pc_energy = [self.energy_non_linearity(energy) for energy in self.pc_energy]
        self.logger.debug(self.pc_energy)
        # If the max value of the pc energy vector is < 1, then don't scale anything
        # else, scale everything accordingly so that max_val == 1.0
        denominator = max(1.0, max(self.pc_energy))
        self.pc_energy = [energy / denominator for energy in self.pc_energy]

    def dispatch(self, msg):
        # Just care about note_on/note_off events
        if msg.type != 'note_on' and msg.type != 'note_off':
            return
        self.logger.debug('Parsing {}'.format(msg))
        note_id = self.get_midi_event_id(msg)
        self.dt = msg.time
        self.t += self.dt
        self.logger.debug('t={}'.format(self.t))
        # Update all the current notes according to the time elapsed
        self.iterate_over_noteattacks()
        # Note released
        if msg.type == 'note_off' or msg.velocity == 0:
            if note_id not in self.noteattacks_dict:
                self.logger.warning('{} has been released but it seems that it is not playing'.format(note_id))
            else:
                noteattack = self.noteattacks_dict[note_id]
                noteattack.release()
        # Note attacked
        else:
            substracted_energy = 0
            if note_id in self.noteattacks_dict:
                self.logger.warning('{} has been attacked but it seems that it was already playing'.format(note_id))
                noteattack = self.noteattacks_dict[note_id]
                substracted_energy = noteattack.energy
                noteattack.attack()
            else:
                noteattack = NoteAttack(decay_damping=self.decay_damping, release_damping=self.release_damping)
                self.noteattacks_dict[note_id] = noteattack
            note_pc = self.get_pitchclass_from_note_id(note_id)
            self.pc_energy[note_pc] += noteattack.energy - substracted_energy
        if self.scaling:
            self.scaling_pitchclass_energy()
        self.output.append(self.pc_energy)

    def output(self):
        if not self.reverse:
            for pc_energy in self.output:
                yield pc_energy
        else:
            for pc_energy in reversed(self.output):
                yield pc_energy

    if __name__ == '__main__':
        import matplotlib.pyplot as plt
        import sys
        if len(sys.argv) == 2:
            release_t = int(sys.argv[1])
        else:
            release_t = 20
        dts = [0.1] * 100
        t = 0
        n = NoteAttack()
        time_arr = []
        energy_arr = []
        for idx, dt in enumerate(dts):
            if idx == release_t:
                n.release()
            t += dt
            n.update_energy(dt)
            time_arr.append(t)
            energy_arr.append(n.energy)
        plt.plot(time_arr, energy_arr)
        plt.show()
