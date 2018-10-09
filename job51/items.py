# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobname=scrapy.Field()
    companyname=scrapy.Field()
    # 公司地址
    jobadd=scrapy.Field()
    #工资
    jobsalary=scrapy.Field()
    #岗位内容
    jobcontent=scrapy.Field()
    #经验
    jobexperience=scrapy.Field()
    #学历
    education=scrapy.Field()
    #人数
    peoplepnumber= scrapy.Field()
    pass
