import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ElcorteinglesSpider(CrawlSpider):
    name = 'elcorteingles'
    allowed_domains = ['elcorteingles.es']
    start_urls = ['https://www.elcorteingles.es/libros/1/']

    rules = (
        Rule(LinkExtractor(restrict_css='.product_link'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_css='link[rel="next"]'), follow=True),
    )

    def parse_name(self, text):
        return '' if text is None else text.lstrip().rstrip().replace('\n', '')

    def parse_text(self, text):
        return '' if text is None else text.lstrip().rstrip().replace('\n', ' ')

    def parse_item(self, response):
        yield {
            'Title': self.parse_name(response.css('.titol > h1 ::text').get()),
            'Category': self.parse_name(','.join(response.css('.tematica > a ::text').getall())),
            'Price': response.css('input[data-soporte="Libro"] ::attr(data-precio)').get(),
            'Link': response.url,
            'Summary': self.parse_text(' '.join(response.css('.sinopsi > p ::text').getall())),
            'Author': response.css('.autor-info > .nom ::text').get(),
        }
