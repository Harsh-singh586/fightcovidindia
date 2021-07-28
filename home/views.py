from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.timezone import now
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
global client
import pymongo
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cowin import CoWinAPI
from .tasks import func1, send_mail
from django.http import JsonResponse
import secrets
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
client = pymongo.MongoClient(os.environ['MONGODB_CL'])
def home(request):
	return render(request, 'landing.html')

def state(request, key):
	send_mail.delay()
	db = client['states']
	districtdata = db['districtdata']
	district = districtdata.find({'statecode' : key})
	statedata = db['statedata']
	state_name = statedata.find_one({'statecode' : key})['state']
	state_api = requests.get('https://api.covid19india.org/data.json')
	json_data = state_api.json()
	covid_data = json_data['statewise'][int(key)]
	dic = {'covid_data':covid_data,'district':district,'state_name' : state_name,'key':key}
	return render(request, 'state.html',context = dic)

def district(request, state, district):
	db1 = client['hospitals']
	hospitaldata = db1[state]
	hospitals = hospitaldata.find({'district_code': district})
	location = hospitaldata.find_one({'location':{'$exists':'true'}})
	if location:
		location_exist = True 
	else:
		location_exist = False
	print(hospitals[0], hospitaldata)
	covid = requests.get("https://api.covid19india.org/district_wise.json")
	covid_json = covid.json()
	covid_data = covid_json['districts'][int(district)]
	hostype = hospitals.distinct('type')
	bedtype = hospitaldata.find_one()['bedtype']
	db = client['states']
	districtdata = db['districtdata']
	statedata = db['statedata']
	link = statedata.find_one({'statecode': state})['link']
	dis_name = districtdata.find_one({'statecode' : state, 'districtcode' : district})['districtname']
	dic = {'covid_data':covid_data, 'hospitals': hospitals,'state' : state, 'district' : district,'hostype': hostype, 'bedtype' : bedtype,'dis_name' : dis_name, 'link' : link,'location_exist':location_exist}
	return render(request, 'district.html', context = dic)

def hospital_update(request, state, district, bedtype, hostype,lat ,lon, distance):
	db1 = client['hospitals']
	hospitaldata = db1[state]
	distance = int(distance) * 1000
	print(distance, lat, lon)
	if lat == '0' and lon == '0':
	   if bedtype == 'All' and hostype != 'All':
		   hospitals = hospitaldata.find({'district_code': district,'type': hostype})
	   elif bedtype != 'All' and hostype == 'All':
		   bedtype = '{x}.Vacant'.format(x = bedtype)
		   hospitals = hospitaldata.find({'district_code': district, bedtype : {'$gt':0}})
	   elif bedtype != 'All' and hostype != 'All':
		   bedtype = '{x}.Vacant'.format(x = bedtype)
		   hospitals = hospitaldata.find({'district_code': district, bedtype : {'$gt':0},'type': hostype})
	   elif bedtype == 'All' and hostype == 'All':
		   hospitals = hospitaldata.find({'district_code': district})
	if lat!= '0' and lon != '0':
		lat = float(lat)
		lon = float(lon)
		print('b')
		if bedtype == 'All' and hostype != 'All':
		   hospitals = hospitaldata.find({'district_code': district,'type': hostype,'location' : {'$near' : {'$geometry' : {'type' : 'Point', 'coordinates' : [lon, lat]},'$maxDistance' : distance}}})
		elif bedtype != 'All' and hostype == 'All':
		   print('a')
		   bedtype = '{x}.Vacant'.format(x = bedtype)
		   hospitals = hospitaldata.find({'district_code': district, bedtype : {'$gt':0},'location' : {'$near' : {'$geometry' : {'type' : 'Point', 'coordinates' : [lon, lat]},'$maxDistance' : distance}}})
		elif bedtype != 'All' and hostype != 'All':
		   bedtype = '{x}.Vacant'.format(x = bedtype)
		   hospitals = hospitaldata.find({'district_code': district, bedtype : {'$gt':0},'type': hostype,'location' : {'$near' : {'$geometry' : {'type' : 'Point', 'coordinates' : [lon, lat]},'$maxDistance' : distance}}})
		elif bedtype == 'All' and hostype == 'All':
		   hospitals = hospitaldata.find({'district_code': district,'location' : {'$near' : {'$geometry' : {'type' : 'Point', 'coordinates' : [lon, lat]},'$maxDistance' : distance}}})
	dic = {'hospitals':hospitals,'bedtype' : bedtype, 'hostype' : hostype}
	#print(hospitals, hostype, bedtype)
	return render(request, 'hospitalupdate.html', context = dic)

def vaccine_search(request, pincode, feetype, vaccinetype, availability):
	cowin = CoWinAPI()
	available_centers = cowin.get_availability_by_pincode(pincode)
	centers = available_centers['sessions']
	lst = []
	if feetype == 'All':
		feetype = ['Free','Paid']
	if vaccinetype == 'All':
		vaccinetype = ['COVAXIN','COVISHIELD']
	if availability == 'DOSE1':
		flag = 'available_capacity_dose1'
	elif availability == 'DOSE2':
		flag = 'available_capacity_dose2'
	for i in centers:
		if availability == 'All':
			if i['fee_type'] in feetype and i['vaccine'] in vaccinetype:
				lst.append(i)
		elif availability == 'Both' :
			if i['fee_type'] in feetype and i['vaccine'] in vaccinetype and i['available_capacity_dose1'] > 0 and i['available_capacity_dose1'] > 0:
				lst.append(i)
		else:
		    if i['fee_type'] in feetype and i['vaccine'] in vaccinetype and i[flag] > 0:
			    lst.append(i)
	return render(request, 'vaccine_search.html', {'centers' : lst})

def email_alert(request, pincode, email, feetype, vaccinetype, availability):
	db = client['emailalert']
	emaildata = db['emaildata']
	emailverify = db['emailverify']
	emaildata.insert_one({'email' : email , 'verified':'False','pincode' : pincode,'feetype' : feetype , 'vaccinetype' : vaccinetype, 'Dose' : availability})
	key = secrets.token_urlsafe(15)
	emailverify.insert_one({'email': email, 'key' : key})
	message = Mail(
        from_email='codersintense@gmail.com',
        to_emails= email,
        subject= 'Verify Your mail',
        html_content = '<h1>Click here to Verify your mail</h1><a href = https://fightcovidindia.herokuapp.com/emailverify/{}>Click Here</a>'.format(key))
	sg = SendGridAPIClient(os.environ['SENDGRID_API'])
	response = sg.send(message)
	code = response.status_code
	print(pincode, feetype, availability)
	status = json.dumps('Verify Your Email, look for Email by codersintense@gmail.com')
	return JsonResponse({'Status': status}, status=200)

def verify_email(request, key):
	db = client['emailalert']
	emaildata = db['emaildata']
	emailverify = db['emailverify']
	inst = emailverify.find_one({'key' : key})
	if inst:
		email = emailverify.find_one({'key' : key})['email'] 
		emaildata.update_one({'email' : email}, {'$set' : {'verified' : 'True'}})
		emailverify.delete_one({'key' : key})
		return HttpResponse('All Set! You Will Recieve daily Alert')
	else:
		return HttpResponse('404')






