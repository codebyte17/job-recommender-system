import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.mb_interaction import MBENZDB

from playwright.sync_api import sync_playwright
from database.siemens_interaction import SiemensDB
from siemens import SiemensCollector , SiemensExtractor
from mbenz import MBEZScraper
class SiemensScraper:
    def __init__(self):
        self.siemens_client = SiemensDB()

    def collector(self) -> None:
        with sync_playwright() as p:

            # Create object of Playwright with headless=False
            browser = p.chromium.launch(headless=False)

            # Build Browser Configuration
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                locale="de-DE"
                    )

            # Open Home page of the Chrome!
            page = context.new_page()

            scraper = SiemensCollector(page,db=self.siemens_client)
            scraper.run()

            browser.close()

    def extractor(self) -> None:
        object = SiemensExtractor(db=self.siemens_client)
        object.run()


class BenzScraper:
    def __init__(self) -> None:
        self.mb_collection = MBENZDB()

    def scraper(self) -> None:
       aldi_object =  MBEZScraper(db=self.mb_collection,headless=False)
       aldi_object.run()

if __name__ == "__main__":
    # TODO : if you want to scrap the siemens data just uncomment the following 3 lines
    #siemens_scraper = SiemensScraper()
    #siemens_scraper.collector()
    #siemens_scraper.extractor()

    # Currently runing the benz scrapers
    mbenz = BenzScraper()
    mbenz.scraper()
