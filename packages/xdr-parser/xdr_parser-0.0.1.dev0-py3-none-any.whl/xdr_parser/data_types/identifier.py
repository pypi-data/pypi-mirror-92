from xdr_parser.data_types.base import Base


class Identifier(Base):
    __slots__ = ("value",)

    def __init__(self, value: str, source: str):
        super().__init__(source)
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __repr__(self) -> str:
        return '<Identifier value="{value}">'.format(value=self.value)
