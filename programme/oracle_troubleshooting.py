# -*- coding: utf-8 -*-
"""
Oracle连接问题诊断脚本
用于诊断和解决ORA-12560等连接问题
"""

import os
import sys
import subprocess
import platform

def check_oracle_installation():
    """检查Oracle安装情况"""
    print("=" * 60)
    print("Oracle安装诊断")
    print("=" * 60)
    
    # 检查环境变量
    oracle_home = os.environ.get('ORACLE_HOME')
    oracle_sid = os.environ.get('ORACLE_SID')
    path = os.environ.get('PATH', '')
    
    print(f"ORACLE_HOME: {oracle_home or '未设置'}")
    print(f"ORACLE_SID: {oracle_sid or '未设置'}")
    
    # 检查PATH中的Oracle路径
    oracle_paths = [p for p in path.split(os.pathsep) if 'oracle' in p.lower()]
    if oracle_paths:
        print("PATH中的Oracle路径:")
        for p in oracle_paths:
            print(f"  - {p}")
    else:
        print("PATH中未找到Oracle路径")
    
    # 检查常见Oracle安装位置
    common_paths = [
        r"C:\oracle\product\19c\client_1",
        r"C:\oracle\product\12c\client_1",
        r"C:\oracle\instantclient_19_19",
        r"C:\oracle\instantclient_21_12",
        r"C:\oracle\instantclient_21_11",
        r"C:\oracle\instantclient_21_10",
        r"C:\oracle\instantclient_21_9",
        r"C:\oracle\instantclient_21_8",
        r"C:\oracle\instantclient_21_7",
        r"C:\oracle\instantclient_21_6",
        r"C:\oracle\instantclient_21_5",
        r"C:\oracle\instantclient_21_4",
        r"C:\oracle\instantclient_21_3",
        r"C:\oracle\instantclient_21_2",
        r"C:\oracle\instantclient_21_1",
        r"C:\oracle\instantclient_20_3",
        r"C:\oracle\instantclient_20_2",
        r"C:\oracle\instantclient_20_1",
        r"C:\oracle\instantclient_19_19",
        r"C:\oracle\instantclient_19_18",
        r"C:\oracle\instantclient_19_17",
        r"C:\oracle\instantclient_19_16",
        r"C:\oracle\instantclient_19_15",
        r"C:\oracle\instantclient_19_14",
        r"C:\oracle\instantclient_19_13",
        r"C:\oracle\instantclient_19_12",
        r"C:\oracle\instantclient_19_11",
        r"C:\oracle\instantclient_19_10",
        r"C:\oracle\instantclient_19_9",
        r"C:\oracle\instantclient_19_8",
        r"C:\oracle\instantclient_19_7",
        r"C:\oracle\instantclient_19_6",
        r"C:\oracle\instantclient_19_5",
        r"C:\oracle\instantclient_19_4",
        r"C:\oracle\instantclient_19_3",
        r"C:\oracle\instantclient_19_2",
        r"C:\oracle\instantclient_19_1",
        r"C:\oracle\instantclient_18_5",
        r"C:\oracle\instantclient_18_4",
        r"C:\oracle\instantclient_18_3",
        r"C:\oracle\instantclient_18_2",
        r"C:\oracle\instantclient_18_1",
        r"C:\oracle\instantclient_12_2",
        r"C:\oracle\instantclient_12_1",
        r"C:\oracle\instantclient_11_2",
        r"C:\oracle\instantclient_11_1",
    ]
    
    found_oracle = []
    for path in common_paths:
        if os.path.exists(path):
            found_oracle.append(path)
            print(f"✓ 找到Oracle安装: {path}")
    
    if not found_oracle:
        print("✗ 未找到Oracle安装，请先安装Oracle Instant Client")
        return False
    
    return True

