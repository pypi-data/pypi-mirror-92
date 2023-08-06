class Base:
    __slots__ = "source"

    def __init__(self, source: str):
        self.source = source

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.source == other.source

    def __repr__(self) -> str:
        return "<Base source={source}>".format(source=self.source)
