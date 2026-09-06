# -*- coding: utf-8 -*-
"""
结构化报错模块测试 — 验证异常类、验证函数、装饰器
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib
matplotlib.use("Agg")

from calc_insight_kit.errors import (
    CASBaseError,
    CASValidationError,
    CASComputationalError,
    CASVisualizationError,
    CASBackendError,
    validate_positive,
    validate_non_negative,
    validate_range,
    validate_limit_context,
    validate_derivative_context,
    validate_riemann_params,
    validate_taylor_params,
    validate_integral_bounds,
    validate_epsilon_delta_demo_params,
    validate_plot_bounds,
    handle_cas_errors,
)


# ── 异常类测试 ───────────────────────────────────────────────

def test_cas_validation_error_attributes():
    e = CASValidationError("test", "hint", "solution")
    assert e.message == "test"
    assert e.teaching_hint == "hint"
    assert e.solution == "solution"
    assert "test" in str(e)
    assert "提示：hint" in str(e)
    assert "建议：solution" in str(e)


def test_cas_validation_error_no_hint():
    e = CASValidationError("only message")
    assert e.message == "only message"
    assert e.teaching_hint == ""
    assert e.solution == ""
    assert "提示：" not in str(e)
    assert "建议：" not in str(e)


def test_exception_hierarchy():
    assert issubclass(CASValidationError, CASBaseError)
    assert issubclass(CASComputationalError, CASBaseError)
    assert issubclass(CASVisualizationError, CASBaseError)
    assert issubclass(CASBackendError, CASBaseError)
    assert issubclass(CASBaseError, Exception)


# ── validate_positive ─────────────────────────────────────────

def test_validate_positive_ok():
    validate_positive(1)
    validate_positive(0.01)
    validate_positive(100)


def test_validate_positive_zero():
    try:
        validate_positive(0)
        assert False
    except CASValidationError as e:
        assert "必须为正值" in str(e)
        assert "提示" in str(e)


def test_validate_positive_negative():
    try:
        validate_positive(-1)
        assert False
    except CASValidationError as e:
        assert "必须为正值" in str(e)


def test_validate_positive_none():
    try:
        validate_positive(None)
        assert False
    except CASValidationError as e:
        assert "不能为 None" in str(e)


def test_validate_positive_wrong_type():
    try:
        validate_positive("abc")
        assert False
    except CASValidationError as e:
        assert "必须为数值类型" in str(e)


def test_validate_positive_named():
    try:
        validate_positive(0, "epsilon")
        assert False
    except CASValidationError as e:
        assert "epsilon" in str(e)


# ── validate_non_negative ────────────────────────────────────

def test_validate_non_negative_ok():
    validate_non_negative(0)
    validate_non_negative(5)


def test_validate_non_negative_negative():
    try:
        validate_non_negative(-1)
        assert False
    except CASValidationError as e:
        assert "不能为负数" in str(e)


# ── validate_range ───────────────────────────────────────────

def test_validate_range_ok():
    validate_range(5, "val", min_val=0, max_val=10)


def test_validate_range_below_min():
    try:
        validate_range(-1, "val", min_val=0)
        assert False
    except CASValidationError as e:
        assert "不能小于 0" in str(e)


def test_validate_range_above_max():
    try:
        validate_range(15, "val", max_val=10)
        assert False
    except CASValidationError as e:
        assert "不能大于 10" in str(e)


# ── validate_limit_context ──────────────────────────────────

def test_validate_limit_context_ok():
    validate_limit_context(0, 1.0, 0.1)


def test_validate_limit_context_zero_eps():
    try:
        validate_limit_context(0, 1.0, 0)
        assert False
    except CASValidationError as e:
        assert "必须为正数" in str(e)


def test_validate_limit_context_negative_eps():
    try:
        validate_limit_context(0, 1.0, -0.1)
        assert False
    except CASValidationError as e:
        assert "必须为正数" in str(e)


def test_validate_limit_context_overly_large():
    try:
        validate_limit_context(0, 1.0, 100)
        assert False
    except CASValidationError as e:
        assert "过大" in str(e)


# ── validate_derivative_context ──────────────────────────────

def test_validate_derivative_context_ok():
    validate_derivative_context("x**2", "x")


def test_validate_derivative_context_empty_var():
    try:
        validate_derivative_context("x**2", "")
        assert False
    except CASValidationError as e:
        assert "必须是字符串" in str(e)


def test_validate_derivative_context_none_expr():
    try:
        validate_derivative_context(None, "x")
        assert False
    except CASValidationError as e:
        assert "必须是字符串" in str(e)


# ── validate_riemann_params ──────────────────────────────────

def test_validate_riemann_params_ok():
    validate_riemann_params(0, 1, 10)
    validate_riemann_params(0, 1, 10, "left")
    validate_riemann_params(0, 1, 10, "right")
    validate_riemann_params(0, 1, 10, "midpoint")


def test_validate_riemann_params_zero_n():
    try:
        validate_riemann_params(0, 1, 0)
        assert False
    except CASValidationError as e:
        assert "正整数" in str(e)


def test_validate_riemann_params_invalid_mode():
    try:
        validate_riemann_params(0, 1, 10, "invalid")
        assert False
    except CASValidationError as e:
        assert "无效" in str(e)


def test_validate_riemann_params_a_b():
    try:
        validate_riemann_params(5, 1, 10)
        assert False
    except CASValidationError as e:
        assert "不能大于上限" in str(e)


# ── validate_taylor_params ───────────────────────────────────

def test_validate_taylor_params_ok():
    validate_taylor_params(3, 0)


def test_validate_taylor_params_zero_order():
    try:
        validate_taylor_params(0, 0)
        assert False
    except CASValidationError as e:
        assert "正整数" in str(e)


def test_validate_taylor_params_negative_order():
    try:
        validate_taylor_params(-1, 0)
        assert False
    except CASValidationError as e:
        assert "正整数" in str(e)


# ── validate_integral_bounds ─────────────────────────────────

def test_validate_integral_bounds_ok():
    validate_integral_bounds(0, 5)


def test_validate_integral_bounds_equal():
    try:
        validate_integral_bounds(5, 5)
        assert False
    except CASValidationError as e:
        assert "不能大于上限" in str(e)


def test_validate_integral_bounds_a_b():
    try:
        validate_integral_bounds(10, 0)
        assert False
    except CASValidationError as e:
        assert "不能大于上限" in str(e)


# ── validate_plot_bounds ─────────────────────────────────────

def test_validate_plot_bounds_ok():
    validate_plot_bounds((-5, 5))
    validate_plot_bounds((-5, 5), ylim=None)


def test_validate_plot_bounds_none():
    try:
        validate_plot_bounds(None)
        assert False
    except CASValidationError as e:
        assert "不能为 None" in str(e)


def test_validate_plot_bounds_wrong_len():
    try:
        validate_plot_bounds((-5, 0, 5))
        assert False
    except CASValidationError as e:
        assert "长度为 2" in str(e)


def test_validate_plot_bounds_reversed():
    try:
        validate_plot_bounds((5, -5))
        assert False
    except CASValidationError as e:
        assert "不能大于" in str(e)


# ── handle_cas_errors 装饰器 ─────────────────────────────────

def _bad_func():
    raise ValueError("test error")


@handle_cas_errors
def decorated_value_error():
    raise ValueError("test")


@handle_cas_errors
def decorated_type_error():
    raise TypeError("test")


@handle_cas_errors
def decorated_zero_division():
    return 1 / 0


@handle_cas_errors
def decorated_general():
    raise RuntimeError("unexpected")


@handle_cas_errors
def decorated_ok():
    return "success"


def test_handle_cas_errors_value_error():
    try:
        decorated_value_error()
        assert False
    except CASValidationError as e:
        assert "参数值错误" in str(e)


def test_handle_cas_errors_type_error():
    try:
        decorated_type_error()
        assert False
    except CASValidationError as e:
        assert "参数类型错误" in str(e)


def test_handle_cas_errors_zero_division():
    try:
        decorated_zero_division()
        assert False
    except CASComputationalError as e:
        assert "除以零" in str(e)


def test_handle_cas_errors_general():
    try:
        decorated_general()
        assert False
    except CASComputationalError as e:
        assert "计算失败" in str(e)


def test_handle_cas_errors_ok():
    assert decorated_ok() == "success"


def test_handle_cas_errors_preserves_cas_base():
    @handle_cas_errors
    def raises_cas():
        raise CASValidationError("existing", "hint", "sol")
    try:
        raises_cas()
        assert False
    except CASValidationError as e:
        assert e.message == "existing"
        assert e.teaching_hint == "hint"
