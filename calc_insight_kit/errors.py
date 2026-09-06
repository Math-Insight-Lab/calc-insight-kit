# -*- coding: utf-8 -*-
"""
结构化报错与教学提示 — 面向学习者的异常系统。

与普通 Python 数学库只返回原始堆栈不同，本模块提供：
  - CASValidationError: 参数校验错误，附带教学提示
  - CASComputationalError: 计算错误，附带原因说明
  - CASVisualizationError: 绘图错误，附带解决建议

每个异常都包含：
  - message: 标准错误信息
  - teaching_hint: 面向学习者的提示文本
  - solution: 建议的解决方案

用法：
    from calc_insight_kit.errors import (
        CASValidationError,
        CASComputationalError,
        validate_positive,
        validate_limit_context,
    )

    # 自动抛出带教学提示的异常
    validate_positive(eps, "epsilon")
    # 如果 eps <= 0，抛出:
    # CASValidationError: epsilon 必须为正值，当前值为 -0.5
    # 提示：ε 应当取大于0的实数，请回顾极限ε-δ定义

    # 手动创建自定义提示
    raise CASValidationError(
        message="ε 必须为正数",
        teaching_hint="ε 代表误差允许范围，在极限定义中必须 ε > 0",
        solution="请检查 epsilon 参数是否大于 0"
    )
"""

from typing import Optional


class CASBaseError(Exception):
    """CAS 计算库基础异常，所有自定义异常的基类。"""

    def __init__(
        self,
        message: str,
        teaching_hint: str = "",
        solution: str = "",
    ):
        self.message = message
        self.teaching_hint = teaching_hint
        self.solution = solution
        # 构建完整消息
        parts = [message]
        if teaching_hint:
            parts.append(f"\n提示：{teaching_hint}")
        if solution:
            parts.append(f"建议：{solution}")
        super().__init__("\n".join(parts))


class CASValidationError(CASBaseError):
    """参数验证错误 — 用户输入不符合数学要求。

    示例：
        validate_positive(0, "n")  # n 为分割数，必须 > 0
    """
    pass


class CASComputationalError(CASBaseError):
    """计算错误 — CAS 引擎无法完成计算。

    示例：
        积分发散、方程无实数解、级数不收敛等。
    """
    pass


class CASVisualizationError(CASBaseError):
    """可视化错误 — 绘图参数有问题或渲染失败。

    示例：
        坐标范围无效、数据超出显示范围、字体缺失等。
    """
    pass


class CASBackendError(CASBaseError):
    """后端错误 — CAS 引擎（SymPy/Maxima）调用失败。

    示例：
        Maxima 进程崩溃、SymPy 语法错误等。
    """
    pass


# ── 便捷验证函数 ──────────────────────────────────────────────────────

def validate_positive(value, name: str = "参数"):
    """验证值是否为正数。"""
    if value is None:
        raise CASValidationError(
            message=f"{name} 不能为 None",
            teaching_hint=f"{name} 必须是一个有效的正数",
            solution="请检查是否遗漏了参数赋值",
        )
    if not isinstance(value, (int, float)):
        raise CASValidationError(
            message=f"{name} 必须为数值类型，当前为 {type(value).__name__}",
            teaching_hint="数学计算中，数值参数必须是 int 或 float 类型",
            solution=f"请将 {name} 改为一个数字，例如 {name}=1.0",
        )
    if value <= 0:
        raise CASValidationError(
            message=f"{name} 必须为正值，当前值为 {value}",
            teaching_hint=_get_positive_hint(name),
            solution=f"请设置 {name} > 0，例如 {name}=0.1",
        )


def validate_non_negative(value, name: str = "参数"):
    """验证值是否为非负数。"""
    if value is None:
        raise CASValidationError(
            message=f"{name} 不能为 None",
            teaching_hint=f"{name} 必须是一个有效的非负数",
            solution="请检查是否遗漏了参数赋值",
        )
    if not isinstance(value, (int, float)):
        raise CASValidationError(
            message=f"{name} 必须为数值类型，当前为 {type(value).__name__}",
            teaching_hint="数学计算中，数值参数必须是 int 或 float 类型",
            solution=f"请将 {name} 改为一个数字",
        )
    if value < 0:
        raise CASValidationError(
            message=f"{name} 不能为负数，当前值为 {value}",
            teaching_hint=f"{name} 应当为非负数",
            solution=f"请设置 {name} >= 0",
        )


