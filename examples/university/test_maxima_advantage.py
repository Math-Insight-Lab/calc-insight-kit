# -*- coding: utf-8 -*-
"""
Maxima vs SymPy 优势对比测试
专注于 Maxima 在符号积分上的核心优势
"""
import sympy as sp
from calc_insight_kit.maxima_bridge import get_cas_backend
import time

def test_integral(expr_str, title, var="x"):
    """测试一个积分，对比 SymPy 和 Maxima"""
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print(f"  被积函数: {expr_str}")
    print(f"{'─'*60}")
    
    x = sp.Symbol(var)
    expr = sp.sympify(expr_str)
    
    # --- SymPy ---
    print("\n【SymPy 结果】")
    t0 = time.time()
    try:
        sp_result = sp.integrate(expr, x)
        sp_time = time.time() - t0
        sp_str = str(sp_result)
        print(f"  耗时: {sp_time:.3f}s")
        print(f"  结果长度: {len(sp_str)} 字符")
        
        if "RootSum" in sp_str or "rootof" in sp_str:
            print("  ❌ 返回了 RootSum (无法直接阅读)")
        elif "Integral(" in sp_str:
            print("  ❌ 返回了未计算的 Integral (超时截断)")
        elif len(sp_str) < 50:
            print("  ⚠️  结果异常短，可能不完整")
        else:
            print("  ✅ 返回了完整表达式")
        
        # 简单显示前120字符
        display = sp_str[:150]
        if len(sp_str) > 150:
            display += "..."
        print(f"  内容预览: {display}")
        
        # 检查数值验证：对结果求导看是否等于原函数
        deriv = sp.diff(sp_result, x)
        diff_check = sp.simplify(deriv - expr)
        if diff_check == 0:
            print("  ✅ 数值验证通过: d/dx(积分结果) == 被积函数")
        else:
            print(f"  ⚠️  验证未通过: d/dx - f = {str(diff_check)[:80]}")
    except Exception as e:
        sp_time = time.time() - t0
        print(f"  ❌ 错误/超时 ({sp_time:.3f}s): {e}")
        sp_result = None
    
    # --- Maxima 文本 ---
    print("\n【Maxima 结果】")
    try:
        max_be = get_cas_backend(prefer_maxima=True)
        t1 = time.time()
        max_result = max_be.integrate(expr_str, var)
        max_time = time.time() - t1
        max_str = max_result.strip()
        print(f"  耗时: {max_time:.3f}s")
        print(f"  结果长度: {len(max_str)} 字符")
        
        # 检查是否包含关键函数
        has_log = "log" in max_str.lower()
        has_atan = "atan" in max_str.lower()
        has_explicit = has_log or has_atan
        
        if has_explicit:
            print("  ✅ 返回了显式的 log/atan 闭式解")
        if len(max_str) < 20:
            print("  ⚠️  结果过短")
        
        # 显示结果（截断）
        display = max_str[:150]
        if len(max_str) > 150:
            display += "..."
        print(f"  内容预览: {display}")
        
        # LaTeX
        max_latex = max_be.integrate_tex(expr_str, var)
        latex_clean = max_latex.replace("\\\\", "\\").strip()
        if latex_clean and "Error" not in latex_clean:
            print(f"  LaTeX: {latex_clean[:150]}")
        
    except Exception as e:
        print(f"  ❌ Maxima 错误: {e}")
    
    # --- 对比总结 ---
    if sp_result is not None:
        print("\n  【对比总结】")
        sp_len = len(str(sp_result)) if "sp_result" in dir() else 0
        if sp_len > 100 and has_explicit:
            print("  两个引擎都给出了完整结果")
        elif sp_len < 50 and has_explicit:
            print("  🔑 Maxima 优势: 给出完整显式解，SymPy 截断")
        elif "RootSum" in str(sp_result) and has_explicit:
            print("  🔑 Maxima 优势: 给出显式解，SymPy 返回 RootSum (不可读)")

def main():
    print("=" * 60)
    print("  Maxima vs SymPy — 符号积分能力对比")
    print("=" * 60)
    
    # Case 1: 经典痛点 —— SymPy 返回不完整结果
    test_integral(
        "1/(1+x^10)",
        "Case 1: 1/(1+x^10) —— SymPy 经典痛点"
    )
    
    # Case 2: 中等复杂度
    test_integral(
        "1/(x^4+1)",
        "Case 2: 1/(x^4+1) —— 四次有理函数"
    )
    
    # Case 3: 高次有理函数
    test_integral(
        "1/(x^5+1)",
        "Case 3: 1/(x^5+1) —— 五次有理函数"
    )
    
    # Case 4: 带参数的积分
    test_integral(
        "1/(x^6+1)",
        "Case 4: 1/(x^6+1) —— 六次有理函数"
    )
    
    # Case 5: 三角有理函数
    test_integral(
        "1/(1+sin(x)^2)",
        "Case 5: 1/(1+sin^2(x)) —— 三角有理函数"
    )
    
    print(f"\n{'='*60}")
    print("  ✅ 对比完成")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
