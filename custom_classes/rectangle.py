class Rectangle:
    def __init__(self, length: int, width: int):
        if not isinstance(length, int) or not isinstance(width, int):
            raise TypeError("length and width must be integers")
        self.length = length
        self.width = width

    def __iter__(self):
        # Yield length first, then width, as requested.
        yield {"length": self.length}
        yield {"width": self.width}
