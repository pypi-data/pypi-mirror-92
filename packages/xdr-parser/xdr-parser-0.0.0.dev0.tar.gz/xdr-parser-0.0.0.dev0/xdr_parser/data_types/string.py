class String:
    __slots__ = ("identifier", "length")

    def __init__(self, identifier: str, length: int):
        self.identifier = identifier
        self.length = length

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.identifier == other.identifier and self.length == other.length

    def __repr__(self) -> str:
        return "<String identifier=\"{identifier:s}\", length={length:d}>".format(identifier=self.identifier,
                                                                                  length=self.length)
