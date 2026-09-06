# -*- coding: utf-8 -*-
"""
基础函数合法性测试
"""
import sympy as sp
from calc_insight_kit import get_cas_backend, derivative_plot_data

def test_cas_basic():
    backend = get_cas_backend("sympy")
    x = sp.Symbol("x")
    assert float(backend.limit(sp.sin(x)/x, x, 0)) == 1.0

def test_derivative_data():
    x = sp.Symbol("x")
    f = sp.sin(x)
    data = derivative_plot_data(f, x, 0)
    assert "f_func" in data
    assert "df_x0" in data
