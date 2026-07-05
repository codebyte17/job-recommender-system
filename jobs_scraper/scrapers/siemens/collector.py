from playwright.sync_api import sync_playwright

class SiemensCollector:
    def __init__(self,page,db=None):
        self.page = page
        self.db = db
        self.job_ids = {}

    def open_site(self):
        # Wait for some time
        self.page.wait_for_timeout(2000)

        # access the Link for career page!
        self.page.goto("https://jobs.siemens.com/en_US/externaljobs/SearchJobs" ,
                       wait_until="networkidle")


    def collect_jobs_ids(self):
        """
        Collect jobs IDs from Siemens site
        :return:
        """
        print("Collecting jobs IDs ....")
        self.page.wait_for_timeout(2000)

        job_ids = self.page.locator(".list-item-jobId")


        count = job_ids.count()

        for i in range(count):
            try :
                text = job_ids.nth(i).inner_text()  # "Job ID: 123456"

                job_id = text.split(":")[-1].strip()  # extract number

                self.job_ids[i] = job_id
            except Exception as e :
                print(type(e).__name__,
                      e.__traceback__.tb_lineno,
                      f"ID {job_ids[1]} :: --- Failed to Collect Job ID!" )
        print(self.job_ids)



    def save_jobs_ids(self):
        self.db.save_job_to_mongodb(self.job_ids)


    def navigate_next_page(self) ->bool:
        try:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(2000)

            next_btn = self.page.locator("a[aria-label*='Next Page']")
            next_btn.click()

            self.page.wait_for_timeout(2000)
            return True
        except Exception as e:
            print(type(e).__name__,
                  e.__traceback__.tb_lineno,
                  "Next Page not found!")

            return False

    def handle_cookies(self) -> None:
        try:
            self.page.locator("button:has-text('Accept')").click(timeout=3000)

        except Exception as e:
            print(type(e).__name__,
                  e.__traceback__.tb_lineno,
                  "The Cookies Does not handled!")



    def run(self):
        # Open the page1
        self.open_site()

        # Handle the cookies if any !
        self.handle_cookies()
        page_id = 1
        while True:
            print("--------------collecting jobs ids from page No:{}-----------".format(page_id))
            self.collect_jobs_ids()
            self.save_jobs_ids()
            if not self.navigate_next_page():
                break
            page_id += 1












