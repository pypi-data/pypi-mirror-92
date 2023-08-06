from xdr_parser.data_types.specifiers.specifier import Specifier
from xdr_parser.data_types.specifiers.sub.union_body import UnionBody


class UnionSpecifier(Specifier):
    __slots__ = ("union_body",)

    def __init__(self, union_body: UnionBody, source: str):
        super().__init__(source)
        self.union_body = union_body

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.union_body == other.union_body

    def __repr__(self) -> str:
        return "<UnionSpecifier union_body={union_body}>".format(
            union_body=self.union_body
        )
