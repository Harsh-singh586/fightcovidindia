import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ['DJANGO_SETTINGS_MODULE'] = 'covidupdate.settings'
os.environ.setdefault('DJANGO_SETTING_MODULE','covidupdate.settings')

app = Celery('covidupdate')
app.conf.enable_utc = False

app.conf.update(timezone = 'Aia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

#celery beat
app.conf.beat_schedule = {
	'send_mail':{
        'task' : 'home.tasks.send_mail',
        'schedule' : crontab(hour = 8, minute = 1)  
	},
	'send_mail':{
        'task' : 'home.tasks.send_mail',
        'schedule' : crontab(hour = 12, minute = 1)  
	},
	'send_mail':{
        'task' : 'home.tasks.send_mail',
        'schedule' : crontab(hour = 16, minute = 1)  
	},
	'send_mail':{
        'task' : 'home.tasks.send_mail',
        'schedule' : crontab(hour = 20, minute = 1)  
	},
	'send_mail':{
        'task' : 'home.tasks.send_mail',
        'schedule' : crontab(hour = 18, minute = 15)  
	}
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
	print(f'Request: (self.request!r)')
