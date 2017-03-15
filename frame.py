class Frame(object):
    def __init__(self, process_time, source, destination, is_ack):
        self.process_time = process_time
        self.source = source
        self.destination = destination
        self.is_ack = is_ack
        self.is_dirty = False
