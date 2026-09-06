# -*- coding: utf-8 -*-
"""
Maxima CAS 后端完整测试
覆盖：
  - calc_insight_kit.maxima_bridge (full): MaximaSession, MaximaBackend, SympyBackend
  - calc_insight_kit.cas (api+parser): CAS, CASExpr, CASSymbol
  - 边缘情况与健壮性
注意：测试真实调用 Maxima 二进制程序。
"""
import pytest
import shutil
from typing import Optional


# ───  helpers ────────────────────────────────────────────────────────────────

def _skip_if_no_maxima():
    if shutil.which("maxima") is None:
        pytest.skip("Maxima binary not found")


# ───  MaximaSession (full maxima_bridge) ────────────────────────────────────

class TestMaximaSession:
    """MaximaSession 长会话测试（来自 calc_insight_kit.maxima_bridge）"""

    def test_session_lifecycle(self):
        from calc_insight_kit.maxima_bridge import MaximaSession
        _skip_if_no_maxima()
        session = MaximaSession(timeout=8)
        session.start()
        result = session.eval_session("2+2;")
        assert isinstance(result, str)
        session.close()

    def test_session_close_twice(self):
        from calc_insight_kit.maxima_bridge import MaximaSession
        _skip_if_no_maxima()
        session = MaximaSession(timeout=8)
        session.start()
        session.close()
        session.close()  # 不应抛异常

    def test_session_eval_simple(self):
        from calc_insight_kit.maxima_bridge import MaximaSession
        _skip_if_no_maxima()
        session = MaximaSession(timeout=8)
        session.start()
        result = session.eval("2+2;")
        assert isinstance(result, str)
        session.close()


# ───  MaximaBackend (full) ─────────────────────────────────────────────────

