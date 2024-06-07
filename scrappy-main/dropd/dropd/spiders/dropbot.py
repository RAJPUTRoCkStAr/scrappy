import scrapy


class DropbotSpider(scrapy.Spider):
    name = "dropbot"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/PcResultGenJune2024/index.htm"]

    custom_settings = {
        'FEED_FORMAT':"csv",
       'FEED_URI' : 'dropdata.csv'
   }

    def parse(self, response):
        pass
