from xdr_parser.data_types.declarations.declaration import Declaration
from xdr_parser.data_types.definitions.definition import Definition


class TypedefDefinition(Definition):
    __slots__ = ("declaration",)

    def __init__(self, declaration: Declaration, source: str):
        super().__init__(source)
        self.declaration = declaration

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.declaration == other.declaration

    def __repr__(self) -> str:
        return "<TypedefDefinition declaration={declaration}>".format(
            declaration=self.declaration
        )
