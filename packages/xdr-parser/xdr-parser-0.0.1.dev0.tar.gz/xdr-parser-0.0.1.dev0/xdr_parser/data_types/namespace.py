from typing import List

from xdr_parser.data_types.base import Base
from xdr_parser.data_types.definitions.definition import Definition
from xdr_parser.data_types.identifier import Identifier


class Namespace(Base):
    __slots__ = ("identifier", "definitions")

    def __init__(
        self, identifier: Identifier, definitions: List[Definition], source: str
    ):
        super().__init__(source)
        self.identifier = identifier
        self.definitions = definitions

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.identifier == other.identifier
            and self.definitions == other.definitions
        )

    def __repr__(self) -> str:
        return "<Namespace identifier={identifier}, definitions={definitions}>".format(
            identifier=self.identifier, definitions=self.definitions
        )
