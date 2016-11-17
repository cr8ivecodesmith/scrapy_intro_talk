import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Product(scrapy.Item):
    title = scrapy.Field()
    current_price = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    primary_image =scrapy.Field()


class LazadaCrawler(CrawlSpider):
    name = 'lazada_crawler'
    start_urls = [
        'http://www.lazada.com.ph/catalog/?q=peanut+butter',
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=(
                    r'(.+)page=[\d]+(.+)',
                ),
                restrict_xpaths=(
                    r'//div[@class="c-paging__wrapper"]/a',
                ),
            ),
            callback='parse_page',
        ),
    ]

    def parse_page(self, response):
        product_grid = response.xpath(
            '//div[@data-component="product_list"]'
            '/div[contains(@class, "product-card")]'
        )

        for selector in product_grid:
            yield self.parse_item(selector)

    def parse_item(self, selector):
        loader = ItemLoader(Product(), selector=selector)
        loader.add_xpath('title', 'a/div/div/span/@title')
        loader.add_xpath('current_price', '@data-price')
        loader.add_xpath('url', 'a/@href')
        loader.add_xpath('sku', '@data-sku')
        loader.add_xpath('primary_image', 'a/div/img/@data-original')
        return loader.load_item()
