# !/usr/bin/env python
# _*_ coding:utf-8 _*_


class Comment:

    def __init__(self, movie):
        self.movie = movie      # 设置评论所属的电影
        self.user_avatar = ''   # 用户头像
        self.user_name = ''     # 用户名
        self.user_id = ''       # 用户Id
        self.user_loc = ''      # 用户所在城市
        self.rate = ''          # 用户评分
        self.comment = ''       # 用户评论内容
        self.create_time = ''   # 用户发布评论时间
        self.vote_count = ''    # 点赞人数