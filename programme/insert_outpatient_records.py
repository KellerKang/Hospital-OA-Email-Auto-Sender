# -*- coding: utf-8 -*-
"""
自动生成门诊记录并插入Oracle数据库
"""
import oracledb
import random
from datetime import datetime, timedelta
from config import DATABASE_CONFIG

# 随机数据生成函数
NAMES = ["张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十", "钱一", "冯二", "陈三", "褚四", "卫五", "蒋六", "沈七", "韩八", "杨九", "朱十", "秦一", "尤二"]
GENDERS = ["男", "女"]
DEPARTMENTS = ["内科", "外科", "儿科", "妇科", "骨科"]
DIAGNOSES = ["感冒", "高血压", "糖尿病", "骨折", "胃炎", "头痛"]
DOCTORS = ["医生A", "医生B", "医生C", "医生D", "医生E", "医生F", "医生G", "医生H", "医生I", "医生J"]

def random_date():
    days_ago = random.randint(0, 365)
    return (datetime.now() - timedelta(days=days_ago)).date()

def generate_record(i):
    return {
        "ID": i,
        "PATIENT_NAME": random.choice(NAMES) + random.choice(["", "明", "华", "强", "丽", "娜"]),
        "GENDER": random.choice(GENDERS),
        "AGE": random.randint(1, 90),
        "VISIT_DATE": random_date(),
        "DEPARTMENT": random.choice(DEPARTMENTS),
        "DIAGNOSIS": random.choice(DIAGNOSES),
        "DOCTOR": random.choice(DOCTORS)
    }

def create_table(conn):
    sql = '''
    CREATE TABLE OUTPATIENT_RECORDS (
        ID           NUMBER(8) PRIMARY KEY,
        PATIENT_NAME VARCHAR2(20),
        GENDER       VARCHAR2(2),
        AGE          NUMBER(3),
        VISIT_DATE   DATE,
        DEPARTMENT   VARCHAR2(20),
        DIAGNOSIS    VARCHAR2(50),
        DOCTOR       VARCHAR2(20)
    )'''
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            print("✓ OUTPATIENT_RECORDS表创建成功")
    except oracledb.DatabaseError as e:
        if "ORA-00955" in str(e):
            print("表已存在，跳过创建")
        else:
            print(f"建表失败: {e}")
            raise

def insert_records(conn, records):
    sql = '''
    INSERT INTO OUTPATIENT_RECORDS (ID, PATIENT_NAME, GENDER, AGE, VISIT_DATE, DEPARTMENT, DIAGNOSIS, DOCTOR)
    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
    '''
    data = [(
        r["ID"], r["PATIENT_NAME"], r["GENDER"], r["AGE"], r["VISIT_DATE"], r["DEPARTMENT"], r["DIAGNOSIS"], r["DOCTOR"]
    ) for r in records]
    with conn.cursor() as cursor:
        cursor.executemany(sql, data)
    conn.commit()
    print(f"✓ 成功插入{len(records)}条门诊记录")

def main():
    print("连接数据库...")
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
    create_table(conn)
    records = [generate_record(i) for i in range(1, 101)]
    insert_records(conn, records)
    conn.close()
    print("全部完成！")

if __name__ == "__main__":
    main() 