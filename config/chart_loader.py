# 加载图表模块封装文件
# 是模块加载器（Loader），负责根据版本导入不同模块，而不是提供UI渲染逻辑

# config/chart_loader.py

def load_chart_modules(version: str = "v1") -> dict:
    """
    🧭 加载图表函数模块（支持 v1 / v2 自动切换，v2 不存在时自动 fallback 到 v1）

    参数:
        version (str): 指定图表渲染版本，支持 "v1"（快速版）或 "v2"（高定制版）

    返回:
        dict: 图表函数字典，包含以下内容：
            - draw_line_chart: 折线图函数
            - draw_pie_chart: 饼图函数
            - draw_bar_chart: 柱状图函数
            - render_info_card: 卡片组件函数（支持 v1/markdown 和 v2/ECharts）
            - apply_chinese_font: 应用中文字体样式的函数
            - is_echarts: 布尔值，标记当前是否使用 ECharts 渲染（True=使用 v2）
    """

    modules = {}         # ✅ 初始化模块字典
    is_echarts = False   # ✅ 默认使用 v1（Plotly/Markdown）

    # ========== 🔄 若选择 v2，则优先导入 v2 封装（如失败自动降级） ==========
    if version == "v2":
        is_echarts = True

        # ✅ 尝试导入 v2 的折线图（ECharts）
        try:
            from utils_v2.line_charts_echarts import draw_line_chart
        except ImportError:
            from utils_v1.line_charts_plotly import draw_line_chart
            is_echarts = False  # ⛔ 降级为 v1

        # ✅ 尝试导入 v2 的饼图（ECharts）
        try:
            from utils_v2.pie_charts_echarts import draw_pie_chart
        except ImportError:
            from utils_v1.pie_charts_plotly import draw_pie_chart
            is_echarts = False

        # ✅ 尝试导入 v2 的柱状图（ECharts）
        try:
            from utils_v2.charts import draw_bar_chart
        except ImportError:
            from utils_v1.charts import draw_bar_chart
            is_echarts = False

        # ✅ 尝试导入 v2 的字体样式模块
        try:
            from utils_v2.theme import apply_chinese_font
        except ImportError:
            from utils_v1.theme import apply_chinese_font
            is_echarts = False

        # ✅ 尝试导入 v2 的卡片组件（使用 ECharts 风格或 Div 渲染）
        try:
            from utils_v2.card_charts_echarts import render_info_card as render_info_card
        except ImportError:
            from utils_v1.card_charts_markdown import render_info_card as render_info_card
            is_echarts = False

    # ========== 📦 否则使用 v1 快速版封装（默认使用 Plotly / Markdown） ==========
    else:
        from utils_v1.line_charts_plotly import draw_line_chart
        from utils_v1.pie_charts_plotly import draw_pie_chart
        from utils_v1.charts import draw_bar_chart
        from utils_v1.theme import apply_chinese_font
        from utils_v1.card_charts_markdown import render_info_card
        is_echarts = False

    # ========== ✅ 封装所有模块函数，返回统一入口 ==========
    modules["draw_line_chart"] = draw_line_chart             # 折线图函数
    modules["draw_pie_chart"] = draw_pie_chart               # 饼图函数
    modules["draw_bar_chart"] = draw_bar_chart               # 柱状图函数
    modules["render_info_card"] = render_info_card           # 卡片组件函数
    modules["apply_chinese_font"] = apply_chinese_font       # 字体应用函数
    modules["is_echarts"] = is_echarts                       # 当前是否使用 ECharts

    return modules






'''
# config/chart_loader.py

def load_chart_modules(version: str = "v1") -> dict:
    """
    🧭 加载图表函数模块（支持 v1 / v2 自动切换，v2 不存在时自动 fallback 到 v1）

    参数:
        version (str): 版本号，支持 "v1" 或 "v2"

    返回:
        dict: 图表函数字典，包含：
              - draw_line_chart
              - draw_pie_chart
              - draw_bar_chart
              - apply_chinese_font
              - is_echarts（是否使用 ECharts 渲染）
    """

    # ✅ 定义返回的模块字典
    modules = {}

    # ✅ 初始化 ECharts 使用标志
    is_echarts = False

    # ========== 🔄 若选择 v2，则优先导入 v2 封装 ==========
    if version == "v2":
        is_echarts = True  # ✅ 标记：默认 v2 使用 ECharts

        try:
            from utils_v2.line_charts_echarts import draw_line_chart
        except ImportError:
            from utils_v1.line_charts_plotly import draw_line_chart
            is_echarts = False  # ⛔ 回落说明不再使用 ECharts

        try:
            from utils_v2.pie_charts_echarts import draw_pie_chart
        except ImportError:
            from utils_v1.pie_charts_plotly import draw_pie_chart
            is_echarts = False

        try:
            from utils_v2.charts import draw_bar_chart
        except ImportError:
            from utils_v1.charts import draw_bar_chart
            is_echarts = False

        try:
            from utils_v2.theme import apply_chinese_font
        except ImportError:
            from utils_v1.theme import apply_chinese_font
            is_echarts = False

    # ========== 📦 否则使用 v1 快速版封装 ==========
    else:
        from utils_v1.line_charts_plotly import draw_line_chart
        from utils_v1.pie_charts_plotly import draw_pie_chart
        from utils_v1.charts import draw_bar_chart
        from utils_v1.theme import apply_chinese_font
        is_echarts = False

    # ✅ 将所有函数封装进模块字典中
    modules["draw_line_chart"] = draw_line_chart           # 折线图
    modules["draw_pie_chart"] = draw_pie_chart             # 饼图
    modules["draw_bar_chart"] = draw_bar_chart             # 柱状图
    modules["apply_chinese_font"] = apply_chinese_font     # 字体样式
    modules["is_echarts"] = is_echarts                     # ✅ 返回真实判断结果

    return modules
    
'''