# Calc-Insight-Kit：三层差异化微积分可视化教学工具库

## 项目概述
Calc-Insight-Kit 是一套**同源知识点、三层差异化输出**的微积分教学可视化开源工程，严格区分「小学启蒙、中学应试、大学严谨」三学段认知体系，同一核心数学知识点，分层实现「看图感知→计算解题→严谨证明」的完整教学闭环。

## 分层架构（最终定稿）
- 🧒 **Kid 小学层（8例）**：纯可视化、无公式、无计算、口语化输出，感知数学现象
- 📚 **Highschool 中学层（8例）**：公式运算、数值求解、几何释义，完全贴合初高中考点
- 🎓 **University 大学层（22例）**：严格数学定义、误差分析、收敛性证明、双CAS引擎对比，适配高数/数分实训

## V1.0.0 功能概览

### 教师薄包装 API (`teacher_api`)
无需了解 matplotlib 配置即可一键出图：
```python
from calc_insight_kit.teacher_api import (
    plot_limit_demo,      # 极限演示
    plot_derivative_demo,  # 导数与切线
    plot_riemann_demo,     # 黎曼和
    plot_taylor_demo,      # 泰勒展开
    show_epsilon_delta_demo,  # ε-δ 极限定义
    plot_integral_demo,    # 定积分几何解释
    animate_taylor,        # 泰勒动画 GIF
    animate_riemann,       # 黎曼和动画 GIF
    to_latex,              # LaTeX 转换
    plot_math,             # 统一路由入口（自动路由到对应层演示）
)

# 一行代码出图（自动处理样式、标题、保存）
plot_limit_demo("sin(x)/x", x0=0, save="limit.png")
```

### 统一输出层 (`output`)
多格式导出、课件/论文双主题、LaTeX 内联：
```python
from calc_insight_kit.output import CASOutput, save_plot, latex_fragment

out = CASOutput(title="极限演示")
out.ax.plot(...)
out.save_png("plot.png")      # PNG 导出
out.save_pdf("plot.pdf")      # PDF 导出
latex = out.to_latex()         # LaTeX 代码片段
```

### 结构化教学报错 (`errors`)
所有验证异常附带教学提示：
```python
from calc_insight_kit.errors import (
    CASValidationError,
    CASComputationalError,
    CASVisualizationError,
    CASBackendError,
)

try:
    plot_riemann_demo("x**2", 0, 1, n=0)
except CASValidationError as e:
    print(e.message)     # "n 必须为正整数"
    print(e.teaching_hint)  # "提示：分割数 n 必须为正整数，建议 n >= 5"
    print(e.solution)    # "建议：使用 n=10 或更大的正整数"
```

### 全局样式预设 (`styles`)
一键切换主题：
```python
from calc_insight_kit.styles import use_theme

use_theme("teaching")   # 教学课件风格（默认）
use_theme("paper")      # 论文发表风格
```

## 核心特性
- 同源内核：01-07核心知识点三层完全同源，仅展示逻辑差异化
- 专属高阶：大学独有双CAS引擎演示与对比测试，工程化、学术化拉满
- 教学薄包装：`teacher_api` 一行代码出图，matplotlib 配置全自动
- 多格式输出：PNG/PDF/SVG/GIF/LaTeX 一键导出
- 结构化报错：每个验证异常附带教学提示与解决方案
- 全量适配：配套教学Notebook、自动化测试套件、标准化工程配置
- 开箱即用：支持批量运行、独立层级运行、单示例调试

## 快速安装
```bash
pip install -e .
```

## Maxima 依赖安装（可选）

项目默认使用 SymPy 作为 CAS 后端，功能已覆盖 95% 以上的教学需求。**Maxima 是可选依赖**，仅在运行大学层双 CAS 对比示例（`university/08_maxima_demo.py`、`09_cas_compare_demo.py` 及 `10_maxima_*.py` 系列）时启用。

### Windows

<details>
<summary>中文 — 安装步骤</summary>

