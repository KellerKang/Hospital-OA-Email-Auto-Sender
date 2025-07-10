# -*- coding: utf-8 -*-
"""
提取门诊记录并保存为Excel
"""
import oracledb
import pandas as pd
from config import DATABASE_CONFIG
from datetime import datetime
import os

def main():
    dsn = oracledb.makedsn(
        DATABASE_CONFIG['host'],
        DATABASE_CONFIG['port'],
        service_name=DATABASE_CONFIG['service_name']
    )
    conn = oracledb.connect(
        user=DATABASE_CONFIG['username'],
        password=DATABASE_CONFIG['password'],
        dsn=dsn
    )
    print("✓ 数据库连接成功")
    sql = "SELECT * FROM OUTPATIENT_RECORDS WHERE ROWNUM <= 100 ORDER BY ID"
    df = pd.read_sql(sql, conn)
    conn.close()
    print(f"✓ 成功提取{len(df)}条门诊记录")
    # 生成文件名
    now_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"D:/outpatient_records_{now_str}.xlsx"
    # 确保D盘存在
    if not os.path.exists('D:/'):
        os.makedirs('D:/')
    df.to_excel(filename, index=False)
    print(f"✓ 数据已保存为: {filename}")

if __name__ == "__main__":
    main() 