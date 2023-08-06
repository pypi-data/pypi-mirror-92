from typing import Union, List

from lark import Transformer, v_args
from lark.tree import Meta
from xdr_parser.data_types import (
    Identifier,
    DecimalConstant,
    HexadecimalConstant,
    OctalConstant,
    Namespace,
    Constant,
)
from xdr_parser.data_types.declarations import *
from xdr_parser.data_types.definitions import *
from xdr_parser.data_types.definitions.definition import Definition
from xdr_parser.data_types.specifiers import *
from xdr_parser.data_types.specifiers.specifier import Specifier
from xdr_parser.data_types.specifiers.sub import *

MAX_LENGTH = 2 ** 32 - 1

KEYWORDS = (
    "bool",
    "case",
    "const",
    "default",
    "double",
    "quadruple",
    "enum",
    "float",
    "hyper",
    "int",
    "opaque",
    "string",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
)


@v_args(meta=True)
class XdrTransformer(Transformer):
    def __init__(self, data: str) -> None:
        super().__init__()
        self.data = data

    def _get_source(self, meta: Meta) -> str:
        return self.data[meta.start_pos : meta.end_pos]

    def identifier(self, children, meta) -> Identifier:
        if children[0] in KEYWORDS:
            raise ValueError(
                "The following are keywords and cannot be used as identifiers: {keywords}.".format(
                    keywords=", ".join(KEYWORDS)
                )
            )
        return Identifier(children[0], self._get_source(meta))

    def decimal_constant(self, children, meta) -> DecimalConstant:
        return DecimalConstant(int(children[0]), self._get_source(meta))

    def hexadecimal_constant(self, children, meta) -> HexadecimalConstant:
        return HexadecimalConstant(int(children[0], 16), self._get_source(meta))

    def octal_constant(self, children, meta) -> OctalConstant:
        return OctalConstant(int(children[0], 8), self._get_source(meta))

    def constant(self, children, meta) -> Constant:
        return children[0]

    def value(self, children, meta) -> Union[Constant, Identifier]:
        return children[0]

    def identifier_specifier(self, children, meta) -> IdentifierSpecifier:
        return IdentifierSpecifier(children[0], self._get_source(meta))

    def int_specifier(self, children, meta) -> Integer:
        return Integer(self._get_source(meta))

    def unsigned_int_specifier(self, children, meta) -> UnsignedInteger:
        return UnsignedInteger(self._get_source(meta))

    def hyper_specifier(self, children, meta) -> Hyper:
        return Hyper(self._get_source(meta))

    def unsigned_hyper_specifier(self, children, meta) -> UnsignedHyper:
        return UnsignedHyper(self._get_source(meta))

    def float_specifier(self, children, meta) -> Float:
        return Float(self._get_source(meta))

    def double_specifier(self, children, meta) -> Double:
        return Double(self._get_source(meta))

    def quadruple_specifier(self, children, meta) -> Quadruple:
        return Quadruple(self._get_source(meta))

    def bool_specifier(self, children, meta) -> Boolean:
        return Boolean(self._get_source(meta))

    def enum_body(self, children, meta) -> EnumBody:
        enum_members = []
        for i in range(0, len(children), 2):
            enum_members.append(
                EnumMember(
                    children[i],
                    children[i + 1],
                    # TODO: improve it
                    "{identifier} = {value}".format(
                        identifier=children[i].source, value=children[i + 1].source
                    ),
                )
            )
        return EnumBody(enum_members, self._get_source(meta))

    def enum_type_specifier(self, children, meta) -> EnumSpecifier:
        return EnumSpecifier(children[0], self._get_source(meta))

    def struct_body(self, children, meta) -> StructBody:
        return StructBody(children, self._get_source(meta))

    def struct_type_specifier(self, children, meta) -> StructSpecifier:
        return StructSpecifier(children[0], self._get_source(meta))

    def case_specifier(self, children, meta) -> UnionCase:
        return UnionCase(children[0:-1], children[-1], self._get_source(meta))

    def union_body(self, children, meta) -> UnionBody:
        default = children[2] if len(children) == 3 else None
        return UnionBody(children[0], children[1], default, self._get_source(meta))

    def union_type_specifier(self, children, meta) -> UnionSpecifier:
        return UnionSpecifier(children[0], self._get_source(meta))

    def type_specifier_declaration(self, children, meta) -> Simple:
        return Simple(children[0], children[1], self._get_source(meta))

    def type_specifier_fixed_length_declaration(self, children, meta) -> Array:
        return Array(
            children[0], children[1], children[2], True, self._get_source(meta)
        )

    def type_specifier_variable_length_declaration(self, children, meta) -> Array:
        length = children[2] if len(children) == 3 else MAX_LENGTH
        return Array(children[0], children[1], length, False, self._get_source(meta))

    def opaque_fixed_length_declaration(self, children, meta) -> Opaque:
        return Opaque(children[0], children[1], True, self._get_source(meta))

    def opaque_variable_length_declaration(self, children, meta) -> Opaque:
        length = children[1] if len(children) == 2 else MAX_LENGTH
        return Opaque(children[0], length, False, self._get_source(meta))

    def string_declaration(self, children, meta) -> String:
        length = children[1] if len(children) == 2 else MAX_LENGTH
        return String(children[0], length, self._get_source(meta))

    def type_specifier_optional_declaration(self, children, meta) -> Optional:
        return Optional(children[0], children[1], self._get_source(meta))

    def void_declaration(self, children, meta) -> Void:
        return Void(self._get_source(meta))

    def constant_definition(self, children, meta) -> ConstantDefinition:
        return ConstantDefinition(children[0], children[1], self._get_source(meta))

    def enum_definition(self, children, meta) -> EnumDefinition:
        return EnumDefinition(children[0], children[1], self._get_source(meta))

    def struct_definition(self, children, meta) -> StructDefinition:
        return StructDefinition(children[0], children[1], self._get_source(meta))

    def typedef_definition(self, children, meta) -> TypedefDefinition:
        return TypedefDefinition(children[0], self._get_source(meta))

    def union_definition(self, children, meta) -> UnionDefinition:
        return UnionDefinition(children[0], children[1], self._get_source(meta))

    def definition(self, children, meta) -> List[Definition]:
        return children[0]

    def specification(self, children, meta) -> List[Specifier]:
        return children

    def type_specifier(self, children, meta) -> Specifier:
        return children

    def namespace(self, children, meta) -> Namespace:
        return Namespace(children[0], children[1:], self._get_source(meta))
