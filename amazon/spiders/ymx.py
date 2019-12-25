# -*- coding: utf-8 -*-
import scrapy
import os

class YmxSpider(scrapy.Spider):
    name = 'ymx'
    allowed_domains = ['amazon.co.uk']
    start_urls = ['https://www.amazon.co.uk/gp/site-directory']

    host = 'https://www.amazon.co.uk'
    base_url = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # 一级分类
    def parse(self, response):

        urls = response.xpath('//td//a/@href').getall()
        for url in urls:
            url = self.host + url
            # print(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse_category2)

    # 二级分类
    def parse_category2(self, response):
        if response.status == 200:
            urls = response.xpath('//div[@class="left_nav browseBox"]//a/@href | //ul[contains(@class, "s-ref-indent-one")]//a/@href | //ul[contains(@class, "s-ref-indent-two")]//a/@href | //li[@class="a-spacing-micro s-navigation-indent-2"]//a/@href').getall()

            if urls != []:
                real_urls = [self.host + url for url in urls]

                # 进入下级目录
                for real_url in real_urls:
                    meta = {}
                    yield scrapy.Request(url=real_url,
                                         callback=self.parse_category2)
            else:
                cat1_name = response.xpath('//li[@class="s-ref-indent-neg-micro"]//text()').getall()
                cat2_name = response.xpath(
                    '//li[@class="a-spacing-micro s-navigation-indent-1"]/span/span/text() | //li[@class="s-ref-indent-one"]//text()').get()
                url = response.url
                if cat1_name != []:
                    for i in cat1_name:
                        i = i.strip()


                        print('上级目录：%s，下级目录：%s，url：%s' % (i,cat2_name,url))
                if cat2_name:

                    with open(self.base_url + '/cat_name.txt', 'a', encoding='utf-8') as f:
                        f.write(cat2_name + ',' + url + '\n')

                yield scrapy.Request(url=response.url,
                                     callback=self.parse_list)

    # 商品列表页
    def parse_list(self, response):
        if response.status == 200:

            pass