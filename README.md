# 一图
---

## 目录
* [功能介绍](#功能介绍)
* [效果图](#效果图)
* [开始使用](#开始使用)
* [主要使用的库](#主要使用的库)

## 功能介绍
一图是一个基于Python语言的豆瓣以及猫眼电影的影评爬取程序（PyCharm项目），并把爬取的数据通过词云图、热力分布图、条形图以及折线图的方式展现给使用者。本程序仅供学习，不用于其他用途，所以以下仅提供效果图，无相应的技术分析。

利用此程序，你可以：  
- [x] 查看影评高频词  
- [x] 查看观影人地区分布  
- [x] 查看各城市观影人数  
- [x] 查看各城市影评平均分  

除此之外，你还可以：  
- [x] 设置屏蔽词  
- [x] 模糊输入电影名  
- [x] 使用语音输入  
- [x] 自由选择爬取的电影平台

## 效果图
### 词云图  
![](http://opl5tlfw9.bkt.clouddn.com/18-9-29/55640167.jpg)  

### 观影人热力分布图
![](http://opl5tlfw9.bkt.clouddn.com/18-9-29/86995584.jpg)  

### 主要城市平均数 - 平均分图  
![](http://opl5tlfw9.bkt.clouddn.com/18-9-29/12280329.jpg)  

## 开始使用
1. 填入你的百度语音配置参数（如果使用语音输入）  
![](http://opl5tlfw9.bkt.clouddn.com/18-9-29/28597918.jpg)

2. 设置词云图屏蔽词  
![](http://opl5tlfw9.bkt.clouddn.com/18-9-29/26207945.jpg)

3. 运行App.py即可打开主程序窗口  
![](http://opl5tlfw9.bkt.clouddn.com/18-9-29/66218178.jpg)

4. 留意PyCharm中输出

## 主要使用的库
- [jieba](https://pypi.org/project/jieba/)
- [pandas](https://pypi.org/project/pandas/)
- [wordcloud](https://pypi.org/project/wordcloud/)
- [pyecharts](http://pyecharts.org/#/)