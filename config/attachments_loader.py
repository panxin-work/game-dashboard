# excel导入加载封装 （需要增加文件模版校错工具）

import os
import pandas as pd
import streamlit as st
from datetime import datetime


def ensure_dir_exists(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)


def save_uploaded_file(uploaded_file, save_dir):
    """
    保存用户上传的 Excel 文件到指定目录。若文件存在则提示是否删除。
    返回保存路径或 None。
    """
    filename = uploaded_file.name
    save_path = os.path.join(save_dir, filename)

    if os.path.exists(save_path):
        # 提示用户删除旧文件
        if st.sidebar.button(f"❗文件已存在：点击删除旧文件（{filename}）"):
            os.remove(save_path)
            st.sidebar.info(f"✅ 旧文件 {filename} 已删除")
        else:
            st.sidebar.warning(f"⚠️ 文件 {filename} 已存在，请删除后重新上传")
            return None

    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"✅ 上传文件已保存为：{filename}")
        return save_path
    except Exception as e:
        st.sidebar.error(f"❌ 文件保存失败：{e}")
        return None


def load_all_excel_files_from_dir(directory):
    """
    读取目录下所有 Excel 文件并合并为一个 DataFrame。
    """
    excel_files = sorted([f for f in os.listdir(directory) if f.endswith(".xlsx")])

    if not excel_files:
        st.sidebar.warning("📂 未找到任何 Excel 文件")
        return None

    all_dfs = []
    for f in excel_files:
        path = os.path.join(directory, f)
        try:
            df = pd.read_excel(path)
            df["来源文件"] = f
            all_dfs.append(df)
        except Exception as e:
            st.sidebar.warning(f"❌ 文件读取失败：{f} - {e}")

    if not all_dfs:
        st.sidebar.error("❌ 所有 Excel 文件均读取失败")
        return None

    st.sidebar.success(f"📚 成功读取 {len(all_dfs)} 个文件")
    return pd.concat(all_dfs, ignore_index=True)


def load_data(uploaded_file, base_dir):
    """
    主入口：处理上传文件 & 加载 attachments/ 中所有 Excel 文件。
    使用 session_state 防止重复保存。
    """
    attachments_dir = os.path.join(base_dir, "attachments")
    ensure_dir_exists(attachments_dir)

    # ✅ 初始化 session_state 防重复
    if "uploaded_saved" not in st.session_state:
        st.session_state["uploaded_saved"] = False

    # ✅ 首次上传后保存文件
    if uploaded_file and not st.session_state["uploaded_saved"]:
        saved_path = save_uploaded_file(uploaded_file, attachments_dir)
        if saved_path is not None:
            st.session_state["uploaded_saved"] = True
        else:
            return None

    # ✅ 加载目录中全部 Excel 文件
    return load_all_excel_files_from_dir(attachments_dir)