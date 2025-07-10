#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医院数据自动化系统 - 清理脚本
清理临时文件、日志文件和缓存
"""

import os
import shutil
import glob
from datetime import datetime, timedelta

def print_banner():
    """打印清理脚本横幅"""
    print("=" * 60)
    print("🧹 医院数据自动化系统 - 清理工具")
    print("=" * 60)
    print(f"清理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def cleanup_logs(days_to_keep=7):
    """清理旧日志文件"""
    print("\n📋 清理日志文件...")
    
    log_files = [
        "main.log",
        "database_extractor.log", 
        "email_sender.log"
    ]
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    cleaned_count = 0
    
    for log_file in log_files:
        if os.path.exists(log_file):
            file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
            if file_time < cutoff_date:
                try:
                    os.remove(log_file)
                    print(f"  🗑️  已删除旧日志: {log_file}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"  ❌ 删除失败 {log_file}: {e}")
            else:
                print(f"  ✅ 保留日志: {log_file}")
    
    print(f"📊 日志清理完成，删除了 {cleaned_count} 个文件")

def cleanup_cache():
    """清理Python缓存文件"""
    print("\n🗂️  清理Python缓存...")
    
    cache_dirs = ["__pycache__", ".pytest_cache"]
    cleaned_count = 0
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"  🗑️  已删除缓存目录: {cache_dir}")
                cleaned_count += 1
            except Exception as e:
                print(f"  ❌ 删除失败 {cache_dir}: {e}")
    
    # 清理.pyc文件
    pyc_files = glob.glob("*.pyc")
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            print(f"  🗑️  已删除缓存文件: {pyc_file}")
            cleaned_count += 1
        except Exception as e:
            print(f"  ❌ 删除失败 {pyc_file}: {e}")
    
    print(f"📊 缓存清理完成，删除了 {cleaned_count} 个项目")

def cleanup_temp_files():
    """清理临时文件"""
    print("\n📄 清理临时文件...")
    
    temp_patterns = [
        "*.tmp",
        "*.temp", 
        "*.bak",
        "*.old"
    ]
    
    cleaned_count = 0
    for pattern in temp_patterns:
        temp_files = glob.glob(pattern)
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
                print(f"  🗑️  已删除临时文件: {temp_file}")
                cleaned_count += 1
            except Exception as e:
                print(f"  ❌ 删除失败 {temp_file}: {e}")
    
    print(f"📊 临时文件清理完成，删除了 {cleaned_count} 个文件")

def cleanup_old_excel_files(days_to_keep=30):
    """清理旧的Excel文件"""
    print("\n📊 清理旧Excel文件...")
    
    excel_files = glob.glob("uploads/*.xlsx")
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    cleaned_count = 0
    
    for excel_file in excel_files:
        file_time = datetime.fromtimestamp(os.path.getmtime(excel_file))
        if file_time < cutoff_date:
            try:
                os.remove(excel_file)
                print(f"  🗑️  已删除旧Excel: {excel_file}")
                cleaned_count += 1
            except Exception as e:
                print(f"  ❌ 删除失败 {excel_file}: {e}")
        else:
            print(f"  ✅ 保留Excel: {excel_file}")
    
    print(f"📊 Excel文件清理完成，删除了 {cleaned_count} 个文件")

def show_disk_usage():
    """显示磁盘使用情况"""
    print("\n💾 磁盘使用情况:")
    
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk("."):
        # 跳过缓存目录
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                total_size += file_size
                file_count += 1
            except:
                pass
    
    # 转换为MB
    total_mb = total_size / (1024 * 1024)
    print(f"  📁 文件总数: {file_count}")
    print(f"  💾 总大小: {total_mb:.2f} MB")

def main():
    """主函数"""
    print_banner()
    
    print("\n请选择清理选项:")
    print("1. 🧹 完整清理 (日志 + 缓存 + 临时文件)")
    print("2. 📋 仅清理日志文件")
    print("3. 🗂️  仅清理缓存文件")
    print("4. 📄 仅清理临时文件")
    print("5. 📊 清理旧Excel文件")
    print("6. 💾 显示磁盘使用情况")
    print("0. 🚪 退出")
    
    choice = input("\n请输入选项 (0-6): ").strip()
    
    if choice == "0":
        print("\n👋 清理工具已退出")
        return
    elif choice == "1":
        cleanup_logs()
        cleanup_cache()
        cleanup_temp_files()
        cleanup_old_excel_files()
    elif choice == "2":
        cleanup_logs()
    elif choice == "3":
        cleanup_cache()
    elif choice == "4":
        cleanup_temp_files()
    elif choice == "5":
        cleanup_old_excel_files()
    elif choice == "6":
        show_disk_usage()
    else:
        print("❌ 无效选项")
        return
    
    print("\n✅ 清理操作完成！")

if __name__ == "__main__":
    main() 