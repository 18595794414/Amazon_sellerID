# -*- coding: utf-8 -*-

import scrapy


class YmxSpider(scrapy.Spider):
    name = 'ymx'
    allowed_domains = ['amazon.co.uk']
    start_urls = ['https://www.amazon.co.uk/gp/site-directory']

    host = 'https://www.amazon.co.uk'

    headers = {
        'sec-fetch-mode':'navigate'
    }

    # 一级分类
    def parse(self, response):

        urls = response.xpath('//td//a/@href').getall()
        for url in urls:
            url = self.host + url
            # print(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse_category2)


    # 主分类
    def parse_category2(self, response):
        if response.status == 200:

            seller_list = response.xpath(
                '//span[@class="a-list-item"]//span[contains(text(), "See more")]/../@href').getall()
            if seller_list != []:
                seller_list_url = self.host + seller_list[-1]
                yield scrapy.Request(url=seller_list_url,
                                     headers=self.headers,
                                     callback=self.parse_seller_list)

            if response.xpath('//li[@class="s-ref-indent-neg-micro"]'):
                url = response.xpath('//li[@class="s-ref-indent-neg-micro"]//a/@href').get()

                if url != None:
                    real_url = self.host + url

                    yield scrapy.Request(url=real_url,
                                         callback=self.parse_category3)

            else:
                yield scrapy.Request(url=response.url,
                                     callback=self.parse_category3)


    # 下级分类
    def parse_category3(self, response):

        # if response.status == 200:

            urls = response.xpath(
                '//ul[contains(@class, "s-ref-indent-one")]//a/@href | //ul[contains(@class, "s-ref-indent-two")]//a/@href | //li[@class="a-spacing-micro s-navigation-indent-2"]//a/@href').getall()
            seller_list = response.xpath(
                '//span[@class="a-list-item"]//span[contains(text(), "See more")]/../@href').getall()
            if seller_list != []:
                seller_list_url = self.host + seller_list[-1]

                yield scrapy.Request(url=seller_list_url,
                                     headers=self.headers,
                                     callback=self.parse_seller_list)

            if urls != []:
                real_urls = [self.host + url for url in urls]

                # 进入下级目录
                for real_url in real_urls:

                    yield scrapy.Request(url=real_url,
                                         callback=self.parse_category3)


    # # 商店列表分类
    # def parse_shop_catgory(self, response):
    #     # if response.status == 200:
    #
    #         urls = response.xpath('//div[@id="center"]/div[2]//span/a/@href').getall()
    #         if urls != []:
    #             for url in urls:
    #                 real_url= self.host + url
    #                 yield scrapy.Request(url=real_url,
    #                                      callback=self.parse_seller_list)
    #         else:
    #             yield scrapy.Request(url=response.url,
    #                                  callback=self.parse_seller_list)

    # 商店列表
    def parse_seller_list(self, response):
        # if response.status == 200:
            urls = response.xpath('//div[@id="center"]/div[4]//span/a/@href').getall()
            if urls != []:
                for url in urls:
                    real_url = self.host + url
                    with open('seller.txt', 'a', encoding='utf-8') as f:
                        f.write(real_url + '\n')