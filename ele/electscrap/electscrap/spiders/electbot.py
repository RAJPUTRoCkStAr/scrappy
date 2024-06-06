import scrapy
from electscrap.items import ElectionResultItem, DetailedResultItem, ResdataItem,ThirddataItem

class ElectbotSpider(scrapy.Spider):
    name = "electbot"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/PcResultGenJune2024/index.htm"]

    def parse(self, response): # main page table
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
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse_next_page)

    def parse_next_page(self, response): # won link data
        Sno = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[1]//text()').extract()
        partycon = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[2]//text()').extract()
        Winca = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[3]//text()').extract()
        Tos = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[4]//text()').extract()
        Marn = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[5]//text()').extract()
        Link2 = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td/a/@href').getall()

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
            if second_page:
                yield scrapy.Request(url=second_page, callback=self.parse_second_page)

    def parse_second_page(self, response): # name link data
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
    def parse_assembly(self, response):
        # Correctly capture the assembly link and follow it
        link3 = response.xpath('//div[@class="custom-tabs"]/ul/li[2]/a/@href').get()
        if link3:
            third_page = response.urljoin(link3)
            yield scrapy.Request(url=third_page, callback=self.third_next_page)

    def third_next_page(self, response):
        Tstate = response.xpath('//div[@class="item"]/div/a/h2/text()').extract()
        Tas = response.xpath('//div[@class="item"]/div/a/ul/li/span[2]/text()').extract()
        Tparties = response.xpath('//div[@class="item"]/div/div/div/a/div[2]/div[1]/text()').extract()
        Tpartiesnumber = response.xpath('//div[@class="item"]/div/div/div/a/div[2]/div[2]/text()').extract()

        for dat in zip(Tstate, Tas, Tparties, Tpartiesnumber):
            resp_data = ThirddataItem(
                PartyState=dat[0],
                TotalSeat=dat[1],
                PartyName=dat[2],
                PartyTotalNumber=dat[3],
            )
            yield resp_data