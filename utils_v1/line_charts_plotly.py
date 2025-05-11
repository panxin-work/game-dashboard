# 折线图封装 100%
# utils/line_charts.py

import plotly.express as px             # 导入 Plotly Express 模块，并简写为 px，用于绘图
import pandas as pd                     # 导入 Pandas 数据分析库，并简写为 pd，用于数据处理
from utils_v1.theme import apply_chinese_font, apply_plot_style             # 从 utils_v1/theme.py 文件中导入中文字体和风格函数，用于图表美化


def draw_line_chart(df, y_col="支付单量", max_ticks=10):              # 定义一个函数，支持指定要绘制的数值列，默认绘制“支付单量”
    """
    📊 画一张横轴为“某种时间”、纵轴为“某个数值字段”的趋势折线图。

    只要满足以下两个基本条件，它就可以直接使用：
    1. 传入的 df 是一个表格（DataFrame），包含一列表示时间的数据（列名需为 'dt'，可以是字符串或 datetime 类型）；
    2. 该表还需包含一列数值列（列名由 y_col 指定，默认是 '支付单量'），用于绘图，可存在空值但必须可转为整数。
    3. 除此之外，max_ticks 是一个可选参数，用于控制横轴刻度的最大数量，默认值为 10，不传也可以运行。

    功能亮点：
    ✅ 自动补全日期（防止跳日期）
    ✅ 若数据超过30天，仅展示近30天（避免横轴过长）
    ✅ 横轴显示唯一日期（非重复）
    ✅ 鼠标提示清晰，含辅助线
    ✅ 图表风格统一，支持中文字体
    ✅ 支持绘制任意数值字段，如“支付单量”“活跃商家数量”“商品数量”等

    参数：
        df（DataFrame）：要求包含 'dt'（日期列）和要绘制的数值列（由 y_col 指定）
        y_col（str）：指定用于绘图的数值列名，默认是 '支付单量'
        max_ticks（int）：控制横轴最多显示的刻度数量，默认值为 10
    """

    # === ✅ 0. 日期预处理：确保 dt 为 datetime 类型 ===
    df["dt"] = pd.to_datetime(df["dt"])  # 把“dt”列从字符串转换为 pandas 支持的 datetime 类型（datetime64[ns]），否则后续不能使用时间差、格式化、绘图等操作


    # === ✅ 1. 如果时间跨度超过30天，只保留最近30天的数据 ===
    if (df["dt"].max() - df["dt"].min()).days > 30:                 # 检查当前数据中的时间跨度是否超过30天（最大日期 - 最小日期），如果没超过则不做处理
        cutoff_date = df["dt"].max() - pd.Timedelta(days=29)        # 如果超过30天，则以“最大日期 - 29天”作为起始时间，构造一个“最近30天”的截取时间点
        df = df[df["dt"] >= cutoff_date].copy()                     # 筛选出“日期大于等于 cutoff_date”的所有数据行，并生成新副本（避免原表引用产生警告）


    # === ✅ 2. 自动补全缺失日期，保证折线连续 ===
    full_dates = pd.date_range(start=df["dt"].min(), end=df["dt"].max(), freq="D")          # 构造完整的日期范围
    df_full = pd.DataFrame({"dt": full_dates})                                              # 创建仅含日期的完整表
    df = pd.merge(df_full, df, on="dt", how="left")                                         # 与原始数据按日期左连接


    # === ✅ 3. 对缺失的数值列填 0，并确保为整数类型 ===
    df[y_col] = df[y_col].fillna(0).astype(int)  # # 将指定的数值列中缺失值填为 0，并转换为整数类型，避免绘图断线或报错


    # === ✅ 4. 构造横轴字符串列，确保唯一、清晰 ===             # 确保图例是离散、唯一、可控的，比如 "05/01", "05/02" 等，不会重复、挤压
    df["日期"] = df["dt"].dt.strftime("%m/%d")                # 将 datetime 类型的 dt 列格式化为字符串（如 "04/29"），用于作为横轴标签，确保清晰且不重复


    # === ✅ 5. 创建基础折线图（x 为日期字符串，y 为指定字段）===
    fig = px.line(                      # 使用 Plotly Express 绘制基础折线图：x 为日期，y 为指定数值字段，圆点用于突出每个数据点
        df,
        x="日期",
        y=y_col,
        markers=True                    # 固定参数，控制是否显示 marker 点（圆点）
    )


    # === ✅ 6. Y 轴刻度适配策略（根据数据量智能处理）===
    max_val = df[y_col].max()               # 获取当前数值列的最大值，用于判断刻度策略

    if max_val <= 10:               # 数据较少时，设置步长为 1，防止出现小数刻度
        fig.update_yaxes(
            title_text=y_col,               # Y轴标题直接使用字段名
            tickformat="d",                 # 设置为整数格式（不显示小数点）
            dtick=1,                        # 每格间隔 1（即：0,1,2,...）
            rangemode="tozero",             # 保证 Y轴从 0 开始，避免图形被截段，或造成视觉误差
            showline=True                   # 显示 Y轴主线
        )
    else:                           # 数据较多时，限制为最多 5 个刻度
        fig.update_yaxes(
            title_text=y_col,
            tickformat="d",
            nticks=5,                       # 最多显示 5 个刻度，防止画出 N 个刻度，导致 Y轴太密看不清
            rangemode="tozero",
            showline=True
        )


    # === ✅ 7. 优化 X 轴显示：分类轴 + 控制最大刻度数量 ===
    fig.update_xaxes(
        title_text=None,                # 不显示横轴标题（如“日期”），让图更简洁
        tickangle=-30,                  # 横轴标签倾斜 30 度，避免日期重叠遮挡
        showline=True,                  # 显示横轴主轴线
        type="category",                # 明确指定横轴为 分类轴 而非 数值轴，防止自动转换为时间线
        tickmode="linear",              # 横轴刻度均匀分布（默认会按数据间距变动）
        nticks=max_ticks                # 最多显示 max_ticks 个刻度，防止标签太密看不清
    )


    # === ✅ 8. 鼠标悬停提示：动态字段名 + 单位 + 不显示 trace 名称 ===
    fig.update_traces(
        hovertemplate=f"日期: %{{x}}<br>{y_col}: %{{y}} 单<extra></extra>"
    )


    # === ✅ 9. 应用全局字体与风格样式（中文 + 项目统一化）===
    fig = apply_chinese_font(fig)     # 中文字体支持
    fig = apply_plot_style(fig)       # 项目配色统一样式


    # === ✅ 10. 开启鼠标悬停时的垂直辅助线（crosshair）===
    fig.update_layout(
        hovermode="x unified"   # 沿 x 轴显示统一提示 + 辅助线
    )


    return fig







