# -*- coding: utf-8 -*-
"""
系统测试脚本
用于验证各个组件是否正常工作
"""

import os
import sys
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_python_environment():
    """测试Python环境"""
    print("=" * 50)
    print("测试Python环境")
    print("=" * 50)
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major >= 3 and python_version.minor >= 8:
        print("✓ Python版本符合要求")
    else:
        print("✗ Python版本过低，需要3.8或更高版本")
        return False
    
    # 检查编码
    print(f"系统编码: {sys.getdefaultencoding()}")
    print("✓ Python环境测试通过")
    return True

def test_dependencies():
    """测试依赖包"""
    print("\n" + "=" * 50)
    print("测试依赖包")
    print("=" * 50)
    
    required_packages = [
        'oracledb',
        'pandas',
        'openpyxl',
        'selenium',
        'webdriver_manager'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} 已安装")
        except ImportError:
            print(f"✗ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少的包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✓ 所有依赖包测试通过")
    return True

def test_config_file():
    """测试配置文件"""
    print("\n" + "=" * 50)
    print("测试配置文件")
    print("=" * 50)
    
    if not os.path.exists('config.py'):
        print("✗ config.py 文件不存在")
        return False
    
    try:
        import config
        print("✓ config.py 文件存在且可导入")
        
        # 检查必要的配置项
        required_configs = [
            'DATABASE_CONFIG',
            'EMAIL_CONFIG',
            'FILE_CONFIG',
            'QUERY_CONFIG',
            'TIME_CONFIG'
        ]
        
        for config_name in required_configs:
            if hasattr(config, config_name):
                print(f"✓ {config_name} 配置存在")
            else:
                print(f"✗ {config_name} 配置缺失")
                return False
        
        print("✓ 配置文件测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 配置文件测试失败: {str(e)}")
        return False

def test_output_directory():
    """测试输出目录"""
    print("\n" + "=" * 50)
    print("测试输出目录")
    print("=" * 50)
    
    try:
        import config
        output_dir = config.FILE_CONFIG['output_dir']
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"✓ 创建输出目录: {output_dir}")
            except Exception as e:
                print(f"✗ 无法创建输出目录: {str(e)}")
                return False
        else:
            print(f"✓ 输出目录已存在: {output_dir}")
        
        # 测试写入权限
        test_file = os.path.join(output_dir, 'test_write.txt')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print("✓ 输出目录写入权限正常")
        except Exception as e:
            print(f"✗ 输出目录写入权限不足: {str(e)}")
            return False
        
        print("✓ 输出目录测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 输出目录测试失败: {str(e)}")
        return False

def test_database_connection():
    """测试数据库连接"""
    print("\n" + "=" * 50)
    print("测试数据库连接")
    print("=" * 50)
    
    try:
        from database_extractor import DatabaseExtractor
        
        extractor = DatabaseExtractor()
        if extractor.test_connection():
            print("✓ 数据库连接测试通过")
            return True
        else:
            print("✗ 数据库连接测试失败")
            return False
            
    except Exception as e:
        print(f"✗ 数据库连接测试异常: {str(e)}")
        return False

def test_oa_connection():
    """测试OA系统连接"""
    print("\n" + "=" * 50)
    print("测试OA系统连接")
    print("=" * 50)
    
    try:
        from email_sender import EmailSender
        
        sender = EmailSender()
        if sender.test_oa_connection():
            print("✓ OA系统连接测试通过")
            return True
        else:
            print("✗ OA系统连接测试失败")
            return False
            
    except Exception as e:
        print(f"✗ OA系统连接测试异常: {str(e)}")
        return False

def test_excel_generation():
    """测试Excel文件生成"""
    print("\n" + "=" * 50)
    print("测试Excel文件生成")
    print("=" * 50)
    
    try:
        import pandas as pd
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill
        
        # 创建测试数据
        test_data = {
            '列1': ['数据1', '数据2', '数据3'],
            '列2': [100, 200, 300],
            '列3': ['A', 'B', 'C']
        }
        
        df = pd.DataFrame(test_data)
        
        # 保存为Excel文件
        test_file = 'test_excel.xlsx'
        with pd.ExcelWriter(test_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='测试', index=False)
            
            # 获取工作表对象
            worksheet = writer.sheets['测试']
            
            # 设置表头样式
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
        
        # 检查文件是否创建成功
        if os.path.exists(test_file):
            print("✓ Excel文件生成成功")
            os.remove(test_file)  # 清理测试文件
            print("✓ Excel文件测试通过")
            return True
        else:
            print("✗ Excel文件生成失败")
            return False
            
    except Exception as e:
        print(f"✗ Excel文件测试异常: {str(e)}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("开始系统测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Python环境", test_python_environment),
        ("依赖包", test_dependencies),
        ("配置文件", test_config_file),
        ("输出目录", test_output_directory),
        ("Excel生成", test_excel_generation),
        ("数据库连接", test_database_connection),
        ("OA系统连接", test_oa_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {str(e)}")
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    print(f"总测试数: {total}")
    print(f"通过测试: {passed}")
    print(f"失败测试: {total - passed}")
    print(f"通过率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常运行。")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关配置。")
        return False

if __name__ == "__main__":
    run_all_tests() 