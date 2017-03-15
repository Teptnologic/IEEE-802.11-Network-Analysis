class Host(object):
    def __init__(self, difs, sifs):
        self.frames = []
        self.reset(difs, sifs)

    def reset(self, difs, sifs):
        self.difs = difs
        self.sifs = sifs
        self.backoff = -1

    def schedule(self, frame):
        self.frames.append(frame)

    def sent_frame(self, channel_is_idle, default_backoff):
        if len(self.frames) == 0:  # is idle
            return
        if self.frames[0].is_ack is False:  # wants to send data frame
            if channel_is_idle:
                if self.backoff == -1:  # is difs state
                    if self.difs > 0:
                        self.difs -= 1
                    else:
                        return self.frames.pop(0)
                else:  # is backoff state
                    if self.backoff > 0:
                        self.backoff -= 1
                    else:
                        return self.frames.pop(0)
            else:
                if self.backoff == -1:  # is difs state
                    self.backoff = default_backoff
                    self.difs = -1
        else:  # wants to send ack frame
            if self.sifs > 0:
                self.sifs = -1
            else:
                return self.frames.pop(0)
