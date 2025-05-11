# 饼图封装程序-echarts版（维护中）

'''
from streamlit_echarts import st_echarts
import pandas as pd
import json

def draw_pie_chart(df: pd.DataFrame, max_slices: int = 10):
    """
    使用 ECharts 渲染饼图，支持前N项+“其他”聚合 + 悬停明细提示 + 完整图例滚动
    """

    # === ✅ Step 1: 数据过滤与排序（仅保留支付单量 > 0）
    df = df[df["支付单量"] > 0]
    df = df.sort_values("支付单量", ascending=False)

    # === ✅ Step 2: 判断是否需要“其他”项
    need_other = len(df) > max_slices
    if need_other:
        top_items = df.head(max_slices - 1)
        other_items = df.iloc[max_slices - 1:]
    else:
        top_items = df
        other_items = pd.DataFrame()

    # === ✅ Step 3: 构建饼图数据 pie_data
    pie_data = []
    for _, row in top_items.iterrows():
        pie_data.append({
            "name": row["游戏名称"],
            "value": int(row["支付单量"])
        })

    # === ✅ Step 4: 构造“其他”项 tooltip（合并明细）
    other_tooltip_map = {}
    if not other_items.empty:
        other_total = int(other_items["支付单量"].sum())
        tooltip_lines = [
            f"{row['游戏名称']}: {int(row['支付单量'])} 单"
            for _, row in other_items.iterrows()
        ]
        tooltip_html = "<br/>" + "<br/>".join(tooltip_lines)
        other_tooltip_map["其他"] = tooltip_html

        pie_data.append({
            "name": "其他",
            "value": other_total
        })

    # === ✅ Step 5: 图例（仅包含实际游戏名称，不含“其他”）
    legend_data = df["游戏名称"].tolist()  # 不添加“其他”

    # === ✅ Step 6: 构建 ECharts option
    options = {
        "tooltip": {
            "trigger": "item",
            "formatter": f"""
                function(params) {{
                    const otherMap = {json.dumps(other_tooltip_map)};
                    if (otherMap[params.name]) {{
                        return params.name + otherMap[params.name];
                    }}
                    return params.name + '<br/>支付单量: ' + params.value + ' 单<br/>占比: ' + params.percent + '%';
                }}
            """
        },
        "legend": {
            "type": "scroll",
            "orient": "horizontal",
            "bottom": 0,
            "data": legend_data
        },
        "series": [
            {
                "type": "pie",
                "name": "支付单量",
                "radius": ["10%", "65%"],
                "avoidLabelOverlap": False,
                "label": {
                    "show": True,
                    "formatter": "{b}: {c} 单"
                },
                "emphasis": {
                    "scale": True,
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                },
                "labelLine": {"show": True},
                "data": pie_data
            }
        ]
    }

    # === ✅ Step 7: 自动高度，图例不遮挡
    legend_rows = int((len(legend_data) - 1) / 6) + 1
    dynamic_height = 420 + legend_rows * 26

    # === ✅ Step 8: 渲染图表
    st_echarts(
        options=options,
        height=f"{dynamic_height}px"
    )



'''


# utils_v2/pie_charts_echarts.py

from streamlit_echarts import st_echarts
import pandas as pd

def draw_pie_chart(df: pd.DataFrame, key=None):  # ✅ 加 key
    """
    🥧 使用 ECharts 渲染饼状图（甜甜圈风格）

    功能特性：
    ✅ 静态展示：游戏名称 + 支付单量
    ✅ 鼠标悬停：当前扇形放大（视觉聚焦）
    ✅ 图例：底部水平排列、可滚动、宽度自适应
    ✅ 数据处理：只显示前9名，其他合并为“其他”
    ✅ 不展示标题，风格清爽
    """

    # === 1. 处理数据，截取前9名，合并其他为“其他” ===
    df_sorted = df.sort_values(by="支付单量", ascending=False)  # 按支付单量降序排列
    top_df = df_sorted.head(9)                                # 前9名单独展示
    other_sum = df_sorted["支付单量"][9:].sum()               # 第10名及之后合并
    if other_sum > 0:
        top_df = pd.concat([
            top_df,
            pd.DataFrame([{"游戏名称": "其他", "支付单量": other_sum}])  # 合并为“其他”
        ], ignore_index=True)

    # === 2. 转换为 ECharts 所需的 data 格式（字典数组） ===
    pie_data = [
        {
            "name": row["游戏名称"],      # 扇形标签
            "value": row["支付单量"]      # 扇形的值（用于占比计算）
        }
        for _, row in top_df.iterrows()
    ]

    # === 3. 构建 ECharts 配置项 ===
    options = {
        "tooltip": {
            "trigger": "item",  # 鼠标悬浮提示类型
            "formatter": "{b}<br/>支付单量: {c} 单<br/>占比: {d}%"  # 悬浮显示格式
        },
        "legend": {
            "orient": "horizontal",  # 水平布局
            "bottom": 10,            # 放在图表底部
            "type": "scroll",        # ✅ 启用滚动（防止图例太多显示不下）
            "width": "90%"           # 宽度自适应
        },
        "series": [
            {
                "type": "pie",                   # 饼图类型
                "name": "支付单量",               # 系列名称
                "radius": ["10%", "65%"],        # 甜甜圈样式（内外半径）
                "avoidLabelOverlap": False,      # 防止标签重叠
                "label": {
                    "show": True,                # ✅ 静态显示标签
                    "formatter": "{b}: {c}单"    # 展示：游戏名 + 支付单量
                },
                "emphasis": {
                    "scale": True,               # 鼠标悬停放大效果
                    "itemStyle": {
                        "shadowBlur": 10,        # 阴影模糊程度
                        "shadowOffsetX": 0,      # 阴影水平偏移
                        "shadowColor": "rgba(0, 0, 0, 0.5)"  # 阴影颜色
                    }
                },
                "labelLine": {"show": True},     # 显示连接线
                "data": pie_data                 # 饼图数据源
            }
        ]
    }

    # === 4. 渲染图表，适配宽度与高度（不需返回 fig） ===
    st_echarts(
        options=options,
        height="420px",  # 图表高度
        key = key  # ✅ Streamlit 必需的图表唯一标识
    )

