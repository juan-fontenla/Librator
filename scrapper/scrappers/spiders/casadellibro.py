
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request


class CasadellibroSpider(CrawlSpider):
    name = 'casadellibro'
    allowed_domains = ['casadellibro.com']
    start_urls = ['http://casadellibro.com/libros']

    custom_settings = {

        'FEED_EXPORT_ENCODING': 'utf-8',

    }
    
    rules = (
        Rule(LinkExtractor(restrict_css='div.col.col-11 > a'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_css='link[rel="next"]'), follow=True),
        Rule(LinkExtractor(restrict_css='.row > div.col-12.col-sm-6.col-md-3 > a'), follow=True),
    )


    def parse_name(self, text):
        return '' if text is None else text.lstrip().rstrip().replace('\n', '')

    def parse_text(self, text):
        return '' if text is None else text.lstrip().rstrip().replace('\n', ' ')

    def parse_ebook(self, response):
        yield {
            'Ebook-price' : response.css('script[data-n-head="ssr"]::text').re_first('"Price":"([\d*\.?\d*]*)"'),
            'Link': response.url
        }
    def get_ebook(self, link):
        print(self, link)
        return Request(link, callback=self.parse_ebook)

    def parse_item(self, response):
        # \\\"Price\\\":\\\"14.20\\\
        price =  response.css('script[data-n-head="ssr"]::text').re_first('"Price":"([\d*\.?\d*]*)"')
        ebookLink = response.css('a[href^="/ebook-"]::attr(href)').extract()
        print(ebookLink)


        yield {
            'Title': self.parse_name(response.css('.product-info > h1 ::text').get()),
            'Category': ','.join(map(self.parse_name, response.css('a > .v-chip__content ::text').getall())),
            'Price': price,
            'Stock': self.parse_name(response.css('div > #disponibilidadproducto ::text').get()),
            'Link': response.url,
            'ebook': self.get_ebook(ebookLink),
            'Summary': self.parse_text(response.css('.dataproduct > .col-md-8 > div > .text-container > div *::text').get()),
            'Author': response.css('meta[property="book:author"] ::attr(content)').get(),
        }
