#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
探索 Maxima 在 calc-insight-kit 中还能支持哪些功能。
测试 Maxima 的各种数学能力，对比现有实现。
"""
import subprocess

def test_maxima(code: str, label: str = ""):
    """执行 Maxima 命令并打印结果"""
    print(f"\n{'─'*60}")
    print(f"  {label or code.strip().rstrip(';')}")
    print(f"  命令: {code.strip()}")
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
        if result:
            print(f"  Maxima: {result}")
        else:
            print("  (empty output)")
    except Exception as e:
        print(f"  ERROR: {e}")

def main():
    print("=" * 60)
    print("  Maxima 功能探索 — 对比 SymPy")
    print("=" * 60)

    # ========== 1. 代数化简 ==========
    print("\n" + "=" * 60)
    print("  1. 代数化简 (Algebraic Simplification)")
    print("=" * 60)

    test_maxima("factor(x^4 - 1);", "因式分解 x⁴-1")
    test_maxima("factor(x^6 - 1);", "因式分解 x⁶-1")
    test_maxima("expand((x+1)^5);", "展开 (x+1)^5")
    test_maxima("expand((a+b)^4);", "展开 (a+b)^4")
    test_maxima("ratsimp((1/x + 1/y)/(1/x - 1/y));", "有理分式化简")
    test_maxima("trigsimp(sin(x)^2 + cos(x)^2);", "三角化简 sin²+cos²")
    test_maxima("trigsimp(sin(2*x));", "三角化简 sin(2x)")
    test_maxima("trigsimp(cos(x)^2 - sin(x)^2);", "三角化简 cos²-sin²")

    # ========== 2. 极限 ==========
    print("\n" + "=" * 60)
    print("  2. 极限 (Limits)")
    print("=" * 60)

    test_maxima("limit(sin(x)/x, x, 0);", "sin(x)/x 当 x→0")
    test_maxima("limit((1+1/x)^x, x, inf);", "(1+1/x)^x 当 x→∞")
    test_maxima("limit(exp(x)/x, x, inf);", "exp(x)/x 当 x→∞")
    test_maxima("limit(sin(x)/x, x, 0, plus);", "sin(x)/x 当 x→0+ (右极限)")
    test_maxima("limit(sin(x)/x, x, 0, minus);", "sin(x)/x 当 x→0- (左极限)")

    # ========== 3. 微分 ==========
    print("\n" + "=" * 60)
    print("  3. 微分 (Derivatives)")
    print("=" * 60)

    test_maxima("diff(x^4 + 3*x^2 + x, x, 2);", "二阶导数")
    test_maxima("diff(exp(x)*sin(x), x, 3);", "三阶导数")
    test_maxima("diff(log(x)/x, x);", "log(x)/x 导数")
    test_maxima("diff(sin(x)/x, x);", "sin(x)/x 导数")
    test_maxima("diff(x^x, x);", "x^x 导数")

    # ========== 4. 积分 ==========
    print("\n" + "=" * 60)
    print("  4. 积分 (Integrals)")
    print("=" * 60)

    test_maxima("integrate(x^2, x);", "∫x²dx")
    test_maxima("integrate(1/(1+x^2), x);", "∫1/(1+x²)dx")
    test_maxima("integrate(exp(x)*sin(x), x);", "∫eˣsin(x)dx")
    test_maxima("integrate(x*exp(x^2), x);", "∫xeˣ²dx")
    test_maxima("integrate(1/(x^2-1), x);", "∫1/(x²-1)dx")
    test_maxima("integrate(sin(x)^3, x);", "∫sin³(x)dx")
    test_maxima("integrate(cos(x)^3, x);", "∫cos³(x)dx")

    # ========== 5. 级数展开 ==========
    print("\n" + "=" * 60)
    print("  5. 级数展开 (Series/Taylor)")
    print("=" * 60)

    test_maxima("taylor(exp(x), x, 0, 6);", "eˣ 泰勒展开 6阶")
    test_maxima("taylor(sin(x), x, 0, 7);", "sin(x) 泰勒展开 7阶")
    test_maxima("taylor(cos(x), x, 0, 6);", "cos(x) 泰勒展开 6阶")
    test_maxima("taylor(log(1+x), x, 0, 5);", "log(1+x) 泰勒展开 5阶")

    # ========== 6. 方程求解 ==========
    print("\n" + "=" * 60)
    print("  6. 方程求解 (Solving Equations)")
    print("=" * 60)

    test_maxima("solve(x^2 - 4, x);", "x²-4=0")
    test_maxima("solve(x^3 - 6*x^2 + 11*x - 6 = 0, x);", "x³-6x²+11x-6=0")
    test_maxima("solve([x+y=3, x-y=1], [x,y]);", "联立方程组")
    test_maxima("solve(x^2 + 2*x + 1 = 0, x);", "x²+2x+1=0 重根")
    test_maxima("solve(x^2 + 1 = 0, x);", "x²+1=0 复根")

    # ========== 7. 特殊函数 ==========
    print("\n" + "=" * 60)
    print("  7. 特殊函数 (Special Functions)")
    print("=" * 60)

    test_maxima("gamma(5);", "Gamma(5) = 4!")
    test_maxima("gamma(1/2);", "Gamma(1/2) = √π")
    test_maxima("beta(3, 4);", "Beta(3,4)")
    test_maxima("besselj(0, x);", "Bessel J₀(x)")

    # ========== 8. 线性代数 ==========
    print("\n" + "=" * 60)
    print("  8. 线性代数 (Linear Algebra)")
    print("=" * 60)

    test_maxima("load(linalg);\ndeterminant(matrix([a,b],[c,d]));", "行列式 |a b; c d|")
    test_maxima("load(linalg);\ninverse(matrix([a,b],[c,d]));", "逆矩阵")
    test_maxima("load(linalg);\neigenvalues(matrix([a,b],[c,d]));", "特征值")

    # ========== 9. 定积分 ==========
    print("\n" + "=" * 60)
    print("  9. 定积分 (Definite Integrals)")
    print("=" * 60)

    test_maxima("integrate(x^2, [x, 0, 1]);", "∫₀¹ x²dx")
    test_maxima("integrate(exp(x), [x, 0, 1]);", "∫₀¹ eˣdx")
    test_maxima("integrate(sin(x), [x, 0, %pi]);", "∫₀^π sin(x)dx")

    print("\n" + "=" * 60)
    print("  ✅ 探索完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