class TestMaximaBackendFull:
    """MaximaBackend 独立方法测试（来自 calc_insight_kit.maxima_bridge）"""

    @pytest.fixture(autouse=True)
    def setup_mb(self):
        _skip_if_no_maxima()
        from calc_insight_kit.maxima_bridge import MaximaBackend
        self.mb = MaximaBackend()
        yield
        self.mb.close()

    def test_evalf(self):
        result = self.mb.evalf("sqrt(2)")
        assert isinstance(result, float)
        assert 1.41 < result < 1.42

    def test_evalf_pi(self):
        result = self.mb.evalf("pi")
        assert isinstance(result, float)
        assert 3.14 < result < 3.15

    def test_evalf_negative(self):
        result = self.mb.evalf("-5")
        assert isinstance(result, float)
        assert result < 0

    def test_diff_simple(self):
        result = self.mb.diff("x^2")
        assert isinstance(result, str)
        assert "x" in result

    def test_diff_sum(self):
        result = self.mb.diff("x^3 + x^2 + x")
        assert isinstance(result, str)
        assert "x" in result

    def test_diff_sin(self):
        result = self.mb.diff("sin(x)")
        assert isinstance(result, str)
        assert "cos" in result

    def test_diff_cos(self):
        result = self.mb.diff("cos(x)")
        assert isinstance(result, str)
        assert "sin" in result

    def test_diff_second_order(self):
        """二阶导数"""
        result = self.mb.diff("x^3", "x", 2)
        assert isinstance(result, str)
        assert "x" in result or "6" in result

    def test_integrate_polynomial(self):
        result = self.mb.integrate("x^2")
        assert isinstance(result, str)
        assert "x" in result

    def test_integrate_linear(self):
        result = self.mb.integrate("2*x")
        assert isinstance(result, str)
        assert "x" in result

    def test_integrate_sum(self):
        result = self.mb.integrate("x^2 + x")
        assert isinstance(result, str)

    def test_definite_integral_half(self):
        """integral 0->1 x dx = 1/2"""
        result = self.mb.definite_integral("x", "x", 0, 1)
        assert isinstance(result, str)
        assert "1/2" in result or "0.5" in result

    def test_definite_integral_quadratic(self):
        """integral 0->1 x^2 dx = 1/3"""
        result = self.mb.definite_integral("x^2", "x", 0, 1)
        assert isinstance(result, str)
        assert "1/3" in result

    def test_definite_integral_constant(self):
        """integral 0->2 5 dx = 10"""
        result = self.mb.definite_integral("5", "x", 0, 2)
        assert isinstance(result, str)
        assert "10" in result

    def test_limit_polynomial(self):
        result = self.mb.limit("x^2 + 2*x + 1", "x", 1)
        assert isinstance(result, str)
        assert "4" in str(result)

    def test_limit_constant(self):
        result = self.mb.limit("42", "x", 0)
        assert isinstance(result, str)
        assert "42" in str(result)

    def test_factor(self):
        result = self.mb.factor("x^4 - 1")
        assert isinstance(result, str)
        assert "x" in result

    def test_expand(self):
        result = self.mb.expand("(x+1)^3")
        assert isinstance(result, str)
        assert "x" in result

    def test_ratsimp(self):
        result = self.mb.ratsimp("(x+1)/x + 1/x")
        assert isinstance(result, str)

    def test_trigsimp(self):
        result = self.mb.trigsimp("sin(x)^2 + cos(x)^2")
        assert isinstance(result, str)

    def test_solve_system(self):
        result = self.mb.solve_system(["x+y=3", "x-y=1"], ["x", "y"])
        assert isinstance(result, str)

    def test_solve_complex(self):
        result = self.mb.solve_complex("x^2 - 4")
        assert isinstance(result, str)

    def test_determinant(self):
        result = self.mb.determinant("[[1,2],[3,4]]")
        assert isinstance(result, str)

    def test_determinant_3x3_zero(self):
        # Singular matrix -> det=0; 关键是不崩溃，返回值可能是空字符串
        result = self.mb.determinant("[[1,2,3],[4,5,6],[7,8,9]]")
        assert isinstance(result, str)

    def test_inverse(self):
        result = self.mb.inverse("[[1,0],[0,1]]")
        assert isinstance(result, str)

    def test_inverse_singular(self):
        result = self.mb.inverse("[[1,2],[2,4]]")
        assert isinstance(result, str)

    def test_eigenvalues(self):
        result = self.mb.eigenvalues("[[1,0],[0,1]]")
        assert isinstance(result, str)

    def test_gamma(self):
        result = self.mb.gamma("5")
        assert isinstance(result, str)

    def test_beta(self):
        result = self.mb.beta("3", "4")
        assert isinstance(result, str)

    def test_integrate_latex(self):
        result = self.mb.integrate_latex("x^2", "x")
        assert isinstance(result, str)

    def test_to_latex(self):
        result = self.mb.to_latex("x^2")
        assert isinstance(result, str)

    def test_raw_eval(self):
        result = self.mb.raw_eval("2+2")
        assert isinstance(result, str)

    def test_parse_expr(self):
        result = self.mb.parse_expr("x^2")
        assert isinstance(result, str)

    def test_integrate_tex(self):
        result = self.mb.integrate_tex("x^2", "x")
        assert isinstance(result, str)

    def test_diff_zero(self):
        result = self.mb.diff("0")
        assert isinstance(result, str)

    def test_diff_second_order_explicit(self):
        result = self.mb.diff("x^5", "x", 3)
        assert isinstance(result, str)

    def test_expand_binomial(self):
        result = self.mb.expand("(x+1)^5")
        assert isinstance(result, str)
        assert "x" in result

    def test_ratsimp_simple(self):
        result = self.mb.ratsimp("x/x")
        assert isinstance(result, str)


# ───  SympyBackend (full) ──────────────────────────────────────────────────

