from apscheduler.schedulers.blocking import BlockingScheduler
from fcm.fcm import prepareData
from cloud_firestore.cloud_firestore import uploadDocIfNotExist


scheduler = BlockingScheduler()


# Visit https://devcenter.heroku.com/articles/clock-processes-python
# to know more
@scheduler.scheduled_job('interval', minutes=15)
def timed_job():
    prepareData()
    print('This job is run every fifteen minutes.')


@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=7)
def scheduled_job():
    uploadDocIfNotExist()
    print('This job is run every weekday at 7am.')


scheduler.start()
