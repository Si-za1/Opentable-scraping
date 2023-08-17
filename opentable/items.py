import scrapy

class OpentableItem(scrapy.Item):
	name = scrapy.Field()
	area = scrapy.Field()
	price = scrapy.Field()
	location = scrapy.Field()
	cuisine = scrapy.Field()
	profile_link = scrapy.Field()
	rating = scrapy.Field()
