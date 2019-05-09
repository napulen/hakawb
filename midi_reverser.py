

class MidiReverser:
    def __init__(self):
        self.midi_stack = []

    def update_msg_note_on(self, msg, note_on):
        if note_on:
            msg.velocity = 80
            msg.type = 'note_on'
        else:
            msg.velocity = 0
            msg.type = 'note_on'
        return msg

    def register_event(self, msg):
        # This deltatime is written in the msg at the top of the stack
        if msg.type != 'note_on' and msg.type != 'note_off':
            return
        if self.midi_stack:
            self.midi_stack[-1].time = msg.time
        msg.time = 0.0
        # Is the event a note_on or note_off?
        if msg.type == 'note_off' or msg.velocity == 0:
            note_on = True
        else:
            note_off = False
        # Now, reverse it!
        note_on = not note_on
        self.midi_stack.append(self.update_msg_note_on(msg, note_on))
