from typing import Union

from xdr_parser.data_types.base import Base

from xdr_parser.data_types.constant import Constant
from xdr_parser.data_types.identifier import Identifier


class EnumMember(Base):
    __slots__ = ("identifier", "value")

    def __init__(
        self, identifier: Identifier, value: Union[Constant, Identifier], source: str
    ):
        super().__init__(source)
        self.identifier = identifier
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.identifier == other.identifier and self.value == other.value

    def __repr__(self) -> str:
        return "<EnumMember identifier={identifier}, value={value}>".format(
            identifier=self.identifier, value=self.value
        )
