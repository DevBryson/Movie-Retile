# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import pyaudio  # 语音的录入与播放
import wave

from aip import AipSpeech

framerate = 16000  # 采样率
channael = 1  # 单声道
samewidth = 2  # 音频采集值的保留位数
record_time = 5  # 录音的时长
CHUNK = 1024  # 缓冲区的大小

APP_ID = '你的APP_ID'  # 应用的APP_ID
API_Key = '你的API_Key'  # 应用的API_Key
Secret_Key = '你的Secret_Key'  # 应用的Secret_Key


class Audio:

    def save_voice(self, files, data):
        vFiles = wave.open('command.wav', 'wb')  # 打开音频储存文件
        vFiles.setframerate(framerate)  # 设置采样率
        vFiles.setsampwidth(samewidth)  # 设置保存的位数
        vFiles.setnchannels(channael)  # 设置声道
        vFiles.writeframes(b''.join(data))  # 把符合音频格式的数据写入到文件中
        vFiles.close()  # 关闭音频文件

    def record_voice(self):  # 语音的录入
        PA = pyaudio.PyAudio()  # 创建一个录音器对象
        stream = PA.open(format=pyaudio.paInt16,  # 设置位深
                         channels=channael,  # 设置声道
                         rate=framerate,  # 设置采样率
                         input=True,  # 支持语音数据的写入
                         frames_per_buffer=CHUNK)  # 设置音频数据存入缓冲区的大小
        print('正在录音....')

        save_voice_data = []  # 用于存储音频数据
        for i in range(int(framerate / CHUNK * record_time)):
            # 数据量 = （采样率 * 采样位数 * 声道数 * 时长）
            save_data = stream.read(CHUNK)  # 音频数据
            save_voice_data.append(save_data)

        with open('command.wav', mode='wb') as f:
            f.close()

        self.save_voice('command.wav', save_voice_data)
        print('录音完成....')
        stream.close()  # 关闭音频文件

    def get_voice_content(self, files):  # 获取音频文件的数据
        with open(files, 'rb') as f:  # 以二进制读的方式打开音频文件
            return f.read()

    def shibie_voice(self):
        client = AipSpeech(APP_ID, API_Key, Secret_Key)  # 通过应用的APP_ID、API_Key、Secret_Key连接百度云

        error_code = [i for i in range(3300, 3313)]  # 构建错误码列表
        print('正在识别.....')
        files = 'command.wav'  # 合成文件路径信息
        content = client.asr(self.get_voice_content(files), 'wav', 16000, {
            'dev_pid': 1536})  # 通过语音应用接口实现音频文件的识别
        if content['err_no'] in error_code:  # 判断识别的结果是否出现错误码
            print('未能识别语音内容....')
            return None
        else:
            print('内容：', content['result'][0])
            return content['result'][0]
