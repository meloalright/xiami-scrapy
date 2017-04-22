import scrapy
import re
import os

class XiamiSpider(scrapy.Spider):
    name = 'xiami'
    allowed_domain = ['xiami.com']
    start_urls = [
        'http://www.xiami.com/song/xL8lVE9d1aa',
        'http://www.xiami.com/song/8GjydGf1fd0',
        'http://www.xiami.com/song/xL7hNId982e'
    ]


    def parse(self, response):
        '''
         @
         @ 把文件名清洗出来
         @ 按照 ./xml/[filename].xml 的方式存储
         @
        '''
        dir = './xml/'

        title_node = response.xpath('//title')[0].extract()
        title = re.match(r'.*title>(.*?)-.*', title_node).group(1)
        filename = dir + title + '.xml'
        with open(filename, 'wb') as f:
            f.write(response.body)