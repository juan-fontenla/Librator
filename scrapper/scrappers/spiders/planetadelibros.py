import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PlanetadelibrosSpider(CrawlSpider):
    name = 'planetadelibros'
    allowed_domains = ['planetadelibros.com']
    start_urls = ['https://www.planetadelibros.com/libros']

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    rules = (
        Rule(LinkExtractor(restrict_css='.resultat-cercador > .llibres-miniatures > li > a'),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_css='.paginacio-seguent > a'), follow=True),
        Rule(LinkExtractor(restrict_css='.tematiques > a'), follow=True),
    )

    def parse_name(self, text):
        return '' if text is None else text.lstrip().rstrip().replace('\n', '')

    def parse_text(self, text):
        return '' if text is None else text.lstrip().rstrip().replace('\n', ' ')

    def parse_item(self, response):
        price = response.css(
            'input[data-soporte="Libro"] ::attr(data-precio)').get()
        if (price is None):
            price = response.css('.preu_format::text').get()

        editorial = response.css('.segell-nom > a::text').get()
        author = response.css('.autor-info > .nom ::text').get()
        if (author is None):
            author = editorial

        isbn = response.xpath(
            '//span[@itemprop="isbn"]/text()').extract_first()
        if (isbn is None):
            isbn = response.xpath(
                '//span[@itemprop="ean13"]/text()').extract_first()

        yield {
            'Title': self.parse_name(response.css('.titol > h1 ::text').get()),
            'Category': self.parse_name(','.join(response.css('.tematica > a ::text').getall())),
            'Price': price,
            'Link': response.url,
            'Summary': self.parse_text(' '.join(response.css('.sinopsi > p ::text').getall())),
            'Author': author,
            'Editorial': editorial,
            'ISBN': isbn
        }
