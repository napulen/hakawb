import logging

class BassModel:
    def __init__(self):
        self.logger = logging.getLogger('hakawb.BassModel')
        # Larger than any midi note number for initialization
        self.bass = 128

    def register_event(self, msg):
        if msg.note < self.bass:
            self.logger.info("This note became the new bass")
            self.bass = msg.note