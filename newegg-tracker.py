import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
import json
from datetime import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class NeweggPriceTracker:
    def __init__(self, url, target_price):
        self.url = url
        self.target_price = target_price
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Get email configuration from environment variables
        self.email_config = {
            'sender_email': os.getenv('SENDER_EMAIL'),
            'app_password': os.getenv('EMAIL_APP_PASSWORD'),
            'receiver_email': os.getenv('RECEIVER_EMAIL')
        }
        
        # Verify all required environment variables are present
        if not all(self.email_config.values()):
            raise ValueError("Missing required environment variables. Please check your .env file.")
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')
        return webdriver.Chrome(options=chrome_options)
    
    def get_price(self):
        try:
            driver = self.setup_driver()
            driver.get(self.url)
            
            wait = WebDriverWait(driver, 10)
            price_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.price-current'))
            )
            
            price_text = price_element.text
            driver.quit()
            
            price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
            if price_match:
                return float(price_match.group(1).replace(',', ''))
            return None
            
        except Exception as e:
            print(f"Error getting price: {str(e)}")
            return None
        
    def send_email_alert(self, current_price):
        try:
            subject = f"Price Alert: Ryzen 7 7800X3D now ${current_price:.2f}"
            body = f"""
            The price has dropped below your target of ${self.target_price:.2f}!
            
            Current price: ${current_price:.2f}
            Product URL: {self.url}
            
            Time of alert: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['receiver_email']
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(
                    self.email_config['sender_email'],
                    self.email_config['app_password']
                )
                server.send_message(msg)
                
            print(f"Price alert email sent successfully!")
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    def track_price(self, check_interval=3600):
        print(f"Starting price tracker for {self.url}")
        print(f"Target price: ${self.target_price:.2f}")
        
        while True:
            current_price = self.get_price()
            
            if current_price is not None:
                print(f"Current price: ${current_price:.2f}")
                
                if current_price <= self.target_price:
                    print("Price is below target! Sending alert...")
                    self.send_email_alert(current_price)
            
            time.sleep(check_interval)

if __name__ == "__main__":
    url = "https://www.newegg.com/amd-ryzen-7-7800x3d-ryzen-7-7000-series-raphael-zen-4-socket-am5/p/N82E16819113793"
    target_price = 400.00  # Set your desired target price
    
    tracker = NeweggPriceTracker(url, target_price)
    tracker.track_price()

############################################################################################
