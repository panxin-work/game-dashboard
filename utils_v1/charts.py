# 图表封装

# utils/charts.py

import plotly.express as px
from utils_v1.theme import apply_chinese_font


'''
# 折线图：用于展示每日支付单量趋势
def draw_line_chart(df):
    # 构建基本折线图：x轴为日期（dt），y轴为支付单量，带数据点
    fig = px.line(df, x="dt", y="支付单量", markers=True)

    # 获取支付单量最大值，用于设置 y 轴范围和刻度
    max_val = df["支付单量"].max()

    # 如果最大值不大，手动将刻度设置为整数间隔 1（dtick=1）以避免重复标签
    if max_val <= 10:
        fig.update_yaxes(
            title_text="支付单量",       # Y轴标题
            tickformat="d",             # Y轴刻度格式为整数（如 1, 2, 3）
            dtick=1,                    # 每个刻度之间间隔 1
            range=[0, max_val * 1.2],   # 设置Y轴范围（最大值上浮 20%）
            showline=True               # 显示 Y轴线条
        )
    else:
        # 数据量大时，不固定刻度间隔，避免卡顿或标签重叠
        fig.update_yaxes(
            title_text="支付单量",
            tickformat="d",
            nticks=5,                   # 自动计算最多显示 5 个刻度
            range=[0, max_val * 1.2],
            showline=True
        )

    # 设置 X 轴（日期轴）优化显示方式
    fig.update_xaxes(
        title_text="日期",             # X轴标题
        tickformat="%m/%d",            # 日期格式为 月/日（例如 04/28）
        tickangle=-30,                 # 刻度文字倾斜角度，更易阅读
        showline=True                  # 显示 X轴线条
    )

    # 强制使用中文字体（你项目中封装了 apply_chinese_font）
    fig = apply_chinese_font(fig)

    return fig
### 以下为方法2

    # 创建基础折线图，横轴为“dt”列（日期），纵轴为“支付单量”列
    fig = px.line(df, x="dt", y="支付单量", markers=True)

    # 设置 Y 轴（支付单量）
    fig.update_yaxes(
        title_text="支付单量",   # Y轴标题文字
        tickformat="d",         # Y轴刻度强制显示为整数（"d" 表示 decimal）
        range=[0, df["支付单量"].max() * 1.2],  # 强制从 0 开始，预留 20% 空间
        title_standoff=10       # Y轴标题距离坐标轴的距离（单位：像素）
    )

    # 设置 X 轴（日期）
    fig.update_xaxes(
        title_text="日期",       # X轴标题文字
        tickformat="%m/%d",      # 日期显示格式为 “月/日”，如 04/28
        tickangle=-35,              # 倾斜显示，防止重叠
        tickmode="auto",            # 自动间隔刻度
        nticks=min(len(df), 7),     # 最多显示7个日期，避免过密
        title_standoff=10        # X轴标题距离坐标轴的距离
    )

    # 优化图表整体外观
    fig.update_layout(
        hovermode="x unified",   # 鼠标悬浮提示：一条垂直线联动显示所有信息
        margin=dict(l=20, r=20, t=40, b=40),  # 设置四周留白，避免拥挤
        height=400               # 图表高度
    )

    # 强制应用中文字体，避免乱码（由自定义函数实现）
    return apply_chinese_font(fig)
'''
'''
# 饼图：用于展示各游戏支付占比
def draw_pie_chart(df, title=""):
    fig = px.pie(
        df,
        names="游戏名称",       # 饼图每一块的名称字段
        values="支付单量",       # 对应值大小字段
        hole=0.3                 # 设置内圈空白，使其成为“环形图”
    )

    # 图表样式优化
    fig.update_traces(
        textinfo="percent+label",   # 显示百分比+名称
        pull=[0.02]*len(df),        # 稍微拉开每块，避免贴合
        sort=False                  # 保持原始顺序
    )

    fig.update_layout(
        title=title,
        showlegend=True,            # 显示图例
        legend_title_text="游戏名称",
        height=400
    )

    return apply_chinese_font(fig)
'''

# 柱状图：展示各游戏的库存占比（渠道 / 平台）
def draw_bar_chart(df):
    fig = px.bar(
        df,
        x="游戏名称",            # 横轴是游戏名称
        y="库存占比",            # 纵轴是库存占比数值
        text="库存占比",         # 在柱子上显示具体数字
        color="游戏名称"          # 每个柱子颜色不同（按游戏分）
    )

    # 设置文字显示在柱子外部
    fig.update_traces(textposition="outside")

    # X轴标签防止太挤，自动旋转
    fig.update_xaxes(tickangle=-45)

    # Y轴设置 0 到 1.0（百分比），并限制小数点位数
    fig.update_yaxes(range=[0, 1.05])

    fig.update_layout(
        showlegend=False,           # 不显示图例，已由X轴表示
        height=400,
        margin=dict(l=20, r=20, t=40, b=40)
    )

    return apply_chinese_font(fig)