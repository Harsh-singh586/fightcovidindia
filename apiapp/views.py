from django.shortcuts import render
from django.shortcuts import render
import pymongo
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cowin import CoWinAPI
import os
# Create your views here.
client = pymongo.MongoClient(os.environ['MONGODB_CL'])
def landing(request):
	return render(request , 'apidoc.html') 

@api_view(['GET'])
def hospitalapi(request,state,district):
	if request.method == 'GET':
		db1 = client['states']
		statedata = db1['statedata']
		disdata = db1['districtdata']
		statecode = statedata.find_one({'state' : state})['statecode']
		discode = disdata.find_one({'statecode' : statecode, 'districtname' : district.upper()})['districtcode']
		db = client['hospitals']
		hospitaldata = db[statecode]
		x = list(hospitaldata.find({'district_code':discode},{'_id':0,'details':0,'bedtype':0}))
		return Response(x)

@api_view(['GET'])
def stateapi(request):
	if request.method == 'GET':
		db = client['states']
		statedata = db['statedata']
		x = list(statedata.find({},{'_id':0}))
		return Response(x)

@api_view(['GET'])
def districtapi(request,state):
	if request.method == 'GET':
		db1 = client['states']
		districtdata = db1['districtdata']
		x = list(districtdata.find({'statecode':state},{'_id':0}))
		return Response(x)

@api_view(['GET'])
def hospitalnear(request, state, lat, lon, distance):
	if request.method == 'GET':
		distance = int(distance) * 1000
		db1 = client['hospitals']
		hospitaldata = db1[state]
		lat = float(lat)
		lon = float(lon)
		x = list(hospitaldata.find({'location' : {'$near' : {'$geometry' : {'type' : 'Point', 'coordinates' : [lon, lat]},'$maxDistance' : distance}}},{'_id':0,'details':0,'bedtype':0}))
		return Response(x)

@api_view(['GET'])
def details(request, state):
	if request.method == 'GET':
		db = client['hospitals']
		hospitaldata = db[state]
		x = hospitaldata.find_one({},{'_id':0,'details':1,'bedtype':1})
		return Response(x)

@api_view(['GET'])
def availablebedtype(request, state, districtcode, bedtype):
	if request.method == 'GET':
		db = client['hospitals']
		hospitaldata = db[state]
		bedtype = '{x}.Vacant'.format(x = bedtype)
		x = list(hospitaldata.find({'district_code':districtcode,bedtype : {'$gt':0}},{'_id':0,'bedtype':0,'details':0}))
		return Response(x)

@api_view(['GET'])
def vaccinecenters(request, pincode, feetype, vaccinetype, avail):
	if request.method == 'GET':
		cowin = CoWinAPI()
		available_centers = cowin.get_availability_by_pincode(pincode)
		centers = available_centers['sessions']
		lst = []
		if feetype == 'All':
			feetype = ['Free','Paid']
		if vaccinetype == 'All':
			vaccinetype = ['COVAXIN','COVISHIELD']
		if avail == 'DOSE1':
			flag = 'available_capacity_dose1'
		elif avail == 'DOSE2':
			flag = 'available_capacity_dose2'
		for i in centers:
			if avail == 'All':
				if i['fee_type'] in feetype and i['vaccine'] in vaccinetype:
					lst.append(i)
			elif avail == 'Both' :
				if i['fee_type'] in feetype and i['vaccine'] in vaccinetype and i['available_capacity_dose1'] > 0 and i['available_capacity_dose1'] > 0:
					lst.append(i)
			else:
			    if i['fee_type'] in feetype and i['vaccine'] in vaccinetype and i[flag] > 0:
				    lst.append(i)
		centers = lst
		return Response(centers)
	
@api_view(['GET'])
def covid_state(request, state):
	state_api = requests.get('https://api.covid19india.org/data.json')
	json_data = state_api.json()
	covid_data = json_data['statewise'][int(state)]
	state = covid_data['state']
	covid = requests.get("https://api.covid19india.org/district_wise.json")
	covid_json = covid.json()
	lst = []
	for i in covid_json['districts']:
		if i['state'] == state:
			lst.append({'district': i['district'], 'active' : i['active'], 'confirmed' : i['confirmed'], 'deaths' : i['deceased'], 'recovered' : i['recovered']})
	res = {'state': covid_data['state'],'active' : covid_data['active'],'confirmed' : covid_data['confirmed'],'deaths': covid_data['deaths'],'recovered' : covid_data['recovered'], 'district_data' : lst}
	return Response(res)
