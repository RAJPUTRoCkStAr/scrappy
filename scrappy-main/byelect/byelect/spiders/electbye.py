import scrapy


class ElectbyeSpider(scrapy.Spider):
    name = "electbye"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/AcResultByeJune2024/index.htm"]


    custom_settings = {
        'FEED_FORMAT':"csv",
       'FEED_URI' : 'data.csv'
   }
    def parse(self, response):
        cityname = response.xpath('//div[@class="box-content"]/h3/text()').extract()
        statname = response.xpath('//div[@class="box-content"]/h4/text()').extract()
        re = response.xpath('//div[@class="box-content"]/h2/text()').extract()
        pname = response.xpath('//div[@class="box-content"]/h5/text()').extract()
        parname = response.xpath('//div[@class="box-content"]/h6/text()').extract()

        for nme in zip(cityname,statname,re,pname,parname):
            data =  {
                'cityname': nme[0],
               'statname': nme[1],
               're': nme[2],
                'pname': nme[3],
                'parname': nme[4],
            }
            yield data
