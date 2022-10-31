# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BookItem(Item):
    # define the fields for your item here like:
    Title = Field()
    Category = Field()
    Price = Field()
    Stock = Field()
    Link = Field()
    Summary = Field()
    Author = Field()
    ISBN = Field()