'''

# 折线图封装 100%
# utils/line_charts.py

import plotly.express as px             # 导入 Plotly Express 模块，并简写为 px，用于绘图
import pandas as pd                     # 导入 Pandas 数据分析库，并简写为 pd，用于数据处理
from utils_v1.theme import apply_chinese_font, apply_plot_style             # 从 utils_v1/theme.py 文件中导入中文字体和风格函数，用于图表美化


def draw_line_chart(df, max_ticks=10):              # 定义一个函数，函数名叫 draw_line_chart（绘制折线图）
    """
    📊 画一张横轴为“某种时间”、纵轴为“某种数值”的趋势折线图。

    只要满足以下两个基本条件，它就可以直接使用：
	1.	传入的 df 是一个表格（DataFrame），包含一列表示时间的数据（列名需为 'dt'，可以是字符串或 datetime 类型）；
	2.	该表还需包含一列数值列（列名为 '支付单量'），表示每个时间点对应的数量，允许存在空值但必须可转为整数。
	3.  除此之外，max_ticks 是一个可选参数，用于控制横轴刻度的最大数量，默认值为 10，不传也可以运行。

    功能亮点：
    ✅ 自动补全日期（防止跳日期）
    ✅ 若数据超过30天，仅展示近30天（避免横轴过长）
    ✅ 横轴显示唯一日期（非重复）
    ✅ 鼠标提示清晰，含辅助线
    ✅ 图表风格统一，支持中文字体

    参数：
        df（DataFrame）：要求包含 'dt'（日期列）和 '支付单量'
        max_ticks（int）：控制横轴最多显示的刻度数量
    """

    # === ✅ 0. 日期预处理：确保 dt 为 datetime 类型 ===
    df["dt"] = pd.to_datetime(df["dt"])  # 若原始是字符串，自动转换

    # === ✅ 1. 如果时间跨度超过30天，只保留最近30天的数据 ===
    if (df["dt"].max() - df["dt"].min()).days > 30:
        cutoff_date = df["dt"].max() - pd.Timedelta(days=29)
        df = df[df["dt"] >= cutoff_date].copy()

    # === ✅ 2. 自动补全缺失日期，保证折线连续 ===
    # 构造完整的日期范围（从最小到最大日期）
    full_dates = pd.date_range(start=df["dt"].min(), end=df["dt"].max(), freq="D")

    # 构造一个完整 DataFrame，仅包含日期
    df_full = pd.DataFrame({"dt": full_dates})

    # 将原始数据合并到完整日期上（左连接）
    df = pd.merge(df_full, df, on="dt", how="left")

    # 对缺失的支付单量填 0，并确保为整数类型
    df["支付单量"] = df["支付单量"].fillna(0).astype(int)

    # === ✅ 3. 构造横轴字符串列，确保唯一、清晰 ===
    df["日期"] = df["dt"].dt.strftime("%m/%d")  # 格式如 "04/29"

    # === ✅ 4. 创建基础折线图 ===
    fig = px.line(
        df,
        x="日期",             # 横轴使用格式化后的日期字符串
        y="支付单量",         # 纵轴为支付单量
        markers=True          # 每个数据点标记圆点
    )

    # === ✅ 5. Y 轴刻度适配策略（根据数据量智能处理）===
    max_val = df["支付单量"].max()  # 获取最大值，用于后续判断

    if max_val <= 10:
        # 数据较少时，设置步长为 1，防止出现小数刻度
        fig.update_yaxes(
            title_text="支付单量",
            tickformat="d",         # 整数格式
            dtick=1,                # 每格间隔 1
            rangemode="tozero",     # 从 0 开始
            showline=True
        )
    else:
        # 数据较多时，限制为最多 5 个刻度
        fig.update_yaxes(
            title_text="支付单量",
            tickformat="d",
            nticks=5,
            rangemode="tozero",
            showline=True
        )

    # === ✅ 6. 优化 X 轴显示：分类轴 + 控制最大刻度数量 ===
    fig.update_xaxes(
        title_text=None,         # 不显示标题“日期”
        tickangle=-30,           # 标签倾斜角度
        showline=True,
        type="category",         # 明确指定为分类轴（防止重复）
        tickmode="linear",       # 等间距显示
        nticks=max_ticks         # 限制横轴最多刻度数
    )

    # === ✅ 7. 鼠标悬停提示：中文字段 + 单位 + 不显示 trace 名称 ===
    fig.update_traces(
        hovertemplate="日期: %{x}<br>支付单量: %{y} 单<extra></extra>"
    )

    # === ✅ 8. 应用全局字体与风格样式（中文 + 项目统一化）===
    fig = apply_chinese_font(fig)     # 中文字体支持
    fig = apply_plot_style(fig)       # 项目配色统一样式

    # === ✅ 9. 开启鼠标悬停时的垂直辅助线（crosshair）===
    fig.update_layout(
        hovermode="x unified"   # 沿 x 轴显示统一提示 + 辅助线
    )

    return fig

'''