from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrappers.items import BookItem

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

        if (price is not None):
            price = float(price.strip().replace('€', '').replace(',', '.'))

        editorial = response.css('.segell-nom > a::text').get()
        author = response.css('.autor-info > .nom ::text').get()
        if (author is None):
            author = editorial

        isbn = response.xpath(
            '//span[@itemprop="isbn"]/text()').extract_first()

        if (isbn is not None):
            item = BookItem()
            item['title'] = self.parse_name(response.css('.titol > h1 ::text').get())
            item['category'] = response.css('.tematica > a ::text').getall()
            item['price'] = price
            item['link'] = response.url
            item['photo'] = response.css('#imatge-portada > div > span > img::attr(src)').get()
            item['summary'] = self.parse_text(' '.join(response.css('.sinopsi > p ::text').getall()))
            item['author'] = author
            item['editorial'] = editorial
            item['isbn'] = isbn
            item['source'] = 'planetadelibros'
            yield item
