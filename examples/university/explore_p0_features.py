#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
探索 P0 功能的 Maxima 实现
"""
import subprocess
import re

def test_maxima(code, label=""):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  cmd: {code.strip()}")
    print(f"{'─'*60}")
    try:
        proc = subprocess.Popen(
            ["maxima", "--very-quiet"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(code.strip() + "\n", timeout=10)
        # 清理输出
        lines = [l.strip() for l in stdout.splitlines() if l.strip() and l.strip() not in ('false', '"lisp"')]
        result = " ".join(lines).strip()
        print(f"  ✅ {result[:200]}")
        if stderr.strip():
            print(f"  ⚠️ stderr: {stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        print("  ❌ TIMEOUT")
    except Exception as e:
        print(f"  ❌ {e}")

# ========== 1. 极限 ==========
print("=" * 60)
print("  1. 极限 (Limits)")
print("=" * 60)

test_maxima("limit(sin(x)/x, x, 0, plus);", "右极限 sin(x)/x")
test_maxima("limit(sin(x)/x, x, 0, minus);", "左极限 sin(x)/x")
test_maxima("limit(sin(1/x), x, 0);", "振荡极限 sin(1/x)")
test_maxima("limit((x^2-4)/(x-2), x, 2);", "可去间断点极限 (x^2-4)/(x-2)")

# ========== 2. 定积分/反常积分 ==========
print("\n" + "=" * 60)
print("  2. 定积分/反常积分 (Definite Integrals)")
print("=" * 60)

test_maxima("defint(x^2, x, 0, 1);", "∫₀¹ x²dx")
test_maxima("defint(exp(-x), x, 0, inf);", "∫₀^∞ e^(-x)dx")
test_maxima("defint(1/(x^2+1), x, 0, inf);", "∫₀^∞ 1/(x²+1)dx")
test_maxima("defint(1/sqrt(x), x, 0, 1);", "反常积分 ∫₀¹ 1/√x dx")

# 带参数定积分
test_maxima("defint(a*x^2, x, 0, 1);", "∫₀¹ a·x²dx")
test_maxima("defint(exp(-a*x), x, 0, inf);", "∫₀^∞ e^(-ax)dx")

# 变上限积分
test_maxima("defint(sin(t), t, 0, x);", "变上限积分 ∫₀^x sin(t)dt")

# 级数求和
print("\n" + "=" * 60)
print("  3. 级数求和 (Sum)")
print("=" * 60)

test_maxima("sum(1/n^2, n, 1, inf);", "∑1/n² (n=1→∞)")
test_maxima("sum(1/2^n, n, 0, inf);", "∑1/2ⁿ (n=0→∞)")
test_maxima("sum(n, n, 1, 10);", "∑n (n=1→10)")
test_maxima("sum(1/n!, n, 0, inf);", "∑1/n! (n=0→∞) = e")
test_maxima("sum(k*x^k, k, 0, n);", "∑kxᵏ (k=0→n)")

# 洛朗展开
print("\n" + "=" * 60)
print("  4. 洛朗展开 (Laurent Series)")
print("=" * 60)

test_maxima("taylor(1/x, x, 0, 5);", "1/x 的洛朗展开")
test_maxima("taylor(1/(x*(1-x)), x, 0, 4);", "1/(x(1-x)) 洛朗展开")

# 符号不等式
print("\n" + "=" * 60)
print("  5. 符号不等式 (Inequalities)")
print("=" * 60)

test_maxima("load(solve_ineq); solve_ineq((x-1)*(x+2) > 0, x);", "(x-1)(x+2)>0")
test_maxima("load(solve_ineq); solve_ineq(x^2 - 3*x + 2 <= 0, x);", "x²-3x+2<=0")
test_maxima("load(solve_ineq); solve_ineq(abs(x-1) < epsilon, x);", "|x-1|<ε")

# 高级化简
print("\n" + "=" * 60)
print("  6. 高级化简 (Advanced Simplification)")
print("=" * 60)

test_maxima("ratsimp((x+1)/(x^2-1) + 1/(x-1));", "ratsimp: (x+1)/(x²-1)+1/(x-1)")
test_maxima("ratsimp((1/x + 1/y)/(1/x - 1/y));", "ratsimp: (1/x+1/y)/(1/x-1/y)")
test_maxima("trigsimp(cos(x)^2 - sin(x)^2);", "trigsimp: cos²-sin²")
test_maxima("trigsimp(sin(2*x)/sin(x));", "trigsimp: sin(2x)/sin(x)")
test_maxima("radcan((x^2-1)/(x-1));", "radcan: (x^2-1)/(x-1)")
test_maxima("radcan((x^3-1)/(x-1));", "radcan: (x^3-1)/(x-1)")

# 方程组
print("\n" + "=" * 60)
print("  7. 非线性方程组 (Nonlinear Systems)")
print("=" * 60)

test_maxima("solve([x+y=3, x*y=2], [x,y]);", "x+y=3, xy=2")

# 定积分带参数 + 求导
print("\n" + "=" * 60)
print("  8. 变限积分求导 (Fenmu)")
print("=" * 60)

test_maxima("diff(defint(sin(t), t, 0, x), x);", "d/dx ∫₀^x sin(t)dt")
test_maxima("diff(defint(t^2, t, 0, x^2), x);", "d/dx ∫₀^{x²} t²dt")
