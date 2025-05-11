# 主程序入口

# ========== 🛠️ 添加项目根目录到模块搜索路径 ==========
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# ========== 📦 标准库导入 ==========
from datetime import timedelta

# ========== 🔧 第三方库 ==========
import streamlit as st
import pandas as pd

# ========== 📚 模块封装 ==========
from config.chart_loader import load_chart_modules              #引入图表渲染版本切换模块
from config.pie_chart_renderer import render_pie_chart          #引入饼图渲染模块


# ========== 🖼️ 页面基本设置 ==========
st.set_page_config(page_title="游戏数据仪表盘", layout="wide")
st.title("🎮 游戏渠道数据分析仪表盘")


# ========== 📁 侧边栏：上传数据文件 ==========
st.sidebar.header("📁 数据源设置")
uploaded_file = st.sidebar.file_uploader("上传 Excel 文件", type=["xlsx"])

# ✅ 引入使用封装好的excel附件导入模块
from config.attachments_loader import load_data  # 🆕 模块封装版本

df = load_data(uploaded_file, BASE_DIR)

# ✅ 若数据加载失败，则终止后续执行
if df is None:
    st.stop()


# ========== 🧭 图表渲染方式设置（v1 / v2） ==========
st.sidebar.header("🧭 图表显示设置")
chart_version = st.sidebar.radio("选择图表渲染版本", ["快速版（v1）", "高定制版（v2）"])
version = "v1" if "v1" in chart_version else "v2"

# ✅ 加载对应版本的图表模块（内部自动 fallback）
charts = load_chart_modules(version=version)

# ✅ 解包图表函数
draw_line_chart = charts["draw_line_chart"]
draw_pie_chart = charts["draw_pie_chart"]
draw_bar_chart = charts["draw_bar_chart"]
apply_chinese_font = charts["apply_chinese_font"]
render_info_card = charts["render_info_card"]  # ✅ 统一从封装中取，避免主程序判断

# ✅ 无有效数据则终止执行
if df is None:
    st.stop()


# ========== 🧹 数据预处理 ==========
# ✅ 转换日期列为 datetime 类型
if "dt" in df.columns:
    df["dt"] = pd.to_datetime(df["dt"])
else:
    st.error("❌ Excel 中必须包含 'dt' 列（日期）")
    st.stop()

# ✅ 获取“今天”与“近7日”的起始日期
today = df["dt"].max()
seven_days_ago = today - timedelta(days=6)

# ✅ 筛选近7日数据
df_7d = df[df["dt"] >= seven_days_ago]


# ========== 🎮 游戏筛选器 ==========
game_list = sorted(df["游戏名称"].unique())
selected_games = st.multiselect("选择要展示的游戏", game_list, default=game_list)

# ✅ 根据选择结果筛选数据
filtered_df = df[df["游戏名称"].isin(selected_games)]
filtered_df_7d = df_7d[df_7d["游戏名称"].isin(selected_games)]

# ========== 🧮 图 1：数据概览（卡片样式-数组） ==========
st.subheader("📌 数据概览")

from config.card_renderer import render_card  # ✅ 卡片渲染封装器

# ✅ 日期准备
day_before = today - timedelta(days=1)

# ✅ 创建三列容器
col1, col2, col3 = st.columns(3)  # 👉 横向一行三卡片展示

# ✅ 图 1.1：活跃商户数
with col1:
    active_merchants_yesterday = df[df["dt"] == today]["商户昵称"].nunique()
    active_merchants_before = df[df["dt"] == day_before]["商户昵称"].nunique()
    delta_merchants = active_merchants_yesterday - active_merchants_before

    render_card(
        render_func=charts["render_info_card"],
        title="活跃商户数（昨日）",
        #subtitle="活跃商户数",
        value=active_merchants_yesterday,
        delta=delta_merchants,
        unit=" 家",
        color="#1890ff"
    )

# ✅ 图 1.2：在售总数
with col2:
    on_sale_yesterday = df[df["dt"] == today]["在售商品数量"].sum()
    on_sale_before = df[df["dt"] == day_before]["在售商品数量"].sum()
    delta_on_sale = on_sale_yesterday - on_sale_before

    render_card(
        render_func=charts["render_info_card"],
        title="在售总数（昨日）",
        #subtitle="在售商品数量",
        value=on_sale_yesterday,
        delta=delta_on_sale,
        unit=" 件",
        color="#faad14"
    )

# ✅ 图 1.3：支付单数
with col3:
    paid_orders_yesterday = df[df["dt"] == today]["支付单量"].sum()
    paid_orders_before = df[df["dt"] == day_before]["支付单量"].sum()
    delta_paid_orders = paid_orders_yesterday - paid_orders_before

    render_card(
        render_func=charts["render_info_card"],
        title="支付单数（昨日）",
        #subtitle="支付成功订单数",
        value=paid_orders_yesterday,
        delta=delta_paid_orders,
        unit=" 单",
        color="#13c2c2"
    )


# ========== 📈 图表 2：每日支付单量趋势（折线图样式） ==========
st.subheader("📈 每日支付单量趋势")
line_data = filtered_df.groupby("dt")["支付单量"].sum().reset_index()
fig_line = draw_line_chart(line_data)
st.plotly_chart(fig_line, use_container_width=True, key="line_chart")


# ========== 🥧 🥠 图表 3: 横向排列显示 3 个支付占比图表 （饼图样式）==========
# ✅ 创建横向三列容器
col1, col2, col3 = st.columns(3)

# ✅ 数据准备：昨天 / 近7日 / 累计
df_yesterday = filtered_df[filtered_df["dt"] == today]
pie_yesterday_data = df_yesterday.groupby("游戏名称")["支付单量"].sum().reset_index()

pie_7d_data = filtered_df_7d.groupby("游戏名称")["支付单量"].sum().reset_index()
pie_all_data = filtered_df.groupby("游戏名称")["支付单量"].sum().reset_index()

# ✅ 在三列中分别渲染图表（标题 + 图表都放入对应容器）
with col1:
    render_pie_chart("🍩 昨日支付", pie_yesterday_data, "pie_chart_yesterday", container=col1, charts=charts)

with col2:
    render_pie_chart("🥧 近7日支付", pie_7d_data, "pie_chart_7d", container=col2, charts=charts)

with col3:
    render_pie_chart("🥠 累计支付", pie_all_data, "pie_chart_all", container=col3, charts=charts)



