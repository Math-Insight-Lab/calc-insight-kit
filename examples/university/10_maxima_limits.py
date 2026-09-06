# -*- coding: utf-8 -*-
"""
10_maxima_limits.py — Maxima 极限计算演示

演示 Maxima 在以下极限问题上的能力：
  - 基本极限：sin(x)/x 在 x→0
  - 左右极限：单边极限的精确计算
  - 振荡极限：sin(1/x) 在 x→0（不存在极限）
  - 可去间断点：(x²-4)/(x-2) 在 x→2
"""
import subprocess


def _clean_maxima_result(raw: str) -> str:
    """将 Maxima 2D 排版输出转为线性可读格式。

    Maxima --very-quiet 输出的分数如 '1 ─ 3'（上下对齐排版），
    这里将其简化为 '1/3'。
    """
    import re
    # 匹配 Maxima 2D 分数: 数字/符号 + 若干空格/制表 + '─'+若干空格 + 数字/符号
    # 例如: "1 ─ 3" → "1/3", "%pi ─── 2" → "%pi/2"
    cleaned = re.sub(r'^(\S+)\s+[─▬─]+\s*(\S+)$', r'\1/\2', raw)
    # 再清理多余空格
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def run_maxima(code: str, label: str = ""):
    """运行一条 Maxima 命令并打印结果。"""
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"  cmd: {code.strip()}")
    print(f"{'─'*60}")
    try:
        # display2d: false 确保线性输出，避免 2D 排版艺术
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
    print("  Maxima 极限计算演示")
    print("=" * 60)

    # 1. 基本极限
    print("\n=== 1. 基本极限 ===")
    run_maxima("limit(sin(x)/x, x, 0);", "sin(x)/x 当 x→0")

    # 2. 右极限
    print("\n=== 2. 右极限 ===")
    run_maxima("limit(sin(x)/x, x, 0, plus);", "sin(x)/x 当 x→0⁺")

    # 3. 左极限
    print("\n=== 3. 左极限 ===")
    run_maxima("limit(sin(x)/x, x, 0, minus);", "sin(x)/x 当 x→0⁻")

    # 4. 振荡极限
    print("\n=== 4. 振荡极限（不存在） ===")
    run_maxima("limit(sin(1/x), x, 0);", "sin(1/x) 当 x→0（振荡，无极限）")

    # 5. 可去间断点
    print("\n=== 5. 可去间断点极限 ===")
    run_maxima(
        "limit((x^2-4)/(x-2), x, 2);", "(x²-4)/(x-2) 当 x→2（约分后得 4）"
    )

    # 6. 无穷极限
    print("\n=== 6. 无穷极限 ===")
    run_maxima("limit(x^2, x, inf);", "x² 当 x→+∞")
    run_maxima("limit(1/x, x, 0, plus);", "1/x 当 x→0⁺（+∞）")
    run_maxima("limit(1/x, x, 0, minus);", "1/x 当 x→0⁻（-∞）")

    # 7. 指数极限
    print("\n=== 7. 指数相关极限 ===")
    run_maxima("limit((1+1/x)^x, x, inf);", "(1+1/x)^x 当 x→∞（= e）")
    run_maxima("limit(exp(x)/x^2, x, inf);", "e^x/x² 当 x→∞")

    # 8. 对数极限
    print("\n=== 8. 对数相关极限 ===")
    run_maxima("limit(log(x)/x, x, inf);", "ln(x)/x 当 x→∞（= 0）")
    run_maxima("limit(x*log(x), x, 0);", "x·ln(x) 当 x→0⁺（= 0）")

    print(f"\n{'='*60}")
    print("  ✅ 极限演示完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
