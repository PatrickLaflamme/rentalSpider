import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import boto
import time

os.chdir("rentalSpider")

testfile = time.strftime("%Y-%m-%d") + ".log"

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('rentals')
process.start() # the script will block here until the crawling is finished

import boto
import boto.s3
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = "AKIAJNTWU2B6PICHAC5A"
AWS_SECRET_ACCESS_KEY = "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"

bucket_name = 'rentalspider'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)


bucket = conn.get_bucket(bucket_name)

k = Key(bucket)
k.key = 'Data/logs/' + testfile
k.set_contents_from_filename(testfile)

os.rename(testfile, "../logs/"+testfile)
