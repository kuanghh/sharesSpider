# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import uuid


class SharesspiderItem(scrapy.Item):
    id = scrapy.Field()
    shares_num = scrapy.Field()
    shares_name = scrapy.Field()
    shares_href = scrapy.Field()
    create_time = scrapy.Field()

    detailed_id = scrapy.Field()
    shares_id = scrapy.Field()
    # create_time = scrapy.Field()
    open_price = scrapy.Field()
    close_price = scrapy.Field()
    ceilling_price = scrapy.Field()
    floor_price = scrapy.Field()
    rise_and_fall_range = scrapy.Field()
    rise_and_fall_quota = scrapy.Field()
    volume = scrapy.Field()
    turn_volume = scrapy.Field()
    turnover_rate = scrapy.Field()
    amplitude = scrapy.Field()
    p_e_ratio = scrapy.Field()
    state = scrapy.Field()



