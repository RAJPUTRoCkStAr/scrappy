import scrapy


class AssembotSpider(scrapy.Spider):
    name = "assembot"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/AcResultGenJune2024/index.htm"]

    def parse(self, response):
        pass
