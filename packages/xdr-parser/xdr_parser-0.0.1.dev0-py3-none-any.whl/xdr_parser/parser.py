import os
from typing import Union, List

from lark.lark import Lark

from xdr_parser.data_types import Namespace
from xdr_parser.data_types.definitions.definition import Definition
from xdr_parser.transformer import XdrTransformer

__all__ = ["parse"]

current_dir_path = os.path.dirname(os.path.realpath(__file__))
grammar_file = os.path.join(current_dir_path, "xdr.lark")

_parser = Lark.open(
    grammar_filename=grammar_file,
    parser="lalr",
    start="document",
    propagate_positions=True,
)


def parse(text: str) -> Union[Namespace, List[Definition]]:
    tree = _parser.parse(text)
    transformer = XdrTransformer(text)
    parsed_object = transformer.transform(tree)
    return parsed_object
