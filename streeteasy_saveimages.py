#!/usr/bin/env python
import requests
import MySQLdb
import os
import urllib
import sys
import random
from boto.s3.connection import S3Connection
from boto.s3.key import Key

def progress_bar(complete, total):
	sys.stdout.write(".")
	sys.stdout.flush()


conn = S3Connection('AKIAJOMBIK5BKALPAVLQ', 'jP7aXFOimwHumf4oTIwhpvfwtBFnzDkRqpj5Pibv')
bucket = conn.get_bucket('referralmovephotos')
k = Key(bucket)

db = MySQLdb.connect(host="127.0.0.1",
						user="root",
						passwd="",
						db="rest")

cur = db.cursor()

cur.execute("SELECT photo,id FROM real_estate_prospects")

for row in cur.fetchall():
	data = str(row)
	strip = data.strip('(,\'L) ')
	parse = strip.split(',')
	uri = parse[0].join(parse[0].split()).strip('\'')
	uid = parse[1].join(parse[1].split())
	print uri

	if "http" in uri:
		path = '/Users/christopher/Desktop/Streeteasy_Photos/'
		tmpfilename = str(random.randint(1, 1000000000))
		fullfilename = os.path.join(path, tmpfilename+'.jpg')
		urllib.urlretrieve(uri, fullfilename)

		f = open(fullfilename)
		k.key = tmpfilename+'.jpg'
		result = k.set_contents_from_file(f, None, True, progress_bar, 10, None, False, None, None)
		k.make_public()
		f.close()
		print ' done'
		bucketurl = os.path.join('http://referralmovephotos.s3-website-us-west-2.amazonaws.com', tmpfilename+'.jpg')


	cur.execute("""UPDATE real_estate_prospects SET photo=%s WHERE id=%s""", (bucketurl, uid))
	db.commit()

	data = None
	strip = None
	parse = None
	uri = None
	uid = None
	tmpfilename = None
	fullfilename = None

db.close()