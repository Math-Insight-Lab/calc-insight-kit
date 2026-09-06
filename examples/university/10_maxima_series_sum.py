# -*- coding: utf-8 -*-
"""
10_maxima_series_sum.py — Maxima 级数求和演示

演示 Maxima 在以下级数问题上的能力：
  - 无穷级数求和：∑1/n², ∑1/2ⁿ, ∑1/n!
  - 有限级数求和：∑n (n=1→10)
  - 经典级数结果验证：巴塞尔问题、等比级数、指数级数
"""
import subprocess


def _clean_maxima_result(raw: str) -> str:
    import re
    cleaned = re.sub(r'^(\S+)\s+[─▬─]+\s*(\S+)$', r'\1/\2', raw)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def run_maxima(code: str, label: str = ""):
    """运行一条 Maxima 命令并打印结果。"""
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"  cmd: {code.strip()}")
    print(f"{'─'*60}")
    try:
        code = "display2d: false;\n" + code
        proc = subprocess.Popen(
            ["maxima", "--very-quiet"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(code.strip() + "\n", timeout=15)
        lines = [
            l.strip()
            for l in stdout.splitlines()
            if l.strip() and l.strip() not in ("false", '"lisp"')
        ]
        raw_result = " ".join(lines).strip()
        display_result = _clean_maxima_result(raw_result)
        print(f"  结果: {display_result[:300]}")
        if stderr.strip():
            print(f"  警告: {stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        print("  [超时]")
    except Exception as e:
        print(f"  [错误: {e}]")


def main():
    print("=" * 60)
    print("  Maxima 级数求和演示")
    print("=" * 60)

    # 1. 巴塞尔问题
    print("\n=== 1. 巴塞尔问题 ===")
    run_maxima("sum(1/n^2, n, 1, inf);", "∑₁^∞ 1/n² = π²/6")

    # 2. 等比级数
    print("\n=== 2. 等比级数 ===")
    run_maxima("sum(1/2^n, n, 0, inf);", "∑₀^∞ 1/2ⁿ = 2")

    # 3. 指数级数
    print("\n=== 3. 指数级数 ===")
    run_maxima("sum(1/n!, n, 0, inf);", "∑₀^∞ 1/n! = e")

    # 4. 有限求和
    print("\n=== 4. 有限求和 ===")
    run_maxima("sum(n, n, 1, 10);", "∑₁¹⁰ n = 55")

    # 5. 更多无穷级数
    print("\n=== 5. 更多无穷级数 ===")
    run_maxima("sum(1/n^3, n, 1, inf);", "∑₁^∞ 1/n³ = ζ(3)（Apery 常数）")
    run_maxima("sum((-1)^(n+1)/n, n, 1, inf);", "∑₁^∞ (-1)^(n+1)/n = ln(2)")
    run_maxima("sum(1/(2*n+1)^2, n, 0, inf);", "∑₀^∞ 1/(2n+1)² = π²/8")

    # 6. 多项式级数
    print("\n=== 6. 多项式级数 ===")
    run_maxima("sum(n^2, n, 1, 10);", "∑₁¹⁰ n² = 385")
    run_maxima("sum(1/(n*(n+1)), n, 1, inf);", "∑₁^∞ 1/(n(n+1)) = 1")

    # 7. 特殊函数级数
    print("\n=== 7. 特殊函数级数 ===")
    run_maxima("sum(1/(n^4), n, 1, inf);", "∑₁^∞ 1/n⁴ = π⁴/90")
    run_maxima("sum(sin(n*%pi/4)/2^n, n, 0, inf);", "∑ sin(nπ/4)/2ⁿ")

    print(f"\n{'='*60}")
    print("  ✅ 级数求和演示完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
