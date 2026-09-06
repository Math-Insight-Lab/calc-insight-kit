# -*- coding: utf-8 -*-
"""
CAS 表达式测试：验证表达式对象功能
"""
import pytest
from calc_insight_kit.cas.parser import CASExpr, CASSymbol, get_cas_backend


def test_cassymbol_basic():
    """CASSymbol 基本功能测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    assert str(x) == "x"
    assert isinstance(x, CASSymbol)


def test_cassymbol_repr():
    """CASSymbol repr 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    assert repr(x) == "CASSymbol('x')"


def test_cassymbol_str():
    """CASSymbol str 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    assert str(x) == "x"


def test_cassymbol_add():
    """CASSymbol 加法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    y = cas.Symbol("y")
    expr = x + y
    assert isinstance(expr, CASExpr)
    assert "x+y" in str(expr)


def test_cassymbol_sub():
    """CASSymbol 减法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    y = cas.Symbol("y")
    expr = x - y
    assert isinstance(expr, CASExpr)
    assert "x-y" in str(expr)


def test_cassymbol_mul():
    """CASSymbol 乘法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    y = cas.Symbol("y")
    expr = x * y
    assert isinstance(expr, CASExpr)
    assert "x*y" in str(expr)


def test_cassymbol_div():
    """CASSymbol 除法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    y = cas.Symbol("y")
    expr = x / y
    assert isinstance(expr, CASExpr)
    assert "x/y" in str(expr)


def test_cassymbol_pow():
    """CASSymbol 幂运算测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2
    assert isinstance(expr, CASExpr)
    assert "x**2" in str(expr)


def test_casexpr_parse():
    """CASExpr 解析测试"""
    cas = get_cas_backend()
    expr = cas.parse_expr("sin(x)/x")
    assert isinstance(expr, CASExpr)
    assert "sin(x)/x" in str(expr)


def test_casexpr_repr():
    """CASExpr repr 测试"""
    cas = get_cas_backend()
    expr = cas.parse_expr("sin(x)/x")
    assert repr(expr) == "CASExpr('sin(x)/x')"


def test_casexpr_str():
    """CASExpr str 测试"""
    cas = get_cas_backend()
    expr = cas.parse_expr("sin(x)/x")
    assert str(expr) == "sin(x)/x"


def test_casexpr_diff():
    """CASExpr diff 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2 + 2*x + 1
    d = cas.diff(expr, x)
    assert isinstance(d, CASExpr)
    assert "2*x+2" in str(d)


def test_casexpr_integrate():
    """CASExpr integrate 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2 + 2*x + 1
    I = cas.integrate(expr, x)
    assert isinstance(I, CASExpr)
    # 积分结果应包含 x**3 项
    assert "x**3/3" in str(I) or "x^3/3" in str(I)


def test_casexpr_limit():
    """CASExpr limit 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2 + 2*x + 1
    lim = cas.limit(expr, x, 1)
    assert isinstance(lim, CASExpr)
    assert "4" in str(lim)


def test_casexpr_solve():
    """CASExpr solve 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2 - 4
    sol = cas.solve(expr, x)
    assert isinstance(sol, CASExpr)
    sol_str = str(sol)
    assert "2" in sol_str or "-2" in sol_str


def test_casexpr_dsolve():
    """CASExpr dsolve 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    y = cas.Symbol("y")
    expr = y.diff(x) - x
    sol = cas.dsolve(expr, y)
    assert isinstance(sol, CASExpr)
    sol_str = str(sol)
    # 解应包含积分项或 exp 项
    assert "integrate" in sol_str.lower() or "exp" in sol_str.lower()


def test_casexpr_series():
    """CASExpr series 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = cas.parse_expr("sin(x)")
    series = cas.series(expr, x, 5)
    assert isinstance(series, CASExpr)
    series_str = str(series)
    # 应包含 x 的一次项
    assert "x" in series_str


def test_casexpr_latex():
    """CASExpr latex 测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2 + 2*x + 1
    latex = cas.latex(expr)
    # 应包含 x^2 或 x**2
    assert "x^2" in latex or "x**2" in latex


def test_casexpr_diff_expr():
    """CASExpr.diff 方法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2
    d = expr.diff(x)
    assert isinstance(d, CASExpr)
    assert "2*x" in str(d)


def test_casexpr_integrate_expr():
    """CASExpr.integrate 方法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2
    I = expr.integrate(x)
    assert isinstance(I, CASExpr)
    assert "x**3/3" in str(I)


def test_casexpr_limit_expr():
    """CASExpr.limit 方法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2
    lim = expr.limit(x, 2)
    assert isinstance(lim, CASExpr)
    assert "4" in str(lim)


def test_casexpr_solve_expr():
    """CASExpr.solve 方法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2 - 4
    sol = expr.solve(x)
    assert isinstance(sol, CASExpr)
    sol_str = str(sol)
    assert "2" in sol_str or "-2" in sol_str


def test_casexpr_dsolve_expr():
    """CASExpr.dsolve 方法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    y = cas.Symbol("y")
    expr = y.diff(x) - x
    sol = expr.dsolve(y)
    assert isinstance(sol, CASExpr)
    sol_str = str(sol)
    assert "integrate" in sol_str.lower() or "exp" in sol_str.lower()


def test_casexpr_series_expr():
    """CASExpr.series 方法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = cas.parse_expr("sin(x)")
    series = expr.series(x, 5)
    assert isinstance(series, CASExpr)
    series_str = str(series)
    assert "x" in series_str


def test_casexpr_latex_expr():
    """CASExpr.latex 方法测试"""
    cas = get_cas_backend()
    x = cas.Symbol("x")
    expr = x**2
    latex = expr.latex()
    assert isinstance(latex, str)
    assert "x^2" in latex or "x**2" in latex
