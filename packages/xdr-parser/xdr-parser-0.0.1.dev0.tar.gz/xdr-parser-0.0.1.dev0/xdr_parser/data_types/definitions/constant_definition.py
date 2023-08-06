from xdr_parser.data_types import Identifier, Constant
from xdr_parser.data_types.definitions.definition import Definition


class ConstantDefinition(Definition):
    __slots__ = ("identifier", "constant")

    def __init__(self, identifier: Identifier, constant: Constant, source: str):
        super().__init__(source)
        self.identifier = identifier
        self.constant = constant

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.identifier == other.identifier and self.constant == other.constant

    def __repr__(self) -> str:
        return "<ConstantDefinition identifier={identifier}, constant={constant}>".format(
            identifier=self.identifier, constant=self.constant
        )
