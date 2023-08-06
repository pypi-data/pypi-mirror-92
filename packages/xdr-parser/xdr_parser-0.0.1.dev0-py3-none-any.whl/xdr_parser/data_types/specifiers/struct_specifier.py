from xdr_parser.data_types.specifiers.specifier import Specifier
from xdr_parser.data_types.specifiers.sub.struct_body import StructBody


class StructSpecifier(Specifier):
    __slots__ = ("struct_body",)

    def __init__(self, struct_body: StructBody, source: str):
        super().__init__(source)
        self.struct_body = struct_body

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.struct_body == other.struct_body

    def __repr__(self) -> str:
        return "<StructSpecifier struct_body={struct_body}>".format(
            struct_body=self.struct_body
        )
