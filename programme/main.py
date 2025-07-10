# -*- coding: utf-8 -*-
"""
主程序
整合数据提取和邮件发送功能
"""

import logging
import sys
from datetime import datetime
from database_extractor import DatabaseExtractor
from email_sender import EmailSender
from config import ensure_output_dir

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AutomationSystem:
    """自动化系统主类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.database_extractor = DatabaseExtractor()
        self.email_sender = EmailSender()
        
    def run_full_process(self):
        """运行完整的自动化流程"""
        try:
            self.logger.info("=" * 50)
            self.logger.info("开始执行自动化数据提取与邮件发送流程")
            self.logger.info("=" * 50)
            
            # 步骤1: 数据提取
            self.logger.info("步骤1: 开始数据提取")
            filepath = self.database_extractor.extract_and_save()
            
            if not filepath:
                self.logger.error("数据提取失败，流程终止")
                return False
            
            self.logger.info(f"数据提取成功，文件路径: {filepath}")
            
            # 步骤2: 邮件发送
            self.logger.info("步骤2: 开始邮件发送")
            email_success = self.email_sender.send_email_with_attachment(filepath)
            
            if email_success:
                self.logger.info("邮件发送成功")
                self.logger.info("=" * 50)
                self.logger.info("自动化流程执行完成")
                self.logger.info("=" * 50)
                return True
            else:
                self.logger.error("邮件发送失败")
                return False
                
        except Exception as e:
            self.logger.error(f"自动化流程执行失败: {str(e)}")
            return False
    
    def test_system(self):
        """测试系统各组件"""
        self.logger.info("开始系统测试")
        
        # 测试数据库连接
        self.logger.info("测试数据库连接...")
        if self.database_extractor.test_connection():
            self.logger.info("✓ 数据库连接测试通过")
        else:
            self.logger.error("✗ 数据库连接测试失败")
            return False
        
        # 测试OA系统连接
        self.logger.info("测试OA系统连接...")
        if self.email_sender.test_oa_connection():
            self.logger.info("✓ OA系统连接测试通过")
        else:
            self.logger.error("✗ OA系统连接测试失败")
            return False
        
        self.logger.info("✓ 系统测试完成")
        return True
    
    def run_test_extraction(self):
        """运行测试数据提取"""
        self.logger.info("运行测试数据提取")
        filepath = self.database_extractor.extract_and_save()
        
        if filepath:
            self.logger.info(f"测试数据提取成功: {filepath}")
            return filepath
        else:
            self.logger.error("测试数据提取失败")
            return None

def print_usage():
    """打印使用说明"""
    print("""
自动化数据提取与邮件发送系统

使用方法:
    python main.py [选项]

选项:
    --test        运行系统测试
    --extract     仅运行数据提取测试
    --run         运行完整自动化流程
    --help        显示此帮助信息

示例:
    python main.py --test      # 测试系统连接
    python main.py --extract   # 测试数据提取
    python main.py --run       # 运行完整流程
    """)

def main():
    """主函数"""
    # 确保输出目录存在
    ensure_output_dir()
    
    # 创建自动化系统实例
    system = AutomationSystem()
    
    # 解析命令行参数
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "--test":
        print("运行系统测试...")
        if system.test_system():
            print("系统测试通过")
        else:
            print("系统测试失败")
    
    elif command == "--extract":
        print("运行数据提取测试...")
        filepath = system.run_test_extraction()
        if filepath:
            print(f"数据提取测试成功: {filepath}")
        else:
            print("数据提取测试失败")
    
    elif command == "--run":
        print("运行完整自动化流程...")
        if system.run_full_process():
            print("自动化流程执行成功")
        else:
            print("自动化流程执行失败")
    
    elif command == "--help":
        print_usage()
    
    else:
        print(f"未知命令: {command}")
        print_usage()

if __name__ == "__main__":
    main() 