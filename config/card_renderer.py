# config/card_renderer.py

import inspect

def render_card(render_func, title, value, delta=None, unit=None, color="#1890ff", key=None, subtitle=None):
    """
    ✅ 通用卡片渲染器封装（适配 render_info_card v1/v2，统一样式与健壮性）

    参数说明：
    - render_func: 实际执行渲染的函数（由 chart_loader 加载）
    - title: 卡片标题（如“活跃商户数”）
    - value: 主体数值（int、float、str 或百分比等）
    - delta: 与昨日变化值，可为正负（None 表示不显示）
    - unit: 单位（如“家”、“%”等，None 表示不拼接单位）
    - color: 主色调（影响字体和边框颜色）
    - key: ECharts 版本专用渲染 key（v1 版本未定义该参数）
    """

    # ✅ 安全兜底处理
    value = value if value is not None else 0
    delta = delta if delta is not None else 0

    # ✅ 获取函数支持的参数列表
    sig = inspect.signature(render_func)
    supported = sig.parameters

    # ✅ 构造参数字典
    kwargs = {
        "title": title,
        "value": value,
        "delta": delta,
        "unit": unit,
        "color": color
    }
    # ✅ 仅在支持的情况下再动态补充
    if "key" in supported:
        kwargs["key"] = key
    if "subtitle" in supported:
        kwargs["subtitle"] = subtitle

    # ✅ 渲染卡片
    render_func(**kwargs)