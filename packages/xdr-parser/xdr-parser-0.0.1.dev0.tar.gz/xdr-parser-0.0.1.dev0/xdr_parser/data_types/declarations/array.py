from typing import Union

from xdr_parser.data_types import Identifier
from xdr_parser.data_types.declarations.declaration import Declaration
from xdr_parser.data_types.specifiers.specifier import Specifier


class Array(Declaration):
    __slots__ = ("identifier", "specifier", "fixed", "length")

    def __init__(
        self,
        specifier: Union[Specifier],
        identifier: Identifier,
        length: int,
        fixed: bool,
        source: str,
    ):
        super().__init__(source)
        self.specifier = specifier
        self.identifier = identifier
        self.length = length
        self.fixed = fixed

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.specifier == other.specifier
            and self.identifier == other.identifier
            and self.length == other.length
            and self.fixed == other.fixed
        )

    def __repr__(self) -> str:
        return "<Array specifier={specifier}, identifier={identifier}, length={length}, fixed={fixed}>".format(
            specifier=self.specifier,
            identifier=self.identifier,
            length=self.length,
            fixed=self.fixed,
        )
