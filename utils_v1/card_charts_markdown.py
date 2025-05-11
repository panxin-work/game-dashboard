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
    🧊 渲染数据概览卡片（v1 版本：使用 st.markdown + HTML 实现样式）

    参数说明：
    - title (str): 主标题，可包含图标，如 "📌 活跃商户数"
    - value (Any): 主体数值（如 113）
    - delta (int/float/None): 与昨日对比的变化量，可正可负，None 表示不显示
    - unit (str/None): 单位文本，如 "家"、"%" 等
    - color (str): 左侧主色条颜色（如 "#1890ff" 蓝色）
    - key (str/None): 保留字段，当前未使用（为 v2 渲染版本预留）
    - with_title (bool): 是否显示主标题，默认为 True（内嵌卡片顶部）
    - subtitle (str/None): 副标题说明文本，可为空，不显示
    - debug (bool): 是否输出调试信息，True 时将输出渲染参数到控制台
    """

    # ✅ Debug：输出调试信息，方便开发者查看当前渲染参数
    if debug:
        print("\n[render_info_card 调试信息]")
        print(f"title = {title}, value = {value}, delta = {delta}, unit = {unit}, color = {color}")
        print(f"key = {key}, subtitle = {subtitle}, with_title = {with_title}")
        print("-" * 40)

    # ✅ 差值变化文案块（根据 delta 值正负情况渲染不同颜色）
    delta_block = ""
    if delta is not None:
        if delta > 0:
            delta_block = (
                f"<div style='font-size:13px; color:#52c41a; margin-top:6px;'>"
                f"与前一日相比 增加 {delta}{unit or ''}</div>"
            )
        elif delta < 0:
            delta_block = (
                f"<div style='font-size:13px; color:#f5222d; margin-top:6px;'>"
                f"与前一日相比 减少 {abs(delta)}{unit or ''}</div>"
            )
        else:
            delta_block = (
                "<div style='font-size:13px; color:#999999; margin-top:6px;'>"
                "与前一日持平</div>"
            )

    # ✅ 主标题块（根据 with_title 控制是否显示，建议包含图标）
    title_block = (
        f"<div style='font-size:16px; font-weight:bold; margin-bottom:8px;'>{title}</div>"
        if with_title else ""
    )

    # ✅ 副标题块（仅当 subtitle 不为空时才显示）
    subtitle_block = (
        f"<div style='font-size:13px; color:#888888;'>{subtitle}</div>"
        if subtitle else ""
    )

    # ✅ 最终卡片 HTML 拼接（注意：无缩进、单行字符串，确保样式渲染一致）
    html = (
        f"<div style='width: 100%; background: white; padding: 16px 20px; border-radius: 12px; "
        f"box-shadow: 0 4px 12px rgba(0,0,0,0.12); border-left: 5px solid {color};'>"
        f"{title_block}"           # 主标题行
        f"{subtitle_block}"        # 副标题说明
        f"<div style='margin-top:4px;'>"
        f"<div style='font-size:28px; font-weight:bold; color:#333333;'>"
        f"{value}{unit or ''}</div>"  # 主值 + 单位
        f"{delta_block}"           # 差值文本行
        f"</div></div>"
    )

    # ✅ 渲染 HTML 到页面（允许插入原生 HTML 样式）
    st.markdown(html, unsafe_allow_html=True)