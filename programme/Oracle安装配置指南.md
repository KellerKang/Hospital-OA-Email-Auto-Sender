# Oracle安装配置指南

## 🚨 ORA-12560错误解决方案

### 错误原因分析
`ORA-12560: TNS:protocol adapter error` 通常由以下原因引起：
1. Oracle Instant Client未正确安装
2. 环境变量配置错误
3. TNSNAMES.ORA文件缺失或配置错误
4. 网络连接问题
5. 服务名或连接字符串错误

## 📥 Oracle Instant Client安装

### 1. 下载Oracle Instant Client
访问Oracle官网下载页面：https://www.oracle.com/database/technologies/instant-client/winx64-downloads.html

**推荐版本**：
- Oracle Instant Client 19.19 (推荐)
- Oracle Instant Client 21.12 (最新)

### 2. 安装步骤

#### 方法一：解压安装（推荐）
```bash
# 1. 创建目录
mkdir C:\oracle

# 2. 解压下载的文件到 C:\oracle\instantclient_19_19

# 3. 将目录添加到系统PATH
# 右键"此电脑" -> 属性 -> 高级系统设置 -> 环境变量
# 在"系统变量"的PATH中添加：C:\oracle\instantclient_19_19
```

#### 方法二：使用安装程序
```bash
# 运行下载的安装程序，按提示完成安装
```

### 3. 验证安装
```bash
# 打开命令提示符，运行：
sqlplus -V
```

## 🔧 环境变量配置

### 必需的环境变量
```bash
# 设置ORACLE_HOME
ORACLE_HOME=C:\oracle\instantclient_19_19

# 设置PATH（添加Oracle目录）
PATH=%PATH%;C:\oracle\instantclient_19_19

# 可选：设置TNS_ADMIN
TNS_ADMIN=C:\oracle\instantclient_19_19\network\admin
```

### 设置方法
1. 右键"此电脑" → 属性
2. 点击"高级系统设置"
3. 点击"环境变量"
4. 在"系统变量"中添加或修改上述变量

## 📝 TNSNAMES.ORA配置

### 1. 创建TNSNAMES.ORA文件
在 `C:\oracle\instantclient_19_19\network\admin\` 目录下创建 `tnsnames.ora` 文件

### 2. 配置示例

#### 使用服务名连接
```ora
ORCL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.100)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
    )
  )
```

#### 使用SID连接
```ora
ORCL_SID =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.100)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SID = orcl)
    )
  )
```

#### 本地连接（Oracle XE）
```ora
LOCAL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = xe)
    )
  )
```

## 🔗 连接字符串格式

### 1. 使用服务名
```bash
sqlplus username/password@host:port/service_name
# 示例：
sqlplus system/password@192.168.1.100:1521/orcl
```

### 2. 使用SID
```bash
sqlplus username/password@host:port:sid
# 示例：
sqlplus system/password@192.168.1.100:1521:orcl
```

### 3. 使用完整连接字符串
```bash
sqlplus username/password@"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=host)(PORT=port))(CONNECT_DATA=(SERVICE_NAME=service_name)))"
# 示例：
sqlplus system/password@"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.1.100)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=orcl)))"
```

## 🧪 测试连接

### 1. 使用SQLPlus测试
```bash
# 测试本地连接
sqlplus system/password@localhost:1521/xe

# 测试远程连接
sqlplus system/password@192.168.1.100:1521/orcl

# 使用TNS别名
sqlplus system/password@ORCL
```

### 2. 使用诊断脚本
```bash
# 运行诊断脚本
python oracle_troubleshooting.py
```

## 🔧 常见问题解决

### 问题1：SQLPlus命令未找到
**解决方案**：
1. 检查Oracle Instant Client是否正确安装
2. 确认PATH环境变量包含Oracle目录
3. 重启命令提示符

### 问题2：ORA-12560错误
**解决方案**：
1. 检查网络连接
2. 确认数据库服务正在运行
3. 验证连接字符串格式
4. 检查防火墙设置

### 问题3：ORA-12541错误
**解决方案**：
1. 确认数据库监听器正在运行
2. 检查端口号是否正确
3. 验证主机地址

### 问题4：ORA-12514错误
**解决方案**：
1. 确认服务名或SID正确
2. 检查数据库是否启动
3. 验证监听器配置

## 📋 配置检查清单

- [ ] Oracle Instant Client已安装
- [ ] 环境变量PATH包含Oracle目录
- [ ] TNSNAMES.ORA文件已创建并配置
- [ ] 网络连接正常
- [ ] 数据库服务正在运行
- [ ] 防火墙允许Oracle端口
- [ ] 用户名密码正确
- [ ] 服务名或SID正确

## 🐍 Python配置

### 1. 安装cx_Oracle
```bash
pip install cx_Oracle
```

### 2. 测试Python连接
```python
import cx_Oracle

# 设置Oracle客户端路径
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_19_19")

# 测试连接
connection = cx_Oracle.connect("username", "password", "host:port/service_name")
print("连接成功！")
connection.close()
```

### 3. 更新项目配置
在 `config.py` 中更新数据库配置：
```python
DATABASE_CONFIG = {
    'host': 'your_oracle_host',        # 数据库主机地址
    'port': 1521,                      # 端口号
    'service_name': 'your_service_name', # 服务名
    'username': 'your_username',       # 用户名
    'password': 'your_password',       # 密码
    'encoding': 'UTF-8'
}
```

## 🚀 快速修复步骤

1. **运行诊断脚本**：
   ```bash
   python oracle_troubleshooting.py
   ```

2. **根据诊断结果修复问题**

3. **测试连接**：
   ```bash
   sqlplus username/password@host:port/service_name
   ```

4. **更新项目配置并测试**：
   ```bash
   python test_system.py
   ```

## 📞 获取帮助

如果问题仍然存在，请：
1. 运行诊断脚本并查看输出
2. 检查Oracle错误日志
3. 确认数据库管理员提供的连接信息
4. 联系技术支持团队 