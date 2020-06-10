# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'bbc'
    start_urls = [
        'https://www.bbc.com/tamil/sri_lanka',
        'https://www.bbc.com/tamil/global',
        'https://www.bbc.com/tamil/india',
        'https://www.bbc.com/tamil/science',
        'https://www.bbc.com/tamil/sport',
        'https://www.bbc.com/tamil/arts_and_culture',
        # 'https://www.bbc.com/tamil/topics/2611f753-ece7-47ea-9782-f912bc1e4088',
        # 'https://www.bbc.com/tamil/media/audio',
        # 'https://www.bbc.com/tamil/media/video',
        # 'https://www.bbc.com/tamil/media/photogalleries',
    ]

    # def parse(self, response):
    # The main method of the spider. It scrapes the URL(s) specified in the
    # 'start_url' argument above. The content of the scraped URL is passed on
    # as the 'response' object.

    # This loops through all the URLs found inside an element of class
    # for news in response.xpath('//a[@class="title-link"]/ancestor::div[1]'):
    #    yield {
    #       'URL':response.url,
    #      'TITLE': news.xpath('./a//span/text()').extract_first(),
    #     'BODY': news.xpath('./p[@class="eagle-item__summary"]').extract_first(),
    #  'DATE': news.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
    #  }
    # yield: collected as item, and it's come as item of output file, inforamtion need to collected need to include
    #   next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
    #   if next_page_url is not None:
    #       yield scrapy.Request(response.urljoin(next_page_url))

    def parse(self, response):
        item = MycrawlerItem()
        for news in response.xpath('//a[@class="title-link"]/ancestor::div[1]'):
            item['URL'] = response.url
            item['TITLE'] = news.xpath('./a/h3[@class="title-link__title"]/span/text()').extract_first()
            item['BODY'] = news.xpath('./p[@class="eagle-item__summary"]/text()').extract_first()
            item['DATE'] = news.xpath('.//li[@class="mini-info-list__item"]/div[@data-datetime]/text()').extract_first()
            yield item
        # yield: collected as item, and it's come as item of output file, inforamtion need to collected need to include
        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

        return item
