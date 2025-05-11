# utils_v1/pie_charts_plotly.py

import plotly.express as px
import pandas as pd
from utils_v1.theme import apply_chinese_font, apply_plot_style


def draw_pie_chart(df, value_col="支付单量", name_col="游戏名称", title=None, max_slices=10, key=None):
    """
    🥧 绘制饼图，用于展示各游戏支付单量占比（支持“其他”合并）

    功能亮点：
    ✅ 自动合并“长尾数据”为“其他”，确保图表清晰
    ✅ 图例完整展示，易于识别
    ✅ 悬浮提示展示占比 + 数量
    ✅ 图表风格统一，支持中文字体

    参数说明：
        df（DataFrame）：数据源，要求至少包含以下两列：
            - 游戏名称列（默认为 '游戏名称'）
            - 数值列（默认为 '支付单量'）
        value_col（str）：用于绘图的数值列名，默认为 '支付单量'
        name_col（str）：用于分组的分类列名，默认为 '游戏名称'
        title（str）：图表标题，可选
        max_slices（int）：最多展示的扇形数量，超过部分合并为“其他”（默认10）

    返回：
        fig（plotly.graph_objs._figure.Figure）：封装好的饼图对象
    """

    # ✅ [步骤1] 数据清洗与排序：移除 0 值项，并按支付量降序排列
    df = df[df[value_col] > 0].sort_values(by=value_col, ascending=False)

    # ✅ [步骤2] 控制展示项数量（最多 max_slices 个）
    if len(df) > max_slices:
        top_df = df.iloc[:max_slices - 1]  # 前 N-1 项
        other_sum = df.iloc[max_slices - 1:][value_col].sum()
        other_row = pd.DataFrame({name_col: ["其他"], value_col: [other_sum]})
        df = pd.concat([top_df, other_row], ignore_index=True)

    # ✅ [步骤3] 绘制基础饼图（环形样式）
    fig = px.pie(
        df,
        values=value_col,
        names=name_col,
        title=title,
        hole=0.3     # 设置为 0 表示普通饼图，>0 为环形图
    )

    # ✅ [步骤4] 优化图例与标签
    fig.update_traces(
        textposition="inside",                  # 标签显示在扇形内
        textinfo="percent+label",               # 显示百分比 + 名称
        hovertemplate="%{label}: %{value} 单<br>占比 %{percent}<extra></extra>"
    )

    # ✅ [步骤5] 应用图表整体布局与中文字体样式
    fig.update_layout(
        showlegend=True,
        legend_title_text="游戏",                # 图例标题
        legend=dict(orientation="h", y=-0.2),    # 横向图例，置于下方
        margin=dict(t=40, b=80)
    )

    fig = apply_chinese_font(fig)               # 支持中文显示
    fig = apply_plot_style(fig)                 # 应用统一配色风格

    return fig