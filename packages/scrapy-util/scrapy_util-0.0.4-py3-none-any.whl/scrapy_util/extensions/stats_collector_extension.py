# -*- coding: utf-8 -*-

# @Date    : 2018-12-12
# @Author  : Peng Shiyu

import requests
from scrapy import signals

from scrapy_util.logger import logger


class StatsCollectorExtension(object):
    """
    日志记录扩展
    """
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, crawler, bot_name=None, stats_collection_url=None):
        self.stats_collection_url = stats_collection_url
        self.bot_name = bot_name
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        stats_collection_url = crawler.spider.settings.get("STATS_COLLECTION_URL")
        bot_name = crawler.spider.settings.get("BOT_NAME")
        return cls(crawler, bot_name=bot_name, stats_collection_url=stats_collection_url)

    def spider_closed(self, spider, reason):
        stats = spider.crawler.stats.get_stats()

        # 获取数据
        item_scraped_count = stats.get("item_scraped_count", 0)
        item_dropped_count = stats.get("item_dropped_count", 0)

        log_error_count = stats.get("log_count/ERROR", 0)

        start_time = stats.get("start_time")
        finish_time = stats.get("finish_time")

        finish_reason = stats.get("finish_reason")

        # 打印收集日志
        duration = (finish_time - start_time).seconds
        item_count = item_scraped_count + item_dropped_count

        logger.info("*" * 30)
        logger.info("* {}".format(spider.name))
        logger.info("* item_count : {}".format(item_count))
        logger.info("* duration : {}".format(duration))
        logger.info("*" * 30)

        # 保存收集到的信息
        item = {
            "project": self.bot_name,
            "spider": spider.name,
            "item_scraped_count": item_scraped_count,
            "item_dropped_count": item_dropped_count,
            "start_time": start_time.strftime(self.DATETIME_FORMAT),
            "finish_time": finish_time.strftime(self.DATETIME_FORMAT),
            "finish_reason": finish_reason,
            "log_error_count": log_error_count,
        }

        self.collection_item(item)

    def collection_item(self, item):
        """处理收集到的数据,以json 形式提交"""
        if self.stats_collection_url is None:
            return

        res = requests.post(self.stats_collection_url, json=item)
        print(res.text)
