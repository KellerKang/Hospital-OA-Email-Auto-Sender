# -*- coding: utf-8 -*-
"""
邮件发送模块
自动登录OA系统并发送邮件
"""

import time
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import EMAIL_CONFIG, get_filename

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class EmailSender:
    """邮件发送器"""
    
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        self.wait = None
        
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        try:
            # Chrome选项配置
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # 可选：无头模式（不显示浏览器窗口）
            # chrome_options.add_argument('--headless')
            
            # 自动下载并设置ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            # 创建WebDriver实例
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            
            self.logger.info("Chrome浏览器驱动设置成功")
            return True
            
        except Exception as e:
            self.logger.error(f"浏览器驱动设置失败: {str(e)}")
            return False
    
    def login_oa_system(self):
        """登录OA系统"""
        try:
            self.logger.info("开始登录OA系统")
            
            # 访问OA系统登录页面
            self.driver.get(EMAIL_CONFIG['oa_url'])
            self.logger.info(f"访问OA系统: {EMAIL_CONFIG['oa_url']}")
            
            # 等待页面加载
            time.sleep(3)
            
            # 查找并填写用户名
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.clear()
            username_input.send_keys(EMAIL_CONFIG['username'])
            self.logger.info("用户名填写完成")
            
            # 查找并填写密码
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(EMAIL_CONFIG['password'])
            self.logger.info("密码填写完成")
            
            # 点击登录按钮
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            self.logger.info("点击登录按钮")
            
            # 等待登录成功
            time.sleep(5)
            
            # 检查是否登录成功（根据实际OA系统调整）
            if "dashboard" in self.driver.current_url or "main" in self.driver.current_url:
                self.logger.info("OA系统登录成功")
                return True
            else:
                self.logger.error("OA系统登录失败")
                return False
                
        except Exception as e:
            self.logger.error(f"登录OA系统失败: {str(e)}")
            return False
    
    def navigate_to_email(self):
        """导航到邮件发送页面"""
        try:
            self.logger.info("导航到邮件发送页面")
            
            # 查找并点击邮件菜单（根据实际OA系统调整）
            email_menu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'邮件') or contains(text(),'Email')]"))
            )
            email_menu.click()
            time.sleep(2)
            
            # 查找并点击写邮件按钮
            compose_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'写邮件') or contains(text(),'Compose')]"))
            )
            compose_button.click()
            time.sleep(2)
            
            self.logger.info("成功进入邮件编写页面")
            return True
            
        except Exception as e:
            self.logger.error(f"导航到邮件页面失败: {str(e)}")
            return False
    
    def fill_email_content(self, filepath):
        """填写邮件内容"""
        try:
            self.logger.info("开始填写邮件内容")
            
            # 填写收件人
            recipients_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "to"))
            )
            recipients_input.clear()
            recipients_input.send_keys(", ".join(EMAIL_CONFIG['recipients']))
            self.logger.info("收件人填写完成")
            
            # 填写邮件主题
            subject_input = self.driver.find_element(By.NAME, "subject")
            subject_input.clear()
            current_date = datetime.now().strftime('%Y年%m月%d日')
            subject = f"{EMAIL_CONFIG['subject_prefix']} - {current_date}"
            subject_input.send_keys(subject)
            self.logger.info("邮件主题填写完成")
            
            # 填写邮件正文
            body_input = self.driver.find_element(By.NAME, "body")
            body_input.clear()
            body_content = f"""
            您好！
            
            附件为今日数据报表，请查收。
            
            生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
            
            此邮件为系统自动发送，请勿回复。
            """
            body_input.send_keys(body_content)
            self.logger.info("邮件正文填写完成")
            
            # 上传附件
            if filepath and os.path.exists(filepath):
                file_input = self.driver.find_element(By.NAME, "attachment")
                file_input.send_keys(filepath)
                self.logger.info(f"附件上传完成: {filepath}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"填写邮件内容失败: {str(e)}")
            return False
    
    def send_email(self):
        """发送邮件"""
        try:
            self.logger.info("开始发送邮件")
            
            # 点击发送按钮
            send_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'发送') or contains(text(),'Send')]"))
            )
            send_button.click()
            
            # 等待发送完成
            time.sleep(5)
            
            # 检查发送结果（根据实际OA系统调整）
            success_message = self.driver.find_elements(By.XPATH, "//div[contains(text(),'发送成功') or contains(text(),'Success')]")
            
            if success_message:
                self.logger.info("邮件发送成功")
                return True
            else:
                self.logger.error("邮件发送失败")
                return False
                
        except Exception as e:
            self.logger.error(f"发送邮件失败: {str(e)}")
            return False
    
    def send_email_with_attachment(self, filepath):
        """完整的邮件发送流程"""
        try:
            self.logger.info("开始邮件发送流程")
            
            # 设置浏览器驱动
            if not self.setup_driver():
                return False
            
            # 登录OA系统
            if not self.login_oa_system():
                return False
            
            # 导航到邮件页面
            if not self.navigate_to_email():
                return False
            
            # 填写邮件内容
            if not self.fill_email_content(filepath):
                return False
            
            # 发送邮件
            if not self.send_email():
                return False
            
            self.logger.info("邮件发送流程完成")
            return True
            
        except Exception as e:
            self.logger.error(f"邮件发送流程失败: {str(e)}")
            return False
        
        finally:
            # 关闭浏览器
            if self.driver:
                self.driver.quit()
                self.logger.info("浏览器已关闭")
    
    def test_oa_connection(self):
        """测试OA系统连接"""
        try:
            if not self.setup_driver():
                return False
            
            self.driver.get(EMAIL_CONFIG['oa_url'])
            time.sleep(3)
            
            if "login" in self.driver.current_url or "登录" in self.driver.page_source:
                self.logger.info("OA系统连接测试成功")
                return True
            else:
                self.logger.error("OA系统连接测试失败")
                return False
                
        except Exception as e:
            self.logger.error(f"OA系统连接测试失败: {str(e)}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()

def main():
    """主函数 - 用于测试"""
    sender = EmailSender()
    
    # 测试OA系统连接
    if sender.test_oa_connection():
        print("OA系统连接测试通过")
        
        # 测试邮件发送（需要提供文件路径）
        test_filepath = "D:\\data_reports\\test_file.xlsx"
        if os.path.exists(test_filepath):
            if sender.send_email_with_attachment(test_filepath):
                print("邮件发送测试成功")
            else:
                print("邮件发送测试失败")
        else:
            print(f"测试文件不存在: {test_filepath}")
    else:
        print("OA系统连接测试失败")

if __name__ == "__main__":
    main() 