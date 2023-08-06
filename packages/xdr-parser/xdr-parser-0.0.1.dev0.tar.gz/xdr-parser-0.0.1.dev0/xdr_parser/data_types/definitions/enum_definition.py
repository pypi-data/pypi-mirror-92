from xdr_parser.data_types import Identifier
from xdr_parser.data_types.definitions.definition import Definition
from xdr_parser.data_types.specifiers.sub import EnumBody


class EnumDefinition(Definition):
    __slots__ = ("identifier", "enum_body")

    def __init__(self, identifier: Identifier, enum_body: EnumBody, source: str):
        super().__init__(source)
        self.identifier = identifier
        self.enum_body = enum_body

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.identifier == other.identifier and self.enum_body == other.enum_body

    def __repr__(self) -> str:
        return "<EnumDefinition identifier={identifier}, enum_body={enum_body}>".format(
            identifier=self.identifier, enum_body=self.enum_body,
        )
