#!/usr/bin/env python
from lxml import html
import requests
import MySQLdb

results = []

db = MySQLdb.connect(host="127.0.0.1",
						user="root",
						passwd="",
						db="rest")

cur = db.cursor()

cur.execute("SELECT link FROM real_estate_prospects")

for row in cur.fetchall():
	data = str(row)
	uri = data.strip('(,\')')

	print row[0]
	page = requests.get('http://streeteasy.com/' + uri)
	tree = html.fromstring(page.content)

	location =  tree.xpath('//p[@class="backend_data"]/text()')

	#parse[0]
	try:
		parse = location[1].split(',')
		city = parse[0].strip()
		print city

		#zipcode[1] + zipcode[2]
		zipcode = parse[1].split(' ')
		print zipcode[2]
	except:
		print 'out of index range'

	cur.execute("""UPDATE real_estate_prospects SET city=%s, state=%s, zipcode=%s WHERE link=%s""", (city, zipcode[1], zipcode[2], row))

db.commit()

db.close()