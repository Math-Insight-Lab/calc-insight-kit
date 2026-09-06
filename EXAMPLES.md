# Examples Guide — 示例使用指南

本文档提供所有示例的快速索引和分步说明。运行方式：
```bash
python examples/quickstart.py          # 运行全部示例
python examples/quickstart.py kid      # 仅小学层
python examples/quickstart.py highschool   # 仅中学层
python examples/quickstart.py university  # 仅大学层
```

---

## 快速启动 Demo（一分钟入门）

5个可独立运行的演示脚本，展示教师薄包装 API 的极简用法：

| 文件名 | 知识点 | 说明 |
|--------|--------|------|
| `quickstart/01_limit_demo.py` | 极限直观 | `plot_limit_demo("sin(x)/x", x0=0)` 一行出图 |
| `quickstart/02_derivative_demo.py` | 导数与切线 | 切线斜率可视化 |
| `quickstart/03_riemann_demo.py` | 黎曼和 | 矩形逼近面积 |
| `quickstart/04_taylor_demo.py` | 泰勒展开 | 多项式逐步逼近 |
| `quickstart/05_eps_delta_demo.py` | ε-δ 极限 | 严格定义可视化 |

---

## 小学层 (kid) — 纯可视化、无公式

| 文件名 | 知识点 | 说明 |
|--------|--------|------|
| `kid/01_limit_demo.py` | 极限直观 | 动态动画感知极限 |
| `kid/02_derivative_demo.py` | 导数直观 | 切线斜率变化 |
| `kid/03_riemann_demo.py` | 黎曼和 | 矩形逼近面积 |
| `kid/04_taylor_demo.py` | 泰勒近似 | 多项式逐步逼近 |
| `kid/05_epsilon_delta_demo.py` | 连续性 | 邻域可视化 |
| `kid/06_removable_singularity_demo.py` | 可去间断 | 可去间断点可视化 |
| `kid/07_infinite_limit_demo.py` | 无穷极限 | 无穷间断与渐近线 |
| `kid/08_function_continuity_demo.py` | 函数连续 | 分段函数 |

---

## 中学层 (highschool) — 公式+数值+几何

| 文件名 | 知识点 | 说明 |
|--------|--------|------|
| `highschool/01_limit_demo.py` | 极限计算 | 代数求值+几何 |
| `highschool/02_derivative_demo.py` | 导数计算 | 求导法则+图像 |
| `highschool/03_riemann_demo.py` | 黎曼和数值 | n→∞收敛 |
| `highschool/04_taylor_demo.py` | 泰勒展开 | 多项式逼近阶数 |
| `highschool/05_epsilon_delta_demo.py` | ε-δ 极限 | 严格定义数值验证 |
| `highschool/06_removable_singularity_demo.py` | 可去间断 | 极限存在但函数无定义 |
| `highschool/07_infinite_limit_demo.py` | 无穷极限 | 无穷间断与渐近线 |

---

## 大学层 (university) — 严格定义+双CAS引擎

### 基础概念 (01-07)

| 文件名 | 知识点 | 说明 |
|--------|--------|------|
| `university/01_limit_demo.py` | 极限严格 | 双侧/单侧/无穷极限 |
| `university/02_derivative_demo.py` | 导数严格 | 定义+高阶+复合 |
| `university/03_riemann_demo.py` | 黎曼和严谨 | 收敛性证明 |
| `university/04_taylor_demo.py` | 泰勒严谨 | 高阶展开与余项 |
| `university/05_epsilon_delta_demo.py` | ε-δ 极限 | 严格定义验证 |
| `university/06_removable_singularity_demo.py` | 可去间断 | 极限存在但函数无定义 |
| `university/07_infinite_limit_demo.py` | 无穷极限 | 渐近线+无穷间断 |

### Maxima 演示 (08-09)

| 文件名 | 知识点 | 说明 |
|--------|--------|------|
| `university/08_maxima_demo.py` | Maxima 基础 | 求导/积分/求解/泰勒 |
| `university/09_cas_compare_demo.py` | SymPy vs Maxima | 结果对比 |

### Maxima 高级能力 (10_*)

| 文件名 | 知识点 | 说明 |
|--------|--------|------|
| `university/10_maxima_limits.py` | 极限 | sin(x)/x, 振荡, 左右极限 |
| `university/10_maxima_definite_integrals.py` | 定积分 | 反常积分, Dirichlet |
| `university/10_maxima_series_sum.py` | 级数求和 | ∑1/n², 等比级数 |
| `university/10_maxima_taylor_laurent.py` | 泰勒/洛朗展开 | 多项式+负幂次展开 |
| `university/10_maxima_simplification.py` | 代数化简 | radcan, ratsimp, trigsimp |
| `university/10_maxima_equations.py` | 方程求解 | 二次方程/方程组/三角方程 |
| `university/10_maxima_inequalities.py` | 不等式求解 | 多项式/有理/绝对值不等式 |
| `university/10_maxima_parametric_integrals.py` | 含参数积分 | Gamma函数, Laplace变换 |

### 探索性示例

| 文件名 | 知识点 | 说明 |
|--------|--------|------|
| `university/test_maxima_advantage.py` | Maxima 优势 | 复杂积分/隐函数/级数对比 |
| `university/explore_maxima_capabilities.py` | Maxima 全览 | 综合能力展示 |
| `university/test_definite_integral.py` | 定积分对比 | SymPy vs Maxima |
| `university/explore_p0_features.py` | P0 特性探索 | 各知识点 Maxima 能力 |
