import csv
import random
import string

import jieba
import pandas as pd
import requests
import json
import os
from wordcloud import WordCloud, STOPWORDS
from pyecharts import Geo, Style, Line, Bar, Overlap
import matplotlib.pyplot as plt

from Comment import Comment

IS_DEBUG = False


class MovieReptile:

    def __init__(self, movie):
        self.movie = movie
        self.start = 0

        path = './' + movie.movie_name
        folder = os.path.exists(path)
        if not folder:
            # 为该电影创建一个文件夹
            os.makedirs('./' + movie.movie_name)
            print('在当前路径创建了名为：【' + movie.movie_name + '】文件夹')

            file_path1 = './' + self.movie.movie_name + '/' + self.movie.movie_name + '1_old.csv'
            f1 = open(file_path1, mode='w', encoding='utf_8_sig', newline='')
            f1.close()

            for i in range(0, 3):
                file_path = './' + self.movie.movie_name + '/' + self.movie.movie_name + str(i) + '.csv'
                f = open(file_path, mode='w', encoding='utf_8_sig', newline='')
                f.close()

    # 获取接口的json数据
    def get_one_page_comment_json(self, start):
        url = 'https://m.douban.com/rexxar/api/v2/movie/' + str(
            self.movie.douban_movie_id) + '/interests?count=50&order_by=hot&start=' \
              + str(start) + '&ck=&for_mobile=1'

        bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
        headers = {'Referer': 'https://m.douban.com/movie/subject/' + str(self.movie.douban_movie_id) + '/comments',
                   'Cookie': 'bid=' + bid,
                   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, '
                                 'like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def decode_json(self, json_str):
        # 创建评论变量
        comments = []

        # 解析关键的根节点
        count = json_str['count']
        start = json_str['start']
        interests = json_str['interests']
        total = json_str['total']

        # print('本次获取的个数为：', count)
        # print('评论为：', interests)
        # print('起始评论数为：', start)
        # print('总评论数为：', total)

        # 解析所需要的评论内容
        for interest in interests:
            comment = Comment(self.movie)

            user = interest['user']
            rating = interest['rating']

            loc = user['loc']
            if loc is not None:
                loc_name = loc['name']
                comment.user_loc = loc_name

            comment.user_avatar = user['avatar']
            comment.user_name = user['name']
            comment.user_id = user['id']
            if rating is not None:
                comment.rate = rating['value']
            comment.comment = interest['comment']
            comment.create_time = interest['create_time']
            comment.vote_count = interest['vote_count']

            comments.append(comment)

        # 保存评论内容到文件中
        self.save_comments(comments, 0)
        return start, len(interests), total

    def get_one_page_comment_json_from_maoyan(self, offset):
        url = 'http://m.maoyan.com/mmdb/comments/movie/' + str(self.movie.maoyan_movie_id) + '.json?_v_=yes&offset=' + str(offset)
        try:
            response = requests.get(url=url)
        except ConnectionError:
            return None
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print('网络请求出错')
        return None

    # 获取评论内容列表
    def get_comments_from_maoyan(self, offset):
        comments = []

        json_str = self.get_one_page_comment_json_from_maoyan(offset)
        if json_str is None:
            return None

        try:
            data1 = json_str['cmts']  # 获取评论内容
            data2 = json_str['hcmts']  # 获取评论内容
            data = data1 + data2
        except KeyError:
            return None
        for item in data:
            comment = Comment(self.movie)
            # 使用get方法获取值，避免出现KeyError
            comment.user_loc = item.get('cityName')
            comment.user_avatar = item.get('avatarurl')
            comment.user_name = item.get('nickName')
            comment.user_id = item.get('userId')
            comment.comment = item.get('content')
            comment.create_time = item.get('time')
            comment.vote_count = item.get('approve')
            comments.append(comment)
        return comments

    def save_comments(self, comments, platform):
        if comments is None:
            return

        file_path = ''

        if platform == 0:
            file_path = './' + self.movie.movie_name + '/' + self.movie.movie_name + str(platform) + '.csv'
        else:
            file_path = './' + self.movie.movie_name + '/' + self.movie.movie_name + str(platform) + \
                        '_old.csv'

        with open(file_path, 'a+', encoding='utf_8_sig', newline='') as f:
            spam = csv.writer(f, dialect='excel')  # 设置文件的打开方式，并将其转化为excel文件对象
            # if self.start == 0:
            #     spam.writerow(['发布时间', '发布者Id', '发布者头像', '发布者名字', '评论内容', '评分', '发布者城市', '点赞人数'])  # 标题

            for comment in comments:
                spam.writerow([comment.create_time,
                               comment.user_id,
                               comment.user_avatar,
                               comment.user_name,
                               comment.comment,
                               comment.rate,
                               comment.user_loc,
                               comment.vote_count])

    def read_comments_from_file(self):
        file_path = './' + self.movie.movie_name + '/' + self.movie.movie_name + str(self.movie.platform) + '.csv'

        if self.movie.platform == 2:
            file_path1 = './' + self.movie.movie_name + '/' + self.movie.movie_name + '0.csv'
            file_path2 = './' + self.movie.movie_name + '/' + self.movie.movie_name + '1.csv'
            self.merge_file(file_path1, file_path2, file_path)

        f = open(file_path, mode='r', encoding='utf-8')
        # 按格式读取数据
        datas = pd.read_csv(f, sep=',', header=None, encoding='utf-8',
                            names=['create_time',
                                   'user_id',
                                   'user_avatar',
                                   'user_name',
                                   'comment',
                                   'rate',
                                   'user_loc',
                                   'vote_count'])
        return datas

    def merge_file(self, file1_name, file2_name, merge_file_name):
        f1 = open(file1_name, 'r', encoding='utf_8_sig', newline='')
        f2 = open(file2_name, 'r', encoding='utf_8_sig', newline='')
        f3 = open(merge_file_name, 'w', encoding='utf_8_sig', newline='')

        for line1 in f1.readlines():
            f3.write(line1)
        for line2 in f2.readlines():
            f3.write(line2)

        f1.close()
        f2.close()
        f3.close()

    # 去除重复的评论
    def remove_duplicates(self):
        old_file_path = './' + self.movie.movie_name + '/' + self.movie.movie_name + '1_old.csv'
        new_file_path = './' + self.movie.movie_name + '/' + self.movie.movie_name + '1.csv'

        oldfile = open(old_file_path, 'r', encoding='utf-8')
        newfile = open(new_file_path, 'w', encoding='utf-8')
        content_list = oldfile.readlines()  # 获取所有评论数据集
        content_alread = []  # 存储去重后的评论数据集

        for line in content_list:
            if line not in content_alread:
                newfile.write(line)
                content_alread.append(line)
        print('去重完毕')

    def get_all_comments(self):
        if self.movie.platform == 0:        # 豆瓣的影评获取
            self.get_douban_comment()
        elif self.movie.platform == 1:        # 猫眼的影评获取
            self.get_maoyan_comment()
        else:
            self.get_douban_comment()
            self.get_maoyan_comment()

    def get_douban_comment(self):
        while True:
            json_str = self.get_one_page_comment_json(self.start)
            self.start, count, total = self.decode_json(json_str)
            print(f'当前start{self.start}，当前的count{count}， 总数{total}')

            if count != 0:
                self.start = self.start + count + 1  # 改变评论起始位置

            if self.start >= total:
                break
            elif self.start >= 500:
                print(f'当前start{self.start}，当前的count{count}， 总数{total}')
                break

    def get_maoyan_comment(self):
        for i in range(0, 50):
            print("开始保存第%d页" % i)

            comments = self.get_comments_from_maoyan(i)
            self.save_comments(comments, 1)
        # 猫眼的接口问题，需要去重
        self.remove_duplicates()

    def get_stop_words(self):
        stopwords = STOPWORDS.copy()
        # 添加屏蔽词
        stopwords.add(self.movie.movie_name)

        with open('stopword.txt', 'r', encoding='utf_8_sig', newline='') as f:
            for line in f.readlines():
                if '\r\n' in line:
                    stopwords.add(line[:len(line) - 2:])
                else:
                    stopwords.add(line)
        # print(stopwords)
        return stopwords

    def create_word_cloud_img(self, data_frame):
        # 分隔评论内容
        comment = jieba.cut(str(data_frame['comment']), cut_all=False)
        wl_space_split = " ".join(comment)

        # 自定义屏蔽词
        stopwords = self.get_stop_words()

        wc = WordCloud(width=1024,
                       height=768,
                       background_color='white',
                       # mask=backgroud_Image,
                       font_path="C:\simhei.ttf",
                       stopwords=stopwords,
                       max_font_size=400, random_state=50)

        wc.generate_from_text(wl_space_split)
        plt.imshow(wc)
        plt.axis('off')  # 不显示坐标轴
        # plt.show()

        file_path = ''
        if self.movie.platform == 0:
            file_path = './' + self.movie.movie_name + '/【豆瓣】《' + self.movie.movie_name + '》词云图.jpg'
        elif self.movie.platform == 1:
            file_path = './' + self.movie.movie_name + '/【猫眼】《' + self.movie.movie_name + '》词云图.jpg'
        else:
            file_path = './' + self.movie.movie_name + '/【豆瓣+猫眼】《' + self.movie.movie_name + '》词云图.jpg'
        wc.to_file(file_path)
        print('词云图创建完毕')

    # 处理原始数据帧(取出城市及评分数据，组成城市——平均分——影评人数的数据帧)
    def process_data_frame(self, data_frame):
        # 对数据进行分组
        city_group = data_frame.groupby('user_loc')

        # 对分组后的rate列进行求平均值（）
        city_data_frame = city_group['rate'].agg(['mean', 'count'])
        # print(city_data_frame)
        # 插入行下标
        city_data_frame.reset_index(inplace=True)
        # 修改mean列数据取两位小数
        city_data_frame['mean'] = round(city_data_frame['mean'], 2)
        # print(city_data_frame)
        return city_data_frame

    # 根据数据创建热力图
    def create_thermal_map(self, city_data_frame):
        data_map = [(city_data_frame['user_loc'][i], city_data_frame['count'][i])
                    for i in range(0, city_data_frame.shape[0])]
        # print(data_map)

        style = Style(title_color="#fff", title_pos="center",
                      width=1200, height=600, background_color="#404a59")

        data_res = '数据来源：'
        file_path = ''
        if self.movie.platform == 0:
            data_res = data_res + '豆瓣电影'
            file_path = './' + self.movie.movie_name + '/【豆瓣】《' + self.movie.movie_name + '》观影热力图.html'
        elif self.movie.platform == 1:
            data_res = data_res + '猫眼电影'
            file_path = './' + self.movie.movie_name + '/【猫眼】《' + self.movie.movie_name + '》观影热力图.html'
        else:
            data_res = data_res + '豆瓣电影、猫眼电影'
            file_path = './' + self.movie.movie_name + '/【豆瓣+猫眼】《' + self.movie.movie_name + '》观影热力图.html'
        geo = Geo("《" + self.movie.movie_name + "》观影人分布热力图", data_res, **style.init_style)

        while True:
            try:
                attr, val = geo.cast(data_map)
                geo.add("", attr, val, visual_range=[0, 20],
                        visual_text_color="#fff", symbol_size=20,
                        is_visualmap=True, is_piecewise=True,
                        visual_split_number=4)
            except ValueError as e:
                e = str(e)
                e = e.split("No coordinate is specified for ")[1]  # 获取不支持的城市名
                for i in range(0, len(data_map)):
                    if e in data_map[i]:
                        del data_map[i]
                        break
            else:
                break
        geo.render(file_path)
        print('热力图创建完毕')

    # 创建折线图 + 柱形图
    def create_line_and_column_chart(self, city_data_frame):
        city_main = city_data_frame.sort_values('count', ascending=False)[0:20]
        # print(city_main)
        attr = city_main['user_loc']
        v1 = city_main['count']
        v2 = city_main['mean']
        # print(attr,v1,v2)
        line = Line("主要城市评分")
        line.add("城市", attr, v2,
                 is_stack=True,
                 xaxis_rotate=30,
                 yaxix_min=4.2,
                 mark_point=['min', 'max'],             # 对最大最小值进行标记
                 xaxis_interval=0,
                 line_color='#2196F3',
                 line_width=4,
                 mark_point_textcolor='#eeeeee',
                 mark_point_color='#2196F3',
                 is_splitline_show=False)

        bar = Bar("主要城市评论数")
        bar.add("城市", attr, v1,
                is_stack=True,
                xaxis_rotate=30,
                yaxix_min=4.2,
                xaxis_interval=0,
                mark_point=['min', 'max'],
                is_splitline_show=False)

        overlap = Overlap()
        overlap.add(bar)
        overlap.add(line, yaxis_index=1, is_add_yaxis=True)

        file_path = ''
        if self.movie.platform == 0:
            file_path = './' + self.movie.movie_name + '/【豆瓣】《' + self.movie.movie_name + '》主要城市评论数_平均分.html'
        elif self.movie.platform == 1:
            file_path = './' + self.movie.movie_name + '/【猫眼】《' + self.movie.movie_name + '》主要城市评论数_平均分.html'
        else:
            file_path = './' + self.movie.movie_name + '/【豆瓣+猫眼】《' + self.movie.movie_name + '》主要城市评论数_平均分.html'
        overlap.render(file_path)
        print('折线 + 柱形图创建完毕')