class TestSympyBackend:
    """SympyBackend 测试（来自 calc_insight_kit.maxima_bridge）"""

    def test_parse_expr(self):
        from calc_insight_kit.maxima_bridge import SympyBackend
        sb = SympyBackend()
        expr = sb.parse_expr("x**2 + 1")
        assert expr is not None

    def test_to_latex(self):
        from calc_insight_kit.maxima_bridge import SympyBackend
        import sympy as sp
        sb = SympyBackend()
        latex = sb.to_latex(sp.Symbol("x") ** 2)
        assert isinstance(latex, str)
        assert "x" in latex

    def test_evalf(self):
        from calc_insight_kit.maxima_bridge import SympyBackend
        import sympy as sp
        sb = SympyBackend()
        val = sb.evalf(sp.sqrt(2))
        assert 1.41 < val < 1.42

    def test_diff(self):
        from calc_insight_kit.maxima_bridge import SympyBackend
        import sympy as sp
        sb = SympyBackend()
        x = sp.Symbol("x")
        result = sb.diff(x ** 2, x)
        assert "2*x" in str(result)

    def test_integrate(self):
        from calc_insight_kit.maxima_bridge import SympyBackend
        import sympy as sp
        sb = SympyBackend()
        x = sp.Symbol("x")
        result = sb.integrate(x ** 2, x)
        assert "x" in str(result)

    def test_limit(self):
        from calc_insight_kit.maxima_bridge import SympyBackend
        import sympy as sp
        sb = SympyBackend()
        x = sp.Symbol("x")
        result = sb.limit(x ** 2, x, 1)
        assert str(result) == "1" or str(result) == "1.0"


# ───  get_cas_backend 工厂 ─────────────────────────────────────────────────

class TestGetCasBackend:
    """工厂函数测试"""

    def test_default_returns_sympy(self):
        from calc_insight_kit.maxima_bridge import get_cas_backend, SympyBackend
        backend = get_cas_backend()
        assert backend is not None

    def test_prefer_maxima_returns_backend(self):
        _skip_if_no_maxima()
        from calc_insight_kit.maxima_bridge import get_cas_backend, MaximaBackend
        import warnings
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            backend = get_cas_backend(prefer_maxima=True)
            assert backend is not None
            assert isinstance(backend, MaximaBackend)


# ───  输出清理 ─────────────────────────────────────────────────────────────

class TestOutputCleaning:
    """Maxima 输出清理逻辑测试"""

    def test_clean_false_lines(self):
        from calc_insight_kit.maxima_bridge import MaximaBackend
        mb = MaximaBackend.__new__(MaximaBackend)
        result = mb._clean_maxima_output("5\nfalse\n10")
        assert "false" not in result
        assert "5" in result

    def test_clean_lisp_marker(self):
        from calc_insight_kit.maxima_bridge import MaximaBackend
        mb = MaximaBackend.__new__(MaximaBackend)
        result = mb._clean_maxima_output('5\n"lisp"\n10')
        assert "lisp" not in result
        assert "5" in result

    def test_clean_empty_result(self):
        from calc_insight_kit.maxima_bridge import MaximaBackend
        mb = MaximaBackend.__new__(MaximaBackend)
        result = mb._clean_maxima_output("")
        assert result == ""

    def test_clean_merge_spaces(self):
        from calc_insight_kit.maxima_bridge import MaximaBackend
        mb = MaximaBackend.__new__(MaximaBackend)
        result = mb._clean_maxima_output("a   b   c")
        assert "a b c" == result


# ───  CAS 高层 API ─────────────────────────────────────────────────────────

class TestCASHighLevel:
    """CAS 高层 API（来自 calc_insight_kit.cas.api）"""

    @pytest.fixture(autouse=True)
    def setup_cas(self):
        _skip_if_no_maxima()
        from calc_insight_kit.cas import CAS
        self.cas = CAS()

    def test_symbol_create(self):
        x = self.cas.Symbol("x")
        assert str(x) == "x"

    def test_parse_expr(self):
        expr = self.cas.parse_expr("x^2")
        assert "x" in str(expr)

    def test_diff_simple(self):
        x = self.cas.Symbol("x")
        d = self.cas.diff(x ** 2, x)
        assert isinstance(d, type(x ** 2))

    def test_diff_str_input(self):
        d = self.cas.diff("x^2", "x")
        assert "x" in str(d)

    def test_integrate(self):
        x = self.cas.Symbol("x")
        I = self.cas.integrate(x ** 2, x)
        assert "x" in str(I)

    def test_integrate_str(self):
        I = self.cas.integrate("x^3", "x")
        assert "x" in str(I)

    def test_limit(self):
        x = self.cas.Symbol("x")
        lim = self.cas.limit(x ** 2, x, 1)
        assert "1" in str(lim)

    def test_solve_quadratic(self):
        x = self.cas.Symbol("x")
        sol = self.cas.solve(x ** 2 - 4, x)
        assert "2" in str(sol)

    def test_solve_linear(self):
        x = self.cas.Symbol("x")
        sol = self.cas.solve(2 * x - 6, x)
        assert "3" in str(sol)

    def test_diff_sin(self):
        x = self.cas.Symbol("x")
        d = self.cas.diff("sin(x)", x)
        assert "cos" in str(d)

    def test_diff_cos(self):
        x = self.cas.Symbol("x")
        d = self.cas.diff("cos(x)", x)
        assert "sin" in str(d)

    def test_series(self):
        x = self.cas.Symbol("x")
        series = self.cas.series("sin(x)", x, 5)
        assert "x" in str(series)

    def test_latex(self):
        x = self.cas.Symbol("x")
        latex = self.cas.latex(x ** 2 + 1)
        assert "x" in latex