def validate_range(value, name: str, min_val=None, max_val=None):
    """验证值是否在指定范围内。"""
    if value is None:
        raise CASValidationError(
            message=f"{name} 不能为 None",
            teaching_hint=f"{name} 必须是一个有效的数值",
            solution="请检查是否遗漏了参数赋值",
        )
    if min_val is not None and value < min_val:
        raise CASValidationError(
            message=f"{name} 不能小于 {min_val}，当前值为 {value}",
            teaching_hint=f"{name} 的下限为 {min_val}",
            solution=f"请设置 {name} >= {min_val}",
        )
    if max_val is not None and value > max_val:
        raise CASValidationError(
            message=f"{name} 不能大于 {max_val}，当前值为 {value}",
            teaching_hint=f"{name} 的上限为 {max_val}",
            solution=f"请设置 {name} <= {max_val}",
        )


def validate_limit_context(x0, lim_val, eps: float):
    """验证极限 ε-δ 定义的参数合理性。

    这是教学向校验的典型例子：普通库只报 ValueError，
    这里会告诉学生为什么错了、该怎么改。
    """
    if not isinstance(eps, (int, float)):
        raise CASValidationError(
            message="epsilon 必须是数值类型",
            teaching_hint="ε 应该是一个正实数，表示允许的误差范围",
            solution="请将 epsilon 设置为一个正数，例如 0.1",
        )
    if eps <= 0:
        raise CASValidationError(
            message=f"epsilon={eps} 必须为正数",
            teaching_hint="ε 应当取大于 0 的实数，请回顾极限 ε-δ 定义",
            solution="请设置 epsilon > 0，例如 epsilon=0.01",
        )
    if not isinstance(x0, (int, float)):
        raise CASValidationError(
            message="x0 必须是数值类型",
            teaching_hint="x0 是极限趋近的点，应该是实数",
            solution="请检查 x0 是否正确设置",
        )
    if not isinstance(lim_val, (int, float)):
        raise CASValidationError(
            message=f"极限值 {lim_val} 无法解析为数值",
            teaching_hint="极限值应该是实数。如果极限不存在（如无穷大），请先确认极限存在",
            solution="请检查函数在 x0 附近是否有确定的极限值",
        )
    # 检查 ε 是否过大
    if eps > 10:
        raise CASValidationError(
            message=f"epsilon={eps} 过大",
            teaching_hint="ε 通常取较小的正数（如 0.01、0.001），过大的 ε 会导致 δ 区间过大，失去极限意义",
            solution="请减小 epsilon，例如 epsilon=0.01",
        )


def validate_derivative_context(expr_str: str, var: str):
    """验证求导参数的合理性。"""
    if not var or not isinstance(var, str):
        raise CASValidationError(
            message="求变量 var 必须是字符串",
            teaching_hint="求导时需要指定对哪个变量求导，例如 'x'",
            solution="请提供求变量名，例如 var='x'",
        )
    if not expr_str or not isinstance(expr_str, str):
        raise CASValidationError(
            message="表达式必须是字符串",
            teaching_hint="表达式需要用字符串表示，例如 'x**2 + 1'",
            solution="请将表达式写成字符串，例如 expr_str='x**2 + 1'",
        )


def validate_riemann_params(a, b, n, mode="midpoint"):
    """验证黎曼和参数的合理性。"""
    if not isinstance(n, int) or n <= 0:
        raise CASValidationError(
            message=f"分割数 n={n} 必须是正整数",
            teaching_hint="n 表示区间 [a,b] 分割成多少份矩形，n 必须是正整数",
            solution="请设置 n 为正整数，例如 n=50",
        )
    if a >= b:
        raise CASValidationError(
            message=f"积分下限 a={a} 不能大于上限 b={b}",
            teaching_hint="黎曼和的积分区间 [a,b] 要求 a < b",
            solution="请交换 a 和 b，使 a < b",
        )
    valid_modes = ["left", "right", "midpoint"]
    if mode not in valid_modes:
        raise CASValidationError(
            message=f"求和模式 '{mode}' 无效",
            teaching_hint=f"支持的求和模式: {', '.join(valid_modes)}",
            solution=f"请将 mode 设为 '{valid_modes[2]}'（中点法则）或其他有效值",
        )


def validate_taylor_params(order: int, x0):
    """验证泰勒展开参数的合理性。"""
    if not isinstance(order, int) or order < 1:
        raise CASValidationError(
            message=f"展开阶数 order={order} 必须是正整数",
            teaching_hint="泰勒展开阶数必须是正整数，阶数越高近似越精确但计算越慢",
            solution="请设置 order 为正整数，例如 order=3",
        )
    if not isinstance(x0, (int, float)):
        raise CASValidationError(
            message=f"展开中心 x0={x0} 必须是数值",
            teaching_hint="x0 是泰勒展开的中心点，应该是实数",
            solution="请设置 x0 为一个实数，例如 x0=0",
        )


