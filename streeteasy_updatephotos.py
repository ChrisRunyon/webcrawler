#!/usr/bin/env python
from lxml import html
import requests
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1",
							user="root",
							passwd="",
							db="rest")

cur = db.cursor()

requestor = [0]*124
for x in xrange(1, len(requestor), 1):
	print x
	page = requests.get('http://streeteasy.com/houses/nyc?page=' + str(x))
	tree = html.fromstring(page.content)
	photos = tree.xpath('//div[@class="photo"]//img[@data-performance-mark="search.Sales.listingImageVisible"]/@data-original')
	titles = tree.xpath('//a[@data-gtm-listing-type="sale"]/text()')

	cur.execute("SELECT title FROM real_estate_prospects")

	for row in cur.fetchall():
		data = str(row)
		print data[0]

		for i in xrange(0, len(titles), 1):
			if data == titles[i]:

				cur.execute("""UPDATE real_estate_prospects SET photo=%s WHERE title=%s""", (photo[i], data))

		#uri = data.strip('(,\')')

		#print row[0]
		#page = requests.get('http://streeteasy.com/' + uri)
		#tree = html.fromstring(page.content)

		#location =  tree.xpath('//p[@class="backend_data"]/text()')

		#parse[0]
		#try:
			#parse = location[1].split(',')
			#city = parse[0].strip()
			#print city

			#zipcode[1] + zipcode[2]
			#zipcode = parse[1].split(' ')
			#print zipcode[2]
		#except:
			#print 'out of index range'

		#cur.execute("""UPDATE real_estate_sales SET city=%s, state=%s, zipcode=%s WHERE link=%s""", (city, zipcode[1], zipcode[2], row))

		#db.commit()

db.close()