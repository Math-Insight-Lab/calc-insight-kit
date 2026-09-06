"""
maxima_bridge.py：Maxima CAS桥接 v0.1-enhanced
SymPy(默认) / Maxima(外部进程)双后端；支持积分、微分、极限、latex导出、数值求值
注意：Maxima是外部可执行程序，需要系统安装maxima
"""
import shutil
import subprocess
import warnings
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
import sympy as sp


def detect_maxima_binary() -> Optional[str]:
    return shutil.which("maxima")


class MaximaSession:
    """长会话，复用maxima子进程，避免反复启动开销"""
    def __init__(self, timeout: float = 8.0):
        self.bin_path = detect_maxima_binary()
        self.timeout = timeout
        self._proc: Optional[subprocess.Popen] = None
        if self.bin_path is None:
            raise RuntimeError("maxima executable not found on system. Please install maxima.")

    def start(self):
        self._proc = subprocess.Popen(
            [self.bin_path, "--very-quiet"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def close(self):
        if self._proc is not None:
            try:
                self._proc.stdin.write("quit();\n")
                self._proc.stdin.flush()
            except Exception:
                pass
            self._proc.terminate()
            self._proc.wait()
            self._proc = None

    def eval(self, maxima_code: str) -> str:
        """执行maxima代码，返回原始输出字符串"""
        # --very-quiet mode doesn't emit reliable prompt markers,
        # so use a fresh subprocess per command for reliability.
        proc = subprocess.Popen(
            [self.bin_path, "--very-quiet"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            stdout, stderr = proc.communicate(maxima_code.strip() + "\n", timeout=self.timeout)
            return stdout or ""
        except subprocess.TimeoutExpired:
            proc.kill()
            return ""

    def eval_session(self, maxima_code: str) -> str:
        """长会话模式：复用已启动的子进程"""
        if self._proc is None:
            self.start()
        assert self._proc is not None
        cmd = maxima_code.strip() + "\n"
        self._proc.stdin.write(cmd)
        self._proc.stdin.flush()
        # Read with timeout using select
        import select
        import time
        buf = ""
        idle_ticks = 0
        deadline = time.monotonic() + self.timeout
        poll = select.poll()
        poll.register(self._proc.stdout, select.POLLIN)
        while time.monotonic() < deadline:
            events = poll.poll(200)
            if not events:
                idle_ticks += 1
                if idle_ticks >= 5:  # 1 second of no output -> done
                    break
                continue
            idle_ticks = 0
            line = self._proc.stdout.readline()
            if not line:
                break
            buf += line
            stripped = line.strip()
            if stripped == "":
                break
        return buf


class CASBackendBase(ABC):
    @abstractmethod
    def parse_expr(self, expr_str: str):
        ...

    @abstractmethod
    def to_latex(self, expr) -> str:
        ...

    @abstractmethod
    def evalf(self, expr) -> float:
        ...

    @abstractmethod
    def diff(self, expr, var):
        ...

    @abstractmethod
    def integrate(self, expr, var):
        ...

    @abstractmethod
    def limit(self, expr, var, x0):
        ...


class SympyBackend(CASBackendBase):
    def __init__(self):
        self.x = sp.Symbol("x")

    def parse_expr(self, expr_str: str):
        return sp.parse_expr(expr_str, transformations='all')

    def to_latex(self, expr) -> str:
        return sp.latex(expr)

    def evalf(self, expr) -> float:
        return float(expr.evalf())

    def diff(self, expr, var):
        return sp.diff(expr, var)

    def integrate(self, expr, var):
        return sp.integrate(expr, var)

    def limit(self, expr, var, x0):
        return sp.limit(expr, var, x0)


class MaximaBackend(CASBackendBase):
    def __init__(self):
        self.session = MaximaSession()
        self.sympy_backend = SympyBackend()

    def parse_expr(self, expr_str: str):
        """返回原始 maxima 表达式字符串，不转 Python 对象；本桥为文本层桥接"""
        return expr_str

    def to_latex(self, expr) -> str:
        """expr: maxima 表达式字符串，调用 tex()"""
        out = self.session.eval(f'display2d: false; tex({expr});\n')
        # 清理 maxima 输出标记 (%i) (%o) 、末尾 false
        lines = [line.strip() for line in out.splitlines() if not line.startswith("(%i") and not line.startswith("(%o)")]
        raw = "\n".join(lines).replace("false","").strip()
        return raw

    def integrate_latex(self, expr, var_name="x") -> str:
        """积分并返回 LaTeX 格式"""
        out = self.session.eval(f'display2d: false; tex(integrate({expr},{var_name}));\n')
        lines = [line.strip() for line in out.splitlines() if not line.startswith("(%i") and not line.startswith("(%o)")]
        raw = "\n".join(lines).replace("false","").strip()
        return raw

    def limit(self, expr, var_name="x", x0=0) -> str:
        result = self._maxima_eval(f"limit({expr},{var_name},{x0});")
        if isinstance(result, str):
            return result
        return float(result)

    def evalf(self, expr) -> float:
        out = self._maxima_eval(f"float({expr});")
        try:
            return float(out)
        except (ValueError, TypeError):
            try:
                s = sp.sympify(expr)
                return float(s.evalf())
            except Exception:
                raise RuntimeError(
                    f"MaximaBackend.evalf({expr!r}) could not evaluate to a number"
                )

    def raw_eval(self, code: str) -> str:
        return self.session.eval(code)

    def _maxima_eval(self, code: str, timeout: Optional[float] = None) -> str:
        """执行 Maxima 命令，统一使用 lisp 格式输出（SymPy 风格）"""
        raw = self.session.eval(f'display2d: false; format: "lisp";\n{code.strip()}\n')
        return self._clean_maxima_output(raw)

    def integrate(self, expr, var_name="x") -> str:
        out = self._maxima_eval(f"integrate({expr},{var_name});")
        return self._clean_maxima_output(out)

    def definite_integral(self, expr, var_name="x", lower=0, upper=1) -> str:
        """
        定积分计算: ∫_{lower}^{upper} expr dx
        使用 Maxima 的 defint(expr, var, a, b)
        """
        result = self._maxima_eval(f"defint({expr},{var_name},{lower},{upper});")
        return self._clean_maxima_output(result)

    def diff(self, expr, var_name="x", n: int = 1) -> str:
        if n == 1:
            return self._maxima_eval(f"diff({expr},{var_name});")
        return self._maxima_eval(f"diff({expr},{var_name},{n});")

    def factor(self, expr) -> str:
        """因式分解: factor(x^4-1) -> (x-1)(x+1)(x^2+1)"""
        return self._maxima_eval(f"factor({expr});")

    def expand(self, expr) -> str:
        """多项式展开: expand((x+1)^5)"""
        return self._maxima_eval(f"expand({expr});")

    def ratsimp(self, expr) -> str:
        """有理分式化简: ratsimp((1/x+1/y)/(1/x-1/y))"""
        return self._maxima_eval(f"ratsimp({expr});")

    def trigsimp(self, expr) -> str:
        """三角化简: trigsimp(sin(x)^2+cos(x)^2) -> 1"""
        return self._maxima_eval(f"trigsimp({expr});")

    def solve_system(self, equations: List[str], variables: List[str]) -> str:
        """
        方程组求解: solve_system(["x+y=3", "x-y=1"], ["x", "y"])
        Maxima 返回 [[x=2, y=1]]
        """
        eq_str = "[" + ",".join(equations) + "]"
        var_str = "[" + ",".join(variables) + "]"
        return self._maxima_eval(f"solve({eq_str},{var_str});")

    def solve_complex(self, expr, var_name="x") -> str:
        """
        求解包含复数根的方程: solve_complex("x^2+1", "x")
        返回 [x=-i, x=i]
        """
        result = self._maxima_eval(f"radcan(solve({expr}={0 if '+' not in expr else '0'},{var_name}));")
        return self._clean_maxima_output(result)

    def determinant(self, matrix_str: str) -> str:
        """行列式: determinant([[a,b],[c,d]])"""
        return self._maxima_eval(f"determinant(matrix({matrix_str}));")

    def inverse(self, matrix_str: str) -> str:
        """逆矩阵: inverse([[a,b],[c,d]])"""
        return self._maxima_eval(f"inverse(matrix({matrix_str}));")

    def eigenvalues(self, matrix_str: str) -> str:
        """特征值: eigenvalues([[a,b],[c,d]])"""
        return self._maxima_eval(f"eigenvalues(matrix({matrix_str}));")

    def gamma(self, expr) -> str:
        """Gamma 函数: gamma(5) -> 24"""
        return self._maxima_eval(f"gamma({expr});")

    def beta(self, a, b) -> str:
        """Beta 函数: beta(3, 4)"""
        return self._maxima_eval(f"beta({a},{b});")

    def _clean_maxima_output(self, out: str) -> str:
        """清理 Maxima lisp 格式输出：去掉 false、格式字符串标记"""
        lines = []
        skip_next = False
        for line in out.splitlines():
            stripped = line.strip()
            # 跳过 Maxima 设置命令的返回值
            if stripped == 'false' or stripped == '"lisp"':
                continue
            # 保留有效输出行
            if stripped:
                lines.append(stripped)
        if not lines:
            return ""
        # 合并所有有效行为一行，用空格分隔
        result = " ".join(lines)
        # 合并多余空格
        import re
        result = re.sub(r'\s+', ' ', result).strip()
        return result

    def integrate_tex(self, expr, var_name="x") -> str:
        # 直接获取 LaTeX 格式
        out = self.session.eval(f'display2d: false; tex(integrate({expr},{var_name}));\n')
        lines = [line.strip() for line in out.splitlines() if not line.startswith("(%i") and not line.startswith("(%o)")]
        raw = "\n".join(lines).replace("false","").strip()
        return raw

    def close(self):
        self.session.close()


def get_cas_backend(prefer_maxima: bool = False) -> CASBackendBase:
    if prefer_maxima:
        bin_path = detect_maxima_binary()
        if bin_path is not None:
            return MaximaBackend()
        else:
            warnings.warn("Maxima binary not found, fallback to SymPy backend")
    return SympyBackend()
