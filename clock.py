from apscheduler.schedulers.blocking import BlockingScheduler
from fcm.fcm import prepareData

scheduler = BlockingScheduler()


# Visit https://devcenter.heroku.com/articles/clock-processes-python
# to know more
@scheduler.scheduled_job('interval', minutes=15)
def timed_job():
    prepareData()
    print('This job is run every three minutes.')


# @scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')


scheduler.start()
