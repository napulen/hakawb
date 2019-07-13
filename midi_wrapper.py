import mido

class MidoWrapper:
    def __init__(self, filename):
        mid = mido.MidiFile(filename)
        self.midi_messages = []
        for mido_msg in mid:
            if mido_msg.type != 'note_on' and mido_msg.type != 'note_off':
                continue
            self.midi_messages.append(
                MidiMessage(
                    mido_msg.type,
                    mido_msg.time,
                    mido_msg.note,
                    mido_msg.channel,
                    mido_msg.velocity
                )
            )

class MidiMessage:
    def __init__(self, typ, time, note, channel, velocity):
        self.type = typ
        self.time = time
        self.note = note
        self.channel = channel
        self.velocity = velocity
    def __str__(self):
        typ = 'note_on' if self.type == 'note_on' and self.velocity > 0 else 'note_off'
        return '<{}, delta={}, channel={}, note={}>'.format(typ, self.time, self.channel, self.note)