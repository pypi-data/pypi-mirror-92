from typing import List, Optional

from xdr_parser.data_types.base import Base
from xdr_parser.data_types.declarations.declaration import Declaration
from xdr_parser.data_types.specifiers.sub.union_case import UnionCase


class UnionBody(Base):
    __slots__ = ("declaration", "union_cases", "default")

    def __init__(
        self,
        declaration: Declaration,
        union_cases: List[UnionCase],
        default: Optional[Declaration],
        source: str,
    ):
        super().__init__(source)
        self.declaration = declaration
        self.union_cases = union_cases
        self.default = default

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.declaration == other.declaration
            and self.union_cases == other.union_cases
            and self.default == other.default
        )

    def __repr__(self) -> str:
        return "<UnionBody declaration={declaration}, union_cases={union_cases}, default={default}>".format(
            declaration=self.declaration,
            union_cases=self.union_cases,
            default=self.default,
        )
