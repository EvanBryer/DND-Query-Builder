import requests
import argparse
import json
from pprint import pprint
#Allow for easy queries if you already know what you want
parser = argparse.ArgumentParser(description='Create D&D characters through the 5e API.')
req = parser.add_argument_group('Required arguments')
parser.add_argument("-q", "--query", help="path to file of new line delimited strings.")
req = parser.parse_args()

#Global url to access the api
global_url = 'https://www.dnd5eapi.co'

#Build sub categories. This is for individual items in the categories selected
def subbuild(j):
	lev1 = j['results']
	d = {}
	c = 0
	d = {}
	for val in lev1:
		d[c] = val['url']
		print(f"{c}. {val['name']}")
		c+=1
	choice = input()
	try:
		choice = int(choice)
		if choice >= 0 and choice < c:
			u = d[choice]
	except:
		u = lev1[choice]
	r = requests.get(f"{global_url}{u}")
	j = json.loads(r.text)
	try:
		if j['count']:
			subbuild(j)
		else: pprint(j)
	except:
		pprint(j)

#Select generic category. This includes classes, items, races, etc
def build(url):
	lev1 = json.loads(requests.get(url).text)
	c = 0
	d = {}
	for val in lev1:
		d[c] = lev1[val]
		print(f"{c}. {val}")
		c+=1
	choice = input()
	try:
		choice = int(choice)
		if choice >= 0 and choice < c:
			u = d[choice]
	except:
		u = lev1[choice]
	r = requests.get(f"{global_url}{u}")
	j = json.loads(r.text)
	try:
		if j['count']:
			subbuild(j)
		else: pprint(j)
	except:
		pprint(j)

#Quick query.
if req.query:
	r = requests.get(f"{global_url}/api/{req.query}")
	pprint(json.loads(r.text))

#Otherwise, start building
else:
	print("D&D query builder! Select a category:")
	build('https://www.dnd5eapi.co/api/')

