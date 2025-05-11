# 字体设置

# utils/theme.py

DEFAULT_FONT = "Microsoft YaHei"

def apply_chinese_font(fig, font_family=DEFAULT_FONT):
    fig.update_layout(
        font=dict(
            family=font_family,
            size=14
        )
    )
    return fig

def apply_plot_style(fig):
    """
    应用统一的图表视觉风格：去除背景网格，优化边框、字体大小等。

    参数：
        fig（Plotly 图对象）：图表对象

    返回：
        fig：增强样式后的图表对象
    """

    fig.update_layout(
        plot_bgcolor="white",      # 图表区域背景白色
        paper_bgcolor="white",     # 图表外围背景白色
        margin=dict(l=40, r=40, t=40, b=40),  # 设置内边距，防止拥挤
        font=dict(size=14),        # 设置全局字体大小
    )

    # 去除多余网格线
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")  # Y轴保留浅灰网格

    return fig