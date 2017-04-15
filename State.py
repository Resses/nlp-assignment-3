class State:

    def __init__(self, k):
        self.tags = ["-1"] * k

    def push(self, tag):
        self.tags.append(tag)
        self.tags.pop(0)

    def __str__(self):
        return ','.join(self.tags)

    # def __copy__(self):
    def getLastTag(self):
        return self.tags[len(self.tags)-1]

    def getStateCode(self):
        print(self.tags)
        return ["0", "1", "2", "3"].index(','.join(self.tags))
        # When there are more states, it will make more sense
