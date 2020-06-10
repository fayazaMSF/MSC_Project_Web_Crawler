# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'Tamilmirror'
    start_urls = [
        'http://www.tamilmirror.lk/news/175',

    ]

    def parse(self, response):
        item = MycrawlerItem()
        for news in response.xpath('//div[@class="col-md-6 cat-ite"]'):
            item['URL'] = response.url
            item['TITLE'] = news.xpath('.//div[2]/a/text()').extract_first()
            item['BODY'] = news.xpath('.//div[3]/text()').extract_first()
           # item['DATE'] = news.xpath('').extract_first()
            yield item
        # yield: collected as item, and it's come as item of output file, inforamtion need to collected need to include
        nextPages = response.xpath("//div[@class='page-nation']//li/a[contains(text(),'Next')]/@href")
        for nextPage in nextPages:
            next_page_url = response.urljoin(nextPage.extract())
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))

        return item
