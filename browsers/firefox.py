'''
We will set selenium to use chrome browser
'''
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


class FirefoxBrowser:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=self.options)


    def get_html(self,url):
        self.driver.get(url)
        html = self.driver.page_source
        return html