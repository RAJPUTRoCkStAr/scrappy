# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ElectionResultItem(scrapy.Item):
    Party = scrapy.Field()
    Won = scrapy.Field()
    Leading = scrapy.Field()
    Total = scrapy.Field()
    link = scrapy.Field()

class DetailedResultItem(scrapy.Item):
    SerialNo = scrapy.Field()
    ParliamentConstituency = scrapy.Field()
    WinningCandidate = scrapy.Field()
    TotalVotes = scrapy.Field()
    Margin = scrapy.Field()
    link2 = scrapy.Field()

class ResdataItem(scrapy.Item):
    Statename = scrapy.Field()
    Cityname = scrapy.Field()
    Result = scrapy.Field()
    Gained = scrapy.Field()
    Outof = scrapy.Field()
    Name = scrapy.Field()
    WonParty = scrapy.Field()