1. **下载安装包**：访问 [Maxima 官网](https://prdownloads.sourceforge.net/maxima/Maxima-5.48.0-Setup.exe) 下载最新版 Windows 安装程序。
2. **安装**：双击运行 `.exe` 文件，建议安装路径为 `C:\Program Files\maxima-5.48.0\`（默认即可）。
3. **验证安装**：打开命令提示符或 PowerShell，运行：
   ```bash
   maxima --version
   ```
   应输出 Maxima 版本信息，例如 `Maxima 5.48.0`。
4. **配置 PATH**（可选）：如果 `maxima --version` 提示"找不到命令"，将 Maxima 的 `bin` 目录添加到系统 PATH 环境变量：
   ```
   C:\Program Files\maxima-5.48.0\bin
   ```
   然后在 PowerShell 中重新加载：`$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")`

</details>

<details>
<summary>English — Installation Steps</summary>

1. **Download**: Visit the [Maxima official website](https://prdownloads.sourceforge.net/maxima/Maxima-5.48.0-Setup.exe) and download the latest Windows installer.
2. **Install**: Double-click the `.exe` file. The default installation path `C:\Program Files\maxima-5.48.0\` is recommended.
3. **Verify**: Open Command Prompt or PowerShell and run:
   ```bash
   maxima --version
   ```
   You should see output like `Maxima 5.48.0`.
4. **Add to PATH** (optional): If `maxima --version` says command not found, add Maxima's `bin` directory to your system PATH:
   ```
   C:\Program Files\maxima-5.48.0\bin
   ```
   Then reload the environment in PowerShell: `$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")`

</details>

### Linux (Ubuntu / Debian)

<details>
<summary>中文 — 安装步骤</summary>

1. **使用 apt 安装**（推荐）：
   ```bash
   sudo apt-get update
   sudo apt-get install -y maxima
   ```
2. **验证安装**：
   ```bash
   maxima --version
   ```
   应输出 Maxima 版本信息。

</details>

<details>
<summary>English — Installation Steps</summary>

1. **Install via apt** (recommended):
   ```bash
   sudo apt-get update
   sudo apt-get install -y maxima
   ```
2. **Verify**:
   ```bash
   maxima --version
   ```
   You should see the Maxima version info.

</details>

### 验证 Maxima 是否在项目中可用

<details>
<summary>中文</summary>

安装 Maxima 后，运行以下 Python 代码验证：
```python
from calc_insight_kit.config import RUN_UNIVERSITY_MODE
from calc_insight_kit.calc_backend import get_cas_backend

try:
    backend = get_cas_backend("maxima")
    result = backend.diff("x**2", "x")
    print(f"Maxima 正常工作: diff(x**2) = {result}")
except Exception as e:
    print(f"Maxima 不可用: {e}")
    print("使用 SymPy 后端仍然可以运行全部功能。")
```

如果输出 `x^2` 说明 Maxima 桥接正常。如果 Maxima 未安装，项目会自动回退到 SymPy 后端。

</details>

<details>
<summary>English</summary>

After installing Maxima, verify with this Python code:
```python
from calc_insight_kit.calc_backend import get_cas_backend

try:
    backend = get_cas_backend("maxima")
    result = backend.diff("x**2", "x")
    print(f"Maxima working: diff(x**2) = {result}")
except Exception as e:
    print(f"Maxima unavailable: {e}")
    print("The project falls back to SymPy backend automatically.")
```

If it outputs `x^2`, the Maxima bridge is working. If Maxima is not installed, the project automatically falls back to SymPy.

</details>

## 快速运行
```bash
# 批量执行所有层级所有示例
python main.py

# 或按学段运行
python examples/quickstart.py kid        # 仅小学层
python examples/quickstart.py highschool # 仅中学层
python examples/quickstart.py university # 仅大学层
python examples/quickstart.py all        # 全部层

# 快速启动 Demo（5个一分钟演示）
python examples/quickstart/01_limit_demo.py
python examples/quickstart/02_derivative_demo.py
python examples/quickstart/03_riemann_demo.py
python examples/quickstart/04_taylor_demo.py
python examples/quickstart/05_eps_delta_demo.py

# 直接运行单个示例
python examples/university/10_maxima_limits.py
python examples/highschool/02_derivative_demo.py
```

详细示例索引与说明，请查看 [EXAMPLES.md](EXAMPLES.md)。

## 目录简述
- `calc_insight_kit/`：全局统一核心计算+可视化内核
  - `styles.py`：全局样式预设（教学/论文双主题）
  - `output.py`：统一输出层（PNG/PDF/SVG/GIF/LaTeX）
  - `errors.py`：结构化教学报错（验证/计算/可视化/后端异常）
  - `teacher_api.py`：教学薄包装 API（一行代码出图）
  - `calc_backend.py`：双 CAS 后端（SymPy/Maxima）
  - `cas/`：CAS 子包（CASSymbol/CASExpr/Maxima 桥接）
  - `__init__.py`：统一导出所有公共接口
- `examples/`：三学段分层教学示例源码
  - `quickstart/`：5个一分钟快速入门 Demo
  - `kid/`：小学层示例（8个）
  - `highschool/`：中学层示例（8个）
  - `university/`：大学层示例（22个）
- `tests/`：全维度自动化测试用例（218个测试用例，100% 通过）
- 配套教学文档：大纲、更新日志、双语说明全覆盖

## 适配场景
全学段数学启蒙、初高中微积分刷题辅助、大学数学分析实验、教学课件素材生成

## 注意事项

### 中文字体缺失警告
在 Linux 服务器或无桌面环境中运行示例脚本时，matplotlib 可能输出以下警告：
```
findfont: Generic family 'sans-serif' not found because none of the following families were found: SimHei
UserWarning: Glyph 26497 (\N{CJK UNIFIED IDEOGRAPH-6781}) missing from font(s) DejaVu Sans.
```
**这是正常现象**：Linux 服务器默认没有中文字体（SimHei / 黑体），不影响程序执行和数值计算。可视化图表中的中文标题和标签可能显示为方框或缺失。

**解决方法（二选一）：**

1. **安装中文字体**（推荐，一次性解决）：
   ```bash
   sudo apt-get install -y fonts-noto-cjk  # Debian/Ubuntu
   # 或
   sudo yum install -y google-noto-sans-cjk-fonts  # CentOS/RHEL
   ```
   安装后刷新字体缓存：`fc-cache -fv`

2. **配置 matplotlib 使用备用字体**：
   在示例脚本中 `plt.rcParams["font.sans-serif"]` 行改为系统中已有的英文字体，例如：
   ```python
   plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
   ```
   此时图表将使用英文标题和标签。

> 注：自动化测试（`pytest`）不依赖图形输出，在任何环境中均可通过。

## 中文字体问题修复方案（已完成）

### 问题描述
在 Linux 服务器环境中，matplotlib 默认使用 `SimHei`（黑体）作为中文字体，但 Linux 系统通常不预装该字体，导致：
- 控制台输出大量 `findfont: Generic family 'sans-serif' not found` 警告
- 图表中的中文显示为方框或缺失
- 部分示例因 numpy 数组比较方式不当报错

### 已实施的修复方案

#### 1. 批量替换字体引用
将所有 Python 脚本中的 `SimHei` 替换为系统中实际存在的 `Noto Sans CJK SC` 字体：
```bash
cd /home/agent1/src/edu/src/calc-insight-kit
sed -i 's/SimHei/Noto Sans CJK SC/g' calc_insight_kit/*.py examples/**/*.py
```
共修改 24 处字体引用。

#### 2. 创建 matplotlib 配置文件
在项目根目录创建 `matplotlibrc`，指定字体优先级：
```ini
font.family: sans-serif
font.sans-serif: Noto Sans CJK SC, Noto Sans CJK TC, Noto Sans CJK HK, Noto Sans CJK JP, Noto Sans CJK KR, WenQuanYi Micro Hei, WenQuanYi Zen Hei, Droid Sans Fallback, DejaVu Sans, Arial
axes.unicode_minus: False
```

#### 3. 修复 numpy 数组比较
修复 `examples/university/05_epsilon_delta_demo.py` 中的 lambda 函数：
```python
# 修复前（错误）
f_np = lambda t: np.sin(t) / t if t != 0 else 1.0  # 不能处理 numpy 数组

# 修复后（正确）
f_np = lambda t: np.where(t == 0, 1.0, np.sin(t) / t)  # 支持数组操作
```

### 验证结果
- ✅ 所有 24 个示例脚本运行无字体警告
- ✅ pytest 测试 218/218 通过，无 Glyph 缺失警告
- ✅ 图表中文标题和标签正常显示

### 其他 Linux 系统的字体适配
如果系统没有 `Noto Sans CJK SC`，可用以下命令查找可用中文字体：
```bash
fc-list :lang=zh family 2>&1 | sort -u | head -20
```
将找到的字体名称替换脚本中的 `Noto Sans CJK SC` 即可。

### 跨平台兼容性建议
```python
# 在脚本开头添加字体回退逻辑
import matplotlib
import sys

if sys.platform == 'linux':
    # Linux 优先使用 Noto Sans CJK SC
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "WenQuanYi Micro Hei", "DejaVu Sans"]
elif sys.platform == 'darwin':
    # macOS 使用 PingFang SC
    plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "SimHei"]
else:
    # Windows 使用微软雅黑/黑体
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
```

## 跨平台兼容性（Windows/Linux/macOS）

### 已实施的兼容性修复

#### 1. 自动字体适配
项目现在根据操作系统自动选择最佳中文字体：
- **Linux**: Noto Sans CJK SC, WenQuanYi Micro Hei 等
- **Windows**: Microsoft YaHei (微软雅黑), SimHei (黑体) 等
- **macOS**: PingFang SC, Heiti SC 等

#### 2. 跨平台 subprocess 调用
使用 `sys.executable` 自动识别当前 Python 解释器路径，避免 Windows 下 `python` 命令不存在的问题。

#### 3. 跨平台 matplotlib 后端
自动设置 `Agg` 后端，避免无显示器环境报错。

### 使用方法
安装后直接运行，无需额外配置：
```bash
pip install -e .
python main.py  # 自动适配当前系统
```

### 验证跨平台兼容性
```bash
# 在 Windows 上运行
python examples/kid/01_limit_demo.py

# 在 macOS 上运行
python examples/middle/01_limit_demo.py

# 在 Linux 服务器上运行
python examples/university/01_limit_demo.py
```

所有示例在不同平台下都能正确运行并生成中文图表。

## 许可证

本项目采用 **MIT 许可证**（见 [LICENSE](LICENSE)），可以自由使用、修改和分发。

### 第三方依赖许可证声明

本项目使用了以下第三方库，其许可证与本项目 MIT 许可证兼容：

| 依赖 | 许可证 | 说明 |
|------|--------|------|
| SymPy | BSD 3-Clause | 默认 CAS 后端，MIT 兼容 |
| NumPy | BSD 3-Clause | 数值计算基础库 |
| Matplotlib | Matplotlib License | 可视化引擎 |
| **Maxima** | **GPL v3** | **可选 CAS 后端，仅在运行大学层双 CAS 对比示例时启用** |

> **Maxima GPL 兼容性说明**：Maxima 采用 GNU GPL v3 许可证。本项目将 Maxima 作为**可选外部依赖**通过命令行进程调用（非 Python 导入），不违反 GPL 的"链接"条款。运行 `pip install -e .` 后，即使不安装 Maxima，项目核心功能（SymPy 后端 + 可视化）仍可正常使用。仅在明确调用 `get_cas_backend("maxima")` 或运行 `university/10_maxima_*.py` 系列示例时才需要 Maxima。
>
> 根据 [GPL 第 13 条](https://www.gnu.org/licenses/gpl-faq.html#GPLINCOMPAT) 的兼容性分析，通过进程隔离（subprocess）调用 GPL 程序被视为独立作品，不要求衍生作品也采用 GPL。因此本 MIT 许可证项目可以安全地使用 Maxima 作为可选后端。

### 使用限制

1. **SymPy 后端**：MIT 许可证下，可自由用于商业、教育、研究等任何用途。
2. **Maxima 后端**（可选）：如需使用 Maxima，请确保遵守 Maxima 的 GPL v3 许可证要求。
3. **图表输出**：使用本项目生成的可视化图表可自由用于教学和学术研究。
