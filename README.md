# webcrawler
Single domain webcrawler

This webcrawler is for StreetEasy.com, the NYC rental website. They have changed their DOM markup since this was created and added Capchas to their pages but this solution I used to scrape images and related rental info to be persisted in MySQL and served the images on Amazon's S3 service. 



streeteasy_scrape.py - extracts data from HTML markup and stores it in MySQL.

streeteasy_updatephotos.py - corrects the Title for each image in MySQL

streeteasy_images.py - saves images to Amazon S3 bucket

streeteasy_getlocation.py - extracts related location info for each image

from Android