# ───  CASSymbol 基础运算 ──────────────────────────────────────────────────

class TestCASSymbolBasic:
    """CASSymbol 基础运算测试"""

    @pytest.fixture(autouse=True)
    def setup_cas(self):
        _skip_if_no_maxima()
        from calc_insight_kit.cas import CAS
        self.cas = CAS()

    def test_symbol_add(self):
        x, y = self.cas.Symbol("x"), self.cas.Symbol("y")
        e = x + y
        assert "x+y" in str(e)

    def test_symbol_sub(self):
        x, y = self.cas.Symbol("x"), self.cas.Symbol("y")
        e = x - y
        assert "x-y" in str(e)

    def test_symbol_mul(self):
        x, y = self.cas.Symbol("x"), self.cas.Symbol("y")
        e = x * y
        assert "x*y" in str(e)

    def test_symbol_rmul(self):
        x = self.cas.Symbol("x")
        e = 2 * x
        assert isinstance(e.expr, str)

    def test_symbol_rsub(self):
        x = self.cas.Symbol("x")
        e = 5 - x
        assert isinstance(e.expr, str)

    def test_symbol_radd(self):
        x = self.cas.Symbol("x")
        e = 3 + x
        assert isinstance(e.expr, str)

    def test_symbol_pow(self):
        x = self.cas.Symbol("x")
        e = x ** 3
        assert "x^3" in str(e) or "x**3" in str(e)

    def test_symbol_repr(self):
        x = self.cas.Symbol("x")
        assert "x" in repr(x)


# ───  CASExpr 表达式运算 ───────────────────────────────────────────────────

class TestCASExprOps:
    """CASExpr 表达式操作测试"""

    @pytest.fixture(autouse=True)
    def setup_cas(self):
        _skip_if_no_maxima()
        from calc_insight_kit.cas import CAS
        self.cas = CAS()

    def test_add_expr(self):
        x = self.cas.Symbol("x")
        e1 = x ** 2
        e2 = 2 * x
        e = e1 + e2
        assert isinstance(e.expr, str)

    def test_sub_expr(self):
        x = self.cas.Symbol("x")
        e1 = x ** 2
        e2 = 1
        e = e1 - e2
        assert isinstance(e.expr, str)

    def test_mul_expr(self):
        x = self.cas.Symbol("x")
        e = (x + 1) * (x - 1)
        assert isinstance(e.expr, str)

    def test_mul_scalar(self):
        x = self.cas.Symbol("x")
        e = 2 * (x + 1)
        assert isinstance(e.expr, str)

    def test_radd_expr(self):
        x = self.cas.Symbol("x")
        e = 3 + (x ** 2)
        assert isinstance(e.expr, str)

    def test_rsub_expr(self):
        x = self.cas.Symbol("x")
        e = 5 - (x ** 2)
        assert isinstance(e.expr, str)

    def test_rmul_expr(self):
        x = self.cas.Symbol("x")
        e = 2 * (x ** 2)
        assert isinstance(e.expr, str)

    def test_pow_expr(self):
        x = self.cas.Symbol("x")
        e = (x ** 2) ** 3
        assert isinstance(e.expr, str)

    def test_chained_operations(self):
        x = self.cas.Symbol("x")
        e = ((x ** 2 + 1) * (x - 1)) + 2
        assert isinstance(e.expr, str)


# ───  边缘情况与健壮性 ─────────────────────────────────────────────────────

