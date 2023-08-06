from typing import Union, List

from xdr_parser.data_types.base import Base
from xdr_parser.data_types.constant import Constant
from xdr_parser.data_types.declarations.declaration import Declaration
from xdr_parser.data_types.identifier import Identifier


class UnionCase(Base):
    __slots__ = ("values", "declaration")

    def __init__(
        self,
        values: List[Union[Identifier, Constant]],
        declaration: Declaration,
        source: str,
    ):
        super().__init__(source)
        self.values = values
        self.declaration = declaration

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.values == other.values and self.declaration == other.declaration

    def __repr__(self) -> str:
        return "<UnionCase values={values}, declaration={declaration}>".format(
            values=self.values, declaration=self.declaration
        )
