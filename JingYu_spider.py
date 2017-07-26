# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from JingYu.items import JingYuBookItem,JingYuBookLoader


class JingyuSpiderSpider(CrawlSpider):
    name = 'JingYu_spider'
    allowed_domains = ['www.jingyu.com']
    start_urls = ['http://www.jingyu.com/']

    rules = (
        Rule(LinkExtractor(allow='ranks'), follow=True),
        Rule(LinkExtractor(allow='search/stack'), follow=True),
        Rule(LinkExtractor(allow='index/.*'), follow=True),
        Rule(LinkExtractor(allow='category?category.*'), follow=True),
        Rule(LinkExtractor(allow='novel/.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        info_item = JingYuBookItem()

        Title = response.xpath('//p[@class="book_name"]/text()').extract_first("").strip()
        Author = response.xpath('//a[@class="author"]/text()').extract_first("")
        Tags = response.xpath('//p[@class="state"]/a/text()').extract_first("")
        Fav_nums = response.xpath('//p[@class="state"]/i[2]/text()').extract_first("")
        Pop_nums=response.xpath('//p[@class="state"]/i[3]/text()').extract_first("")
        Score= response.xpath('//p[@class="js-evaluate-score number"]/text()').extract_first("")
        Cover_img_url = response.xpath('//div[@class="book_left"]/a/img/@src').extract_first("")

        info_item['Url'] = response.url
        info_item['Title'] = Title
        info_item['Author'] = Author
        info_item['Tags'] = Tags
        info_item['Fav_nums'] = Fav_nums
        info_item['Pop_nums'] = Pop_nums
        info_item['Score'] = Score
        info_item['Cover_img_url'] = [Cover_img_url]
        info_item['Cover_img_url_forSQL'] = Cover_img_url
        #
        # info_item= JingYuBookLoader(item= JingYuBookItem(), response= response)
        # info_item.add_xpath('Title','//p[@class="book_name"]/text()')
        # info_item.add_value('Url',response.url)
        # info_item.add_xpath('Author', '//a[@class="author"]/text()')
        # info_item.add_xpath('Tags', '//p[@class="state"]/a/text()')
        # info_item.add_xpath('Fav_nums', '//p[@class="state"]/i[2]/text()')
        # info_item.add_xpath('Pop_nums', '//p[@class="state"]/i[3]/text()')
        # info_item.add_xpath('Score', '//p[@class="js-evaluate-score number"]/text()')
        # info_item.add_value('Cover_img_url', [Cover_img_url])
        # info_item.add_value('Cover_img_url_forSQL', Cover_img_url)

        return info_item
