import ast
import functools
import sys
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from tokenize_rt import NON_CODING_TOKENS
from tokenize_rt import Offset
from tokenize_rt import Token

from add_trailing_comma._ast_helpers import ast_to_offset
from add_trailing_comma._data import ParseState
from add_trailing_comma._data import register
from add_trailing_comma._data import TokenFunc
from add_trailing_comma._token_helpers import find_simple
from add_trailing_comma._token_helpers import Fix
from add_trailing_comma._token_helpers import fix_brace
from add_trailing_comma._token_helpers import START_BRACES


def _fix_literal(
        i: int,
        tokens: List[Token],
        version: Tuple[int, ...],
        *,
        one_el_tuple: bool,
) -> None:
    if tokens[i].src in START_BRACES:  # pragma: no branch (<py38)
        fix_brace(
            tokens, find_simple(i, tokens),
            add_comma=True,
            remove_comma=not one_el_tuple,
        )


@register(ast.Set)
def visit_Set(
        parse_state: ParseState,
        node: ast.Set,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    func = functools.partial(_fix_literal, one_el_tuple=False)
    yield ast_to_offset(node), func


@register(ast.List)
def visit_List(
        parse_state: ParseState,
        node: ast.List,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if node.elts:
        func = functools.partial(_fix_literal, one_el_tuple=False)
        yield ast_to_offset(node), func


@register(ast.Dict)
def visit_Dict(
        parse_state: ParseState,
        node: ast.Dict,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if node.values:
        func = functools.partial(_fix_literal, one_el_tuple=False)
        yield ast_to_offset(node), func


def _find_tuple(i: int, tokens: List[Token]) -> Optional[Fix]:
    # tuples are evil, we need to backtrack to find the opening paren
    i -= 1
    while tokens[i].name in NON_CODING_TOKENS:
        i -= 1
    # Sometimes tuples don't even have a paren!
    # x = 1, 2, 3
    if tokens[i].src != '(' and tokens[i].src != '[':
        return None

    return find_simple(i, tokens)


def _fix_tuple(
        i: int,
        tokens: List[Token],
        version: Tuple[int, ...],
        *,
        one_el_tuple: bool,
) -> None:
    fix_brace(
        tokens,
        _find_tuple(i, tokens),
        add_comma=True,
        remove_comma=not one_el_tuple,
    )


@register(ast.Tuple)
def visit_Tuple(
        parse_state: ParseState,
        node: ast.Tuple,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if node.elts:
        is_one_el = len(node.elts) == 1
        if (
                ast_to_offset(node) == ast_to_offset(node.elts[0]) or
                # in < py38 tuples lie about offset -- later we must backtrack
                sys.version_info < (3, 8)
        ):
            func = functools.partial(_fix_tuple, one_el_tuple=is_one_el)
            yield ast_to_offset(node), func
        else:  # pragma: no cover (py38+)
            func = functools.partial(_fix_literal, one_el_tuple=is_one_el)
            yield ast_to_offset(node), func
