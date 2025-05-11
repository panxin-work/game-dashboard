import streamlit as st

def render_pie_chart(title, data, chart_key, container=None, charts=None):
    """
    🎯 通用饼图渲染函数（适配 Plotly v1 / ECharts v2）
    - 支持横向列布局（col1, col2, col3）
    - 自动处理 v1/v2 渲染方式
    - 自动注入 Streamlit key（避免图表冲突）

    参数说明：
    - title: 图表标题（字符串），例如 "🍩 昨日支付占比"
    - data: pandas.DataFrame，必须包含 ['游戏名称', '支付单量'] 两列
    - chart_key: 字符串，用于 Streamlit 图表唯一标识（防止刷新冲突）
    - container: Streamlit 的列容器对象，例如 col1 / col2（可选）
    - charts: chart_loader.load_chart_modules(version=...) 的返回结果字典，必须包含：
        - "is_echarts": bool，是否使用 ECharts 渲染
        - "draw_pie_chart": 函数，用于绘制饼图（需支持传入 key）

    使用示例：
        from config.pie_chart_renderer import render_pie_chart
        render_pie_chart("昨日支付", df_data, "pie_chart_yesterday", container=col1, charts=charts)
    """

    # ✅ 安全校验：charts 不能为 None 且必须包含 draw_pie_chart 函数
    if charts is None or "draw_pie_chart" not in charts:
        st.error("❌ charts 渲染模块未传入或格式错误")
        return

    # ✅ === 分支处理：Plotly 渲染（v1 快速版） ===
    if not charts["is_echarts"]:
        # ▶ 如果有传容器（如 col1），就在该列中渲染标题和图表
        if container:
            container.subheader(title)
            fig = charts["draw_pie_chart"](data)  # v1 返回 Plotly 图对象
            if fig is not None:
                container.plotly_chart(fig, use_container_width=True, key=chart_key)
        else:
            # ▶ 如果没有传容器，就用主区域 st 渲染
            st.subheader(title)
            fig = charts["draw_pie_chart"](data)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True, key=chart_key)

    # ✅ === 分支处理：ECharts 渲染（v2 高定制） ===
    else:
        # ⚠️ 注意：ECharts 是通过 st_echarts()/components.html() 实现，必须强制用 container.container()
        if container:
            container.subheader(title)
            block = container.container()  # ✅ 新建一个“容器区块”，强制将图表限制在 col1/col2 内
            with block:
                charts["draw_pie_chart"](data, key=chart_key)  # ✅ 确保传入 key
        else:
            st.subheader(title)
            charts["draw_pie_chart"](data, key=chart_key)