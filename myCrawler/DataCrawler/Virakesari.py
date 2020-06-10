# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'Virakesari'
    start_urls = [
        'http://www.virakesari.lk/category/local',
        'http://www.virakesari.lk/category/world',
        'http://www.virakesari.lk/category/business',
        'http://www.virakesari.lk/category/technology',
        'http://www.virakesari.lk/category/sports',
        'http://www.virakesari.lk/category/cinema',
    ]

    def parse(self, response):
        item = MycrawlerItem()
        for news in response.xpath('//div[@class="media-body"]'):
            item['URL'] = response.url
            item['TITLE'] = news.xpath('.//a/h4/text()').extract_first()
            item['BODY'] = news.xpath('.//p/text()').extract_first()
            item['DATE'] = news.xpath('.//div/text()').extract_first()
            yield item
        # yield: collected as item, and it's come as item of output file, inforamtion need to collected need to include
        nextPages = response.xpath("//ul[@class='pagination']/li/a/@href")
        for nextPage in nextPages:
            next_page_url = response.urljoin(nextPage.extract())
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))

        return item
