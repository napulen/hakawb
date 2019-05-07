import logging
import math

class NoteAttack:
    def __init__(self, decay_damping=0.8, release_damping=0.1):
        self.logger = logging.getLogger('hakawb.NoteHeat')
        self.logger.info('Creating new NoteHeat object')
        self.heat = 1.0
        self.internal_t = 0
        self.offset = 0
        self.decay_damping = decay_damping
        self.release_damping = release_damping
        self.damping = self.decay_damping

    def release(self):
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
        self.noteheat_dict = {}
        self.notestatus_dict = {}
        self.pc_heat_dict = {}
        self.scaling = scaling
        self.t = 0

    def get_midi_event_id(self, msg):
        # The idea is that a related note_on and note_off
        # events should generate the same midi_event_id
        return 'note_{}_channel_{}_pc_{}'.format(msg.note, msg.channel, msg.note % 12)

    def get_pitchclass_from_note_id(self, note_id):
        return int(note_id.split('_')[-1])

    def iterate_over_noteheats(self):
        pc_heat = [0] * 12
        for note_id, noteheat in self.noteheat_dict.items():
            noteheat.update(self.t, self.notestatus_dict[note_id])
            note_pc = self.get_pitchclass_from_note_id(note_id)
            pc_heat[note_pc] += noteheat.heat
        self.pc_heat_dict[self.t] = pc_heat

    def parse_midi_event(self, msg):
        # Just care about note_on/note_off events
        if msg.type != 'note_on' and msg.type != 'note_off':
            return
        note_id = self.get_midi_event_id(msg)
        if msg.type == 'note_off' or msg.velocity == 0:
            note_on = False
        else:
            note_on = True
        self.t += msg.time
        self.logger.debug('{} {} {}'.format(self.t, note_id, note_on))
        if note_id in self.noteheat_dict:
            noteheat = self.noteheat_dict[note_id]
        else:
            noteheat = NoteHeat()
            self.noteheat_dict[note_id] = noteheat
        # noteheat = self.noteheat_dict.get(note_id, NoteHeat())
        # self.noteheat_dict[note_id] = noteheat
        self.notestatus_dict[note_id] = note_on
        self.logger.debug(list(self.noteheat_dict.keys()))
        self.iterate_over_noteheats()
        if self.scaling:
            self.logger.info('User wants scaling. TODO')
        return self.pc_heat_dict[self.t]


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
