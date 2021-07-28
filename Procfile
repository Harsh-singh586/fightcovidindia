web: waitress-serve --port=$PORT covidupdate.wsgi:application
worker: celery worker -app=tasks.send_mail
