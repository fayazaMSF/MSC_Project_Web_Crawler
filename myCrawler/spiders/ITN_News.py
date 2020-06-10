# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'ITN'
    start_urls = [
        'http://www.itnnews.lk/ta/local/',
        'http://www.itnnews.lk/ta/international/',
        'http://www.itnnews.lk/ta/entertainment/',
        'http://www.itnnews.lk/ta/business/',
        'http://www.itnnews.lk/ta/sports/',
        'https://www.bbc.com/tamil/arts_and_culture',
    ]

    def parse(self, response):
        item = MycrawlerItem()
        for news in response.xpath('//div[@class="article-content"]'):
            item['URL'] = response.url
            item['TITLE'] = news.xpath('./h2/a/text()').extract_first()
            item['BODY'] = news.xpath('./p/text()').extract_first()
            item['DATE'] = news.xpath('./span/a/text()').extract()
            yield item
        # yield: collected as item, and it's come as item of output file, inforamtion need to collected need to include
        next_page_url = response.xpath('//a[contains(text(),"Next Page")]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

        return item
