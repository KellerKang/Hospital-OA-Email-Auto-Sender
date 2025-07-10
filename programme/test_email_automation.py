# -*- coding: utf-8 -*-
"""
测试自动化邮件发送
适配简单的OA邮箱系统
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import EMAIL_CONFIG
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleOAEmailSender:
    """简单的OA邮箱发送器"""
    
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        self.wait = None
        
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
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
            self.driver.get(EMAIL_CONFIG['oa_url'] + '/login')
            self.logger.info(f"访问OA系统: {EMAIL_CONFIG['oa_url']}")
            
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
            
            time.sleep(3)
            
            # 检查是否登录成功
            if "inbox" in self.driver.current_url:
                self.logger.info("OA系统登录成功")
                return True
            else:
                self.logger.error("OA系统登录失败")
                return False
                
        except Exception as e:
            self.logger.error(f"登录OA系统失败: {str(e)}")
            return False
    
    def navigate_to_compose(self):
        """导航到写邮件页面"""
        try:
            self.logger.info("导航到写邮件页面")
            
            # 直接访问写邮件页面
            self.driver.get(EMAIL_CONFIG['oa_url'] + '/compose')
            time.sleep(2)
            
            self.logger.info("成功进入写邮件页面")
            return True
            
        except Exception as e:
            self.logger.error(f"导航到写邮件页面失败: {str(e)}")
            return False
    
    def fill_email_content(self, filepath):
        """填写邮件内容"""
        try:
            self.logger.info("开始填写邮件内容")
            
            # 填写收件人
            recipient_select = self.wait.until(
                EC.presence_of_element_located((By.NAME, "recipient"))
            )
            recipient_select.click()
            # 选择第一个收件人
            recipient_option = self.driver.find_element(By.XPATH, "//option[text()='user1']")
            recipient_option.click()
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

附件为今日门诊数据报表，请查收。

生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

此邮件为系统自动发送，请勿回复。
            """
            body_input.send_keys(body_content)
            self.logger.info("邮件正文填写完成")
            
            # 上传附件
            if filepath:
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
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            send_button.click()
            
            time.sleep(3)
            
            # 检查发送结果
            if "inbox" in self.driver.current_url:
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
            
            # 导航到写邮件页面
            if not self.navigate_to_compose():
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

def main():
    """主函数"""
    print("测试自动化邮件发送")
    print("=" * 50)
    
    # 测试文件路径（使用之前生成的Excel文件）
    test_filepath = "D:/outpatient_records_20250709_160105.xlsx"
    
    sender = SimpleOAEmailSender()
    
    if sender.send_email_with_attachment(test_filepath):
        print("🎉 自动化邮件发送测试成功！")
        print("请检查OA邮箱系统的收件箱查看邮件。")
    else:
        print("❌ 自动化邮件发送测试失败")
        print("请检查OA邮箱系统是否正常运行。")

if __name__ == "__main__":
    main() 