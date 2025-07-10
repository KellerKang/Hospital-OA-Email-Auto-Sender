# -*- coding: utf-8 -*-
"""
Oracle连接测试脚本
用于测试数据库连接
"""

import oracledb
import sys

def test_oracle_connection():
    """测试Oracle连接"""
    print("Oracle连接测试")
    print("=" * 50)
    
    # 测试配置 - 请根据实际情况修改
    test_configs = [
        {
            "name": "本地Oracle 12c",
            "host": "localhost",
            "port": 1521,
            "service_name": "orcl",
            "username": "system",
            "password": "root"
        },
        {
            "name": "本地Oracle 12c (SID)",
            "host": "localhost",
            "port": 1521,
            "service_name": "orcl",
            "username": "system",
            "password": "root"
        }
    ]
    
    for config in test_configs:
        print(f"\n测试配置: {config['name']}")
        print(f"主机: {config['host']}:{config['port']}")
        print(f"服务名: {config['service_name']}")
        print(f"用户名: {config['username']}")
        
        try:
            # 构建连接字符串
            dsn = oracledb.makedsn(
                config['host'],
                config['port'],
                service_name=config['service_name']
            )
            
            # 尝试连接
            connection = oracledb.connect(
                user=config['username'],
                password=config['password'],
                dsn=dsn
            )
            
            print("✓ 连接成功！")
            
            # 测试查询
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()
            print(f"✓ 查询测试成功: {result[0]}")
            
            # 获取数据库版本
            cursor.execute("SELECT * FROM V$VERSION WHERE ROWNUM = 1")
            version = cursor.fetchone()
            print(f"✓ 数据库版本: {version[0]}")
            
            cursor.close()
            connection.close()
            print("✓ 连接已关闭")
            
            return True
            
        except Exception as e:
            print(f"✗ 连接失败: {str(e)}")
            print("请检查:")
            print("1. 数据库服务是否正在运行")
            print("2. 网络连接是否正常")
            print("3. 用户名密码是否正确")
            print("4. 服务名是否正确")
    
    return False

def test_simple_connection():
    """使用简单连接字符串测试"""
    print("\n" + "=" * 50)
    print("简单连接字符串测试")
    print("=" * 50)
    
    # 简单连接字符串示例
    connection_strings = [
        "system/root@localhost:1521/orcl",
        "system/root@localhost:1521:orcl"
    ]
    
    for conn_str in connection_strings:
        print(f"\n测试连接字符串: {conn_str}")
        
        try:
            connection = oracledb.connect(conn_str)
            print("✓ 连接成功！")
            
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()
            print(f"✓ 查询测试成功: {result[0]}")
            
            cursor.close()
            connection.close()
            print("✓ 连接已关闭")
            
            return True
            
        except Exception as e:
            print(f"✗ 连接失败: {str(e)}")
    
    return False

def main():
    """主函数"""
    print("Oracle连接测试工具")
    print("=" * 50)
    
    # 检查oracledb模块
    try:
        import oracledb
        print(f"✓ oracledb模块已安装，版本: {oracledb.version}")
    except ImportError:
        print("✗ oracledb模块未安装")
        print("请运行: pip install oracledb")
        return
    
    # 测试连接
    success = test_oracle_connection()
    
    if not success:
        print("\n尝试简单连接字符串...")
        success = test_simple_connection()
    
    if success:
        print("\n🎉 Oracle连接测试成功！")
        print("您可以更新config.py中的数据库配置并运行自动化系统。")
    else:
        print("\n❌ Oracle连接测试失败")
        print("请检查:")
        print("1. Oracle数据库是否正在运行")
        print("2. 网络连接是否正常")
        print("3. 连接参数是否正确")
        print("4. 防火墙设置")

if __name__ == "__main__":
    main() 