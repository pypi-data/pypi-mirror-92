import os
from typing import List, Union

from lark.lark import Lark
from lark import Transformer, v_args

current_dir_path = os.path.dirname(os.path.realpath(__file__))
grammar_file = os.path.join(current_dir_path, "xdr.lark")
max_length = 2 ** 32 - 1


class Identifier:
    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self):
        return "<Identifier value = {value}>".format(value=self.value)


class EnumTypeDef:
    def __init__(self, identifier: str, enum_body: List["EnumBody"], source):
        self.identifier = identifier
        self.enum_body = enum_body
        self.source = source

    def __repr__(self):
        return "<EnumTypeDef identifier = {identifier}, enum_body = {enum_body}>" \
            .format(identifier=self.identifier, enum_body=self.enum_body)


class EnumBody:
    # TODO: rename
    def __init__(self, identifier: str, value: Union[str, int]):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return "<EnumBody identifier = {identifier}, value = {value}>".format(identifier=self.identifier,
                                                                              value=self.value)


class ConstantDefinition:
    def __init__(self, identifier: str, constant: int):
        self.identifier = identifier
        self.constant = constant

    def __repr__(self):
        return "<ConstantDefinition identifier = {identifier}, constant = {constant}>".format(
            identifier=self.identifier,
            constant=self.constant)


##########################################################################
class Specifier:
    pass


class IntSpecifier(Specifier):
    def __repr__(self):
        return "<IntSpecifier>"

class UnsignedIntSpecifier(Specifier):
    def __repr__(self):
        return "<UnsignedIntSpecifier>"


class HyperSpecifier(Specifier):
    def __repr__(self):
        return "<HyperSpecifier>"


class FloatSpecifier(Specifier):
    def __repr__(self):
        return "<FloatSpecifier>"


class DoubleSpecifier(Specifier):
    def __repr__(self):
        return "<DoubleSpecifier>"


class QuadrupleSpecifier(Specifier):
    def __repr__(self):
        return "<QuadrupleSpecifier>"


class BoolSpecifier(Specifier):
    def __repr__(self):
        return "<BoolSpecifier>"


class EnumSpecifier(Specifier):
    def __repr__(self):
        return "<EnumSpecifier>"


class StructSpecifier(Specifier):
    def __repr__(self):
        return "<StructSpecifier>"


class UnionSpecifier(Specifier):
    def __repr__(self):
        return "<UnionSpecifier>"


class IdentifierSpecifier(Specifier):
    def __init__(self, identifier: str):
        self.identifier = identifier

    def __repr__(self):
        return "<IdentifierSpecifier identifier = {identifier}>".format(identifier=self.identifier)


##########################################################################
class Declaration:
    pass


class TypeSpecifierDeclaration(Declaration):
    def __init__(self, type_specifier: Specifier, identifier: Identifier, is_optional, is_array, is_fixed, length):
        self.type_specifier = type_specifier
        self.identifier = identifier
        self.is_optional = is_optional
        self.is_array = is_array
        self.is_fixed = is_fixed
        self.length = length

    def __repr__(self):
        return "<TypeSpecifierDeclaration type_specifier = {type_specifier}, identifier = {identifier}, is_optional = {is_optional}>".format(
            type_specifier=self.type_specifier, identifier=self.identifier, is_optional=self.is_optional)


class VoidDeclaration(Declaration):
    def __repr__(self):
        return "<VoidDeclaration>"


class StringDeclaration(Declaration):
    def __init__(self, identifier: Identifier, length):
        self.identifier = identifier
        self.length = length

    def __repr__(self):
        return "<StringDeclaration identifier = {identifier}, length = {length}>".format(
            identifier=self.identifier, length=self.length)


class OpaqueDeclaration(Declaration):
    def __init__(self, identifier: Identifier, length, is_fixed):
        self.identifier = identifier
        self.length = length
        self.is_fixed = is_fixed

    def __repr__(self):
        return "<StringDeclaration identifier = {identifier}, length = {length}, is_fixed = {is_fixed}>".format(
            identifier=self.identifier, length=self.length, is_fixed=self.is_fixed)


##########################################################################
class Definition:
    pass


class TypedefDefinition(Definition):
    def __init__(self, declaration: Declaration):
        self.declaration = declaration

    def __repr__(self):
        return "<TypeSpecifierDeclaration declaration = {declaration}>".format(
            declaration=self.declaration)


class EnumDefinition(Definition):
    def __init__(self, identifier, enum_body: List[EnumBody]):
        self.identifier = identifier
        self.enum_body = enum_body

    def __repr__(self):
        return "<EnumDefinition identifier = {identifier}, enum_body = {enum_body}>".format(
            identifier=self.identifier, enum_body=self.enum_body)


class UnionBody:
    def __init__(self, declaration, case_specifier, default):
        self.declaration = declaration
        self.case_specifier = case_specifier
        self.default = default

    def __repr__(self):
        return "<UnionBody declaration = {declaration}, case_specifier = {case_specifier}, default = {default}>".format(
            declaration=self.declaration, case_specifier=self.case_specifier, default=self.default)


