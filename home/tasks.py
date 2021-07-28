from celery import shared_task
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pymongo
import requests

@shared_task(bind=True)
def func1(self):
	print('celery')
	return('Done')

@shared_task(bind=True)
def send_mail(self):
    client = pymongo.MongoClient("mongodb://covidupdate:qzmp1234@cluster0-shard-00-00.iqzh9.mongodb.net:27017,cluster0-shard-00-01.iqzh9.mongodb.net:27017,cluster0-shard-00-02.iqzh9.mongodb.net:27017/Cluster0?ssl=true&replicaSet=atlas-12y13c-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client['emailalert']
    emaildata = db['emaildata']
    email_lst = emaildata.find({'verified' : 'True'})
    for i in email_lst:
    	pincode = i['pincode']
    	feetype = i['feetype']
    	vaccinetype = i['vaccinetype']
    	dose = i['Dose']
    	email = i['email']
    	url = 'https://fightcovidindia.herokuapp.com/api/vaccine/pincode/{}/{}/{}/{}'.format(pincode, feetype, vaccinetype, dose)
    	centers = requests.get(url).json()
    	if centers:
    		message = Mail(
		        from_email='codersintense@gmail.com',
		        to_emails= email,
		        subject= 'Vaccine Centers Found',
		        html_content = '<h1>Hurrah! Vaccine Centers Found in Your pincode {}</h1>'.format(pincode))
    		sg = SendGridAPIClient('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')
    		response = sg.send(message)
    		code = response.status_code

