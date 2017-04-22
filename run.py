import os

os.system('cd xiami && rm -rf xml && mkdir xml && scrapy crawl xiami')
os.system('cd xiami/xml && open .')