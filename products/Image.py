class Image:
    def __init__(self, src: str, alt: str, width: int, height: int, variant_ids: list, position=1):
        self.src = src
        self.position = position
        self.alt = alt
        self.width = width
        self.height = height
        self.variant_ids = variant_ids

    def __eq__(self, other):
        return self.get_src() == other.get_src() and self.get_position() == other.get_position() and self.get_alt() == other.get_alt() and self.get_width() == other.get_width() and self.get_height() == other.get_height() and self.get_variant_ids() == other.get_variant_ids()

    def get_src(self):
        return self.src

    def get_position(self):
        return self.position

    def get_alt(self):
        return self.alt

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_variant_ids(self):
        return self.variant_ids

    def set_variant_ids(self, variant_ids):
        self.variant_ids = variant_ids

    def set_src(self, src):
        self.src = src

    def set_position(self, position):
        self.position = position

    def set_alt(self, alt):
        self.alt = alt

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def __str__(self):
        return {
            "position": self.get_position(),
            "src": self.get_src(),
            "alt": self.get_alt(),
            "width": self.get_width(),
            "height": self.get_height(),
            "variant_ids": self.get_variant_ids()
        }
