import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from ubp.items import Article


class UbpspiderSpider(scrapy.Spider):
    name = 'ubpspider'
    start_urls = ['https://www.ubp.com/en/newsroom/']

    def parse(self, response):
        links = response.xpath('//a[@class="flink"]/@href').getall()
        yield from response.follow_all(links, self.parse_for_new)

    def parse_for_new(self, response):

        yield response.follow(response.url, self.parse_article, dont_filter=True)
        if 'pdf' in response.url or 'files' in response.url or 'ubp' not in response.url:
            return
        other_pages = response.xpath('//a[@class="flink"]/@href').getall()
        yield from response.follow_all(other_pages, self.parse_for_new)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()
        if 'pdf' in response.url or 'files' in response.url or 'ubp' not in response.url:
            return
        else:
            title = response.xpath('//h1/text()').get().strip() if type(
                response.xpath('//h1/text()').get()) == str else "No title"
            date = response.xpath('(//span[@class="box-date"])[1]/text()').get()
            if not date:
                return
            date = date.strip()
            date = datetime.strptime(date, '%d.%m.%Y')
            date = date.strftime('%Y/%m/%d')

            content = response.xpath('//div[@itemprop="articleBody"]//text()').getall()
            content = [text for text in content if type(text) == str and text.strip()]
            if content:
                content = "\n".join(content).strip()
            else:
                content = "No body"

        category = response.xpath('(//span[@class="box-tag"])[1]/text()').get() or \
                   response.xpath('//div[@class="box-intro-txt col-xs-11'
                                  ' col-s-12 col-md-13 col-lg-14"]//span[@class="box-tag"]/text()').get()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('category', category)

        return item.load_item()
