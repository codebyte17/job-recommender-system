from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

class SiemensExtractor:

    def __init__(self, headless=False,db=None):
        self.headless = headless
        self.browser = None
        self.page = None
        self.p = None
        self.db = db
        self.job_details = None
    # ---------------------------
    # START BROWSER (ONCE)
    # ---------------------------
    def start(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=self.headless)
        context = self.browser.new_context(
            locale='en-US',
            timezone_id='America/New_York'
        )
        self.page = context.new_page()

    # ----------------------------
    # HANDLE COOKIES
    # ----------------------------
    def handle_cookies(self) -> None:
        try:
            self.page.locator("button:has-text('Accept')").click(timeout=3000)

        except Exception as e:
            print(type(e).__name__,
                  e.__traceback__.tb_lineno,
                  "The Cookies Does not handled!")

    # ---------------------------
    # STOP BROWSER
    # ---------------------------
    def stop(self):
        self.browser.close()
        self.p.stop()


    # ---------------------------
    # Load JOBs IDs
    # ---------------------------
    def load_jobs_ids(self):

        jobs = self.db.load_jobs_ids_from_mongodb()

        return jobs


    # ---------------------------
    # MAIN RUNNER
    # ---------------------------
    def run(self):
        self.start()
        jobs = self.load_jobs_ids()


        for job_id in jobs:
            if not job_id:
                continue
            try:
                self.process_job(job_id)
                self.db.insert_jobs_details(self.job_details)
                self.db.update_jobs_id_status(job_id)
            except Exception as e:
                print(f"Error with job {job_id}: {e}",e.__traceback__.tb_lineno)

        return True

    # ---------------------------
    # PROCESS SINGLE JOB
    # ---------------------------
    def process_job(self, job_id):
        self.handle_cookies()
        url = f"https://jobs.siemens.com/en_US/externaljobs/JobDetail/{job_id}/"

        print(f"Opening: {url}")

        self.page.goto(url)

        # Wait for content
        self.page.wait_for_selector(".grid__item.grid__item--main")

        html = self.page.content()

        return self.parse(html, job_id)

    # ---------------------------
    # PARSER (BeautifulSoup)
    # ---------------------------
    def parse(self, html, job_id):
        soup = BeautifulSoup(html, "html.parser")

        self.job_details = {
            "job_id": job_id,
            "job_title" : None
        }

        # ---------------------------
        # TITLE
        # ---------------------------
        # Targeted search by class
        title_tag = soup.find('h3', class_='section__header__text__title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            self.job_details["job_title"] = title
        # ---------------------------
        # ALL LABEL-VALUE FIELDS
        # ---------------------------
        fields = soup.select(".article__content__view__field")

        for field in fields:
            label_tag = field.select_one(".article__content__view__field__label")
            value_tag = field.select_one(".article__content__view__field__value")

            if not label_tag or not value_tag:
                continue

            label = label_tag.get_text(strip=True).lower()
            value = value_tag.get_text(strip=True)

            # clean key (important)
            key = label.replace(" ", "_").replace(":", "")

            self.job_details[key] = value

        # ---------------------------
        # DESCRIPTION (MAIN TARGET)
        # ---------------------------
        description_container = soup.find_all(class_="article__content__view__field__value")

        def get_text_length(tag):
            return len(tag.get_text(strip=True))

        # find index of the longest item
        max_index = max(range(len(description_container)), key=lambda i: get_text_length(description_container[i]))

        description = (
            description_container[max_index].get_text(separator="\n", strip=True)
            if description_container[max_index] else " "
        )

        self.job_details["description"] = description
        # Write dictionary to a file
        #with open('data.json', 'w', encoding='utf-8') as f:
        #    json.dump(data, f, indent=4, ensure_ascii=False)


