import scrapy

from scrapy.loader import ItemLoader

from ..items import AlbarakabanktnItem
from itemloaders.processors import TakeFirst


class AlbarakabanktnSpider(scrapy.Spider):
	name = 'albarakabanktn'
	start_urls = ['http://www.albarakabank.com.tn/fr/actualites']

	def parse(self, response):
		post_links = response.xpath('//ul[@class="liste-news"]/li/div/h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="field field--name-node-title field--type-ds field--label-hidden field--item"]/h2/text()').get()
		description = response.xpath('//div[@class="details-txt field field--name-body field--type-text-with-summary field--label-hidden field--item"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="date field field--name-field-date field--type-datetime field--label-hidden field--item"]/text()').get()

		item = ItemLoader(item=AlbarakabanktnItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
