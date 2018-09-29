# !/usr/bin/env python
# _*_ coding:utf-8 _*_
from json import JSONDecodeError
from urllib.parse import quote
import requests
import json


class Movie:

    def __init__(self):
        self.platform = 0         # 抓取影评的平台（0：豆瓣；1：猫眼）
        self.douban_movie_id = ''
        self.maoyan_movie_id = ''
        self.movie_name = ''      # 电影名字
        self.movie_img = ''       # 电影封面

    def search_movie(self, str, platform):
        self.platform = platform
        if platform == 0:       # 豆瓣电影
            if not self.search_from_douban(str):
                print('豆瓣暂无该电影')
                return False
            return True
        elif platform == 1:     # 猫眼电影
            if not self.search_from_maoyan(str):
                print('猫眼暂无该电影')
                return False
            return True
        else:
            if not self.search_from_douban(str):
                print('豆瓣暂无该电影')
                return False

            if not self.search_from_maoyan(str):
                print('猫眼暂无该电影')
                return False
        return True

    def search_from_douban(self, str):
        url = 'https://movie.douban.com/j/subject_suggest?q=' + quote(str, 'utf-8')
        response = requests.get(url=url)
        items = json.loads(response.text)

        if len(items) == 0:
            return False
        else:  # 自动选取第一个
            self.douban_movie_id = items[0]['id']
            self.movie_name = items[0]['title']
            print('豆瓣搜索到', self.movie_name)
            self.movie_img = items[0]['img']
            return True

    def search_from_maoyan(self, str):
        url = 'http://maoyan.com/ajax/suggest?kw=' + quote(str, 'utf-8')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/69.0.3497.92 Safari/537.36'}
        response = requests.get(url=url, headers=headers)

        try:
            json_str = json.loads(response.text)
            items = json_str['movies']['list']
        except JSONDecodeError:
            print('查询猫眼电影Id出现Json解析异常')
            print(response.text)
            return False

        if len(items) == 0:
            return False
        else:  # 自动选取第一个
            self.maoyan_movie_id = items[0]['id']
            self.movie_name = items[0]['nm']
            print('猫眼搜索到', self.movie_name)
            self.movie_img = items[0]['img']
            return True