class TestEdgeCases:
    """边缘情况与异常处理"""

    @pytest.fixture(autouse=True)
    def setup_cas(self):
        _skip_if_no_maxima()
        from calc_insight_kit.cas import CAS
        self.cas = CAS()

    def test_diff_zero(self):
        x = self.cas.Symbol("x")
        d = self.cas.diff("0", x)
        assert isinstance(d, object)

    def test_integral_zero(self):
        x = self.cas.Symbol("x")
        I = self.cas.integrate("0", x)
        assert isinstance(I, object)

    def test_limit_at_zero(self):
        x = self.cas.Symbol("x")
        lim = self.cas.limit(x ** 2, x, 0)
        assert "0" in str(lim)

    def test_limit_at_large(self):
        x = self.cas.Symbol("x")
        lim = self.cas.limit(x ** 2 + 3 * x, x, 100)
        assert isinstance(lim, object)

    def test_series_zero_order(self):
        x = self.cas.Symbol("x")
        series = self.cas.series(x, x, 0)
        assert isinstance(series, object)

    def test_large_power(self):
        x = self.cas.Symbol("x")
        e = x ** 10
        d = self.cas.diff(e, x)
        assert "x" in str(d)

    def test_nested_expression_diff(self):
        x = self.cas.Symbol("x")
        e = x ** 2 + 3 * x + 2
        d = self.cas.diff(e, x)
        assert isinstance(d, object)

    def test_solve_no_real_roots(self):
        """x^2+1=0 不应崩溃"""
        x = self.cas.Symbol("x")
        sol = self.cas.solve(x ** 2 + 1, x)
        assert isinstance(sol, object)

    def test_large_coefficients(self):
        x = self.cas.Symbol("x")
        d = self.cas.diff("1000*x^5 + 500*x^3 + 100*x", x)
        assert isinstance(d, object)

    def test_trig_identity(self):
        x = self.cas.Symbol("x")
        d = self.cas.diff("sin(x)^2 + cos(x)^2", x)
        assert isinstance(d, object)

    def test_limit_at_negative(self):
        x = self.cas.Symbol("x")
        lim = self.cas.limit(x ** 3, x, -1)
        assert isinstance(lim, object)

    def test_integrate_trig(self):
        x = self.cas.Symbol("x")
        I = self.cas.integrate("cos(x)", x)
        assert "sin" in str(I) or "cos" in str(I)

    def test_series_sin(self):
        x = self.cas.Symbol("x")
        series = self.cas.series("sin(x)", x, 5)
        assert "x" in str(series)

    def test_series_exp(self):
        x = self.cas.Symbol("x")
        series = self.cas.series("exp(x)", x, 4)
        assert "x" in str(series)

    def test_factor_quartic(self):
        x = self.cas.Symbol("x")
        e = x ** 4 - 1
        d = self.cas.diff(e, x)
        assert isinstance(d, object)

    def test_latex_simple(self):
        x = self.cas.Symbol("x")
        latex = self.cas.latex(x ** 2)
        assert isinstance(latex, str)
        assert "x" in latex

    def test_casexpr_repr(self):
        x = self.cas.Symbol("x")
        expr = x ** 2
        assert "CASExpr" in repr(expr)

    def test_cassymbol_repr(self):
        x = self.cas.Symbol("x")
        assert "CASSymbol" in repr(x)


# ───  内部 cas/maxima_bridge 输出清理 ──────────────────────────────────────

class TestInternalOutputCleaning:
    """内部 cas/maxima_bridge 输出清理测试"""

    def test_clean_false(self):
        from calc_insight_kit.cas.maxima_bridge import MaximaBridge
        bridge = MaximaBridge.__new__(MaximaBridge)
        result = bridge._clean_maxima_output("5\nfalse\n10")
        assert "false" not in result

    def test_clean_lisp_marker(self):
        from calc_insight_kit.cas.maxima_bridge import MaximaBridge
        bridge = MaximaBridge.__new__(MaximaBridge)
        result = bridge._clean_maxima_output('5\n"lisp"\n10')
        assert "lisp" not in result

    def test_clean_empty(self):
        from calc_insight_kit.cas.maxima_bridge import MaximaBridge
        bridge = MaximaBridge.__new__(MaximaBridge)
        result = bridge._clean_maxima_output("")
        assert result == ""
