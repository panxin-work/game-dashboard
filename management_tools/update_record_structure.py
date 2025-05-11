import os

# 定义项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 定义目标文件路径
TARGET_FILE = os.path.join(PROJECT_ROOT, "management_tools", "record_structure.py")
print(f"Target file path: {TARGET_FILE}")  # 打印目标路径，确认是否正确

# 定义需要排除的目录和文件
EXCLUDED_DIRS = {".venv", "management_tools", ".idea", "__pycache__"}
EXCLUDED_FILES = {"__init__.py"}

# 定义注释内容备用
COMMENTS = {
    "LogPulse": "日志脉动：项目根目录，包含所有代码和配置",
    ".venv": "虚拟环境目录",
    "management_tools": "管理工具（记录项目结构等）",
    "quick_tests": "快速测试目录，独立的小测试脚本",
    "src": "主代码目录，包含核心代码",
    "backend": "后端核心代码",
    "frontend": "前端核心代码",
    "log_parser": "日志解析的核心目录",
    "tools": "工具目录",
    #   "config": "配置目录，存放数据库文件",
    #   "db": "数据库相关代码",
    #   "frontend": "前端代码",
    #   "modules": "业务逻辑目录",
    #   "README.md": "项目说明文件",
    }

# 最大对齐宽度
ALIGN_WIDTH = 68


def is_text_file(file_path):
    """
    判断文件是否为文本文件
    :param file_path: 文件路径
    :return: 如果是文本文件，返回 True，否则返回 False
    """
    try:
        with open(file_path, "rb") as file:
            # 尝试读取文件的前 1024 字节并检查是否包含二进制字符
            chunk = file.read(1024)
            if b'\0' in chunk:  # 如果包含空字节，则认为是二进制文件
                return False
        return True
    except Exception as e:
        print(f"无法判断文件类型 {file_path}，错误：{e}")
        return False


def extract_first_line_comment(file_path):
    """
    提取文件第一行注释
    :param file_path: 文件路径
    :return: 注释内容（如果没有注释，则返回空字符串）
    """
    if not is_text_file(file_path):  # 如果不是文本文件，直接返回空注释
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            if first_line.startswith("#"):
                return first_line[1:].strip()  # 去掉 '#' 和前后空白
    except Exception as e:
        print(f"无法读取文件 {file_path}，错误：{e}")
    return ""


def generate_directory_structure(start_path, prefix=""):
    """
    递归生成项目目录结构，并动态提取注释
    :param start_path: 起始目录
    :param prefix: 前缀缩进
    :return: 带注释的目录结构字符串
    """
    structure = ""
    for root, dirs, files in os.walk(start_path):
        # 获取当前目录的深度，用于生成缩进
        depth = root.replace(start_path, "").count(os.sep)

        # 跳过排除的目录
        if any(excluded in root for excluded in EXCLUDED_DIRS):
            continue

        # 添加目录本身
        indent = "│   " * depth + "├── "
        dir_name = os.path.basename(root)
        dir_line = f"{indent}{dir_name}/"
        comment = f"# {COMMENTS.get(dir_name, '')}"
        structure += f"{dir_line.ljust(ALIGN_WIDTH)} {comment}\n"

        # 添加文件
        for file in files:
            if file in EXCLUDED_FILES:
                continue
            file_indent = "│   " * (depth + 1) + "├── "
            file_line = f"{file_indent}{file}"
            file_path = os.path.join(root, file)

            # 优先从文件提取注释
            comment = extract_first_line_comment(file_path)
            if not comment:  # 如果文件中无注释，使用预定义注释
                comment = COMMENTS.get(file, "")
            structure += f"{file_line.ljust(ALIGN_WIDTH)} # {comment}\n"
    return structure


def update_record_structure():
    """
    自动更新 record_structure.py 文件
    """
    try:
        # 动态生成目录结构
        directory_structure = generate_directory_structure(PROJECT_ROOT)

        # 写入文件
        with open(TARGET_FILE, "w", encoding="utf-8") as file:
            file.write(f"# 项目目录结构\n\n")
            file.write(f"directory_structure = '''\n{directory_structure}'''\n")
        print(f"目录结构已成功写入到：{TARGET_FILE}")
    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    update_record_structure()