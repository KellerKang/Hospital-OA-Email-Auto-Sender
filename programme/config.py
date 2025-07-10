# -*- coding: utf-8 -*-
"""
配置文件
包含数据库连接参数、邮件发送配置等
"""

import os
from datetime import datetime

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',         # 必须是 localhost 或 127.0.0.1
    'port': 1521,
    'service_name': 'orcl',     # 已注册的实例
    'username': 'system',
    'password': 'root',
    'encoding': 'UTF-8'
}

# 邮件配置
EMAIL_CONFIG = {
    'oa_url': 'http://localhost:5000',  # 本地OA系统地址
    'username': 'admin',                # 邮箱用户名
    'password': 'admin123',             # 邮箱密码
    'recipients': ['user1', 'user2'],   # 收件人列表
    'subject_prefix': '数据报表',        # 邮件主题前缀
}

# 文件配置
FILE_CONFIG = {
    'output_dir': 'D:\\data_reports',  # 输出目录
    'file_prefix': '数据报表',         # 文件前缀
    'file_extension': '.xlsx'          # 文件扩展名
}

# 查询配置
QUERY_CONFIG = {
    'sql_query': '''
        SELECT 
            column1,
            column2,
            column3,
            TO_CHAR(SYSDATE, 'YYYY-MM-DD') as report_date
        FROM your_table_name
        WHERE condition = 'your_condition'
        ORDER BY column1
    ''',  # 需要执行的SQL查询
    'sheet_name': '数据报表'  # Excel工作表名称
}

# 时间配置
TIME_CONFIG = {
    'schedule_time': '09:00',  # 每日执行时间
    'timezone': 'Asia/Shanghai'  # 时区
}

def get_filename():
    """生成带时间戳的文件名"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{FILE_CONFIG['file_prefix']}_{timestamp}{FILE_CONFIG['file_extension']}"

def get_filepath():
    """获取完整的文件路径"""
    filename = get_filename()
    return os.path.join(FILE_CONFIG['output_dir'], filename)

def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(FILE_CONFIG['output_dir']):
        os.makedirs(FILE_CONFIG['output_dir'])
        print(f"创建输出目录: {FILE_CONFIG['output_dir']}") 