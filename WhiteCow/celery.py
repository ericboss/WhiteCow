from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WhiteCow.settings')
app = Celery('WhiteCow')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = 'GMT+1'
days = ['mon,tue,wed,thu,fri,sat,sun', 'sat,sun']
times = [5,6,7,8,17,20,21,22]
count = 1
app.conf.beat_schedule={}
for day in days:
    for time in times:
        task = "task "+str(count)
        app.conf.beat_schedule[task] = {
            'task':'deal.tasks.email',
            'schedule':crontab(minute=0,hour=time, day_of_week=day)
        

        }
        count+=1


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


