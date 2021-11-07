# class to represent hosts being pinged

# takes the name and process object associated with this host
class Host:
    def __init__(self, name, process):
        self.name = name
        self.process = process
        # number of failed pings
        self.fails = 0