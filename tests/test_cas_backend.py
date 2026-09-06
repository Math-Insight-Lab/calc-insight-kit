# -*- coding: utf-8 -*-
"""
CAS引擎精度与稳定性测试
"""
from calc_insight_kit import get_cas_backend
import sympy as sp

def test_sympy_precision():
    be = get_cas_backend("sympy")
    x = sp.Symbol("x")
    res = be.limit((x**2-1)/(x-1), x, 1)
    assert float(res) == 2.0
