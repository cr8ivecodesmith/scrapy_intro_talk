import scrapy
from scrapy.loader import ItemLoader


class Product(scrapy.Item):
    title = scrapy.Field()
    current_price = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    primary_image =scrapy.Field()


class LazadaScraper(scrapy.Spider):
    name = 'lazada_scraper'
    start_urls = [
        'http://www.lazada.com.ph/catalog/?q=peanut+butter',
    ]

    def parse(self, response):
        product_grid = response.xpath(
            '//div[@data-component="product_list"]'
            '/div[contains(@class, "product-card")]'
        )

        for selector in product_grid:
            loader = ItemLoader(Product(), selector=selector)
            loader.add_xpath('title', 'a/div/div/span/@title')
            loader.add_xpath('current_price', '@data-price')
            loader.add_xpath('url', 'a/@href')
            loader.add_xpath('sku', '@data-sku')
            loader.add_xpath('primary_image', 'a/div/img/@data-original')
            yield loader.load_item()

