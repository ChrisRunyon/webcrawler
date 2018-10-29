#!/usr/bin/env python
from lxml import html
import requests
import MySQLdb

requestor = [0]*124
for x in xrange(1, len(requestor), 1):
	print x
	page = requests.get('http://streeteasy.com/houses/nyc?page=' + str(x))
	tree = html.fromstring(page.content)
	photos = tree.xpath('//div[@class="photo"]//img[@data-performance-mark="search.Sales.listingImageVisible"]/@data-original')
	titles = tree.xpath('//a[@data-gtm-listing-type="sale"]/text()')
	prices = tree.xpath('//span[@class="price"]/text()')
	beds = tree.xpath('//span[@class="first_detail_cell"]/text()')
	#baths = tree.xpath('//span[@class="detail_cell"]/text()')
	sqfts = tree.xpath('//span[@class="last_detail_cell"]/text()')
	links = tree.xpath('//div[@class="details-title"]//a[@data-gtm-listing-type="sale"]/@href')
	#locale = tree.xpath("//div[re:match(text(), 'in')]", namespaces={"re": "http://exslt.org/regular-expressions"})
	encode_beds = []
	encode_sqft = []

	print 'Photo: ', photos
	print 'Title: ', len(titles)
	print 'Info: ', len(prices)
	print 'Beds: ', len(beds)
	#print 'Baths: ', len(baths)
	print 'SqFt: ', len(sqfts)
	print 'Link: ', len(links)
	#print 'Locale: ', locale

	for j in xrange(len(beds)):
		encode_beds.append(beds[j].encode('UTF-8'))
		#print beds[k]

	for k in xrange(len(sqfts)):
		encode_sqft.append(sqfts[k].encode('UTF-8'))
		#print encode_sqft[t]

	db = MySQLdb.connect(host="127.0.0.1",
						 user="root",
						 passwd="",
						 db="rest",
						 use_unicode=True,
						 charset='utf8')

	cur = db.cursor()

	for i in xrange(0, len(titles)):
		try:
			encode_beds[i+1]
		except IndexError:
			encode_beds.append(None)

		try:
			encode_sqft[i+1]
		except IndexError:
			encode_sqft.append(None)

		#print encode_beds[i]
		#print encode_sqft[i]
		cur.execute("INSERT INTO real_estate_prospects(photo, title, price, beds, sqft, link) VALUES (%s, %s, %s, %s, %s, %s)" , (photos[i], titles[i], prices[i], encode_beds[i], encode_sqft[i], links[i]))
		#cur.execute("""UPDATE real_estate_sales SET photo=%s WHERE title=%s""", (photo[i], ))


	db.commit()

	page = None
	tree = None
	photos = None
	titles = None
	prices = None
	beds = None
	sqfts = None
	links = None
	encode_sqft = None
	encode_beds = None

db.close()