import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException
import json
import os
import datetime
from dotenv import load_dotenv
import argparse
import re
import logging


class Scrapper():
    logger = logging.getLogger('coin_scrapper')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    log_filename = os.path.join(os.getenv("LOGS_PATH", "."), f"Run_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    def __init__(self, task_id, hostname, port):
        from .models import Tasks
        load_dotenv("../.env")
        self.task_id = task_id
        self.task_instance = Tasks.objects.get(id=task_id)
        self.coin = self.task_instance.coin
        self.url = "https://coinmarketcap.com/currencies/" + self.coin + "/"

        self.hostname = hostname
        self.port = port

        self.chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
        self.chrome_binary_path = os.getenv("CHROME_BINARY_PATH")

        self.logger.info("Scrapper initialized for %s" % self.coin)

    def remove_non_ascii_regex(self, text):
        return re.sub(r'[^\x00-\x7F]+|\n|\r', '', text)

    def get_ip(self):
        try:
            self.driver.get("https://ipv4.icanhazip.com/")
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/pre')))
            return element.text
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Unable to get ip address")
            return ""

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.binary_location = self.chrome_binary_path
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--remote-allow-origins=*")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--crash-dumps-dir=/tmp")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

        # chrome_options.add_argument('--proxy-server=http://%s:%s' % (self.hostname, self.port))

        service = Service(self.chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()


    def find_element(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            if element:
                return element.text.strip()
            return ""
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Unable to get %s" % field_name)


    def find_price_change(self, xpath):
        try:
            price_change = self.driver.find_element(By.XPATH, xpath)
            if price_change:
                color = price_change.value_of_css_property('color')
                if color == "red":
                    return "-" + price_change.text.strip().split('%')[0]
                else:
                    return "+" + price_change.text.strip().split('%')[0]
            return None
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Unable to get price change")
            return None


    def extract_contracts(self, data):
        try:
            contract_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-role='body'] a.chain-name")
            for element in contract_elements:
                contract_name = element.text.split(':')[0].strip()
                contract_address = element.get_attribute('href').split('/')[-1]
                data['contracts'].append({
                    "name": contract_name.lower(),
                    "address": contract_address
                })
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Unable to get contracts")
            return None

    def extract_social_and_official_links(self, data):
        social_sites = ['twitter', 'telegram', 'facebook', 'reddit', 'github', 'linkedin', 'medium', 'discord', 'youtube', 'instagram']
        try:
            link_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-role='body'] a[href*='http']")
            for element in link_elements:
                href = element.get_attribute('href')
                name = self.remove_non_ascii_regex(element.text.strip().lower())
                if name not in social_sites:
                    data['official_links'].append({
                        "name": "website",
                        "link": href
                        })
                elif name in social_sites:
                    data['social'].append({
                        "name": name,
                        "url": href
                    })
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Unable to get social and/or official_links")


    def run_scrapper(self):
        self.setup_driver()
        ip_address = self.get_ip()
        try:
            self.driver.get(self.url)
            time.sleep(5)

            data = {
                "ip_address": ip_address,
                "coin_name": self.coin,
                "price": self.find_element('/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/section/div/div[2]/span').split('$')[1],
                "price_change": self.find_price_change('/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/section/div/div[2]/div/div/p'),
                "market_cap": self.find_element('//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dd').split('$')[1],
                "market_cap_rank": self.find_element('//*[@id="section-coin-stats"]/div/dl/div[1]/div[2]').split('#')[1],
                "volume": self.find_element('//*[@id="section-coin-stats"]/div/dl/div[2]/div[1]/dd').split('$')[1],
                "volume_rank": self.find_element('//*[@id="section-coin-stats"]/div/dl/div[2]/div[2]/div').split('#')[1],
                "volume_change": self.find_element('/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[1]/div/dl/div[3]/div/dd').split('%')[0],
                "circulating_supply": self.find_element('//*[@id="section-coin-stats"]/div/dl/div[4]/div/dd').split(' ')[0],
                "total_supply": self.find_element('//*[@id="section-coin-stats"]/div/dl/div[4]/div/dd').split(' ')[0],
                "diluted_market_cap": self.find_element('//*[@id="section-coin-stats"]/div/dl/div[7]/div/dd').split('$')[1],
                "contracts": [],
                "official_links": [],
                "social": [],
                "is_running": False,
                "is_completed": False,
                "selenium_logs": self.logger.handlers[0].baseFilename
            }

            self.extract_contracts(data)
            self.extract_social_and_official_links(data)

            self.logger.info("Successfully scraped data for %s" % self.coin)
            self.logger.info(data)


            from .serializers import TaskUpdateSerializer
            task_serializer = TaskUpdateSerializer(self.task_instance, data=data)
            if task_serializer.is_valid():
                self.logger.info("Saving data for %s" % self.coin)
                task_serializer.save()
            else:
                self.logger.error(task_serializer.errors)
                self.logger.error("Unable to save data for %s" % self.coin)
                self.driver.quit()
                return

            #make is_completed = True
            self.task_instance.is_completed = True
            self.task_instance.save()

            self.logger.info("Successfully updated task %s" % self.task_id)

            self.driver.quit()
            return
        except Exception as e:
            self.logger.error(e)
            self.driver.quit()
            return
