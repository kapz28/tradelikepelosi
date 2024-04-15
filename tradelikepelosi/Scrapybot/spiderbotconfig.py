import os
import sys

TMP_FILE = os.path.join(os.path.join(os.getcwd(),"spiderbotdatadump"), '{}.csv'.format("datadump"))
SPIDER_NAME = 'PelosiBot'
SPIDER_TARGET_URL = 'https://disclosures-clerk.house.gov/FinancialDisclosure#'
SPIDER_DOMAIN = 'disclosures-clerk.house.gov'
SPIDER_USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
SPIDER_FEED_FORMAT = 'CSV'
SPIDER_FEED_URI = TMP_FILE