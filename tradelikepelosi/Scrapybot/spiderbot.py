import scrapy
from Scrapybot.spiderbotconfig import SPIDER_NAME, SPIDER_DOMAIN, SPIDER_TARGET_URL, SPIDER_FEED_FORMAT, SPIDER_FEED_URI, SPIDER_USER_AGENT, TMP_FILE
from scrapy.crawler import CrawlerProcess

class SpiderBot(scrapy.Spider):
    # Your spider definition
    name = SPIDER_NAME
    allowed_domains = [SPIDER_DOMAIN]
    start_urls = [SPIDER_TARGET_URL]

    def parse(self, response):
        print('url:', response.url)

class SpiderBotLauncher():
    def __init__(self) -> None:
        print("\nWriting spider bot crawled data to:",SPIDER_FEED_URI,"\n")
        self.process = CrawlerProcess(    
            settings = {
                'FEEDS':{
                    SPIDER_FEED_URI:{'format': SPIDER_FEED_FORMAT, 'overwrite': True}
                }
            }
        )

    def launch(self) -> None:
        self.process.crawl(SpiderBot)
        self.process.start()  