from datetime import datetime
from . import db
from pymongo.errors import BulkWriteError

class MBENZDB:
    def __init__(self):
        self.collection = db["mercedes-benz_jobs"]


    def add_new_batch(self,jobs):
        '''
        Add new jobs to the database in form of Batch (size of the jobs available at the page)
        :param jobs:
            jobs : list of dicts (each dict shows job)
        :return:
            True or False
        '''
        try:
            self.collection.insert_many(jobs, ordered=False)
        except BulkWriteError as e:
            print("Some duplicates skipped")