def check_tnsnames():
    """检查TNSNAMES.ORA文件"""
    print("\n" + "=" * 60)
    print("TNSNAMES.ORA文件检查")
    print("=" * 60)
    
    # 查找tnsnames.ora文件
    tnsnames_locations = [
        os.path.join(os.environ.get('ORACLE_HOME', ''), 'network', 'admin', 'tnsnames.ora'),
        os.path.join(os.environ.get('TNS_ADMIN', ''), 'tnsnames.ora'),
        r"C:\oracle\product\19c\client_1\network\admin\tnsnames.ora",
        r"C:\oracle\product\12c\client_1\network\admin\tnsnames.ora",
        r"C:\oracle\instantclient_19_19\network\admin\tnsnames.ora",
        r"C:\oracle\instantclient_21_12\network\admin\tnsnames.ora",
    ]
    
    tnsnames_found = False
    for tnsnames_path in tnsnames_locations:
        if os.path.exists(tnsnames_path):
            print(f"✓ 找到tnsnames.ora: {tnsnames_path}")
            tnsnames_found = True
            
            # 读取文件内容
            try:
                with open(tnsnames_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("文件内容预览:")
                    print(content[:500] + "..." if len(content) > 500 else content)
            except Exception as e:
                print(f"读取文件失败: {e}")
    
    if not tnsnames_found:
        print("✗ 未找到tnsnames.ora文件")
        print("建议: 创建tnsnames.ora文件或使用完整连接字符串")
    
    return tnsnames_found

def test_sqlplus_connection():
    """测试SQLPlus连接"""
    print("\n" + "=" * 60)
    print("SQLPlus连接测试")
    print("=" * 60)
    
    # 检查sqlplus是否可用
    try:
        result = subprocess.run(['sqlplus', '-V'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ SQLPlus可用")
            print(f"版本信息: {result.stdout.strip()}")
        else:
            print("✗ SQLPlus不可用")
            return False
    except FileNotFoundError:
        print("✗ SQLPlus未找到，请检查Oracle安装")
        return False
    
    return True

def generate_connection_examples():
    """生成连接示例"""
    print("\n" + "=" * 60)
    print("连接字符串示例")
    print("=" * 60)
    
    examples = [
        {
            "name": "使用服务名连接",
            "format": "username/password@host:port/service_name",
            "example": "system/password@192.168.1.100:1521/orcl"
        },
        {
            "name": "使用SID连接",
            "format": "username/password@host:port:sid",
            "example": "system/password@192.168.1.100:1521:orcl"
        },
        {
            "name": "使用完整连接字符串",
            "format": "username/password@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=host)(PORT=port))(CONNECT_DATA=(SERVICE_NAME=service_name)))",
            "example": "system/password@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.1.100)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=orcl)))"
        }
    ]
    
    for example in examples:
        print(f"\n{example['name']}:")
        print(f"格式: {example['format']}")
        print(f"示例: {example['example']}")

def create_tnsnames_template():
    """创建tnsnames.ora模板"""
    print("\n" + "=" * 60)
    print("TNSNAMES.ORA模板")
    print("=" * 60)
    
    template = """
# TNSNAMES.ORA 模板文件
# 将此文件保存到 Oracle安装目录/network/admin/tnsnames.ora

# 示例1: 使用服务名
ORCL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.100)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
    )
  )

# 示例2: 使用SID
ORCL_SID =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.100)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SID = orcl)
    )
  )

# 示例3: 本地连接
LOCAL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = xe)
    )
  )
"""
    
    print("TNSNAMES.ORA模板内容:")
    print(template)
    
    # 保存模板文件
    try:
        with open('tnsnames_template.ora', 'w', encoding='utf-8') as f:
            f.write(template)
        print("\n✓ 模板文件已保存为: tnsnames_template.ora")
    except Exception as e:
        print(f"\n✗ 保存模板文件失败: {e}")

def check_python_oracle():
    """检查Python Oracle连接"""
    print("\n" + "=" * 60)
    print("Python Oracle连接检查")
    print("=" * 60)
    
    try:
        import oracledb
        print("✓ oracledb模块已安装")
        print(f"版本: {oracledb.version}")
        
        # 检查Oracle客户端版本
        try:
            client_version = oracledb.clientversion()
            print(f"Oracle客户端版本: {client_version}")
        except Exception as e:
            print(f"无法获取客户端版本: {e}")
        
        return True
        
    except ImportError:
        print("✗ oracledb模块未安装")
        print("请运行: pip install oracledb")
        return False
    except Exception as e:
        print(f"✗ oracledb检查失败: {e}")
        return False

def main():
    """主函数"""
    print("Oracle连接问题诊断工具")
    print("=" * 60)
    
    # 检查Oracle安装
    oracle_ok = check_oracle_installation()
    
    # 检查tnsnames.ora
    tnsnames_ok = check_tnsnames()
    
    # 测试SQLPlus
    sqlplus_ok = test_sqlplus_connection()
    
    # 检查Python Oracle
    python_ok = check_python_oracle()
    
    # 生成连接示例
    generate_connection_examples()
    
    # 创建模板
    create_tnsnames_template()
    
    # 总结
    print("\n" + "=" * 60)
    print("诊断总结")
    print("=" * 60)
    
    if oracle_ok and sqlplus_ok and python_ok:
        print("✓ 基本环境正常")
        if not tnsnames_ok:
            print("⚠️  建议: 配置tnsnames.ora文件或使用完整连接字符串")
    else:
        print("✗ 环境配置有问题，请根据上述建议进行修复")
    
    print("\n常见解决方案:")
    print("1. 确保Oracle Instant Client已正确安装并添加到PATH")
    print("2. 配置正确的tnsnames.ora文件")
    print("3. 使用完整的连接字符串而不是服务名")
    print("4. 检查网络连接和防火墙设置")
    print("5. 确认数据库服务正在运行")

if __name__ == "__main__":
    main() 