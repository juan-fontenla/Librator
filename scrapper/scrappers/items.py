# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BookItem(Item):
    # define the fields for your item here like:
    title = Field()
    category = Field()
    editorial = Field()
    price = Field()
    stock = Field()
    link = Field()
    summary = Field()
    author = Field()
    isbn = Field()
    source = Field()
