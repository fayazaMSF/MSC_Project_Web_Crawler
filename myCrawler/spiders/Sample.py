import scrapy
from scrapy import Request
from myCrawler.items import MycrawlerItem

class BBCSpider(scrapy.Spider):
    name = "BBC"
    #allowed_domains = ["https://www.bbc.com"]
    start_urls = [
        'https://www.bbc.com/tamil/sri_lanka',
        'https://www.bbc.com/tamil/global',
        'https://www.bbc.com/tamil/india',
        'https://www.bbc.com/tamil/science',
        'https://www.bbc.com/tamil/sport',
        'https://www.bbc.com/tamil/arts_and_culture',
    ]

    def parse(self, response):
        item = MycrawlerItem()
        all_News = response.xpath('//a[@class="title-link"]/ancestor::div[1]')

        for news in all_News:
            relative_url = news.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title = news.xpath('./a//span/text()').extract_first()
            date = news.xpath('.//li[@class="mini-info-list__item"]/div[@data-datetime]/text()').extract_first()

            yield Request(absolute_url, callback=self.parse_page,
                          meta={'URL': absolute_url, 'TITLE': title, 'DATE': date})

      #  relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
      #  absolute_next_url = "https://newyork.craigslist.org" + relative_next_url

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

       # return item
      #  yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('TITLE')
        date = response.meta.get('DATE')
        body = response.xpath('.//div[@class="story-body"]/p/text()').extract_first()
        yield {'URL': url, 'TITLE': title, 'BODY': body, 'DATE': date}
