import midi_wrapper

class MidiReverser:
    def __init__(self):
        self.midi_stack = []
        self.msg = None

    def update_msg(self):
        # Delta time will be set by the next event
        self.msg.time = 0.0
        # If note_off, make it note_on
        if self.msg.type == 'note_off' or self.msg.velocity == 0:
            self.msg.velocity = 80
            self.msg.type = 'note_on'
        # if note_on, make it note_off
        else:
            self.msg.velocity = 0
            self.msg.type ='note_on'

    def register_event(self, msg):
        # This deltatime is written in the msg at the top of the stack
        if msg.type != 'note_on' and msg.type != 'note_off':
            return
        self.msg = midi_wrapper.MidiMessage(
            msg.type,
            msg.time,
            msg.note,
            msg.channel,
            msg.velocity)
        if self.midi_stack:
            self.midi_stack[-1].time = self.msg.time
        self.update_msg()
        self.midi_stack.append(self.msg)

    def reverse(self):
        while self.midi_stack:
            yield self.midi_stack.pop()