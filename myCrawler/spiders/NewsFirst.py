# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem
from scrapy import Request


def parse_main_news(response):
    item = MycrawlerItem()
    item['URL'] = response.meta.get('URL')
    item['TITLE'] = response.xpath('.//div[@class="main-news-heading visible-xs visible-sm"]/h1/text()').extract_first()
    item['DATE'] = response.meta.get('DATE')
    item['BODY'] = response.xpath('//div[@class="text-left w-300 editor-styles"]/p/text()').extract_first()
    return item


def parse_sub_news(response):
    item = MycrawlerItem()
    item['URL'] = response.meta.get('URL')
    item['TITLE'] = response.xpath('//div[@class="main-news-heading visible-xs visible-sm"]/h1/text()').extract_first
    item['DATE'] = response.meta.get('DATE')
    item['BODY'] = response.xpath('//div[@class="lts-txt2"]/text()').extract_first()
    return item

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'News_First'
    start_urls = [
        'https://www.newsfirst.lk/tamil/category/local/',
        'https://www.newsfirst.lk/tamil/category/world/',
        'https://www.newsfirst.lk/tamil/category/sports/',
        'https://www.newsfirst.lk/tamil/category/business/',
        'https://www.newsfirst.lk/tamil/category/entertainment/',
    ]

    def parse(self, response):
        items = []
        for news in response.xpath('//div[@class="col-md-12 news-lf-section"]'):
            relative_url = news.xpath('.//div//h1/ancestor::div[1]/a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title = news.xpath('./div//h1/text()').extract_first()
            date = news.xpath('./div//p/text()').extract_first()
            yield Request(absolute_url, callback=parse_main_news, meta={'URL': response.url, 'DATE': date}, dont_filter = True)

        for news in response.xpath('//div[@class="sub-1-news-heading"]/ancestor::div[2]'):
            relative_url = news.xpath('./div/a[2]/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title = news.xpath('./div/a[2]/div/h2/text()').extract_first()
            date = news.xpath('.//div//p/text()').extract_first()
            yield Request(absolute_url, callback=parse_main_news,
                          meta={'URL': response.url, 'DATE': date}, dont_filter=True)

        next_page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

       # return item
    #  yield Request(absolute_next_url, callback=self.parse)

