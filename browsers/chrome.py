'''
We will set selenium to use chrome browser
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class ChromeBrowser:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

    # get html code
    def get_html(self,url):
        self.driver.get(url)
        # wait 10 seconds for the page to load, if it loads before 10 seconds it will continue
        self.driver.implicitly_wait(10)
        html = self.driver.page_source

        return html

    # restart browser
    def restart(self):
        self.driver.quit()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
    
    # close browser
    def close(self):
        self.driver.quit()