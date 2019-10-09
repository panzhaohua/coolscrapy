# @Time    : 2019/10/9 14:38
# @Author  : MosesPan
# @Email   : 269258169@qq.com
# @File    : huxiu_spider.py
# @Software: PyCharm

from coolscrapy.items import  HuxiuItem
import scrapy
class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    web_url = "https://www.huxiu.com"
    allowed_domains = ["huxiu.com"]
    start_urls=["https://www.huxiu.com/index.php"]

    def parse(self, response):
        for sel in response.xpath('//div[@class="mob-ctt index-article-list-yh"]'):
            item = HuxiuItem()
            item['title'] = sel.xpath('h2/a/text()').extract_first()
            item['link']  = sel.xpath('h2/a/@href')[0].extract()
            # url = response.urljoin("https://www.huxiu.com"+item['link'])
            url = response.urljoin(item['link'])
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()')[0].extract()
            # print(item['title'], item['link'], url,item['desc'])
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        detail = response.xpath('//div[@class="article__bottom-content__right fl"]')
        item = HuxiuItem()
        item['title'] = detail.xpath('div/h1/text()')[0].extract()
        item['link'] = response.url
        item['posttime'] = detail.xpath('div/span[@class="article__time"]/text()')[0].extract()
        print(item['title'], item['link'], item['posttime'])
        yield item