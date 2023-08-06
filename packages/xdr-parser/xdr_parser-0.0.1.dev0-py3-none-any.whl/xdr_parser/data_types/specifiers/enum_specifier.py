from xdr_parser.data_types.specifiers.specifier import Specifier
from xdr_parser.data_types.specifiers.sub.enum_body import EnumBody


class EnumSpecifier(Specifier):
    __slots__ = ("enum_body",)

    def __init__(self, enum_body: EnumBody, source: str):
        super().__init__(source)
        self.enum_body = enum_body

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.enum_body == other.enum_body

    def __repr__(self) -> str:
        return "<EnumSpecifier enum_body={enum_body}>".format(enum_body=self.enum_body)
