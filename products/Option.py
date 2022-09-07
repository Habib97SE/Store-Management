class Option:
    def __init__(self, name: str, values: list, position=1):
        self.name = name
        self.values = values
        self.position = position

    def get_name(self):
        return self.name

    def get_values(self):
        return self.values

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def set_name(self, name):
        self.name = name

    def set_values(self, values):
        self.values = values

    def get_option(self):
        return {
            "name": self.get_name(),
            "position": 1,
            "values": self.get_values()
        }
