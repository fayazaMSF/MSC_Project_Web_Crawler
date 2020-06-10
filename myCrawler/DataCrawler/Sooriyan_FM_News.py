# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem
from scrapy import Request


def parse_page(response):
    item = MycrawlerItem()
    item['URL'] = response.meta.get('URL')
    item['TITLE'] = response.meta.get('TITLE')
    item['DATE'] = response.meta.get('DATE')
    item['BODY'] = response.xpath(
        '//div[@class="lts-txt2"]/text() | //div[@class="lts-txt2"]/div/text() | //div[@class="lts-txt2"]/p/text() | //div[@class="lts-txt2"]/div/p').extract_first()
    yield item
    # {'URL': url, 'TITLE': title, 'BODY': body, 'DATE': date}


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'Sooriyan_FM_News'
    start_urls = [
        'http://www.hirunews.lk/sooriyanfmnews/local-news.php',
        'http://www.hirunews.lk/sooriyanfmnews/international-news.php',
        'http://www.hirunews.lk/sooriyanfmnews/sports-news.php',
        'http://www.hirunews.lk/sooriyanfmnews/business-news.php',
        'http://www.hirunews.lk/sooriyanfmnews/entertainment-news.php',
    ]

    def parse(self, response):
        for news in response.xpath('//div[@class="rp-mian"]'):
            relative_url = news.xpath('.//a[contains(text(),"Read More")]/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title = news.xpath('./div[3]/a/text()').extract_first()
            date = news.xpath('./div[2]/text()').extract()
            yield Request(absolute_url, callback=parse_page, meta={'URL': response.url, 'TITLE': title, 'DATE': date},
                          dont_filter=True)

        # dont_filter (boolean) – indicates that this request should not be filtered by the scheduler. This is used when you want to perform an identical request multiple times, to ignore the duplicates filter. Use it with care, or you will get into crawling loops. Default to False.
        next_page_url = response.xpath('//div[@class="pagi"]//a[@title="next page"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    # return item
    #  yield Request(absolute_next_url, callback=self.parse)
