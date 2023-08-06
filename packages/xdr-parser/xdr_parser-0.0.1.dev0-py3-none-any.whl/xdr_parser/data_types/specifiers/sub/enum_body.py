from typing import List

from xdr_parser.data_types.base import Base
from xdr_parser.data_types.specifiers.sub.enum_member import EnumMember


class EnumBody(Base):
    __slots__ = ("members",)

    def __init__(self, members: List[EnumMember], source: str):
        super().__init__(source)
        self.members = members

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.members == other.members

    def __repr__(self) -> str:
        return "<EnumBody members={members}>".format(members=self.members)
