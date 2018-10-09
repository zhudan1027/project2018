#导入scrapy和正则表达式的包
import scrapy
import requests
import re
from job51.items import Job51Item
#将items中的类导进来

#类名要与工程名相同
class job51spider(scrapy.Spider):
    name="job51"
    #要爬的地址初始化，不要更改
    start_urls=[]
    #寻找地址规律进行页数的循环储存在数组中分给多个线程同时进行
    for pagenumber in range(1801,2000):
        start_urls.append("https://search.51job.com/list/000000,000000,0100,01,9,99,%2520,2,"+str(pagenumber)+".html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=")
    #获取已经获得的连接里的数据
    def getjobcontent(self,urlstr):
        response=requests.get(urlstr)
        jobContentHtml=response.content.decode('GBK')
        reg2 = re.compile(
            r'<div class="tCompany_main" >.*?<em class="i1"></em>(.*?)</span>.*?<em class="i2"></em>(.*?)</span>.*?<em class="i3"></em>招(.*?)人</span>.*?<span class="bname">(.*?)<div class="share">',
            re.S)
        items2 = re.findall(reg2,jobContentHtml)
        return items2



    def parse(self, response):
        #抓取数据
        htmlstr=response.body.decode('GBK')
        #正则表达式
        reg=re.compile(
            r'class="t1.*?title="(.*?)" href="(.*?)".*? <span class="t2"><a target="_blank" title="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*? <span class="t5">(.*?)</span>',
            re.S)
        items=re.findall(reg,htmlstr)
        for x in items:
             item=Job51Item()
             item['jobname']=x[0]
             item['companyname']=x[2]
             item['jobadd']=x[3]
             item['jobsalary']=x[4]
             for y in self.getjobcontent(x[1]):
                 item['jobcontent'] = re.sub(r'<.*?>|&nbsp|\t|\n|\r|\s;','',y[3]).replace(r"\t","").replace(r"\r","")
                 item['jobexperience'] = y[0]
                 item['education'] = y[1]
                 item['peoplepnumber'] = y[2]
                 yield item

