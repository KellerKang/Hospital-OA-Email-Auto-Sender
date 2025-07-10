# -*- coding: utf-8 -*-
"""
数据库数据提取模块
从Oracle数据库提取数据并保存为Excel文件
"""

import oracledb
import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
import logging
from datetime import datetime
from config import DATABASE_CONFIG, QUERY_CONFIG, get_filepath, ensure_output_dir

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_extractor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class DatabaseExtractor:
    """数据库数据提取器"""
    
    def __init__(self):
        self.connection = None
        self.logger = logging.getLogger(__name__)
        
    def connect_database(self):
        """连接Oracle数据库"""
        try:
            # 构建连接字符串
            dsn = oracledb.makedsn(
                DATABASE_CONFIG['host'],
                DATABASE_CONFIG['port'],
                service_name=DATABASE_CONFIG['service_name']
            )
            
            # 建立连接
            self.connection = oracledb.connect(
                user=DATABASE_CONFIG['username'],
                password=DATABASE_CONFIG['password'],
                dsn=dsn,
                encoding=DATABASE_CONFIG['encoding']
            )
            
            self.logger.info("数据库连接成功")
            return True
            
        except Exception as e:
            self.logger.error(f"数据库连接失败: {str(e)}")
            return False
    
    def execute_query(self):
        """执行SQL查询并返回结果"""
        try:
            if not self.connection:
                self.logger.error("数据库未连接")
                return None
                
            cursor = self.connection.cursor()
            cursor.execute(QUERY_CONFIG['sql_query'])
            
            # 获取列名
            columns = [col[0] for col in cursor.description]
            
            # 获取数据
            rows = cursor.fetchall()
            
            cursor.close()
            
            self.logger.info(f"查询执行成功，获取到 {len(rows)} 条记录")
            return columns, rows
            
        except Exception as e:
            self.logger.error(f"查询执行失败: {str(e)}")
            return None
    
    def save_to_excel(self, columns, rows):
        """将数据保存为Excel文件"""
        try:
            # 确保输出目录存在
            ensure_output_dir()
            
            # 获取文件路径
            filepath = get_filepath()
            
            # 创建DataFrame
            df = pd.DataFrame(rows, columns=columns)
            
            # 保存为Excel文件
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=QUERY_CONFIG['sheet_name'], index=False)
                
                # 获取工作表对象
                worksheet = writer.sheets[QUERY_CONFIG['sheet_name']]
                
                # 设置列宽
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                # 设置表头样式
                header_font = Font(bold=True, color="FFFFFF")
                header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                header_alignment = Alignment(horizontal="center", vertical="center")
                
                for cell in worksheet[1]:
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = header_alignment
            
            self.logger.info(f"数据已保存到: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"保存Excel文件失败: {str(e)}")
            return None
    
    def extract_and_save(self):
        """执行完整的数据提取和保存流程"""
        try:
            self.logger.info("开始数据提取流程")
            
            # 连接数据库
            if not self.connect_database():
                return None
            
            # 执行查询
            result = self.execute_query()
            if not result:
                return None
            
            columns, rows = result
            
            # 保存到Excel
            filepath = self.save_to_excel(columns, rows)
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"数据提取流程失败: {str(e)}")
            return None
        
        finally:
            # 关闭数据库连接
            if self.connection:
                self.connection.close()
                self.logger.info("数据库连接已关闭")
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            if self.connect_database():
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1 FROM DUAL")
                result = cursor.fetchone()
                cursor.close()
                self.connection.close()
                
                if result:
                    self.logger.info("数据库连接测试成功")
                    return True
                    
        except Exception as e:
            self.logger.error(f"数据库连接测试失败: {str(e)}")
            
        return False

def main():
    """主函数 - 用于测试"""
    extractor = DatabaseExtractor()
    
    # 测试连接
    if extractor.test_connection():
        print("数据库连接测试通过")
        
        # 执行数据提取
        filepath = extractor.extract_and_save()
        if filepath:
            print(f"数据提取完成，文件保存在: {filepath}")
        else:
            print("数据提取失败")
    else:
        print("数据库连接测试失败")

if __name__ == "__main__":
    main() 