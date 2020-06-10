# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'Thinakkural'
    start_urls = [
        'http://thinakkural.lk/article/category/local',
        'http://thinakkural.lk/article/category/world',
        'http://thinakkural.lk/article/category/business',
        'http://thinakkural.lk/article/category/technology',
        'http://thinakkural.lk/article/category/sports',
        'http://thinakkural.lk/article/category/cinema',
        'http://thinakkural.lk/article/category/medicine',
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
        for news in response.xpath('//article'):
            item['URL'] = response.url
            item['TITLE'] = news.xpath('./text()').extract_first()
            item['BODY'] = news.xpath('.//div[@class="entry-content"]/text()').extract_first()
            item['DATE'] = news.xpath('.//span[@class="entry-date post-date"]/abbr/text()').extract()
            yield item
        # yield: collected as item, and it's come as item of output file, inforamtion need to collected need to include
        nextPages = response.xpath("//div[@class='wp-pagenavi iegradient']/a/@href")
        for nextPage in nextPages:
            next_page_url = response.urljoin(nextPage.extract())
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))

        return item
