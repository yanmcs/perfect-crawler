'''
We will create a crawler that will be able to get any website HTML code
first we will try to use requests library to get the HTML code using requests and cfscrape
if it all fails we will use chrome, firefox or brave to get the HTML code
'''
import time
import json
# requests session
import cfscrape
# selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# webdriver options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager


class Crawler:
    def __init__(self,
                browser="chrome",
                always_use_browser=False,
                headless=True):
        '''
        :param url (string): url to get the HTML code from
        :param browser (string): standard is "brave", it is the browser to use to get the HTML code, can be: "chrome", "firefox" or "brave"
        :param always_use_browser (bool): if True we will always use browser to get the HTML code
        :param headless (bool): if True we will use headless browser
        '''

        # cfscrape works better than requests
        self.cfscraper = cfscrape.create_scraper()
        self.always_use_browser = always_use_browser

        # setting browser options
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox") # linux only
            options.add_argument("--disable-dev-shm-usage") # linux only
            options.add_argument("--disable-setuid-sandbox") # linux only
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            capabilities = DesiredCapabilities.CHROME
            capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
            if headless:
                options.add_argument("--headless")
            self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options, desired_capabilities=capabilities)
        elif browser == "firefox":
            options = FirefoxOptions()
            capabilities = DesiredCapabilities.FIREFOX
            capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
            if headless:
                options.add_argument("--headless")
            self.browser = webdriver.Firefox(GeckoDriverManager().install(), options=options, desired_capabilities=capabilities)
        elif browser == "brave":
            options = ChromeOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox") # linux only
            options.add_argument("--disable-dev-shm-usage") # linux only
            options.add_argument("--disable-setuid-sandbox") # linux only
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            capabilities = DesiredCapabilities.CHROME
            capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
            if headless:
                options.add_argument("--headless")
            self.browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), options=options, desired_capabilities=capabilities)
        else:
            raise Exception("Browser not supported")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.quit()

    # Navigate to url
    def get(self, url):
        # Check if we will always use browser
        if self.always_use_browser:
            # We will use browser
            self.browser.get(url)
            # Wait 10 seconds for the page to load
            i = 0
            while i < 10:
                i += 1
                if self.browser.execute_script("return document.readyState") == "complete":
                    break
                else:
                    time.sleep(1)                
            self.content = self.browser.page_source
            self.status_code = self.get_status(self.browser.get_log('performance'))
            self.cookies = self.browser.get_cookies()
        else:
            # We will use cfscrape
            # check if response is not empty and if it is 200
            r = self.cfscraper.get(url)
            if r.content and r.status_code == 200:
                self.content = r.content
                self.status_code = r.status_code
                self.cookies = r.cookies
            else:
                # We will use browser to get the HTML code
                self.browser.get(url)
                self.content = self.browser.page_source
                self.status_code = self.get_status(self.browser.get_log('performance'))
                self.cookies = self.browser.get_cookies()

    # Get page status if we use browser        
    def get_status(self, logs):
        for log in logs:
            if log['message']:
                d = json.loads(log['message'])
                try:
                    content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                    response_received = d['message']['method'] == 'Network.responseReceived'
                    if content_type and response_received:
                        return d['message']['params']['response']['status']
                except:
                    pass

if __name__ == '__main__':
    with Crawler(always_use_browser=True) as crawler:
        print(crawler.get("https://www.google.com/"))
        print(crawler.content)
        print(crawler.status_code)
        print(crawler.cookies)
