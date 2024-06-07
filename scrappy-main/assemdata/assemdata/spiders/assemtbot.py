import scrapy


class AssemtbotSpider(scrapy.Spider):
    name = "assemtbot"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/AcResultGenJune2024/index.htm"]

    custom_settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'assemtbot.csv',
    }

    def parse(self, response):
        statename = response.xpath('//div[@class="item"]/div/a/h2/text()').extract()
        totalse = response.xpath('//div[@class="item"]/div/a/ul/li/span[2]/text()').extract()
        partiesname = response.xpath('//div[@class="pr-row"]/div[1]/text()').extract()
        partieseat = response.xpath('//div[@class="pr-row"]/div[2]/text()').extract()

        for assemdata in zip(statename,totalse,partiesname,partieseat):
            res = {
                'statename': assemdata[0],
                'total_seats': assemdata[1],
                'partiesname': assemdata[2],
                'partieseat': assemdata[3],
            }
            yield res