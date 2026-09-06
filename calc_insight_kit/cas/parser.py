# -*- coding: utf-8 -*-
"""
CAS 表达式解析：模仿 SymPy 风格的封装
"""
import subprocess
import shutil
from typing import Optional, List, Dict, Any, Union

import sympy as sp

from .maxima_bridge import MaximaBackend, make_maxima_session, quit_maxima, get_cas_backend


def _get_bridge():
    """获取 CAS 后端"""
    return get_cas_backend()


def _normalize_var(var) -> str:
    """将变量名标准化为字符串"""
    if isinstance(var, CASSymbol):
        return var.name
    return str(var)


class CASSymbol:
    """CAS 符号类：模仿 sympy.Symbol 的 API，但底层是 Maxima 表达式"""
    def __init__(self, name: str) -> None:
        self.name = name
        self.expr = name

    def __repr__(self) -> str:
        return f"CASSymbol({self.name!r})"

    def __str__(self) -> str:
        return self.name

    def __add__(self, other) -> "CASExpr":
        if isinstance(other, (int, float)):
            return CASExpr(f"({self.expr}+{other})")
        return CASExpr(f"({self.expr}+{other.expr})")

    def __sub__(self, other) -> "CASExpr":
        if isinstance(other, (int, float)):
            return CASExpr(f"({self.expr}-{other})")
        return CASExpr(f"({self.expr}-{other.expr})")

    def __mul__(self, other) -> "CASExpr":
        if isinstance(other, (int, float)):
            return CASExpr(f"({self.expr}*{other})")
        return CASExpr(f"({self.expr}*{other.expr})")

    def __rmul__(self, other: int) -> "CASExpr":
        return CASExpr(f"{other}*{self.expr}")

    def __rsub__(self, other: int) -> "CASExpr":
        return CASExpr(f"{other}-{self.expr}")

    def __pow__(self, exp: int) -> "CASExpr":
        return CASExpr(f"{self.expr}^{exp}")

    def __radd__(self, other: int) -> "CASExpr":
        return CASExpr(f"{other}+{self.expr}")

    def diff(self, var: Union["CASSymbol", str]) -> "CASExpr":
        """对 var 求导"""
        var_str = _normalize_var(var)
        bridge = _get_bridge()
        code = f"diff({self.expr},{var_str});\n"
        out = bridge.eval(code)
        return CASExpr(out)


class CASExpr:
    """CAS 表达式类：封装 Maxima 表达式字符串，提供 SymPy 风格的 API"""
    def __init__(self, expr: str) -> None:
        self.expr = expr
        self._backend = None

    def __repr__(self) -> str:
        return f"CASExpr({self.expr!r})"

    def __str__(self) -> str:
        return self.expr

    def __add__(self, other: Union["CASExpr", int, float, "CASSymbol"]) -> "CASExpr":
        if isinstance(other, (int, float)):
            return CASExpr(f"({self.expr}+{other})")
        return CASExpr(f"({self.expr}+{other.expr})")

    def __radd__(self, other: int) -> "CASExpr":
        return CASExpr(f"({other}+{self.expr})")

    def __sub__(self, other: Union["CASExpr", int, float, "CASSymbol"]) -> "CASExpr":
        if isinstance(other, (int, float)):
            return CASExpr(f"({self.expr}-{other})")
        return CASExpr(f"({self.expr}-{other.expr})")

    def __rsub__(self, other: int) -> "CASExpr":
        return CASExpr(f"({other}-{self.expr})")

    def __mul__(self, other: Union["CASExpr", int, float, "CASSymbol"]) -> "CASExpr":
        if isinstance(other, (int, float)):
            return CASExpr(f"({other})*({self.expr})")
        return CASExpr(f"({self.expr}*{other.expr})")

    def __rmul__(self, other: int) -> "CASExpr":
        return CASExpr(f"({other})*({self.expr})")

    def __pow__(self, exp: int) -> "CASExpr":
        return CASExpr(f"({self.expr})^{exp}")

    @property
    def backend(self) -> MaximaBackend:
        if self._backend is None:
            self._backend = _get_bridge()
        return self._backend

    def diff(self, var: Union["CASSymbol", str]) -> "CASExpr":
        """对 var 求导"""
        var_str = _normalize_var(var)
        code = f"diff({self.expr},{var_str});\n"
        out = self.backend.eval(code)
        return CASExpr(out)

    def integrate(self, var: Union["CASExpr", int, float, "CASSymbol"]) -> "CASExpr":
        """对 var 积分"""
        var_str = _normalize_var(var)
        code = f"integrate({self.expr},{var_str});\n"
        out = self.backend.eval(code)
        return CASExpr(out)

    def limit(self, var: Union["CASExpr", int, float, "CASSymbol"], point: float) -> "CASExpr":
        """计算 var -> point 的极限"""
        var_str = _normalize_var(var)
        code = f"limit({self.expr},{var_str},{point});\n"
        out = self.backend.eval(code)
        return CASExpr(out)

    def solve(self, *vars: Union["CASExpr", int, float, "CASSymbol"]) -> "CASExpr":
        """求解方程"""
        var_names = [_normalize_var(v) for v in vars]
        code = f"solve({self.expr},{','.join(var_names)});\n"
        out = self.backend.eval(code)
        return CASExpr(out)

    def dsolve(self, *vars: Union["CASExpr", int, float, "CASSymbol"]) -> "CASExpr":
        """求解微分方程"""
        var_names = [_normalize_var(v) for v in vars]
        code = f"ode2({self.expr},{var_names[-1]},{var_names[0]});\n"
        out = self.backend.eval(code)
        return CASExpr(out)

    def series(self, var: Union["CASExpr", int, float, "CASSymbol"], order: int) -> "CASExpr":
        """泰勒级数展开"""
        var_str = _normalize_var(var)
        code = f"taylor({self.expr},{var_str},0,{order});\n"
        out = self.backend.eval(code)
        return CASExpr(out)

    def latex(self) -> str:
        """导出 LaTeX 字符串"""
        return self.backend.parse(self.expr).__str__()


class MaximaBackend:
    """Maxima CAS 后端（Python 层封装，模仿 SymPy 风格）"""
    def __init__(self, bridge: "MaximaBridge"):
        self._bridge = bridge

    def eval(self, code: str, timeout: Optional[float] = None) -> str:
        return self._bridge.eval(code, timeout)

    def _recv(self, timeout: Optional[float] = None) -> str:
        return self._bridge._recv(timeout)

    def _send(self, code: str) -> None:
        self._bridge._send(code)

    def _sympyify(self, s: str) -> sp.Expr:
        return sp.sympify(s)

    def parse(self, expr_str: str) -> sp.Expr:
        """将 Maxima 输出字符串解析为 SymPy 表达式。"""
        s = expr_str.strip()
        lines = s.splitlines()
        s = "\n".join(line for line in lines if not line.startswith("print"))
        s = s.strip()
        if not s:
            return sp.Integer(0)
        return self._sympyify(s)

    def to_latex(self, expr: sp.Expr) -> str:
        """将 SymPy 表达式转换为 LaTeX 字符串。"""
        code = f"tulu({expr});\n"
        out = self.eval(code)
        return out
