class FixedLengthArray:
    __slots__ = ("data_type", "identifier")

    def __init__(self, data_type, identifier):
        self.data_type = data_type
        self.identifier = identifier

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return True

    def __repr__(self) -> str:
        return "<FixedLengthArray>"
