# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'Thinakaran'
    start_urls = [
        'http://www.thinakaran.lk/news',
        'http://www.thinakaran.lk/political',
        'http://www.thinakaran.lk/business',
        'http://www.thinakaran.lk/world',
        'http://www.thinakaran.lk/legal-police',
        'http://www.thinakaran.lk/sport',
        'http://www.thinakaran.lk/gossip',
        'http://www.thinakaran.lk/Technology',
    ]

    def parse(self, response):
        item = MycrawlerItem()
        for news in response.xpath('//div[@class="region region-promoted"]'):
            item['URL'] = response.url
            item['TITLE'] = news.xpath('.//div[@class="views-field views-field-title text-justify"]/span/a/text()').extract_first()
            item['BODY'] = news.xpath(
                './/div[@class="views-field views-field-body text-justify  padding-right-zero"]/span/text()').extract_first()
            item['DATE'] = news.xpath('.//div[@class="views-field views-field-field-date-publishing"]/div/text()').extract_first()
            yield item

        for news in response.xpath('//div[@id="block-system-main"]//li'):
            item['URL'] = response.url
            item['TITLE'] = news.xpath('./div[2]/span/a/text()').extract_first()
            item['BODY'] = news.xpath(
                    './div[3]/span/text()').extract_first()
            item['DATE'] = news.xpath(
                    './div[4]/div/text()').extract_first()
            yield item
        for news in response.xpath('//div[@id="content-footer-inside"]//ul[@class="item"]/li'):
            item['URL'] = response.url
            item['TITLE'] = news.xpath('./div[2]/span/a/text()').extract_first()
            item['BODY'] = news.xpath(
                    './div[3]/span/text()').extract_first()
            item['DATE'] = news.xpath('./div[4]/div/text()').extract()
            yield item

        # yield: collected as item, and it's come as item of output file, inforamtion need to collected need to include

        #nextPages = response.xpath("//ul[@class='pagination']/li/a/@href")
        #for nextPage in nextPages:
          #  next_page_url = response.urljoin(nextPage.extract())
           # if next_page_url is not None:
            #    yield scrapy.Request(response.urljoin(next_page_url))

        #for news in response.xpath('/div[@id="block-system-main"]'):
         #   yield response.follow(news, self.parse_News)

        #return item