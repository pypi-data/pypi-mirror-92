from xdr_parser.data_types import Identifier
from xdr_parser.data_types.specifiers.specifier import Specifier


class IdentifierSpecifier(Specifier):
    __slots__ = ("identifier",)

    def __init__(self, identifier: Identifier, source: str):
        super().__init__(source)
        self.identifier = identifier

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.identifier == other.identifier

    def __repr__(self) -> str:
        return '<IdentifierSpecifier identifier="{identifier}">'.format(
            identifier=self.identifier
        )
