# Scrapy util

## 启用数据收集功能

此功能配合spider-admin-pro 使用

```python
# 项目名默认是（不需要设置）
BOT_NAME = 'scrapy_demo'

# 设置收集运行日志的路径,会以post方式提交json数据
STATS_COLLECTION_URL = "http://127.0.0.1:5001/api/collection"

# 启用数据收集扩展
EXTENSIONS = {
   # 'scrapy.extensions.telnet.TelnetConsole': None,
   'scrapy_util.extensions.SpiderItemCountExtension': 100
}

```

## 使用脚本Spider

```python
# -*- coding: utf-8 -*-

from scrapy import cmdline

from scrapy_util.spiders import ScriptSpider


class BaiduScriptSpider(ScriptSpider):
    name = 'baidu_script'

    def execute(self):
        print("hi")


if __name__ == '__main__':
    cmdline.execute('scrapy crawl baidu_script'.split())

```