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

def remove_non_ascii_regex(text):
    return re.sub(r'[^\x00-\x7F]+|\n|\r', '', text)


load_dotenv("../.env")

print(os.getenv("CHROMEDRIVER_PATH"))
print(os.getenv("CHROME_BINARY_PATH"))


parser = argparse.ArgumentParser()

parser.add_argument("-n", "--hostname", help = "hostname", required = True)
parser.add_argument("-p", "--port", help = "port", required = True)
parser.add_argument("-c", "--coin", help = "coin_name", required = True)
parser.add_argument("-t", "--test", help = "test", required = False, action='store_true', default=False)

# Read arguments from command line
args = parser.parse_args()

chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
chrome_binary_path = os.getenv("CHROME_BINARY_PATH")

chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
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

print("Proxy: %s:%s" % (args.hostname, args.port))
#chrome_options.add_argument('--proxy-server=http://%s:%s' % (args.hostname, args.port))

url = "https://coinmarketcap.com/currencies/" + args.coin.strip() + "/"

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()


def switchToNewTab(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

def switchToTab(driver, tab):
    driver.switch_to.window(driver.window_handles[tab])

def get_ip(driver):
    driver.get("https://ipv4.icanhazip.com/")
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/pre')))
        return element.text
    except Exception as e:
        print("Unable to get ip address")
        return ""

def find_element(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        if element:
            return element.text.strip()
        return ""
    except Exception as e:
        print("Unable to get %s" % field_name)


def find_price_change(driver, xpath):
    try:
        price_change = driver.find_element(By.XPATH, xpath)
        if price_change:
            color = price_change.value_of_css_property('color')
            if color == "red":
                return "-" + price_change.text.strip().split('%')[0]
            else:
                return "+" + price_change.text.strip().split('%')[0]
        return None
    except Exception as e:
        print("Unable to get price_change")

def extract_contracts(driver, data):
    try:
        contract_elements = driver.find_elements(By.CSS_SELECTOR, "[data-role='body'] a.chain-name")
        for element in contract_elements:
            contract_name = element.text.split(':')[0].strip()
            contract_address = element.get_attribute('href').split('/')[-1]
            data['contracts'].append({
                "name": contract_name.lower(),
                "address": contract_address
            })
    except Exception as e:
        print(e)
        print("Unable to get contracts")
        return None

social_sites = ['twitter', 'telegram', 'facebook', 'reddit', 'github', 'linkedin', 'medium', 'discord', 'youtube', 'instagram']
def extract_social_and_official_links(driver, data):
    try:
        link_elements = driver.find_elements(By.CSS_SELECTOR, "[data-role='body'] a[href*='http']")
        for element in link_elements:
            href = element.get_attribute('href')
            name = remove_non_ascii_regex(element.text.strip().lower())
            print("name:", name)
            if name not in social_sites:
                data['official_links'].append({
                    "name": "website",
                    "link": href
                    })
            elif name in social_sites:
                data['socials'].append({
                    "name": name,
                    "url": href
                })
    except Exception as e:
        print(e)
        print("Unable to get socials and official_links")


if args.test:
    print("Test mode")
    get_ip(driver)
    driver.quit()
    exit(0)
else:
    ip_address = get_ip(driver)

    try:
        driver.get(url)
        time.sleep(5)

        data = {
            "ip": ip_address,
            "coin_name": args.coin,
            "price": find_element(driver, '/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/section/div/div[2]/span').split('$')[1],
            "price_change": find_price_change(driver, '/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/section/div/div[2]/div/div/p'),
            "market_cap": find_element(driver, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dd').split('$')[1],
            "market_cap_rank": find_element(driver, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[2]').split('#')[1],
            "volume": find_element(driver, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[1]/dd').split('$')[1],
            "volume_rank": find_element(driver, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[2]/div').split('#')[1],
            "volume_change": find_element(driver, '/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[1]/div/dl/div[3]/div/dd').split('%')[0],
            "circulating_supply": find_element(driver, '//*[@id="section-coin-stats"]/div/dl/div[4]/div/dd').split(' ')[0],
            "total_supply": find_element(driver, '//*[@id="section-coin-stats"]/div/dl/div[4]/div/dd').split(' ')[0],
            "diluted_market_cap": find_element(driver, '//*[@id="section-coin-stats"]/div/dl/div[7]/div/dd').split('$')[1],
            "contracts": [],
            "official_links": [],
            "socials": []
        }

        extract_contracts(driver, data)
        extract_social_and_official_links(driver, data)

        print(data)

        # save data to db using serializer
        # data["is_running"] = False
        # data["is_completed"] = True
        #

        driver.quit()
        exit(0)
    except Exception as e:
        print(e)
        driver.quit()
        exit(1)
