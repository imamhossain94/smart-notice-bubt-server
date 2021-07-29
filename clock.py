from apscheduler.schedulers.blocking import BlockingScheduler
from fcm.fcm import prepareData

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=5)
def timed_job():
    prepareData()
    print('This job is run every three minutes.')


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


sched.start()
