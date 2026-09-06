# -*- coding: utf-8 -*-
"""
CAS 模块：封装 Maxima 调用，提供 SymPy 风格的接口
"""
from .maxima_bridge import MaximaBackend, get_cas_backend
from .parser import CASExpr, CASSymbol
from .api import CAS

__all__ = [
    "CAS",
    "CASExpr",
    "CASSymbol",
    "get_cas_backend",
    "MaximaBackend",
]
