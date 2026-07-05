'''
aldi/scraper.py

Use to scrape the jobs from aldi.careers.com.

Main components :
    - Scraper
    - Extractor
    - DB

Scraper :
Iterate over the jobs at current pages and collect the address of each job and save into list.

--- Come up with list of the jobs url

Extractor :
This class will provide list of methods to extract the jobs details from list of urls get from Scraper.
Parse the jobs to some extend and save in DB.

DB:
   Help in providing the interface to DB for Extractor to dump the jobs.
'''
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from .extractor import MBExtractor

class Scraper:
    def __init__(self, db=False,headless=False):
        self.headless = headless
        self.urls = []
        self.browser = None
        self.p = None
        self.page = None
        self.db = db

    def start(self):
        try:
            self.p = sync_playwright().start()
            self.browser = self.p.chromium.launch(headless=self.headless)
            context = self.browser.new_context(
                locale="en-US",
                extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9"
                    }
            )
            self.page = context.new_page()
        except Exception as e:
            print(type(e).__name__,e , type(e).__traceback__.tb_lineno)

    def accept_cookies(self):
        try:
            btn = self.page.locator('[data-testid="uc-accept-all-button"]')
            btn.wait_for(state="visible", timeout=8000)
            btn.click()
        except:
            print("Cookie banner not found or already accepted")

    def open_site(self):


        # access the Link for career page!
        self.page.goto("https://jobs.mercedes-benz.com/en?en=",wait_until="domcontentloaded")
        self.accept_cookies()
        # Wait for some time
        self.page.wait_for_timeout(2000)


    def run(self):

        self.start()
        self.open_site()
        while True:
            try:

                self.page.wait_for_selector(".mjp-job-ad-card a")

                self.urls = self.page.eval_on_selector_all(
                        "a",
                        "elements => elements.map(e => e.href)"
                    )
                self.urls = [
                    u
                    for u in self.urls
                    if re.search(r"(mer\d+[a-z0-9]+)$", u)
                ]

                self.page.wait_for_timeout(2000)
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.next_page()
                # pass to the extractor
                self.mbenz_extractor = MBExtractor(self.db,self.urls[-10:])
                self.mbenz_extractor.extract_jobs()

                self.page.wait_for_timeout(2000)
            except Exception as e:
                print(type(e).__name__,e , type(e).__traceback__.tb_lineno)




    def next_page(self):
        # navigate to new page
        self.page.wait_for_timeout(2000)
        self.page.get_by_text("Load More Jobs").click()

    def stop(self):
        self.browser.close()
        self.p.stop()