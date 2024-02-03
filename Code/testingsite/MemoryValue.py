class MemoryValue:
    def __init__(self, memAddress, memValue=-1):
        self.memAddress = memAddress
        self.memValue = memValue

    def to_dict(self):
        return {
            "memAddress": self.memAddress.value,
            "memValue": self.memValue
        }

    def set_mem_value(self, memvalue):
        self.memValue = memvalue
