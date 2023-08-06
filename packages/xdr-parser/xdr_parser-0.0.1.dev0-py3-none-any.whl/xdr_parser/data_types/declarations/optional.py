from xdr_parser.data_types.declarations.declaration import Declaration
from xdr_parser.data_types.identifier import Identifier
from xdr_parser.data_types.specifiers.specifier import Specifier


class Optional(Declaration):
    __slots__ = ("identifier", "specifier")

    def __init__(self, specifier: Specifier, identifier: Identifier, source: str):
        super().__init__(source)
        self.specifier = specifier
        self.identifier = identifier

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.identifier == other.identifier and self.specifier == other.specifier

    def __repr__(self) -> str:
        return "<Optional specifier={specifier}, identifier={identifier}>".format(
            specifier=self.specifier, identifier=self.identifier,
        )
