from typing import List

from xdr_parser.data_types.base import Base
from xdr_parser.data_types.declarations.declaration import Declaration


class StructBody(Base):
    __slots__ = ("members",)

    def __init__(self, members: List[Declaration], source: str):
        super().__init__(source)
        self.members = members

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.members == other.members

    def __repr__(self) -> str:
        return "<StructBody members={members}>".format(members=self.members)
