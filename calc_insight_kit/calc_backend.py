# -*- coding: utf-8 -*-
"""
双 CAS 计算后端核心 V1.0.0
支持 SymPy 正式运行、Maxima 预留扩展、双引擎对比接口
"""
import sympy as sp
from typing import Dict, Any, Optional, Tuple
from .config import DEFAULT_CAS_ENGINE, SUPPORT_CAS_ENGINE


class SympyBackend:
    """SymPy 高精度符号计算后端"""
    def __init__(self):
        self.engine = "sympy"

    def limit(self, expr, var, point, dir: Optional[str] = None):
        if dir is None:
            return sp.limit(expr, var, point)
        return sp.limit(expr, var, point, dir=dir)

    def diff(self, expr, var, order: int = 1):
        return sp.diff(expr, var, order)

    def integrate(self, expr, var, bounds: Optional[Tuple] = None):
        if bounds is None:
            return sp.integrate(expr, var)
        return sp.integrate(expr, (var, *bounds))

    def taylor(self, expr, var, x0, order: int):
        return sp.series(expr, var, x0=x0, n=order+1).removeO()


class MaximaBackend:
    """Maxima 后端预留扩展（大学对比测试专用）。
    
    实际实现位于 ``calc_insight_kit.maxima_bridge.MaximaBackend``。
    此类仅为保持向后兼容的占位符，不应直接实例化使用。
    """
    pass


def get_cas_backend(engine: Optional[str] = None):
    if engine is None:
        engine = DEFAULT_CAS_ENGINE
    if engine not in SUPPORT_CAS_ENGINE:
        raise ValueError(f"不支持的 CAS 引擎：{engine}，支持列表：{SUPPORT_CAS_ENGINE}")
    
    if engine == "sympy":
        return SympyBackend()
    elif engine == "maxima":
        from .maxima_bridge import get_cas_backend as maxima_get_cas_backend
        return maxima_get_cas_backend(prefer_maxima=True)


def limit_epsilon_delta(expr, var, x0, eps: float, backend) -> Dict[str, Any]:
    lim_val = backend.limit(expr, var, x0)
    lim_float = float(lim_val)
    delta = eps * 1.2
    return {
        "limit_value": lim_float,
        "epsilon": eps,
        "delta": delta,
        "x_left": x0 - delta,
        "x_right": x0 + delta
    }