def validate_integral_bounds(a, b):
    """验证积分上下限的合理性。"""
    if not isinstance(a, (int, float)):
        raise CASValidationError(
            message=f"积分下限 a={a} 必须是数值",
            teaching_hint="积分限必须是实数",
            solution="请设置 a 为一个实数",
        )
    if not isinstance(b, (int, float)):
        raise CASValidationError(
            message=f"积分上限 b={b} 必须是数值",
            teaching_hint="积分限必须是实数",
            solution="请设置 b 为一个实数",
        )
    if a >= b:
        raise CASValidationError(
            message=f"积分下限 a={a} 不能大于上限 b={b}",
            teaching_hint="积分区间 [a,b] 要求 a < b",
            solution="请交换 a 和 b",
        )


def validate_epsilon_delta_demo_params(f_func, x0, lim_val, eps):
    """验证 ε-δ 演示参数的合理性。"""
    validate_limit_context(x0, lim_val, eps)
    if f_func is None:
        raise CASValidationError(
            message="函数 f 不能为 None",
            teaching_hint="ε-δ 定义需要明确的函数表达式",
            solution="请提供函数 f，例如 lambda x: (x**2 - 1) / (x - 1)",
        )


def validate_plot_bounds(xlim, ylim=None):
    """验证绘图坐标范围。"""
    if xlim is None:
        raise CASValidationError(
            message="x 轴范围 xlim 不能为 None",
            teaching_hint="绘图需要指定 x 轴显示范围",
            solution="请设置 xlim，例如 xlim=(-5, 5)",
        )
    if not isinstance(xlim, (list, tuple)) or len(xlim) != 2:
        raise CASValidationError(
            message=f"xlim 应该是长度为 2 的序列，当前为 {xlim}",
            teaching_hint="xlim 格式为 (x_min, x_max)",
            solution="请设置 xlim=(xmin, xmax)",
        )
    if xlim[0] >= xlim[1]:
        raise CASValidationError(
            message=f"xlim[0]={xlim[0]} 不能大于 xlim[1]={xlim[1]}",
            teaching_hint="x 轴范围应该是 (最小值, 最大值)",
            solution="请交换 xlim 的两个值",
        )


# ── 内部辅助 ─────────────────────────────────────────────────────────

def _get_positive_hint(name: str) -> str:
    """根据参数名返回具体的教学提示。"""
    hints = {
        "epsilon": "ε 代表误差允许范围，在极限定义中必须 ε > 0",
        "delta": "δ 代表自变量允许的变化范围，在极限定义中必须 δ > 0",
        "n": "n 表示区间分割数，必须是正整数",
        "order": "阶数必须是正整数，阶数越高近似越精确",
        "h": "步长 h 必须是正数，h → 0 时导数定义成立",
    }
    return hints.get(name, f"{name} 必须为正数")


# ── 统一异常处理装饰器 ───────────────────────────────────────────────

def handle_cas_errors(func):
    """装饰器：将 CAS 计算中的常见异常转换为友好的教学异常。

    用法：
        @handle_cas_errors
        def compute_limit(expr, x, x0):
            ...  # 内部 SymPy/Maxima 调用

        compute_limit("sin(x)/x", "x", 0)
        # 如果出错，会抛出带教学提示的 CASValidationError 等
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CASBaseError:
            raise  # 已经是我们的异常，直接抛出
        except ValueError as e:
            raise CASValidationError(
                message=f"参数值错误: {e}",
                teaching_hint="请检查输入参数是否符合数学要求",
                solution="查看函数文档确认参数格式",
            )
        except TypeError as e:
            raise CASValidationError(
                message=f"参数类型错误: {e}",
                teaching_hint="请检查参数类型是否正确",
                solution="确保所有参数类型与文档一致",
            )
        except ZeroDivisionError:
            raise CASComputationalError(
                message="计算中出现除以零",
                teaching_hint="函数在计算点可能无定义或趋于无穷",
                solution="请检查函数在该点是否有定义",
            )
        except Exception as e:
            raise CASComputationalError(
                message=f"计算失败: {type(e).__name__}: {e}",
                teaching_hint="CAS 引擎在执行计算时遇到了意外错误",
                solution="请检查表达式是否正确，或尝试简化问题",
            )

    return wrapper
