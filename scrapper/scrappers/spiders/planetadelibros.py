from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrappers.items import BookItem
from scrapy_splash import SplashRequest

class PlanetadelibrosSpider(CrawlSpider):
    name = 'planetadelibros'
    allowed_domains = ['planetadelibros.com']
    start_urls = ['https://www.planetadelibros.com/libros']

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    
    script = """
        function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(1))
        return splash:html()
        end
    """
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url, callback = self.parse_category, endpoint='execute',
                args={'wait': 1, 'lua_source': self.script}
            )

    def parse_category(self, response):
        for url in response.css('.tematiques > a::attr(href)').extract():
            yield SplashRequest(
                url, callback = self.parse_book, endpoint='execute',
                args={'wait': 1, 'lua_source': self.script},
                meta= {'books': []}
            )

    def parse_book(self, response):
        print(response.css('.paginacio-numeros >span::text').get())
        try:
            page = response.css('.paginacio-numeros >span::text').get()
            if(page is None):
                page = 0
            else:
                page = int(page)
        except ValueError:
            page = 0
        
        if( page <= 5):
            books_links = response.css('.resultat-cercador > .llibres-miniatures > li > a::attr(href)').extract()
            for url in response.css('.paginacio-seguent > a::attr(href)').extract():
                if (response.meta["books"] is not None):
                    response.meta["books"].append(books_links)
                else:
                    response.meta["books"] = []
                yield SplashRequest(
                    url, callback = self.parse_book, endpoint='execute',
                    args={'wait': 0.5, 'lua_source': self.script},
                    meta = {'books': response.meta["books"]}
                )
        else:
            for books in response.meta["books"]:
                for book in books:
                    yield SplashRequest(
                        book, callback = self.parse_item, endpoint='execute',
                        args={'wait': 0.5, 'lua_source': self.script}
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
        isbn = isbn.replace("-", "")

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
