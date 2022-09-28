'''
We will create a crawler that will be able to get any website HTML code
first we will try to use requests library to get the HTML code using requests and cfscrape
if it all fails we will use chrome, firefox or brave to get the HTML code
'''

import cfscrape
import requests
# my scripts
from browsers.chrome import ChromeBrowser
from browsers.firefox import FirefoxBrowser
from browsers.brave import BraveBrowser

class Crawler:
    def __init__(self, url, browser="brave", always_use_browser=False, headless=True):
        '''
        :param url (string): url to get the HTML code from
        :param browser (string): standard is "brave", it is the browser to use to get the HTML code, can be: "chrome", "firefox" or "brave"
        :param always_use_browser (bool): if True we will always use browser to get the HTML code
        :param headless (bool): if True we will use headless browser
        '''

        self.url = url
        self.scraper = cfscrape.create_scraper()
        self.always_use_browser = always_use_browser

        # setting browser option
        if browser == "chrome":
            self.browser = ChromeBrowser(headless=headless)
        elif browser == "firefox":
            self.browser = FirefoxBrowser(headless=headless)
        else:
            self.browser = BraveBrowser(headless=headless)
        

    def get_html(self):
        # We will use requests first
        html = self.scraper.get(self.url).content
        # Check if we will always use browser
        if self.always_use_browser:
            # We will use browser to get the HTML code
            html = self.browser.get_html(self.url)
            return html
        else:
            # check if response is not empty and if it is 200
            if html and self.scraper.get(self.url).status_code == 200:
                return html
            else:
                # We will use cfscrape to get the HTML code
                html = requests.get(self.url).content
                # check if response is not empty and if it is 200
                if html and self.scraper.get(self.url).status_code == 200:
                    return html
                else:
                    # We will use browser to get the HTML code
                    html = self.browser.get_html(self.url)
                    return html
            

if __name__ == '__main__':
    url = 'https://www.google.com'
    crawler = Crawler(url)
    html = crawler.get_html()
    print(html)
