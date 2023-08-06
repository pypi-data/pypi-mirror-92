from xdr_parser.data_types.identifier import Identifier

from xdr_parser.data_types.declarations.declaration import Declaration


class Simple(Declaration):
    __slots__ = ("identifier", "specifier")

    def __init__(self, specifier, identifier: Identifier, source: str):
        super().__init__(source)
        self.identifier = identifier
        self.specifier = specifier

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.identifier == other.identifier and self.specifier == other.specifier

    def __repr__(self) -> str:
        return "<Simple specifier={specifier}, identifier={identifier}>".format(
            identifier=self.identifier, specifier=self.specifier
        )
