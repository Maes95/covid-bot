from apscheduler.schedulers.blocking import BlockingScheduler
from jobs import GetCovidDate
import os

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    GetCovidDate.tryGetDate()

sched.start()

# GetCovidDate.tryGetDate()



