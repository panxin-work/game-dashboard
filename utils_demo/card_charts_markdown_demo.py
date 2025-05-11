

import streamlit as st

def render_info_card(
    title: str,
    value,
    delta=None,
    unit=None,
    color="#1890ff",
    key=None,
    with_title=True,
    subtitle=None,
    debug=False
):
    """
    🧊 渲染数据概览卡片（v1 版本：使用 st.markdown + HTML）

    参数说明：
    - title (str): 主标题（支持带图标，如 "📌 活跃商户数"）
    - value (Any): 主数值（例如 123）
    - delta (int/float/None): 与昨日对比的变化量，None 表示不显示
    - unit (str/None): 单位文本（如 "家"、"个"、"单" 等）
    - color (str): 左侧主色条颜色（支持十六进制色值）
    - key (str/None): 保留字段，用于与 v2 接口保持一致（当前未使用）
    - with_title (bool): 是否显示卡片顶部的标题，默认为 True
    - subtitle (str/None): 副标题说明文本，默认不显示
    - debug (bool): 是否输出调试信息，默认 False

    返回：None（直接渲染）
    """

    # ✅ Debug 输出（用于开发调试）
    if debug:
        print("\n[🔍 render_info_card 调试信息]")
        print(f"title     = {title}")
        print(f"value     = {value}")
        print(f"delta     = {delta}")
        print(f"unit      = {unit}")
        print(f"color     = {color}")
        print(f"key       = {key}")
        print(f"subtitle  = {subtitle}")
        print("-" * 40)

    # ✅ 构建变化量的文案块
    delta_block = """
    if delta is not None:
        if delta > 0:
            text, text_color = f"与前一日相比 增加 {delta}{unit}", "#52c41a"
        elif delta < 0:
            text, text_color = f"与前一日相比 减少 {abs(delta)}{unit}", "#f5222d"
        else:
            text, text_color = "与前一日持平", "#999999"

        delta_block = f"""
        <div style='font-size:13px; color:{text_color}; margin-top:6px;'>
            {text}
        </div>
        """

    # ✅ 构建标题块（是否展示可配置）
    title_block = f"""
        <div style='font-size:16px; font-weight:bold; margin-bottom:8px;'>
            {title}
        </div>
    """ if with_title else ""

    # ✅ 构建副标题块（如果提供则显示）
    subtitle_block = f"""
        <div style='font-size:13px; color:#888888;'>
            {subtitle}
        </div>
    """ if subtitle else ""

    # ✅ 最终 HTML 卡片
    html = f"""
    <div style="
        width: 100%;
        background: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border-left: 5px solid {color};
    ">
        {title_block}
        {subtitle_block}
        <div style="margin-top:4px;">
            <div style="font-size:28px; font-weight:bold; color:#333333;">
                {value}{unit if unit else ""}
            </div>
            {delta_block}
        </div>
    </div>
    """.strip()

    # ✅ 渲染 HTML 到页面
    st.markdown(html, unsafe_allow_html=True)




'''
import streamlit as st

def render_info_card(title: str, value, delta=None, unit=None, color="#1890ff"):
    """
    🧊 渲染数据概览卡片（轻量型 Markdown 实现，适用于 v1）

    功能特点：
    ✅ 支持主数值显示
    ✅ 支持相较昨日的增减变化值（可选）
    ✅ 可自定义单位（也可以不传单位）
    ✅ 使用 Streamlit + HTML 实现卡片样式，适配横向/纵向布局

    参数说明：
    - title (str): 卡片标题，例如 "活跃商户数"
    - value (int | float | str | None): 主体数值，支持数字或百分比等字符串，None 会被处理为 0
    - delta (int | float | None): 与昨日相比的变化量，可正可负，None 表示不显示
    - unit (str | None): 单位（如 "家" / "个" / "%"），可选，默认不拼接单位
    - color (str): 左侧色条的颜色，默认蓝色 "#1890ff"

    使用示例：
        render_info_card("支付成功率", "95%")
        render_info_card("活跃商户", 132, delta=5, unit="家")
    """

    # ✅ 安全处理主值：如果为 None，默认显示为 0
    value = value if value is not None else 0

    # ✅ 变化量文字内容（默认不显示）
    delta_str = ""
    if delta is not None:
        # 决定变化符号（正数加 +，负数保留，0 无符号）
        sign = "+" if delta > 0 else ""
        # 设置变化文字颜色（上升绿、下降红、持平灰）
        if delta > 0:
            delta_color = "#52c41a"  # 绿色（上升）
        elif delta < 0:
            delta_color = "#f5222d"  # 红色（下降）
        else:
            delta_color = "#999999"  # 灰色（持平）

        # 如果单位存在则拼接，否则为空字符串
        unit_display = unit if unit else ""

        # 构建变化量 HTML 片段（用于展示 ±xx单位）
        delta_str = f"<span style='color:{delta_color}; font-size: 13px;'>{sign}{delta}{unit_display}</span>"

    # ✅ 主数值 + 单位拼接（根据 unit 是否存在判断）
    main_value_str = f"{value}{unit}" if unit else str(value)

    # ✅ 如果有 delta，则拼接变化量；否则只显示主值
    value_block = f"{main_value_str} {delta_str}" if delta_str else main_value_str

    # ✅ 构建 HTML 卡片样式：背景白色、左侧色条、圆角阴影
    html = f"""
    <div style="
        background: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border-left: 5px solid {color};
    ">
        <div style="font-size: 13px; color: #888;">{title}</div>
        <div style="font-size: 28px; font-weight: bold; color: #333; margin-top: 4px;">
            {value_block}
        </div>
    </div>
    """

    # ✅ 使用 Streamlit 渲染 HTML（启用 unsafe_allow_html 才能插入富文本）
    st.markdown(html, unsafe_allow_html=True)
    
    
'''