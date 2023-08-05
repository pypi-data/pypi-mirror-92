from .constant import Constant


class DecimalConstant(Constant):
    __slots__ = ("value",)

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __repr__(self) -> str:
        return "<DecimalConstant value={value:d}>".format(value=self.value)
