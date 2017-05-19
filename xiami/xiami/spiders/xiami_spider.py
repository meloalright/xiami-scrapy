import scrapy
import re
import os

from xlwt import Workbook


class XiamiSpider(scrapy.Spider):
    name = 'xiami'
    allowed_domain = ['xiami.com']
    start_urls = [
        'http://www.xiami.com/song/U55CSj2ca18',#mine
        'http://www.xiami.com/song/xL7hNId982e',#shake it off
        'http://www.xiami.com/song/xLoG03af13c',#back to december
        'http://www.xiami.com/song/OMZ5622d8',#last christmas
        'http://www.xiami.com/song/xLoG02d8685',#speak now
        'http://www.xiami.com/song/mQ3HBX5ec82',#echanted
        'http://www.xiami.com/song/xL8lVE9d1aa',#blank space
        'http://www.xiami.com/song/mQ3HBQ7aecc',#sparks fly
        'http://www.xiami.com/song/dCfw32c7fa',#red
        'http://www.xiami.com/song/Up7o77a3c'#love story
    ]


    def parse(self, response):
        '''
         @
         @ [1]
         @ 把文件名清洗出来
         @
        '''
        dir = './xml/'

        title_node = response.xpath('//title')[0].extract()
        title = re.match(r'.*title>(.*?)-.*', title_node).group(1)


        '''
         @
         @ [2]
         @ 初始化excel
         @ 设定sheet名称 列宽度
         @
        '''
        excel = Workbook()
        sheet1 = excel.add_sheet(title)
        sheet1.col(0).width = 1024*20
        sheet1.col(1).width = 512*20
        sheet1.col(2).width = 256*20
        sheet1.col(3).width = 256*20

        '''
         @
         @ [3]
         @ 洗出评论 用户 设备 日期
         @ 并且写入excel
         @
        '''
        comment_list = response.xpath('//div[@class="post_item"]')
        index = 0
        for o in comment_list:
            '''
                comment = scrapy.Field()
                user = scrapy.Field()
                device = scrapy.Field()
                date = scrapy.Field()
            '''
            comment = o.xpath('div[@class="brief"]/div/node()')[0].extract().replace(' ', '').replace('\n', '')
            user = o.xpath('p[@class="usr_cover"]/a/@title')[0].extract()
            device = o.xpath('div[@class="brief"]/div/a/node()')
            device = device[0].extract() if len(device) > 0 else '未知终端'# 容错
            date = o.xpath('div[@class="info"]/span[@class="time"]/node()')[0].extract()


            '''
             @ 朗读第一个
            '''
            if index < 3:
                print('{0} \n{1} {2} {3}\n'.format(comment, user, device, date))

            index += 1
            row = sheet1.row(index)
            row.write(0, comment)
            row.write(1, user)
            row.write(2, device)
            row.write(3, date)

        '''
         @
         @ [4]
         @ excel保存
         @
        '''

        excelname = dir + title + '.xls'
        excel.save(excelname)
        print('{0} 的评论下载成功啦\n'.format(title))
        os.system('say {0}'.format(title))








