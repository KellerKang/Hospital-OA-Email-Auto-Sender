# -*- coding: utf-8 -*-
"""
简单的OA邮箱系统
使用Flask + SQLite实现
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 数据库初始化
def init_db():
    conn = sqlite3.connect('oa_mail.db')
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    # 创建邮件表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            recipient_id INTEGER,
            subject TEXT NOT NULL,
            body TEXT,
            attachment_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (recipient_id) REFERENCES users (id)
        )
    ''')
    
    # 插入测试用户
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, email) 
        VALUES ('admin', 'admin123', 'admin@oa.com')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, email) 
        VALUES ('user1', 'user123', 'user1@oa.com')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, email) 
        VALUES ('user2', 'user123', 'user2@oa.com')
    ''')
    
    conn.commit()
    conn.close()

# 路由：首页
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('inbox'))

# 路由：登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('oa_mail.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username FROM users WHERE username = ? AND password = ?', 
                      (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('登录成功！', 'success')
            return redirect(url_for('inbox'))
        else:
            flash('用户名或密码错误！', 'error')
    
    return render_template('login.html')

# 路由：收件箱
@app.route('/inbox')
def inbox():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('oa_mail.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.id, e.subject, e.body, e.created_at, u.username as sender
        FROM emails e
        JOIN users u ON e.sender_id = u.id
        WHERE e.recipient_id = ?
        ORDER BY e.created_at DESC
    ''', (session['user_id'],))
    emails = cursor.fetchall()
    conn.close()
    
    return render_template('inbox.html', emails=emails)

# 路由：发件箱
@app.route('/sent')
def sent():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('oa_mail.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.id, e.subject, e.body, e.created_at, u.username as recipient
        FROM emails e
        JOIN users u ON e.recipient_id = u.id
        WHERE e.sender_id = ?
        ORDER BY e.created_at DESC
    ''', (session['user_id'],))
    emails = cursor.fetchall()
    conn.close()
    
    return render_template('sent.html', emails=emails)

# 路由：写邮件
@app.route('/compose', methods=['GET', 'POST'])
def compose():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        body = request.form['body']
        
        # 处理附件
        attachment_path = None
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file.filename:
                filename = f"{uuid.uuid4()}_{file.filename}"
                file.save(os.path.join('uploads', filename))
                attachment_path = filename
        
        conn = sqlite3.connect('oa_mail.db')
        cursor = conn.cursor()
        
        # 获取收件人ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (recipient,))
        recipient_user = cursor.fetchone()
        
        if recipient_user:
            cursor.execute('''
                INSERT INTO emails (sender_id, recipient_id, subject, body, attachment_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (session['user_id'], recipient_user[0], subject, body, attachment_path))
            conn.commit()
            flash('邮件发送成功！', 'success')
        else:
            flash('收件人不存在！', 'error')
        
        conn.close()
        return redirect(url_for('inbox'))
    
    # 获取用户列表
    conn = sqlite3.connect('oa_mail.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE id != ?', (session['user_id'],))
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return render_template('compose.html', users=users)

# 路由：查看邮件
@app.route('/email/<int:email_id>')
def view_email(email_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('oa_mail.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.subject, e.body, e.created_at, e.attachment_path,
               u1.username as sender, u2.username as recipient
        FROM emails e
        JOIN users u1 ON e.sender_id = u1.id
        JOIN users u2 ON e.recipient_id = u2.id
        WHERE e.id = ? AND (e.sender_id = ? OR e.recipient_id = ?)
    ''', (email_id, session['user_id'], session['user_id']))
    email = cursor.fetchone()
    conn.close()
    
    if not email:
        flash('邮件不存在！', 'error')
        return redirect(url_for('inbox'))
    
    return render_template('view_email.html', email=email)

# 路由：登出
@app.route('/logout')
def logout():
    session.clear()
    flash('已登出！', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # 创建uploads目录
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # 初始化数据库
    init_db()
    
    print("OA邮箱系统启动中...")
    print("访问地址: http://localhost:5000")
    print("测试账号:")
    print("  - 用户名: admin, 密码: admin123")
    print("  - 用户名: user1, 密码: user123")
    print("  - 用户名: user2, 密码: user123")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 