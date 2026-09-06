#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Maxima 定积分的正确语法
"""
import subprocess

def test_maxima(code, label=""):
    print(f"\n--- {label} ---")
    print(f"Command: {code.strip()}")
    try:
        proc = subprocess.Popen(
            ["maxima", "--very-quiet"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(code.strip() + "\n", timeout=10)
        lines = [l.strip() for l in stdout.splitlines() if l.strip() and l.strip() not in ('false', '"lisp"')]
        result = " ".join(lines).strip()
        print(f"Result: {result[:200]}")
        if stderr.strip():
            print(f"Stderr: {stderr.strip()[:200]}")
    except Exception as e:
        print(f"ERROR: {e}")

# Test definite integral syntax variations
test_maxima("integrate(x^2, x, 0, 1);", "integrate(expr, var, a, b)")
test_maxima("integrate(x^2, [x, 0, 1]);", "integrate(expr, [var, a, b])")
test_maxima("integrate(sin(x), [x, 0, %pi]);", "integrate(sin(x), [x, 0, %pi])")
test_maxima("defintegral1:true,integrate(x^2,[x,0,1]);", "with defintegral1:true")
test_maxima("defintegral2:true,integrate(sin(x),[x,0,4*atan(1)]);", "with defintegral2:true")
test_maxima("defint(x^2,x,0,1);", "defint(expr, var, a, b)")
