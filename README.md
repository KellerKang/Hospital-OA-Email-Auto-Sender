# Hospital-OA-Email-Auto-Sender# 
🏥 医院数据自动化系统

## 项目简介
这是一个完整的医院数据自动化系统，实现从Oracle数据库提取门诊数据，生成Excel报表，并通过院内OA系统自动发送邮件的全流程自动化。

## 🚀 快速开始

### 方法一：使用启动脚本（推荐）
```bash
# Windows用户直接双击运行
启动系统.bat

# 或者命令行运行
python start_system.py
```

### 方法二：手动运行
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 测试数据库连接
python test_oracle_connection.py

# 3. 插入测试数据
python insert_outpatient_records.py

# 4. 提取数据到Excel
python extract_outpatient_to_excel.py

# 5. 启动OA邮箱系统
python simple_oa_mail.py

# 6. 测试邮件自动化
python test_email_automation.py

# 7. 设置定时任务
python schedule_task.py
```

## 📁 项目结构

```
programme/
├── 📄 核心程序文件
│   ├── main.py                    # 主程序入口
│   ├── config.py                  # 系统配置
│   ├── start_system.py            # 启动脚本
│   └── requirements.txt           # 依赖包列表
│
├── 🗄️ 数据库相关
│   ├── database_extractor.py      # 数据库提取模块
│   ├── extract_outpatient_to_excel.py  # 数据提取到Excel
│   ├── insert_outpatient_records.py    # 插入测试数据
│   ├── test_oracle_connection.py  # 数据库连接测试
│   ├── oracle_troubleshooting.py  # Oracle问题诊断
│   └── tnsnames_template.ora      # Oracle配置文件模板
│
├── 📧 邮件系统
│   ├── email_sender.py            # 邮件发送模块
│   ├── simple_oa_mail.py          # OA邮箱系统
│   └── test_email_automation.py   # 邮件自动化测试
│
├── ⚙️ 系统管理
│   ├── schedule_task.py           # 定时任务管理
│   ├── test_system.py             # 系统功能测试
│   ├── cleanup.py                 # 清理工具
│   └── 清理系统.bat               # 清理工具启动脚本
│
├── 🎨 模板文件
│   └── templates/                 # OA系统HTML模板
│       ├── base.html              # 基础模板
│       ├── login.html             # 登录页面
│       ├── inbox.html             # 收件箱
│       ├── compose.html           # 写邮件
│       ├── sent.html              # 发件箱
│       └── view_email.html        # 邮件查看
│
├── 📊 数据文件
│   ├── uploads/                   # 上传文件目录
│   └── oa_mail.db                 # OA系统数据库
│
├── 📋 日志文件
│   ├── main.log                   # 主程序日志
│   ├── database_extractor.log     # 数据库提取日志
│   └── email_sender.log           # 邮件发送日志
│
├── 📚 文档文件
│   ├── 项目结构说明.md            # 项目结构详细说明
│   ├── 使用说明.md                # 详细使用指南
│   ├── 可行性分析.md              # 项目可行性分析
│   ├── 流程图说明.md              # 系统流程图说明
│   └── Oracle安装配置指南.md      # Oracle配置指南
│
└── 🚀 启动文件
    └── 启动系统.bat               # 一键启动脚本
```

## 🛠️ 系统功能

### ✅ 已实现功能
- [x] Oracle数据库连接和数据提取
- [x] 门诊数据Excel报表生成
- [x] 轻量级OA邮箱系统
- [x] 自动化邮件发送（Selenium）
- [x] Windows计划任务管理
- [x] 完整的错误处理和日志记录
- [x] 模块化设计，易于维护
- [x] 用户友好的操作界面

### 🔄 自动化流程
1. **数据提取** → 从Oracle数据库提取门诊数据
2. **报表生成** → 将数据保存为Excel文件
3. **邮件发送** → 通过OA系统自动发送邮件
4. **定时执行** → 通过Windows计划任务每日自动运行

## 📋 系统要求

### 软件要求
- Python 3.7+
- Oracle Database 11g+
- Windows 10/11

### Python依赖包
```
oracledb>=1.4.0
pandas>=1.5.0
openpyxl>=3.0.0
flask>=2.0.0
selenium>=4.0.0
schedule>=1.2.0
```

## 🔧 配置说明

### 数据库配置
编辑 `config.py` 文件：
```python
# Oracle数据库配置
ORACLE_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'service_name': 'orcl',
    'user': 'your_username',
    'password': 'your_password'
}
```

### 邮件配置
```python
# OA系统配置
OA_CONFIG = {
    'base_url': 'http://localhost:5000',
    'username': 'admin',
    'password': 'admin123'
}
```

## 🧪 测试账号

### OA邮箱系统测试账号
- **管理员**: admin / admin123
- **用户1**: user1 / user123  
- **用户2**: user2 / user123

## 📞 技术支持

### 常见问题
1. **Oracle连接失败** → 运行 `oracle_troubleshooting.py`
2. **依赖包安装失败** → 检查Python版本和网络连接
3. **邮件发送失败** → 检查OA系统是否正常运行

### 日志查看
- 主程序日志: `main.log`
- 数据库日志: `database_extractor.log`
- 邮件日志: `email_sender.log`

## 🧹 系统维护

### 清理工具
```bash
# 运行清理工具
python cleanup.py

# 或双击运行
清理系统.bat
```

### 清理功能
- 清理旧日志文件（7天前）
- 清理Python缓存文件
- 清理临时文件
- 清理旧Excel文件（30天前）

## 📈 性能优化

### 建议配置
- 数据库连接池大小: 10-20
- Excel文件大小限制: 50MB
- 邮件发送间隔: 2-3秒
- 日志保留天数: 7天

## 🔒 安全说明

### 安全措施
- 数据库密码加密存储
- 文件上传类型限制
- SQL注入防护
- XSS攻击防护
- 会话管理

### 注意事项
- 定期备份重要数据
- 及时更新依赖包
- 监控系统日志
- 定期清理临时文件

## 📄 许可证

本项目仅供学习和内部使用，请勿用于商业用途。

---

**开发团队**: 四中心暑期实习项目组  
**最后更新**: 2025年7月  
**版本**: v1.0.0 
