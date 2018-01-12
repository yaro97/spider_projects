from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
import requests

# xpath解析标题
url = 'http://toutiao.com/group/6458859321533923853/'
response = requests.get(url)
selector = etree.HTML(response.text)
result = selector.xpath('//title/text()')[0]
print(result)
# 或者
url = 'http://toutiao.com/group/6458859321533923853/'
response = requests.get(url)
tree = html.fromstring(response.text)
result = tree.xpath('//title/text()')[0]
print(result)

# beautifulsoup解析
url = 'http://toutiao.com/group/6458859321533923853/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
title = soup.select('title')[0].get_text()
print(title)
