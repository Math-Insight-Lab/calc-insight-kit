# -*- coding: utf-8 -*-
"""
cas/maxima_bridge.py — CAS 子包的极简 Maxima 桥接层
复用 ..maxima_bridge.MaximaSession 做子进程管理，避免重复实现。
仅暴露 cas/parser.py 需要的最小组合 API (eval/parse/to_latex)。
"""

from typing import Optional

# 复用主模块的子进程管理，消除代码重复
from ..maxima_bridge import MaximaSession


class MaximaBridge:
    """适配器：将 MaximaSession 包装为 cas/parser.py 需要的极简接口"""
    def __init__(self, timeout: float = 8.0):
        self._session = MaximaSession(timeout=timeout)

    def eval(self, code: str, timeout: Optional[float] = None) -> str:
        return self._session.eval(code)

    def _send(self, code: str) -> None:
        self._session.eval(code)

    def _recv(self, timeout: Optional[float] = None) -> str:
        # cas 子包不单独调用 _recv，始终为空
        return ""

    @staticmethod
    def _clean_maxima_output(out: str) -> str:
        """清理 Maxima 输出：去掉 false、\"lisp\" 标记等噪声行。"""
        lines = []
        for line in out.splitlines():
            stripped = line.strip()
            if stripped in ("false", '"lisp"', ''):
                continue
            if stripped:
                lines.append(stripped)
        if not lines:
            return ""
        import re
        result = " ".join(lines)
        result = re.sub(r'\s+', ' ', result).strip()
        return result


class MaximaBackend:
    """CAS 子包的极简后端，仅支持 eval / parse / to_latex。

    注意：这是与 top-level ``calc_insight_kit.maxima_bridge.MaximaBackend``
    不同的精简实现，专供 ``cas/parser.py`` 内部的 ``CASExpr`` 使用。
    """
    def __init__(self, bridge: Optional[MaximaBridge] = None):
        self._bridge = bridge or MaximaBridge()

    def eval(self, code: str, timeout: Optional[float] = None) -> str:
        return self._bridge.eval(code, timeout)

    def _recv(self, timeout: Optional[float] = None) -> str:
        return self._bridge._recv(timeout)

    def _send(self, code: str) -> None:
        self._bridge._send(code)

    def _sympyify(self, s: str):
        import sympy as sp
        return sp.sympify(s)

    def parse(self, expr_str: str):
        """将 Maxima 输出字符串解析为 SymPy 表达式。"""
        s = expr_str.strip()
        lines = s.splitlines()
        s = "\n".join(line for line in lines if not line.startswith("print"))
        s = s.strip()
        if not s:
            import sympy as sp
            return sp.Integer(0)
        return self._sympyify(s)

    def to_latex(self, expr) -> str:
        """导出 LaTeX 格式字符串。"""
        code = f"tex({expr});\n"
        out = self.eval(code)
        return out


def make_maxima_session(bridge=None, timeout: float = 8.0):
    """兼容旧 API：直接返回 MaximaSession 实例。"""
    return MaximaSession(timeout=timeout)


def quit_maxima(proc=None):
    """兼容旧 API：关闭 MaximaSession 或 Popen 进程。"""
    if proc is None:
        return
    if hasattr(proc, "close"):
        proc.close()
    else:
        try:
            proc.terminate()
            proc.wait()
        except Exception:
            pass


def get_cas_backend() -> MaximaBackend:
    """CAS 后端工厂（cas 子包专用）。"""
    return MaximaBackend()
