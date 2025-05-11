# utils_v2/line_charts_advanced.py

import plotly.express as px
import pandas as pd
from utils_v2.theme import apply_chinese_font, apply_plot_style


def draw_line_chart(df, max_ticks=10):
    """
    📊 [v2] 高阶折线图封装（预留未来增强逻辑）

    功能目标（计划）：
    ✅ 支持多游戏对比折线图（颜色区分）
    ✅ 可配置单位、图例位置、自定义 Tooltip
    ✅ 支持双轴（如订单量 vs 转化率）
    ✅ 响应更复杂的数据结构（按 game_id 分组等）

    当前状态：
    🚧 功能占位中，保留接口，仅实现基础结构。
    """

    # === 🚧 占位实现（当前保持最小结构，后续逐步扩展）===
    df["日期"] = df["dt"].dt.strftime("%m/%d")

    fig = px.line(
        df,
        x="日期",
        y="支付单量",
        markers=True
    )

    fig.update_yaxes(
        title_text="支付单量",
        tickformat="d",
        nticks=5,
        rangemode="tozero",
        showline=True
    )

    fig.update_xaxes(
        title_text=None,
        tickangle=-30,
        type="category",
        tickmode="linear",
        nticks=max_ticks
    )

    fig.update_traces(
        hovertemplate="日期: %{x}<br>支付单量: %{y} 单<extra></extra>"
    )

    fig.update_layout(hovermode="x unified")
    fig = apply_chinese_font(fig)
    fig = apply_plot_style(fig)

    return fig