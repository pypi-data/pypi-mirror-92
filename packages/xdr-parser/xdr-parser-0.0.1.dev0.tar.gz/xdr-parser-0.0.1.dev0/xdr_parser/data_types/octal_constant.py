from xdr_parser.data_types.constant import Constant


class OctalConstant(Constant):
    __slots__ = ("value",)

    def __init__(self, value: int, source: str):
        super().__init__(source)
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __repr__(self) -> str:
        return "<OctalConstant value=0{value:o}>".format(value=self.value)
