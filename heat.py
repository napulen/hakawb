import logging
import math

class NoteAttack:
    def __init__(self, decay_damping=0.8, release_damping=0.1):
        self.logger = logging.getLogger('hakawb.NoteHeat')
        self.logger.info('new NoteAttack() <- decay_damping={}, release_damping={}'.format(decay_damping, release_damping))
        self.heat = 1.0
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
        self.heat = 1.0

    def release(self):
        self.logger.debug('release()')
        self.damping = self.release_damping
        self.offset = math.log10(self.heat) / math.log10(self.release_damping)
        self.internal_t = 0

    def update_heat(self, delta_t):
        self.internal_t += delta_t
        self.heat = self.damping ** (self.internal_t + self.offset)

class Midi2PitchClassHeat:
    def __init__(self, scaling=False):
        self.logger = logging.getLogger('hakawb.Midi2PitchClassHeat')
        self.logger.info('Creating Midi2PitchClassHeat object')
        self.noteattacks_dict = {}
        self.pc_heat_dict = {}
        self.notes_to_release = []
        self.scaling = scaling
        self.t = 0
        self.dt = 0

    def get_midi_event_id(self, msg):
        # The idea is that a related note_on and note_off
        # events should generate the same midi_event_id
        return 'note_{}_channel_{}_pc_{}'.format(msg.note, msg.channel, msg.note % 12)

    def get_pitchclass_from_note_id(self, note_id):
        return int(note_id.split('_')[-1])

    def iterate_over_noteattacks(self):
        pc_heat = [0] * 12
        self.logger.debug(list(self.noteattacks_dict.keys()))
        for note_id, noteattack in self.noteattacks_dict.items():
            noteattack.update_heat(self.dt)
            note_pc = self.get_pitchclass_from_note_id(note_id)
            pc_heat[note_pc] += noteattack.heat
            self.logger.debug('{}: {}'.format(note_id, noteattack.heat))
        self.pc_heat_dict[self.t] = pc_heat

    def release_scheduled(self):
        # Release is done until the heat for this timestep has been computed
        for note_id in self.notes_to_release:
            noteattack = self.noteattacks_dict[note_id]
            noteattack.release()
        self.notes_to_release = []

    def parse_midi_event(self, msg):
        # Just care about note_on/note_off events
        if msg.type != 'note_on' and msg.type != 'note_off':
            return
        self.logger.debug('Parsing {}'.format(msg))
        note_id = self.get_midi_event_id(msg)
        self.dt = msg.time
        self.t += self.dt
        self.logger.debug('t={}'.format(self.t))
        # Note released
        if msg.type == 'note_off' or msg.velocity == 0:
            if note_id not in self.noteattacks_dict:
                self.logger.warning('{} has been released but it seems that it is not playing'.format(note_id))
            else:
                noteattack = self.noteattacks_dict[note_id]
                self.notes_to_release.append(note_id)
        # Note attacked
        else:
            if note_id in self.noteattacks_dict:
                self.logger.warning('{} has been attacked but it seems that it was already playing'.format(note_id))
                noteattack = self.noteattacks_dict[note_id]
                noteattack.attack()
            else:
                self.noteattacks_dict[note_id] = NoteAttack()
        self.iterate_over_noteattacks()
        if self.scaling:
            self.logger.info('User wants scaling. TODO')
        self.release_scheduled()



    if __name__ == '__main__':
        import matplotlib.pyplot as plt
        import sys
        if len(sys.argv) == 2:
            release_t = int(sys.argv[1])
        else:
            release_t = 10
        dts = [0.1] * 100
        t = 0
        n = NoteAttack()
        time_arr = []
        heat_arr = []
        for idx, dt in enumerate(dts):
            if idx == release_t:
                n.release()
            t += dt
            n.update_heat(dt)
            time_arr.append(t)
            heat_arr.append(n.heat)
        plt.plot(time_arr, heat_arr)
        plt.show()
