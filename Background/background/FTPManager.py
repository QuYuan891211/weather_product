#!/usr/bin/env python

# encoding: utf-8

# @Time    : 2020/7/2 9:53
# @Author  : Qu Yuan
# @Site    : 
# @File    : FTPManager.py
# @Software: PyCharm

import os
import socket
import configparser
import time
from ftplib import FTP

import codecs

# config_path = r'E:\projects\pycharm\NearGoos\background\byQY\config\Config.ini'
class FTPManager:

    def __init__(self, config_path, section):
        self.config_path = config_path
        self.ftp = FTP()
        self.section = section

        # 重新设置下编码方式
        self.ftp.encoding = 'UTF-8'

    def ftp_connect(self, host, username, password):
        """
        连接FTP
        :param host: 主机地址
        :param username: 用户名
        :param password: 密码
        :return:
        """
        # socket.setdefaulttimeout(3600)

        self.ftp.connect(host)
        self.ftp.login(username, password)


    def get_file_info_list(self, filepath):
        """
        以文本的方式获得文件信息列表
        :param filepath: 文件目录
        :return:
        """
        self.ftp.cwd(filepath)
        file_list = self.ftp.retrlines('MLSD')
        # file_list = self.ftp.nlst()
        # print(file_list)
        return file_list

    def get_config(self):
        """
        获取配置文件信息
        :return: 配置文件类
        """
        config = configparser.ConfigParser()
        config.read(self.config_path, encoding='UTF-8-sig')
        return config

    def close_connect(self):
        """
        关闭FTP链接
        :return:
        """
        self.ftp.close()

    def get_filename(self, file_need, filepath):
        """
        返回指定文件名的文件目录
        :param file_need: 需被匹配的文件名
        :param filepath: 文件目录
        :return: 文件名数组
        """
        self.ftp.cwd(filepath)
        files = [filename for filename in self.ftp.nlst() if file_need in filename]
        return files


    def get_file_size(self, file_need, filepath):
        self.ftp.cwd(filepath)
        files = [filename for filename in self.ftp.nlst() if file_need in filename]
    # # 存储
    # def upload(self, target_path, old_path):
    #     fp = open(old_path, "rb")
    #     buf_size = 1024
    #     self.storbinary("STOR {}".format(target_path), fp, buf_size)
    #     fp.close()
    # def is_exist_file(self, local_file, remote_file):
    #     str_year = self.getCreateTime(self, remote_file)
    #

    def is_same_size(self, local_file, remote_file):
        """
        判断远程文件和本地文件大小是否一致
        :param local_file: 本地文件
        :param remote_file: 远程文件
        :return: 是否一致的布尔值
        """

        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception as err:
            # self.debug_print("is_same_size() 错误描述为：%s" % err)
            remote_file_size = -1
        try:
            local_file_size = os.path.getsize(local_file)
        except Exception as err:
            # self.debug_print("is_same_size() 错误描述为：%s" % err)
            local_file_size = -1
        # self.debug_print('local_file_size:%d  , remote_file_size:%d' % (local_file_size, remote_file_size))
        if remote_file_size == local_file_size:
            return 1
        else:
            return 0

    # [to-do] 此处可增加为批量下载
    def download_file(self, local_file, remote_file, local_file_dir):
        """
        下载远程文件至本地
        :param local_file:本地文件
        :param remote_file:远程文件
        :return:
        """
        if os.path.exists(local_file):
            # self.debug_print('%s 文件大小相同，无需下载' % local_file)
            print('文件已有无需下载')
            return 0
        else:
            if not os.path.exists(local_file_dir):
                os.makedirs(local_file_dir)
            # self.debug_print('>>>>>>>>>>>>下载文件 %s ... ...' % local_file)
            buf_size = 1024
            file_handler = open(local_file, 'wb')
            self.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size)
            file_handler.close()
            print('下载数据成功')
            with open(local_file, 'rb+') as fp:
                content = fp.read()
                try:
                    #
                    content.decode("utf8")
                except:
                    content = content.decode("ANSI",'ignore').encode("utf8")
                    fp.seek(0)
                    fp.write(content)
                fp.close()
            print('转码成功')

            return 1

    def upload_file(self, local_file, remote_file):
        """
        从本地上传文件至FTP
        :param local_path:
        :param remote_path:
        :return:
        """
        if not os.path.isfile(local_file):
            # self.debug_print('%s 不存在' % local_file)
            print('不存在')
            return False
        if self.is_same_size(local_file, remote_file):
            # self.debug_print('%s 文件大小相同，无需上传' % local_file)
            print('大小相同无需上传')
            return False

        buff_size = 1024

        file_handler = open(local_file, 'rb')
        self.ftp.storbinary('STOR %s' % remote_file, file_handler, buff_size)
        file_handler.close()
        # self.debug_print('上传: %s' % local_file + "成功!")
        return True

    # 获取年份
    def getCreateTime(self, remote_file):
       L = list(self.ftp.sendcmd('MDTM ' + remote_file))
       str = L[4]+L[5]+L[6]+L[7]
       return str