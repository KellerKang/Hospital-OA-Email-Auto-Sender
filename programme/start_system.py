#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医院数据自动化系统 - 启动脚本
提供菜单式操作界面，方便用户选择不同的功能
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_banner():
    """打印系统横幅"""
    print("=" * 60)
    print("🏥 医院数据自动化系统")
    print("=" * 60)
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_requirements():
    """检查系统依赖"""
    print("🔍 检查系统依赖...")
    try:
        import oracledb
        import pandas
        import openpyxl
        import flask
        import selenium
        print("✅ 所有依赖包已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def run_script(script_name, description):
    """运行指定的Python脚本"""
    print(f"\n🚀 正在启动: {description}")
    print(f"脚本: {script_name}")
    print("-" * 40)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 脚本执行成功")
            if result.stdout:
                print("输出:")
                print(result.stdout)
        else:
            print("❌ 脚本执行失败")
            if result.stderr:
                print("错误信息:")
                print(result.stderr)
                
    except Exception as e:
        print(f"❌ 执行脚本时出错: {e}")

def test_oracle_connection():
    """测试Oracle数据库连接"""
    print("\n🔍 测试Oracle数据库连接...")
    run_script("test_oracle_connection.py", "Oracle数据库连接测试")

def insert_test_data():
    """插入测试数据"""
    print("\n📊 插入测试门诊数据...")
    run_script("insert_outpatient_records.py", "插入测试门诊记录")

def extract_data_to_excel():
    """提取数据到Excel"""
    print("\n📈 提取门诊数据到Excel...")
    run_script("extract_outpatient_to_excel.py", "提取门诊数据到Excel")

def start_oa_system():
    """启动OA邮箱系统"""
    print("\n📧 启动OA邮箱系统...")
    print("系统将在浏览器中打开: http://localhost:5000")
    print("测试账号:")
    print("  - 用户名: admin, 密码: admin123")
    print("  - 用户名: user1, 密码: user123")
    print("  - 用户名: user2, 密码: user123")
    print("\n按 Ctrl+C 停止服务器")
    
    try:
        subprocess.run([sys.executable, "simple_oa_mail.py"])
    except KeyboardInterrupt:
        print("\n🛑 OA邮箱系统已停止")

def test_email_automation():
    """测试邮件自动化"""
    print("\n🤖 测试邮件自动化流程...")
    run_script("test_email_automation.py", "邮件自动化测试")

def run_full_automation():
    """运行完整自动化流程"""
    print("\n🔄 运行完整自动化流程...")
    run_script("main.py", "完整自动化流程")

def setup_schedule_task():
    """设置定时任务"""
    print("\n⏰ 设置Windows计划任务...")
    run_script("schedule_task.py", "设置定时任务")

def run_system_test():
    """运行系统测试"""
    print("\n🧪 运行系统功能测试...")
    run_script("test_system.py", "系统功能测试")

def show_project_info():
    """显示项目信息"""
    print("\n📋 项目信息:")
    print("-" * 40)
    
    # 读取README文件
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print("README.md 文件不存在")
    
    print("\n📁 项目文件:")
    files = [
        ("main.py", "主程序"),
        ("config.py", "配置文件"),
        ("database_extractor.py", "数据库提取模块"),
        ("email_sender.py", "邮件发送模块"),
        ("simple_oa_mail.py", "OA邮箱系统"),
        ("schedule_task.py", "定时任务管理"),
        ("使用说明.md", "使用说明"),
        ("Oracle安装配置指南.md", "Oracle配置指南")
    ]
    
    for filename, description in files:
        if os.path.exists(filename):
            print(f"  ✅ {filename} - {description}")
        else:
            print(f"  ❌ {filename} - {description} (文件不存在)")

def main_menu():
    """主菜单"""
    while True:
        print_banner()
        print("\n请选择要执行的操作:")
        print("1.  🔍 测试Oracle数据库连接")
        print("2.  📊 插入测试门诊数据")
        print("3.  📈 提取数据到Excel")
        print("4.  📧 启动OA邮箱系统")
        print("5.  🤖 测试邮件自动化")
        print("6.  🔄 运行完整自动化流程")
        print("7.  ⏰ 设置定时任务")
        print("8.  🧪 运行系统测试")
        print("9.  📋 显示项目信息")
        print("0.  🚪 退出系统")
        
        choice = input("\n请输入选项 (0-9): ").strip()
        
        if choice == "0":
            print("\n👋 感谢使用医院数据自动化系统！")
            break
        elif choice == "1":
            test_oracle_connection()
        elif choice == "2":
            insert_test_data()
        elif choice == "3":
            extract_data_to_excel()
        elif choice == "4":
            start_oa_system()
        elif choice == "5":
            test_email_automation()
        elif choice == "6":
            run_full_automation()
        elif choice == "7":
            setup_schedule_task()
        elif choice == "8":
            run_system_test()
        elif choice == "9":
            show_project_info()
        else:
            print("❌ 无效选项，请重新选择")
        
        if choice != "0":
            input("\n按回车键继续...")

if __name__ == "__main__":
    # 检查依赖
    if not check_requirements():
        print("\n请先安装所需依赖包，然后重新运行此脚本")
        sys.exit(1)
    
    # 显示主菜单
    main_menu() 