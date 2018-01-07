from configparser import ConfigParser
from urllib.parse import quote
import scrapy
from scrapy.http import Request
from ..items import Cnkispider10Item
import copy

class CnkiSpider(scrapy.Spider):
    name = "cnki"
    # 从配置文件里获取查询关键字和最大获取页数
    cf = ConfigParser()
    cf.read("config.conf", encoding='utf-8')
    keywords = cf.get('base', 'keyword')
    start_urls = ['http://search.cnki.net/Search.aspx?q='+quote(keywords)]  # quote
    maxpage = cf.getint('base', 'maxpage')
    # 设置爬取页数maxpage
    #maxpage = 15
    i = 1
    #start_urls = ['http://search.cnki.net/Search.aspx?q=%E9%92%99%E9%92%9B%E7%9F%BF%20%E9%87%8F%E5%AD%90']#http://search.cnki.net/search.aspx?q=qw:%E9%92%99%E9%92%9B%E7%9F%BF&cluster=all&val=&p=0
    v_nextPageUrl_list = []

    # 获取index页面内容
    def parse(self, response):
        print(response)
        ck = Cnkispider10Item()
        # title_list = response.xpath("//*[@class='articles']/div[@class='wz_tab']/div[1]/h3/a[1]/text()").extract()
        sources_list = response.xpath("//*[@class='articles']/div[@class='wz_tab']/div[1]/span/span[1]/text()").extract()#(中国科学技术大学  博士论文  2017年)各项见以&nbsp;&nbsp;隔开
        referCount_list = response.xpath("//*[@class='articles']/div[@class='wz_tab']/div[1]/span/span[2]/text()").extract()#下载次数（47）| 被引次数（4）
        downloadUrl_list = response.xpath("//*[@class='articles']/div[@class='wz_tab']/div[1]/h3/a[2]/@href").extract()#下载链接

        v_detailUrl_list = response.xpath("//*[@class='articles']/div[@class='wz_tab']/div[1]/h3/a[1]/@href").extract()
        # print("输出结果",title_list)
        
        v_nextPageUrlist = response.xpath("//*[@id='page']/a[last()]/@href").extract()
        for sources, ref, durl, detail in zip(sources_list, referCount_list, downloadUrl_list, v_detailUrl_list):
            # ck["TITLE"] = "".join(title_list)
            # print(sources)
            if len(sources.split('  ')) == 3:
                ck["source"] = sources.split('  ')[1]  # 注意此处的字符（串）要以爬取输出中的内容为标准，否则可能无法分割
                ck["time"] = sources.split('  ')[2]
                ck["institution"] = sources.split('  ')[0]
            else:
                ck["source"] = "刊物"
                ck["time"] = sources.split('  ')[1]
                ck["institution"] = sources.split('  ')[0]

            ck["refer"] = ref
            ck["download"] = durl
            print("!!!", detail)
            yield Request(url=detail, meta={'key': copy.deepcopy(ck)}, callback=self.de_page)
            
        #爬取下一页
        if self.i < self.maxpage:
            self.i += 1
            v_nextPageUrl = "http://search.cnki.net/" + v_nextPageUrlist[0]  # 此处网址不全时可能会出现valueError
            yield Request(url=v_nextPageUrl, callback=self.parse)

    # 获取详情页内容(尚有专利页面（已知）布局不同，(title keywords abstract)待添条件语句爬取---已解决
    # 另有一些科技成果、会议论文、页面信息不全的文章可能不会被爬取)
    def de_page(self, response):
        print("GGG",response)
        ck = response.meta['key']
        title_list = response.xpath("//*[@id='spanTitle']/span[@id='chTitle']/text()").extract()
        title_list1 = response.xpath("/html/body/table[1]/tr/td[2]/text()").extract()
        title_list2 = response.xpath("/html/body/table[3]/tr/td[2]/strong/text()").extract()
        title_list3 = response.xpath("/html/body/table[1]/tr/td[2]/strong/text()").extract()
        #print(title_list)
        abstract_list = response.xpath("//*[@id='ChDivSummary']/text()").extract()
        keywords_list = response.xpath("//*[@id='ChDivKeyWord']/a/text()").extract()
        '''ck['title'] = ''.join(title_list)  # 使用join而不是title_list[0]，防止采集不全
        ck['abstract'] = ''.join(abstract_list)  # 由于页面不尽相同，可用join方法来消除IndexError
        ck['keywords'] = '、'.join(keywords_list)
        #print(response.xpath("/html/body/table[1]/tbody/tr/td[2]/text()").extract())
        ck['title'] = ''.join(response.xpath("/html/body/table[1]/tbody/tr/td[2]/text()").extract())
        ck['keywords'] = ''.join(response.xpath("//*[@id='box']/tbody/tr[12]/text()").extract())
        ck['abstract'] = ''.join(response.xpath("/html/body/table[@id='box']/tbody/tr[11]/td[@class='checkItem']/text()").extract())'''
        if len(title_list) != 0:
            ck['title'] = ''.join(title_list)  # 使用join而不是title_list[0]，防止采集不全
            ck['abstract'] = ''.join(abstract_list)  # 由于页面不尽相同，可用join方法来消除IndexError
            ck['keywords'] = '、'.join(keywords_list)
            
        else:#专利等页面待解决爬不到的问题
            ck['title'] = ''.join(title_list1) + ''.join(title_list2) + ''.join(title_list3)
            ck['keywords'] = ''.join(response.xpath("/html/body/table[@id='box']/tr[12]/td/text()").extract())
            ck['abstract'] = ''.join(response.xpath("/html/body/table[@id='box']/tr[11]/td[@class='checkItem']/text()").extract())
        yield ck

