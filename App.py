from tkinter import *

import threading
import PIL

from Audio import Audio
from Movie import Movie
from moviereptile import MovieReptile


def click(E1, E2):
    print("开始搜索")
    file_name = E1.get()
    platform = E2.get()

    if '豆瓣' in platform and \
            '猫眼' in platform or \
            '全网' in platform:
        platform = 2
    elif '豆瓣' in platform:
        platform = 0
    elif '猫眼' in platform:
        platform = 1

    print('输入的电影名称：', file_name)
    print('输入的平台名称：', platform)

    movie = Movie()
    result = movie.search_movie(file_name, int(platform))

    if result is True:
        t = threading.Thread(target=do_job, args=(movie,))
        t.start()
        t.join()


def do_job(movie):
    try:
        reptile = MovieReptile(movie)
        reptile.get_all_comments()
        data_frame = reptile.read_comments_from_file()

        # 创建词云图
        reptile.create_word_cloud_img(data_frame)

        # 根据原始数据帧进行分组聚合，得到城市——平均分——影评人数的数据帧
        city_data_frame = reptile.process_data_frame(data_frame)
        # # 创建观影人的区域分布图
        reptile.create_thermal_map(city_data_frame)
        # 创建柱形图 + 折线图
        reptile.create_line_and_column_chart(city_data_frame)

        file_path = create_img_path(movie) + ".jpg"
        # print(file_path)
        PIL.Image.open(file_path).show()
    except ConnectionError:
        print('请检查网络连接')


def create_img_path(movie):
    file_path = './' + movie.movie_name + '/'

    if movie.platform == 0:
        file_path += '【豆瓣】《'
    elif movie.platform == 1:
        file_path += '【猫眼】《'
    elif movie.platform == 2:
        file_path += '【豆瓣+猫眼】《'

    file_path += movie.movie_name
    file_path += '》词云图'

    return file_path


def sound_input1(E1):
    audio = Audio()
    audio.record_voice()
    text = audio.shibie_voice()
    if text is not None:
        E1.insert(END, text)


def sound_input2(E2):
    audio = Audio()
    audio.record_voice()
    text = audio.shibie_voice()
    if text is not None:
        E2.insert(END, text)


def create_search(title):
    root = Tk()
    root.title(title)
    root.geometry("300x200")
    Label(root, text="请输入电影名").grid(row=0, column=1)
    E1 = Entry(root, bd=5)
    E1.grid(row=0, column=2)
    Button(text="语音输入", command=lambda: sound_input1(E1)).grid(row=0, column=3)

    Label(root, text="请输入平台").grid(row=1, column=1)
    E2 = Entry(root, bd=5)
    E2.grid(row=1, column=2)
    Button(text="语音输入", command=lambda: sound_input2(E2)).grid(row=1, column=3)

    Button(text="搜索", command=lambda: click(E1, E2)).grid(row=2, column=2)
    root.mainloop()


if __name__ == '__main__':
    create_search("一图")
