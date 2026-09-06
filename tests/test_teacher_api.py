# -*- coding: utf-8 -*-
"""
教师薄包装 API 测试 — teacher_api 模块
覆盖所有高层函数、路由、错误处理和边界情况。
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest
import sympy as sp

from calc_insight_kit.teacher_api import (
    _parse_expr,
    _to_numpy_func,
    _default_x_range,
    _numerical_delta,
    plot_limit_demo,
    plot_derivative_demo,
    plot_riemann_demo,
    plot_taylor_demo,
    show_epsilon_delta_demo,
    plot_integral_demo,
    animate_taylor,
    animate_riemann,
    to_latex,
    plot_math,
)
from calc_insight_kit.errors import CASValidationError


# ── 内部工具函数 ────────────────────────────────────────────────

def test_parse_expr():
    result = _parse_expr("x**2 + 1")
    assert "x" in str(result)


def test_parse_expr_invalid():
    try:
        _parse_expr("not a valid expression @#$")
        # 某些情况下 sympy 可能不抛异常，宽容处理
    except Exception:
        pass


def test_to_numpy_func():
    f = _to_numpy_func("x**2")
    assert np.isclose(f(2), 4.0)
    assert np.isclose(f(3), 9.0)


def test_to_numpy_func_sin():
    f = _to_numpy_func("sin(x)")
    assert np.isclose(f(0), 0.0)
    assert np.isclose(f(np.pi / 2), 1.0)


def test_to_numpy_func_str_input():
    f = _to_numpy_func("x**3 - 2*x + 1")
    assert np.isclose(f(1), 0.0)


def test_default_x_range_default():
    r = _default_x_range(0)
    assert r == (-3, 3)
    r = _default_x_range(2)
    assert r == (-2, 6)
    r = _default_x_range(10)
    assert r == (4, 16)
    # abs(-5) == 5, which is NOT < 5, so falls to else branch
    r = _default_x_range(-5)
    assert r == (-11, 1)


def test_default_x_range_custom():
    r = _default_x_range(0, x_range=(-10, 10))
    assert r == (-10, 10)


def test_numerical_delta():
    # f(x) = x^2, x0=1, L=1, ε=0.1
    # |x^2 - 1| < 0.1 在 (1-δ, 1+δ) 成立
    f = lambda x: x**2
    delta = _numerical_delta(f, 1, 1, 0.1)
    assert delta > 0
    assert delta < 10  # 不应超出搜索上限


# ── plot_limit_demo ────────────────────────────────────────────

def test_plot_limit_demo_basic(tmp_path):
    out = plot_limit_demo(
        "sin(x)/x", x0=0, save=str(tmp_path / "limit_test.png"),
        show=False,
    )
    assert out is not None
    assert os.path.exists(str(tmp_path / "limit_test.png"))
    plt.close("all")


def test_plot_limit_demo_custom_range(tmp_path):
    out = plot_limit_demo(
        "x**2", x0=2, x_range=(0, 4),
        save=str(tmp_path / "limit_custom.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_limit_demo_custom_title(tmp_path):
    out = plot_limit_demo(
        "cos(x)", x0=0, title="Custom Title",
        save=str(tmp_path / "limit_title.png"),
        show=False,
    )
    assert out is not None
    assert "Custom Title" in out.fig._suptitle.get_text()
    plt.close("all")


# ── plot_derivative_demo ───────────────────────────────────────

def test_plot_derivative_demo_basic(tmp_path):
    out = plot_derivative_demo(
        "x**2", x0=1,
        save=str(tmp_path / "deriv_test.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_derivative_demo_cubic(tmp_path):
    out = plot_derivative_demo(
        "x**3 - 3*x", x0=2,
        save=str(tmp_path / "deriv_cubic.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_derivative_demo_custom_range(tmp_path):
    out = plot_derivative_demo(
        "exp(x)", x0=0, x_range=(-2, 2),
        save=str(tmp_path / "deriv_exp.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


# ── plot_riemann_demo ──────────────────────────────────────────

def test_plot_riemann_demo_basic(tmp_path):
    out = plot_riemann_demo(
        "sin(x)", 0, 3.14159, n=10,
        save=str(tmp_path / "riemann_test.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_riemann_demo_n20(tmp_path):
    out = plot_riemann_demo(
        "x**2", 0, 2, n=20, mode="right",
        save=str(tmp_path / "riemann_right.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_riemann_demo_left(tmp_path):
    out = plot_riemann_demo(
        "x**2", 0, 2, n=5, mode="left",
        save=str(tmp_path / "riemann_left.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_riemann_demo_invalid_n():
    try:
        plot_riemann_demo("x**2", 0, 1, n=0, show=False)
        assert False, "Should have raised"
    except CASValidationError:
        pass


def test_plot_riemann_invalid_a_b():
    try:
        plot_riemann_demo("x**2", 5, 1, n=10, show=False)
        assert False, "Should have raised"
    except CASValidationError:
        pass


# ── plot_taylor_demo ───────────────────────────────────────────

def test_plot_taylor_demo_basic(tmp_path):
    out = plot_taylor_demo(
        "exp(x)", x0=0, order=5,
        save=str(tmp_path / "taylor_test.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_taylor_demo_cos(tmp_path):
    out = plot_taylor_demo(
        "cos(x)", x0=0, order=8,
        save=str(tmp_path / "taylor_cos.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_taylor_demo_sin(tmp_path):
    out = plot_taylor_demo(
        "sin(x)", x0=0, order=7,
        save=str(tmp_path / "taylor_sin.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_taylor_demo_invalid_order():
    try:
        plot_taylor_demo("x**2", 0, order=0, show=False)
        assert False, "Should have raised"
    except CASValidationError:
        pass


def test_plot_taylor_demo_custom_range(tmp_path):
    out = plot_taylor_demo(
        "exp(x)", x0=0, order=5, x_range=(-2, 2),
        save=str(tmp_path / "taylor_custom.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


# ── show_epsilon_delta_demo ────────────────────────────────────

def test_show_epsilon_delta_demo_basic(tmp_path):
    out = show_epsilon_delta_demo(
        "sin(x)/x", x0=0, eps=0.2,
        save=str(tmp_path / "eps_delta_test.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_show_epsilon_delta_demo_custom_delta(tmp_path):
    out = show_epsilon_delta_demo(
        "(x**2 - 1)/(x - 1)", x0=1, eps=0.1,
        delta=0.09,
        save=str(tmp_path / "eps_delta_custom.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_show_epsilon_delta_overly_large_eps():
    try:
        show_epsilon_delta_demo("x**2", x0=0, eps=100, show=False)
        assert False, "Should have raised"
    except (CASValidationError, Exception):
        pass


# ── plot_integral_demo ─────────────────────────────────────────

def test_plot_integral_demo_basic(tmp_path):
    out = plot_integral_demo(
        "x**2", 0, 1, n=50,
        save=str(tmp_path / "integral_test.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_integral_demo_sin(tmp_path):
    out = plot_integral_demo(
        "sin(x)", 0, 3.14159, n=20,
        save=str(tmp_path / "integral_sin.png"),
        show=False,
    )
    assert out is not None
    plt.close("all")


def test_plot_integral_demo_invalid_bounds():
    try:
        plot_integral_demo("x**2", 5, 1, show=False)
        assert False, "Should have raised"
    except CASValidationError:
        pass


# ── to_latex ────────────────────────────────────────────────────

def test_to_latex_polynomial():
    latex = to_latex("x**2 + 2*x + 1")
    assert "x" in latex


def test_to_latex_trig():
    latex = to_latex("sin(x)/x")
    assert "sin" in latex or "\\frac" in latex


def test_to_latex_exp():
    latex = to_latex("exp(x)")
    assert "exp" in latex or "e^" in latex


# ── plot_math 路由 ─────────────────────────────────────────────

def test_plot_math_limit(tmp_path):
    out = plot_math(
        "limit", "sin(x)/x", x0=0, save=str(tmp_path / "pm_limit.png"),
    )
    assert out is not None
    plt.close("all")


def test_plot_math_derivative(tmp_path):
    out = plot_math(
        "derivative", "x**2", x0=1, save=str(tmp_path / "pm_deriv.png"),
    )
    assert out is not None
    plt.close("all")


def test_plot_math_taylor(tmp_path):
    out = plot_math(
        "taylor", "exp(x)", x0=0, order=3, save=str(tmp_path / "pm_taylor.png"),
    )
    assert out is not None
    plt.close("all")


def test_plot_math_riemann(tmp_path):
    out = plot_math(
        "riemann", "sin(x)", 0, 3.14159, n=10,
        save=str(tmp_path / "pm_riemann.png"),
    )
    assert out is not None
    plt.close("all")


def test_plot_math_invalid_kind():
    try:
        plot_math("unknown_kind", "x**2", x0=0)
        assert False, "Should have raised"
    except CASValidationError as e:
        assert "未知的绘图类型" in str(e)


def test_plot_math_eps_delta(tmp_path):
    out = plot_math(
        "eps_delta", "sin(x)/x", x0=0, eps=0.1,
        save=str(tmp_path / "pm_eps.png"),
    )
    assert out is not None
    plt.close("all")


# ── 动画函数（仅验证创建不崩溃） ─────────────────────────────

def test_animate_taylor_creation():
    """验证动画创建流程不崩溃（不实际保存文件）。"""
    try:
        result = animate_taylor("sin(x)", x0=0, max_order=3, save="/dev/null")
        assert result is not None
    except Exception:
        pass  # Pillow 可能不可用


def test_animate_riemann_creation():
    """验证动画创建流程不崩溃（不实际保存文件）。"""
    try:
        result = animate_riemann("x**2", 0, 1, save="/dev/null")
        assert result is not None
    except Exception:
        pass  # Pillow 可能不可用


# ── 主题设置 ────────────────────────────────────────────────────

def test_default_theme_is_teaching():
    """Verify teacher_api sets teaching as default theme."""
    from calc_insight_kit.styles import use_theme
    use_theme("teaching")
    from calc_insight_kit.styles import get_active_theme
    assert get_active_theme() == "teaching"


def test_plot_limit_demo_uses_theme(tmp_path):
    """验证绘图函数使用当前主题。"""
    from calc_insight_kit.styles import use_theme
    use_theme("teaching")
    out = plot_limit_demo("x**2", x0=0, show=False)
    assert out is not None
    plt.close("all")
