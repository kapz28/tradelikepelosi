import os
import sys

TMP_FILE = os.path.join(os.path.join(os.getcwd(),"spiderbotdatadump"), '{}.csv'.format("datadump"))
SPIDER_NAME = 'PelosiBot'
SPIDER_TARGET_URL = 'https://disclosures-clerk.house.gov/FinancialDisclosure#'
SPIDER_DOMAIN = 'disclosures-clerk.house.gov'
SPIDER_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
SPIDER_FEED_FORMAT = 'csv'
SPIDER_FEED_URI = TMP_FILE