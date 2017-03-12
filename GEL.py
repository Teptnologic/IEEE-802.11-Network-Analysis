import packet
import event

class GEL(object):
    def __init__(self):
        self.head = None

    def schedule(self, type, time, packet):
        new_event = event.Event(time, packet, type, None, None)
        self.insert(new_event)

    def insert(self, new_event):
        if self.head == None:
            self.head = new_event
            return None
        iterator = self.head
        if iterator.time > new_event.time:
            self.head = new_event
            new_event.next = iterator
            iterator.prev = new_event
            return new_event
        while (iterator.next != None) and (new_event.time > iterator.next.time):
            iterator = iterator.next
        new_event.prev = iterator
        new_event.next = iterator.next
        iterator.next = new_event
        if new_event.next != None:
            new_event.next.prev = new_event
        return new_event

    def pop(self):
        if self.head == None:
            return None
        first_event = self.head
        if first_event.next != None:
            first_event.next.prev = None
        self.head = first_event.next
        first_event.next = None
        return first_event

    def print_elements(self):
        iterator = self.head
        while iterator != None:
            print(iterator.time)
            iterator = iterator.next
