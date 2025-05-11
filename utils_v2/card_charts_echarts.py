# utils_v2/card_charts_echarts.py

from streamlit_echarts import st_echarts

def render_info_card(title: str, value, delta=None, unit=None, color="#1890ff", key=None):
    """
    🧊 使用 ECharts 渲染数据概览卡片（高定制版，适用于 v2）

    功能特点：
    ✅ 主数值居中放大显示
    ✅ 支持 delta 增减变化（绿色↑ / 红色↓ / 灰色持平）
    ✅ 支持无单位情况（如百分比）
    ✅ 自动居中对齐内容，可在三列布局中使用

    参数说明：
    - title: 卡片标题（如“活跃商户数”）
    - value: 主体数值（支持 int / float / str / None）
    - delta: 与昨日对比的变化值，正数为增加，负数为减少，None 表示不显示
    - unit: 单位，可选（如“家”、“%”等），None 表示不展示单位
    - color: 主数值字体颜色，默认为蓝色
    - key: Streamlit 渲染用唯一标识
    """

    # ✅ 安全处理主值为空情况
    value = value if value is not None else 0

    # ✅ 如果有单位，则拼接；否则只显示纯值
    unit_display = unit if unit else ""
    main_value_text = f"{value}{unit_display}"

    # ✅ 构建 delta 显示部分（变化箭头 + 颜色 + 位置）
    delta_part = {}
    if delta is not None:
        # 符号选择与颜色设置
        if delta > 0:
            direction = "↑"
            delta_color = "#52c41a"  # 绿色：上升
        elif delta < 0:
            direction = "↓"
            delta_color = "#f5222d"  # 红色：下降
        else:
            direction = "-"
            delta_color = "#999999"  # 灰色：持平

        # 构建显示文字（注意单位拼接）
        delta_value = f"{direction} {abs(delta)}{unit_display}"

        # 作为 ECharts graphic text 的配置项添加
        delta_part = {
            "value": delta_value,
            "textStyle": {
                "fontSize": 14,
                "color": delta_color,
            },
            "top": "60%",  # 控制纵向位置
        }

    # ✅ 构建 ECharts 渲染配置
    option = {
        "graphic": [
            {
                "type": "group",
                "left": "center",
                "top": "middle",
                "children": [
                    {
                        "type": "text",
                        "left": "center",
                        "top": "20%",
                        "style": {
                            "text": title,
                            "fontSize": 14,
                            "fill": "#666",
                            "fontWeight": 500,
                        }
                    },
                    {
                        "type": "text",
                        "left": "center",
                        "top": "40%",
                        "style": {
                            "text": main_value_text,
                            "fontSize": 28,
                            "fontWeight": "bold",
                            "fill": color,
                        }
                    },
                ] + ([{
                        "type": "text",
                        "left": "center",
                        **delta_part
                    }] if delta_part else [])
            }
        ]
    }

    # ✅ 使用 streamlit_echarts 进行渲染
    st_echarts(options=option, height="120px", key=key)