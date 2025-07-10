# -*- coding: utf-8 -*-
"""
Windows计划任务设置脚本
用于设置每日自动运行数据提取和邮件发送任务
"""

import os
import subprocess
import sys
from datetime import datetime
from config import TIME_CONFIG

class TaskScheduler:
    """Windows计划任务管理器"""
    
    def __init__(self):
        self.task_name = "数据提取与邮件发送任务"
        self.task_description = "每日自动从Oracle数据库提取数据并发送邮件"
        self.script_path = os.path.abspath("main.py")
        self.python_path = sys.executable
        
    def create_task(self):
        """创建Windows计划任务"""
        try:
            print("开始创建Windows计划任务...")
            
            # 构建schtasks命令
            command = [
                "schtasks", "/create", "/tn", self.task_name,
                "/tr", f'"{self.python_path}" "{self.script_path}" --run',
                "/sc", "daily",
                "/st", TIME_CONFIG['schedule_time'],
                "/f"  # 强制创建，如果任务已存在则覆盖
            ]
            
            print(f"执行命令: {' '.join(command)}")
            
            # 执行命令
            result = subprocess.run(command, capture_output=True, text=True, encoding='gbk')
            
            if result.returncode == 0:
                print("✓ Windows计划任务创建成功")
                print(f"任务名称: {self.task_name}")
                print(f"执行时间: 每日 {TIME_CONFIG['schedule_time']}")
                print(f"执行脚本: {self.script_path}")
                return True
            else:
                print("✗ Windows计划任务创建失败")
                print(f"错误信息: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"创建计划任务时发生错误: {str(e)}")
            return False
    
    def delete_task(self):
        """删除Windows计划任务"""
        try:
            print("开始删除Windows计划任务...")
            
            command = ["schtasks", "/delete", "/tn", self.task_name, "/f"]
            
            print(f"执行命令: {' '.join(command)}")
            
            result = subprocess.run(command, capture_output=True, text=True, encoding='gbk')
            
            if result.returncode == 0:
                print("✓ Windows计划任务删除成功")
                return True
            else:
                print("✗ Windows计划任务删除失败")
                print(f"错误信息: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"删除计划任务时发生错误: {str(e)}")
            return False
    
    def query_task(self):
        """查询Windows计划任务状态"""
        try:
            print("查询Windows计划任务状态...")
            
            command = ["schtasks", "/query", "/tn", self.task_name, "/fo", "table"]
            
            result = subprocess.run(command, capture_output=True, text=True, encoding='gbk')
            
            if result.returncode == 0:
                print("✓ 计划任务查询成功")
                print("任务详情:")
                print(result.stdout)
                return True
            else:
                print("✗ 计划任务查询失败")
                print(f"错误信息: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"查询计划任务时发生错误: {str(e)}")
            return False
    
    def run_task_now(self):
        """立即运行计划任务"""
        try:
            print("立即运行Windows计划任务...")
            
            command = ["schtasks", "/run", "/tn", self.task_name]
            
            result = subprocess.run(command, capture_output=True, text=True, encoding='gbk')
            
            if result.returncode == 0:
                print("✓ 计划任务启动成功")
                return True
            else:
                print("✗ 计划任务启动失败")
                print(f"错误信息: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"运行计划任务时发生错误: {str(e)}")
            return False
    
    def list_all_tasks(self):
        """列出所有计划任务"""
        try:
            print("列出所有Windows计划任务...")
            
            command = ["schtasks", "/query", "/fo", "table"]
            
            result = subprocess.run(command, capture_output=True, text=True, encoding='gbk')
            
            if result.returncode == 0:
                print("所有计划任务:")
                print(result.stdout)
                return True
            else:
                print("查询计划任务列表失败")
                print(f"错误信息: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"列出计划任务时发生错误: {str(e)}")
            return False

def print_usage():
    """打印使用说明"""
    print("""
Windows计划任务管理工具

使用方法:
    python schedule_task.py [选项]

选项:
    --create      创建计划任务
    --delete      删除计划任务
    --query       查询任务状态
    --run         立即运行任务
    --list        列出所有任务
    --help        显示此帮助信息

示例:
    python schedule_task.py --create   # 创建每日自动运行任务
    python schedule_task.py --query    # 查询任务状态
    python schedule_task.py --run      # 立即运行任务
    """)

def main():
    """主函数"""
    scheduler = TaskScheduler()
    
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "--create":
        scheduler.create_task()
    
    elif command == "--delete":
        scheduler.delete_task()
    
    elif command == "--query":
        scheduler.query_task()
    
    elif command == "--run":
        scheduler.run_task_now()
    
    elif command == "--list":
        scheduler.list_all_tasks()
    
    elif command == "--help":
        print_usage()
    
    else:
        print(f"未知命令: {command}")
        print_usage()

if __name__ == "__main__":
    main() 