import scrapy
from Scrapybot.spiderbotconfig import SPIDER_NAME, SPIDER_DOMAIN, SPIDER_TARGET_URL, SPIDER_FEED_FORMAT, SPIDER_FEED_URI, SPIDER_USER_AGENT
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
        self.process = CrawlerProcess({
                'USER_AGENT': SPIDER_USER_AGENT, 
                'FEED_FORMAT': SPIDER_FEED_FORMAT, 
                'FEED_URI': SPIDER_FEED_URI,
        })

    def launch(self) -> None:
        self.process.crawl(SpiderBot)
        self.process.start()  