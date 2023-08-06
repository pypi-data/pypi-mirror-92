from xdr_parser.data_types import Identifier
from xdr_parser.data_types.definitions.definition import Definition
from xdr_parser.data_types.specifiers.sub import StructBody


class StructDefinition(Definition):
    __slots__ = ("identifier", "struct_body")

    def __init__(self, identifier: Identifier, struct_body: StructBody, source: str):
        super().__init__(source)
        self.identifier = identifier
        self.struct_body = struct_body

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.identifier == other.identifier
            and self.struct_body == other.struct_body
        )

    def __repr__(self) -> str:
        return "<StructDefinition identifier={identifier}, struct_body={struct_body}>".format(
            identifier=self.identifier, struct_body=self.struct_body,
        )
