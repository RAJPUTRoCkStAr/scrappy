# import scrapy
# from urllib.parse import urljoin
# import csv
# from threading import Lock

# class ElectionSpider(scrapy.Spider):
#     name = "election1"
#     allowed_domains = ["results.eci.gov.in"]
#     start_urls = ["https://results.eci.gov.in/AcResultGenJune2024/index.htm"]
#     count = 0
#     lock = Lock()

#     custom_settings = {
#         'DOWNLOAD_DELAY': 2,
#         'ROBOTSTXT_OBEY': True,
#     }

#     headers = {
#         'authority': 'results.eci.gov.in',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'accept-language': 'en-US,en;q=0.9',
#         'cache-control': 'max-age=0',
#         'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
#     }

#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(url, headers=self.headers, callback=self.parse_party)

#     def parse_party(self, response):
#         # Adjusting the XPath to correctly find party URLs
#         party_urls = response.xpath('//div[@class="item"]/div/a/@href').getall()
#         self.logger.info(f'Found {len(party_urls)} parties to follow.')
#         for party_url in party_urls:
#             absolute_party_url = urljoin(response.url, party_url)
#             yield scrapy.Request(absolute_party_url, headers=self.headers, callback=self.parse_state)

#     def parse_state(self, response):
#         # Extract state URLs
#         state_urls = response.xpath('//table[@class="table"]/tbody/tr/td[2]/a/@href').getall()
#         self.logger.info(f'Found {len(state_urls)} state links to follow.')
#         for state_url in state_urls:
#             absolute_state_url = urljoin(response.url, state_url)
#             yield scrapy.Request(absolute_state_url, headers=self.headers, callback=self.parse_constituency)

#     def parse_constituency(self, response):
#         # Extract constituency URLs
#         constituency_urls = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[2]/a/@href').getall()
#         self.logger.info(f'Found {len(constituency_urls)} constituency links to follow.')
#         for constituency_url in constituency_urls:
#             absolute_constituency_url = urljoin(response.url, constituency_url)
#             constituency_name = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[2]/a/text()').get()
#             yield scrapy.Request(absolute_constituency_url, headers=self.headers, callback=self.parse_candidate, meta={'constituency_name': constituency_name})

#     def parse_candidate(self, response):
#         constituency_name = response.meta['constituency_name']
#         candidate_cards = response.xpath('//div[@class="cand-box"]')
#         finalDataList = []

#         for card in candidate_cards:
#             self.count += 1
#             finalData = {
#                 'ref': str(self.count),
#                 'constituency': constituency_name,
#                 'img_link':card.xpath('.//figure/img/@src').getall(),
#                 'won status': card.xpath('.//div[@class="cand-info"]/div/div/text()/text()').get(default='').strip(),
#                 'votes': card.xpath('.//div[@class="cand-info"]/div/div[2]/text()').get(default='').strip(),
#                 '(votes)': card.xpath('.//div[@class="cand-info"]/div/div[2]/span/text()').get(default='').strip(),
#                 'Name': card.xpath('.//div[@class="cand-info"]/div[@class="nme-prty"]/h5/text()').get(default='').strip(),
#                 'Party Name': card.xpath('.//div[@class="cand-info"]/div[@class="nme-prty"]/h6/text()').get(default='').strip()
#             }
#             finalDataList.append(finalData)

#         # Write each candidate's data to the CSV file in a thread-safe manner
#         self.write_to_csv(finalDataList)

#         yield from finalDataList

#     def write_to_csv(self, data_list):
#         with self.lock:
#             with open('2ndpagedata.csv', mode='a', newline='', encoding='utf-8') as csv_file:
#                 fieldnames = ['ref', 'constituency','image','won status', 'votes', '(votes)', 'Name', 'Party Name']
#                 writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#                 if csv_file.tell() == 0:
#                     writer.writeheader()
#                 for data in data_list:
#                     writer.writerow(data)


import scrapy
from urllib.parse import urljoin
import csv
from threading import Lock

class ElectionSpider(scrapy.Spider):
    name = "election1"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/AcResultGenJune2024/index.htm"]
    count = 0
    lock = Lock()

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': True,
    }

    headers = {
        'authority': 'results.eci.gov.in',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_party)

    def parse_party(self, response):
        party_urls = response.xpath('//div[@class="item"]/div/a/@href').getall()
        self.logger.info(f'Found {len(party_urls)} parties to follow.')
        for party_url in party_urls:
            absolute_party_url = urljoin(response.url, party_url)
            yield scrapy.Request(absolute_party_url, headers=self.headers, callback=self.parse_state)

    def parse_state(self, response):
        state_urls = response.xpath('//table[@class="table"]/tbody/tr/td[2]/a/@href').getall()
        self.logger.info(f'Found {len(state_urls)} state links to follow.')
        for state_url in state_urls:
            absolute_state_url = urljoin(response.url, state_url)
            yield scrapy.Request(absolute_state_url, headers=self.headers, callback=self.parse_constituency)

    def parse_constituency(self, response):
        constituency_urls = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[2]/a/@href').getall()
        self.logger.info(f'Found {len(constituency_urls)} constituency links to follow.')
        for constituency_url in constituency_urls:
            absolute_constituency_url = urljoin(response.url, constituency_url)
            constituency_name = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[2]/a/text()').get()
            yield scrapy.Request(absolute_constituency_url, headers=self.headers, callback=self.parse_candidate, meta={'constituency_name': constituency_name})

    def parse_candidate(self, response):
        constituency_name = response.meta['constituency_name']
        state_name = response.xpath('//div[@class="page-title"]/h2/span/strong/text()').get()
        candidate_cards = response.xpath('//div[@class="cand-box"]')
        finalDataList = []

        for card in candidate_cards:
            self.count += 1
            finalData = {
                'ref': str(self.count),
                'state': state_name,
                'constituency': constituency_name,
                'img_link': card.xpath('.//figure/img/@src').get(),
                'won_status': card.xpath('./div[@class="cand-info"]/div/div[1]/text()').get(default='').strip(),
                'votes': card.xpath('./div[@class="cand-info"]/div/div[2]/text()').get(default='').strip(),
                'votes_percentage': card.xpath('./div[@class="cand-info"]/div/div[2]/span/text()').get(default='').strip(),
                'name': card.xpath('./div[@class="cand-info"]/div[@class="nme-prty"]/h5/text()').get(default='').strip(),
                'party_name': card.xpath('./div[@class="cand-info"]/div[@class="nme-prty"]/h6/text()').get(default='').strip()
            }
            finalDataList.append(finalData)

        self.write_to_csv(finalDataList)

        yield from finalDataList

    def write_to_csv(self, data_list):
        with self.lock:
            with open('secpageda.csv', mode='a', newline='', encoding='utf-8') as csv_file:
                fieldnames = ['ref','state','constituency', 'img_link', 'won_status', 'votes', 'votes_percentage', 'name', 'party_name']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                if csv_file.tell() == 0:
                    writer.writeheader()
                for data in data_list:
                    writer.writerow(data)
