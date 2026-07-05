from bs4 import BeautifulSoup
import requests
class MBExtractor:
    def __init__(self,db=None,jobs_list=None):
        print("MBExtractor -- Class Initialization")
        self.jobs_list = jobs_list
        self.db = db

    def extract_jobs(self):
        print("MBExtractor -- Extracting Jobs")

        list_of_jobs = []
        # iterate over the list of jobs
        for job in self.jobs_list:
            try:
                session = requests.Session()

                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/137.0.0.0 Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,de;q=0.9,en;q=0.8",
                }

                response = session.get(job, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.title.text.strip() if soup.title else None

                container = soup.find_all("section")[1]
                part1 = container.find(class_="mjp-job-ad__content-block-container")
                parsed_jobs_details = self.parse_job_details(part1.find_all(class_="mjp-info-tag"))

                print("Parsing Job Details")

                part2 = container.find(class_="mjp-job-ad__content-texts")
                parsed_jobs_details["description"] = part2.text
                parsed_jobs_details["title"] = title

                print(parsed_jobs_details)

                list_of_jobs.append(parsed_jobs_details)



            except Exception as e:
                print(type(e),e.__traceback__.tb_lineno,e)

        self.db.add_new_batch(list_of_jobs)



    def parse_job_details(self,data):
        print("MBExtractor -- Parsing Job Details")
        jobs_details = {
            "job_id": None,
            "title": None,
            "location": None,
            "job_category": None,
            "organization": None,
            "working_mode": None,
            "Department": None,
            "publication": None,
            "start_date": None
        }
        for job in data:
            item = job.text
            if ":" not in item:
                continue

            key, value = item.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "job category":
                jobs_details["job_category"] = value

            elif key == "department":
                jobs_details["Department"] = value

            elif key == "organization":
                jobs_details["organization"] = value

            elif key == "location":
                jobs_details["location"] = value

            elif key == "start date":
                jobs_details["start_date"] = value

            elif key == "publication date":
                jobs_details["publication"] = value

            elif key == "job number":
                jobs_details["job_id"] = value

            elif key == "working time":
                jobs_details["working_mode"] = value

        return jobs_details






