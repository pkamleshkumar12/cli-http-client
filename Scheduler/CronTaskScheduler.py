import schedule
import time
import os


def job():
    print("Running job!!")
    os.system('python JobRunner.py')


schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
