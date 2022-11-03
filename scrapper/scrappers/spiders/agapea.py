
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy_splash import SplashRequest

class AgapeaSpider(Spider):
    name = 'agapea'
    books = []
    allowed_domains = ['agapea.com']
    start_urls = 'https://www.agapea.com/'

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    script = """
            function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            local element = splash:select('#click')
            if(not(element == NIL)) then
                element.mouse_click()
                assert(splash:wait(0.5))
            end

            return splash:html()
            end
        """
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url, callback = self.parse_category, endpoint='execute',
                args={'wait': 2.5, 'lua_source': self.script}
            )


    def parse_name(self, text):
        return '' if text is None else text.lstrip().rstrip().replace('\n', '')

    def parse_text(self, text):
        return '' if text is None else text.lstrip().rstrip().replace('\n', ' ')

    def parse_category(self, response) :
        for url in response.css('.nav-list > li > a::attr(href)').extract():
            yield SplashRequest(
                self.start_requests[0] + url, callback = self.parse_subcategory, endpoint='execute',
                args={'wait': 2.5, 'lua_source': self.script}
            )

    def parse_subCategory(self, response) :
        
        for url in response.css('.botbot::attr(href)').extract():
            yield SplashRequest(
                response.url + url, callback = self.parse_book, endpoint='execute',
                args={'wait': 2.5, 'lua_source': self.script, 'books': []}
            )

        for url in response.css('.span4 >ul> li > a::attr(href)').extract():
            yield SplashRequest(
                response.url + url, callback = self.parse_book, endpoint='execute',
                args={'wait': 2.5, 'lua_source': self.script, 'books': []}
            )

    def parse_book(self, response):
        if("p10i.htm" in response.url):
            for url in response.css('.span4 >ul> li > a::attr(href)').extract():
                yield SplashRequest(
                    response.url + url, callback = self.parse_book, endpoint='execute',
                    args={'wait': 2.5, 'lua_source': self.script, 'books': []}
                )

            books_links = response.css('.info > h4 >a::attr(href)')
            for url in response.css('.nav-list > li > a::attr(href)').extract():
                yield SplashRequest(
                    self.start_urls[0]+ url, callback = self.parse_book, endpoint='execute',
                    args={'wait': 2.5, 'lua_source': self.script, 'books': response.books.append(books_links)}
                )

            for url in response.css('.pull-right >ul > li > a::attr(href)').extract():
                yield SplashRequest(
                    self.start_urls[0]+ url, callback = self.parse_book, endpoint='execute',
                    args={'wait': 2.5, 'lua_source': self.script, 'books': response.books.append(books_links) }
                )    

        for book in response.books:
            yield SplashRequest(
                self.start_urls[0] + book, callback = self.parse_book, endpoint='execute',
                args={'wait': 2.5, 'lua_source': self.script}
            )    

    def  parse_item(self, response) :
        info = response.css('title::text').get().split(' - ')
        yield {
            'Title': info[0],
            'Category': self.parse_name(','.join(response.css('.tematica > a ::text').getall())),
            'Price': response.css('.precio > strong::text').get(),
            'Link': response.url,
            'Summary': self.parse_text(' '.join(response.css('#resumen >p::text ').getall())),
            'Author': info[1],
            'Editorial': response.css('tr > td::text').getall()[0],
            'ISBN': info[2]
        }



