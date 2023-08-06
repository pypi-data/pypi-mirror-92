from xdr_parser.data_types import Identifier
from xdr_parser.data_types.definitions.definition import Definition
from xdr_parser.data_types.specifiers.sub import UnionBody


class UnionDefinition(Definition):
    __slots__ = ("identifier", "union_body")

    def __init__(self, identifier: Identifier, union_body: UnionBody, source: str):
        super().__init__(source)
        self.identifier = identifier
        self.union_body = union_body

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.identifier == other.identifier and self.union_body == other.union_body
        )

    def __repr__(self) -> str:
        return "<UnionDefinition identifier={identifier}, union_body={union_body}>".format(
            identifier=self.identifier, union_body=self.union_body,
        )
