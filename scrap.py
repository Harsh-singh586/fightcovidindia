from bs4 import BeautifulSoup
import requests
import pymongo
client = pymongo.MongoClient("xyz")
db = client['hospitals']
def puducherry():
	hospitaldata = db['27']
	url = "https://covid19dashboard.py.gov.in/BedAvailabilityDetails"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, "html.parser")
	tr = soup.find_all('tr')
	tr = tr[4:]
	lst = []
	for i in tr:
		td = i.find_all('td')
		x = []
		for j in td:
			x.append(j.text.strip())
		lst.append(x)
	for k in lst:
		if len(k) == 8:
			flag = hospitaldata.find_one({'name': k[0]})
			if flag:
				hospitaldata.update_one({'name' : k[0]},{'$set':{'updatetime' : k[1], 'Isolation.Alloted' : int(k[2]), 'Isolation.Vacant' : int(k[3]), 'Oxygen.Alloted' : int(k[4]), 'Oxygen.Vacant' : int(k[5]), 'Ventilator.Alloted' : int(k[6]), 'Ventilator.Vacant' : k[7]}})
	#print(lst)

def mp():
	hospitaldata = db['20']
	url = "http://sarthak.nhmmp.gov.in/covid/wp-content/themes/covid/facilities_occupancy_excel.php?district_id=0&facility_org_type=0&facility=0"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, "html.parser")
	tr = soup.find_all('tr')
	tr = tr[1:]
	lst = []
	for i in tr:
		td = i.find_all('td')
		x = []
		for j in td:
			x.append(j.text.strip())
		lst.append(x)
	#print(len(lst))
	for k in lst[1:291]:
		hospitaldata.update_one({'district' : k[1],'name' : k[2]},{'$set':{'updatetime' : k[13],'Isolation.Capacity': int(k[7]),'Isolation.Vacant' : int(k[8]), 'Oxygen.Capacity' : int(k[9]), 'Oxygen.Vacant' : int(k[10]), 'Ventilator.Capacity' : int(k[11]), 'Ventilator.Vacant' : int(k[12])}})
	#print(lst)

def haryana():
	hospitaldata = db['12']
	url = "https://coronaharyana.in/"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, "html.parser")
	div = soup.find_all("div", {"class": "psahuDiv community-post wow fadeInUp"})
	lst = []
	for i in div:
		x = []
		name = i.find('h6').text.split(':')[1].strip()
		x.append(name)
		a = i.find_all('a')
		for j in a:
			x.append(j.text.strip())
		drugs = i.find_all('i')
		for k in drugs:
			x.append(k.text.strip())
		li = i.find('li').text.split('n:')[1].strip()
		x.append(li)
		lst.append(x)
	for n in lst:
		if len(n) == 13:
			try:
				print(hospitaldata.update_one({'name' : n[0]},{'$set':{'updatetime': n[12],'Oxygen.Vacant': n[1], 'Non-Oxygen.Vacant' : n[2], 'ICU.Vacant' : n[3],'Ventilator.Vacant' : n[4],'Oxygen Available' : n[7], 'Antiviral Available' : n[8], 'Steroids Available' : n[9],'Anticoagulant Available' : n[10], 'Antipyretic Available' : n[11]}}), n[0])
			except:
				continue
def bihar():
	hospitaldata = db['5']
	url = "https://covid19health.bihar.gov.in/DailyDashboard/BedsOccupied"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, "html.parser")
	tr = soup.find_all('tr')
	lst = []
	for i in tr:
		td = i.find_all('td')
		x = []
		for j in td:
			x.append(j.text.strip())
		lst.append(x)
	for k in lst:
		try:
			print(hospitaldata.update_one({'name' : k[1], 'district': k[0]},{'$set':{'updatetime': k[4],'Total.Capacity': k[5], 'Total.Vacant' : k[6], 'ICU.Capacity' : k[7], 'ICU.Vacant' : k[8]}}))
		except:
			continue

def rajasthan():
	hospitaldata = db['29']
	url = "https://covidinfo.rajasthan.gov.in/Covid-19hospital-wisebedposition-wholeRajasthan.aspx"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, "html.parser")
	tr = soup.find_all('tr')
	tr = tr[3:]
	lst = []
	for i in tr:
		td = i.find_all('td')
		x = []
		for j in td:
			x.append(j.text.strip())
		lst.append(x)
	for k in lst:
		try:
			print(hospitaldata.update_one({'district' : k[1], 'name' : k[2]},{'$set' : {'updatetime' : k[17], 'Oxygen.Total' : int(k[6]), 'Oxygen.Occupied' : int(k[7]), 'Oxygen.Vacant' : int(k[8]),'ICU.Total' : int(k[9]), 'ICU.Occupied' : int(k[10]),'ICU.Vacant' : int(k[11]), 'Ventilator.Total' : int(k[12]), 'Ventilator.Occupied' : int(k[13]), 'Ventilator.Vacant' : int(k[14]), 'General.Total' : int(k[3]), 'General.Occupied' : int(k[4]), 'General.Vacant' : int(k[5])}}))
		except:
			print('error')
#rajasthan()
#haryana()
#bihar()

def uttarakhand():
	hospitaldata = db['36']
	url = 'https://covid19.uk.gov.in/bedssummary.aspx'
	req = requests.get(url)
	soup = BeautifulSoup(req.text, 'html.parser')
	tr = soup.find_all('tr')
	tr = tr[1:]
	lst = []
	for i in tr:
		span = i.find_all('span')
		x = []
		for j in span:
			x.append(j.text.strip())
		lst.append(x)
	for k in lst:
		try:
			print(hospitaldata.update_one({'district' : k[0], 'name' : k[1]},{'$set' : {'General.Capacity' : int(k[5]), 'General.Vacant' : int(k[6]),'Oxygen.Capacity' : int(k[7]), 'Oxygen.Vacant' : int(k[8]), 'ICU.Capacity' : int(k[9]), 'ICU.Vacant' : int(k[10]), 'Ventilator.Capacity' : int(k[11]), 'Ventilator.Vacant' : int(k[12]), 'updatetime' : k[13]}}))
		except:
			continue
