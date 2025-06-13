import builtins

import pytest
from lark import LarkError, Tree

from lox import *
from lox.ast import *


@pytest.fixture
def expr():
    return True


@pytest.fixture
def src():
    return "(1, 2, 3)"


@pytest.fixture
def src_():
    return "()"


@pytest.fixture
def src__():
    return "((1,), (2 + 1, x), ())"


def test_suporta_listas(cst: Tree, cst_):
    print(pretty := cst.pretty())
    assert "1" in pretty
    assert "2" in pretty
    assert "3" in pretty


def test_suporta_listas_aninhadas(cst__):
    print(pretty := cst__.pretty())
    assert "1" in pretty
    assert "2" in pretty
    assert "x" in pretty


def test_suporta_construção_de_ast(astf, ast_f, ast__f):
    cls = Tuple
    assert isinstance(astf(), cls), "Defina uma classe Tuple em lox/ast.py"
    assert isinstance(ast_f(), cls), "Deve suportar tuplas vazias"
    assert isinstance(ast__f(), cls), "Deve suportar tuplas aninhadas"


def test_aceita_vírgula_no_final():
    ast = parse_expr("(1,)")
    result = ast.eval(Ctx())
    assert isinstance(result, tuple)
    assert result == (1,)

    with pytest.raises((SyntaxError, LarkError)):
        src = "(1, 2,)"
        print(f"Recusa tupla com vírgula no final (ex.: {src})")
        parse_expr(src)


@pytest.mark.parametrize("exemplo", ["(,)", "(1,,2)", "(1, 2,,)", "(,1, 2)"])
def test_recusa_listas_inválidas(exemplo):
    with pytest.raises((SyntaxError, LarkError)):
        parse_expr(exemplo)


def test_implementa_a_função_eval(exs):
    def ctx():
        return Ctx.from_dict({"x": 1})

    for ex in exs:
        print(f"Testando {ex.src=}")
        result = ex.ast.eval(ctx())
        expect = builtins.eval(ex.src, {}, ctx())

        assert (
            result == expect
        ), f"[Tuple.eval]: esperava {expect} mas encontrei {result}"
