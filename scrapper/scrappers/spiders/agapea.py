
from scrapy_splash import SplashRequest
from scrapy.spiders import CrawlSpider
from scrappers.items import BookItem


class AgapeaSpider(CrawlSpider):
    name = 'agapea'
    books = []
    allowed_domains = ['agapea.com']
    start_urls = ['https://www.agapea.com']

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
                self.start_urls[0] + url, callback = self.parse_subCategory, endpoint='execute',
                args={'wait': 2.5, 'lua_source': self.script}
            )

    def parse_subCategory(self, response) :
        
        for url in response.css('.botbot::attr(href)').extract():
            yield SplashRequest(
                self.start_urls[0] + url, callback = self.parse_book, endpoint='execute',
                args={'wait': 0.5, 'lua_source': self.script},
                meta= {'books': []}
            )

        for url in response.css('.span4 >ul> li > a::attr(href)').extract():
            yield SplashRequest(
                self.start_urls[0] + url, callback = self.parse_book, endpoint='execute',
                args={'wait': 0.5, 'lua_source': self.script},
                meta= {'books': []}
            )

    def parse_book(self, response):
        print(response.url)
        if("p10i.htm" not in response.url):
            for url in response.css('.span4 >ul> li > a::attr(href)').extract():
                yield SplashRequest(
                    self.start_urls[0] + url, callback = self.parse_book, endpoint='execute',
                    args={'wait': 0.5, 'lua_source': self.script},
                    meta = {'books': []}
                )
            books_links = response.css('.info > h4 >a::attr(href)').extract()
            for url in response.css('.nav-list > li > a::attr(href)').extract():
                yield SplashRequest(
                    self.start_urls[0]+ url, callback = self.parse_book, endpoint='execute',
                    args={'wait': 0.5, 'lua_source': self.script},
                    meta = {'books': response.meta["books"].append(books_links)}
                )

            for url in response.css('.pull-right >ul > li > a::attr(href)').extract():
                yield SplashRequest(
                    self.start_urls[0]+ url, callback = self.parse_book, endpoint='execute',
                    args={'wait': 0.5, 'lua_source': self.script},
                    meta = {'books': response.meta["books"].append(books_links)}
                )   

        for books in response.meta["books"]:
            for book in books:
                yield SplashRequest(
                    self.start_urls[0] + book, callback = self.parse_item, endpoint='execute',
                    args={'wait': 0.5, 'lua_source': self.script}
                )    

    def parse_item(self, response) :
        info = response.css('title::text').get().split(' - ')

        price = response.css('.precio > strong::text').get()
        if (price is not None):
            price = float(price.strip().replace('€', '').replace(',', '.'))

        if(len(info) >= 3):
            item = BookItem()
            item['title'] = info[0]
            item['category'] = response.css('.breadcrumb > li >a ::text').getall(),
            item['price'] = price,
            item['link'] = response.url
            item['summary'] = self.parse_text(' '.join(response.css('#resumen ::text').getall())),
            item['author'] = info[1],
            item['editorial'] = response.css('tr > td::text').getall()[0],
            item['isbn'] = info[2]
            item['source'] = 'agapea'
            yield item