class UnionDefinition(Definition):
    def __init__(self, identifier, union_body):
        self.identifier = identifier
        self.union_body = union_body

    def __repr__(self):
        return "<UnionDefinition identifier = {identifier}, union_body = {union_body}>".format(
            identifier=self.identifier, union_body=self.union_body)


class CaseSpecifier:
    def __init__(self, value: List, declaration):
        self.value = value
        self.declaration = declaration

    def __repr__(self):
        return "<CaseSpecifier value = {value}, declaration = {declaration}>".format(
            value=self.value, declaration=self.declaration)


class StructBody:
    def __init__(self, declaration):
        self.declaration = declaration

    def __repr__(self):
        return "<StructBody declaration = {declaration}>".format(
            declaration=self.declaration)


class StructDefinition(Declaration):
    def __init__(self, identifier, struct_body: List['StructBody']):
        self.identifier = identifier
        self.struct_body = struct_body

    def __repr__(self):
        return "<StructDefinition identifier = {identifier}, struct_body = {struct_body}>".format(
            identifier=self.identifier, struct_body=self.struct_body)


@v_args(tree=True)
class XdrTransformer(Transformer):
    def __init__(self, data: str):
        super().__init__()
        self.data = data

    def enum_body(self, tree):
        body = []
        for i in range(0, len(tree.children), 2):
            body.append(EnumBody(tree.children[i], tree.children[i + 1]))
        return body

    def enum_type_def(self, tree):
        return EnumTypeDef(tree.children[0], tree.children[1], self.data[tree.meta.start_pos: tree.meta.end_pos])

    def constant_definition(self, tree):
        return ConstantDefinition(tree.children[0], tree.children[1])

    def identifier(self, tree):
        return Identifier(tree.children[0])

    def decimal_constant(self, tree):
        return int(tree.children[0])

    def hexadecimal_constant(self, tree):
        return int(tree.children[0], 16)

    def octal_constant(self, tree):
        return int(tree.children[0], 8)

    def constant(self, tree):
        return tree.children[0]

    # specifier
    def int_specifier(self, tree):
        print(tree)
        return IntSpecifier()

    def unsigned_int_specifier(self, tree):
        print(tree)
        return UnsignedIntSpecifier()

    def hyper_specifier(self, tree):
        return HyperSpecifier()

    def float_specifier(self, tree):
        return FloatSpecifier()

    def double_specifier(self, tree):
        return DoubleSpecifier()

    def quadruple_specifier(self, tree):
        return QuadrupleSpecifier()

    def bool_specifier(self, tree):
        return BoolSpecifier

    def enum_specifier(self, tree):
        return tree

    def struct_specifier(self, tree):
        return tree

    def union_specifier(self, tree):
        return tree

    def identifier_specifier(self, tree):
        return IdentifierSpecifier(tree.children[0])

    def type_specifier_declaration(self, tree):
        return TypeSpecifierDeclaration(tree.children[0], tree.children[1], False, False, None, None)

    def type_specifier_fixed_declaration(self, tree):
        return TypeSpecifierDeclaration(tree.children[0], tree.children[1], False, True, True, tree.children[2])

    def type_specifier_dynamic_declaration(self, tree):
        return TypeSpecifierDeclaration(tree.children[0], tree.children[1], False, True, False, tree.children[2])

    def type_specifier_optional_declaration(self, tree):
        return TypeSpecifierDeclaration(tree.children[0], tree.children[1], True, False, None, None)

    def opaque_fixed_declaration(self, tree):
        return OpaqueDeclaration(tree.children[0], tree.children[1], True)

    def opaque_dynamic_declaration(self, tree):
        return OpaqueDeclaration(tree.children[0], tree.children[1], False)

    def string_declaration(self, tree):
        return StringDeclaration(tree.children[0], tree.children[1])

    def void_declaration(self, tree):
        return VoidDeclaration()

    ###########################

    def typedef_definition(self, tree):
        return TypedefDefinition(tree.children[0])

    def enum_definition(self, tree):
        body = []
        for i in range(0, len(tree.children[1]), 2):
            body.append(EnumBody(tree.children[i], tree.children[i + 1]))
        return EnumDefinition(tree.children[0], body)

    def case_specifier(self, tree):
        return CaseSpecifier(tree.children[0: -1], tree.children[1])

    def union_body(self, tree):
        return UnionBody(tree.children[0], tree.children[:-1], tree.children[-1])

    def union_definition(self, tree):
        return UnionDefinition(tree.children[0], tree.children[1])

    def struct_body(self, tree):
        body = []
        for i in range(0, len(tree.children)):
            body.append(StructBody(tree.children[i]))
        return body

    def struct_definition(self, tree):
        return StructDefinition(tree.children[0], tree.children[1])


parser = Lark.open(
    grammar_filename=grammar_file,
    parser='lalr',
    start="document",
    propagate_positions=True,
)

text = """
unsigned  int
"""
tree = parser.parse(text)
print(tree)
print("-" * 64)
transformer = XdrTransformer(text)
print(transformer.transform(tree))
# print(transformer.transform(tree).children[0].source)
