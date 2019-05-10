class MidiMessage:
    def __init__(self, typ, time, note, channel, velocity):
        self.type = typ
        self.time = time
        self.note = note
        self.channel = channel
        self.velocity = velocity

