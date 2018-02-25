# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
from uuid import uuid1
import time
from sharesSpider.items import SharesspiderItem


class SharesListSpider(scrapy.Spider):
    # 爬虫名字
    name = "sharesList"

    # 爬虫范围
    def start_requests(self):
        urls = [
            # 'https://hq.gucheng.com/List.aspx?TypeId=3&sort=chg&d=1&page=1'  # 上证A股
            'https://hq.gucheng.com/List.aspx?TypeId=2&sort=chg&d=1&page=23'  # 深证A股
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 解析列表页面
    def parse(self, response):

        trElems = response.xpath('//table[@runat="server"]/tr')

        now = time.strftime("%Y-%m-%d", time.localtime())  # 获取当地时间

        i = 0
        for trElem in trElems:
            i = i + 1
            if i == 1:  # 不要第一行数据
                continue

            trElemHtml = trElem.extract()
            elem = etree.HTML(trElemHtml)

            shares_name = elem.xpath("//td[1]//a/text()")[0]  # 股票名字
            shares_num = elem.xpath("//td[2]//a/text()")[0]  # 股票代码
            shares_href = 'https://hq.gucheng.com' + elem.xpath("//td[2]/a/@href")[0]  # 股票链接
            new_price = elem.xpath("//td[3]/text()")[0]  # 最新价  # 可以当成收盘价
            rise_and_fall_range = elem.xpath("//td[4]/text()")[0]  # 涨跌幅 例如：0.31%，-0.97%
            rise_and_fall_quota = elem.xpath("//td[5]/text()")[0]  # 涨跌额 例如：-0.27，12.25
            volume = elem.xpath("//td[8]/text()")[0]  # 成交量（手）
            turn_volume = elem.xpath("//td[9]/text()")[0]  # 成交额（万）
            open_price = elem.xpath("//td[10]/text()")[0]  # 开盘价
            ceilling_price = elem.xpath("//td[12]/text()")[0]  # 最高价
            floor_price = elem.xpath("//td[12]/text()")[0]  # 最低价

            item = SharesspiderItem()
            id_ = uuid1().__str__()
            item['id'] = id_
            item['shares_num'] = shares_num
            item['shares_name'] = shares_name
            item['shares_href'] = shares_href
            item['create_time'] = now

            item['detailed_id'] = uuid1().__str__()
            item['shares_id'] = id_
            item['open_price'] = float(open_price) * float(100)
            item['close_price'] = float(new_price) * float(100)
            item['ceilling_price'] = float(ceilling_price) * float(100)
            item['floor_price'] = float(floor_price) * float(100)

            item['rise_and_fall_range'] = float(rise_and_fall_range.split('%')[0]) * float(100)
            item['rise_and_fall_quota'] = float(rise_and_fall_quota) * float(100)

            item['volume'] = volume
            item['turn_volume'] = turn_volume

            # 抓取详情页面
            request = scrapy.Request(shares_href, meta={'item': item}, callback=self.paser_detailed)
            yield request

        # todo 抓取下一页数据




    # 解析详情页面
    def paser_detailed(self, response):

        item = response.meta['item']

        turnover_rate = response.xpath("//div[@class='s_date']//dl[3]//dd[1]/text()")[0].extract()  # 换手率
        amplitude = response.xpath("//div[@class='s_date']//dl[3]//dd[2]/text()")[0].extract()  # 振幅
        p_e_ratio = response.xpath("//div[@class='s_date']//dl[7]//dd[1]/text()")[0].extract()  # 市盈率

        item['turnover_rate'] = float(turnover_rate.split('%')[0]) * float(100)
        item['amplitude'] = float(amplitude.split('%')[0]) * float(100)
        item['p_e_ratio'] = float(p_e_ratio) * float(100)

        item['state'] = 1 # todo 状态 需要变动

        yield item



