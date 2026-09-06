# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
CAS API：高层接口，模仿 SymPy 风格
"""
import shutil
import subprocess
from typing import List, Tuple, Optional, Union
from .parser import CASExpr, CASSymbol, get_cas_backend
from .maxima_bridge import MaximaBackend
import sympy as sp

class CAS:
    """
    CAS 计算后端工厂类。
    
    用法：
        cas = CAS()
        x = cas.Symbol("x")
        expr = x**2 + 2*x + 1
        print(expr.diff(x))    # 求导
        print(expr.integrate(x))  # 积分
        print(expr.limit(x, 0)) # 极限
        print(expr.solve())     # 求解
        print(expr.series(x, 5))  # 级数展开
        print(expr.latex())     # 导出 LaTeX
    """
    def __init__(self):
        self._backend = get_cas_backend()

    def Symbol(self, name: str) -> CASSymbol:
        """创建符号对象"""
        return CASSymbol(name)

    def parse_expr(self, expr_str: str) -> CASExpr:
        """解析 Maxima 表达式字符串"""
        return CASExpr(expr_str)

    def diff(self, expr: Union["CASExpr", str], var: str) -> "CASExpr":
        """对 expr 求导，返回 CASExpr"""
        if isinstance(expr, str):
            expr = CASExpr(expr)
        return expr.diff(var)

    def integrate(self, expr: Union["CASExpr", str], var: str) -> "CASExpr":
        """对 expr 积分，返回 CASExpr"""
        if isinstance(expr, str):
            expr = CASExpr(expr)
        return expr.integrate(var)

    def limit(self, expr: Union["CASExpr", str], var: str, point: float) -> "CASExpr":
        """计算 expr 在 var → point 的极限"""
        if isinstance(expr, str):
            expr = CASExpr(expr)
        return expr.limit(var, point)

    def solve(self, expr: Union["CASExpr", str], *vars: str) -> "CASExpr":
        """求解方程 expr，返回解列表"""
        if isinstance(expr, str):
            expr = CASExpr(expr)
        return expr.solve(*vars)

    def dsolve(self, expr: Union["CASExpr", str], *vars: str) -> "CASExpr":
        """求解微分方程 expr"""
        if isinstance(expr, str):
            expr = CASExpr(expr)
        return expr.dsolve(*vars)

    def series(self, expr: Union["CASExpr", str, "CASSymbol"], var: str, order: int) -> "CASExpr":
        """泰勒级数展开"""
        if isinstance(expr, str):
            expr = CASExpr(expr)
        if isinstance(expr, CASSymbol):
            expr = CASExpr(expr.expr)
        return expr.series(var, order)

    def latex(self, expr: Union["CASExpr", str]) -> str:
        """导出 LaTeX 字符串"""
        if isinstance(expr, str):
            expr = CASExpr(expr)
        return expr.latex()

    def _recv(self, timeout: Optional[float] = None) -> str:
        """从 Maxima 接收输出"""
        return self._backend._recv(timeout)

    def _send(self, code: str) -> None:
        """向 Maxima 发送命令"""
        self._backend._send(code)


def get_cas_backend() -> MaximaBackend:
    """
    CAS 后端工厂：返回 Maxima 后端实例。
    
    注意：底层调用 quit() 会退出 Maxima，所以每次 eval 都是独立会话。
    如需复用进程，请在外部管理会话对象。
    """
    bridge = MaximaBridge()
    return MaximaBackend(bridge)


class MaximaBridge:
    """Maxima 桥接层：管理 Maxima 子进程，发送/接收消息"""
    def __init__(self, timeout: float = 8.0):
        self.timeout = timeout
        self.bin_path = shutil.which("maxima")
        if self.bin_path is None:
            raise RuntimeError("Maxima 未安装。请安装 maxima 二进制程序：sudo apt install maxima")
        
    def _send(self, code: str) -> None:
        proc = self._proc
        if proc is None:
            self._proc = subprocess.Popen(
                [self.bin_path, "--very-quiet"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        assert self._proc is not None
        cmd = code.strip() + "\n"
        self._proc.stdin.write(cmd)
        self._proc.stdin.flush()

    def _recv(self, timeout: Optional[float] = None) -> str:
        proc = self._proc
        assert proc is not None
        stdout, stderr = proc.communicate(timeout=timeout)
        out = stdout.decode("utf-8").rstrip("\n")
        proc = None
        return out

    def eval(self, code: str, timeout: Optional[float] = None) -> str:
        self._send(code)
        return self._recv(timeout)


def make_maxima_session(bridge: MaximaBridge, timeout: float = 8.0) -> subprocess.Popen:
    """
    长会话：复用 maxima 子进程，避免反复启动开销。
    
    返回：Popen 对象。使用者需负责 quit 调用。
    """
    bridge._proc = subprocess.Popen(
        [bridge.bin_path, "--very-quiet"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return bridge._proc


def quit_maxima(proc: subprocess.Popen) -> None:
    """退出 Maxima 进程"""
    if proc is not None:
        try:
            proc.stdin.write("quit();\n")
            proc.stdin.flush()
        except Exception:
            pass
        proc.terminate()
        proc.wait()
        proc = None


def get_cas_backend() -> "MaximaBackend":
    """
    CAS 后端工厂：返回 Maxima 后端实例。
    
    注意：底层调用 quit() 会退出 Maxima，所以每次 eval 都是独立会话。
    如需复用进程，请在外部管理会话对象。
    """
    bridge = MaximaBridge()
    return MaximaBackend(bridge)


class MaximaBackend:
    """Maxima CAS 后端（Python 层封装，模仿 SymPy 风格）"""
    def __init__(self, bridge: MaximaBridge):
        self._bridge = bridge

    def eval(self, code: str, timeout: Optional[float] = None) -> str:
        return self._bridge.eval(code, timeout)

    def _recv(self, timeout: Optional[float] = None) -> str:
        return self._bridge._recv(timeout)

    def _send(self, code: str) -> None:
        self._bridge._send(code)

    def _sympyify(self, s: str) -> sp.Expr:
        return sp.sympify(s, transformations="all")

    def parse(self, expr_str: str) -> sp.Expr:
        """
        将 Maxima 输出字符串解析为 SymPy 表达式。
        
        内部调用 sp.sympify，并清理可能残留的打印输出。
        """
        s = expr_str.strip()
        lines = s.splitlines()
        s = "\n".join(line for line in lines if not line.startswith("print"))
        s = s.strip()
        if not s:
            return sp.Integer(0)
        return self._sympyify(s)

    def to_latex(self, expr: sp.Expr) -> str:
        """
        将 SymPy 表达式转换为 LaTeX 字符串。
        
        底层调用 maxima 的 tulu() 函数导出 LaTeX。
        """
        code = f"tulu({expr});\\n"
        out = self.eval(code)
        return out
