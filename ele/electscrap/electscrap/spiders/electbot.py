import scrapy
from electscrap.items import ElectionResultItem, DetailedResultItem, ResdataItem

class ElectbotSpider(scrapy.Spider):
    name = "electbot"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/PcResultGenJune2024/index.htm"]

    def parse(self, response): 
        Party = response.xpath('//table[@class="table"]/tbody/tr/td[1]/text()').extract()
        Won = response.xpath('//table[@class="table"]/tbody/tr/td[2]/a/text()').extract()
        Leading = response.xpath('//table[@class="table"]/tbody/tr/td[3]//text()').extract()
        Total = response.xpath('//table[@class="table"]/tbody/tr/td[4]/text()').extract()
        Link = response.xpath('//table[@class="table"]/tbody/tr/td/a/@href').extract()

        for item in zip(Party, Won, Leading, Total, Link):
            election_result = ElectionResultItem(
                Party=item[0],
                Won=item[1],
                Leading=0,
                Total=item[3],
                link=item[4],
            )
            yield election_result

            next_page = response.urljoin(item[4])
            self.logger.info(f'Following next page: {next_page}')
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse_next_page)

    def parse_next_page(self, response): 
        Sno = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[1]//text()').extract()
        partycon = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[2]//text()').extract()
        Winca = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[3]//text()').extract()
        Tos = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[4]//text()').extract()
        Marn = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[5]//text()').extract()
        Link2 = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td/a/@href').extract()

        for data in zip(Sno, partycon, Winca, Tos, Marn, Link2):
            detailed_result = DetailedResultItem(
                SerialNo=data[0],
                ParliamentConstituency=data[1],
                WinningCandidate=data[2],
                TotalVotes=data[3],
                Margin=data[4],
                link2=data[5],
            )
            yield detailed_result

        for link in Link2:
            second_page = response.urljoin(link)
            self.logger.info(f'Following second page: {second_page}')
            if second_page:
                yield scrapy.Request(url=second_page, callback=self.parse_second_page)

    def parse_second_page(self, response): 
        result = response.xpath('//div[@class="cand-info"]/div/div[1]/text()').extract()
        gained = response.xpath('//div[@class="cand-info"]/div[1]/div[2]/text()').extract()
        outof = response.xpath('//div[@class="cand-info"]/div[1]/div[2]/span/text()').extract()
        name = response.xpath('//div[@class="cand-info"]/div[2]/h5/text()').extract()
        wparty = response.xpath('//div[@class="cand-info"]/div[2]/h6/text()').extract()

        for res in zip(result, gained, outof, name, wparty):
            res_data = ResdataItem(
                Result=res[0],
                Gained=res[1],
                Outof=res[2],
                Name=res[3],
                WonParty=res[4]
            )
            yield res_data

        # Additionally, loop through all links in Link2 for the next request
        Link2 = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td/a/@href').extract()
        for link in Link2:
            next_second_page = response.urljoin(link)
            self.logger.info(f'Following additional second page: {next_second_page}')
            if next_second_page:
                yield scrapy.Request(url=next_second_page, callback=self.parse_second_page)
