import requests
import argparse
import json
import re
from pprint import pprint
#Allow for easy queries if you already know what you want
parser = argparse.ArgumentParser(description='Create D&D characters through the 5e API.')
req = parser.add_argument_group('Required arguments')
parser.add_argument("-q", "--query", help="path to file of new line delimited strings.")
req = parser.parse_args()
blacklist = ['index','url','subclasses']
#Global url to access the api
global_url = 'https://www.dnd5eapi.co'

#Format the dictionary keys to look more like real values
def formatter(s):
	s = re.sub("_", " ", s)
	return str.title(s)

#Unroll the nested dictionaries
def unrolldict(d,v,offset=0):
	if isinstance(v, dict):
		for n,i in v.items():
			if isinstance(i, dict):
				nform = formatter(n)
				print("\t"*offset+f"{nform}")
				unrolldict(n,i,offset+1)
			else:
				if isinstance(i, list):
					unrolllist(n,i,offset)
				else:
					if n not in blacklist:
						nform = formatter(n)
						if isinstance(i, str) and ":" in i:
							print("\t"*offset+f"{i}")
						else:
							print("\t"*offset+f"{nform}: {i}")

#Unroll the nested lists
def unrolllist(d,v,offset=0):
	print()
	if isinstance(v, list):
		if len(v) == 0: return
		if isinstance(v[0], dict):
			form = formatter(d)
			print("\t"*offset+f"{form}: ")
			for val in v:
				unrolldict(d,val,offset+1)
		else:
			form = formatter(d)
			print("\t"*offset+f"{form}:",end="")
			for val in v:
				print("\t"*(offset+1)+f"{val}")

#Handle the response and print formatted information from query
def typehandle(d,v):
	form = formatter(d)
	if isinstance(v, int) or isinstance(v, float): print(f"{form}: {v}"); return
	if '/api/' in v: return
	if isinstance(v, str) or isinstance(v, bool): print(f"{form}: {v}"); return
	if isinstance(v, list):
		unrolllist(d,v)
		return
	if isinstance(v, dict):
		unrolldict(d,v)
		return

#Print formatted information depending on choice
def dndprint(s,pick):
	print("\n\n")
	#if pick == 'magic-items':
	for d,v in s.items():
		if d in blacklist: continue
		if d == 'area_of_effect': print(f"Area: {v['type']} of size {v['size']}"); continue
		if d == 'components': print(f"Components:", *v); continue
		else:
			typehandle(d,v)

	print()

#Build sub categories. This is for individual items in the categories selected
def subbuild(j,pick):
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
	j2 = json.loads(r.text)
	dndprint(j2,pick)

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
	pick = u.split('/api/')[1]
	j = json.loads(r.text)
	if j['count']:
		subbuild(j,pick)


#Quick query.
if req.query:
	r = requests.get(f"{global_url}/api/{req.query}")
	pprint(json.loads(r.text))

#Otherwise, start building
else:
	print("D&D query builder! Select a category:")
	build('https://www.dnd5eapi.co/api/')

