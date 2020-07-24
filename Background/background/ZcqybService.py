#!/usr/bin/env python

# encoding: utf-8

# @Time    : 2020/7/23 10:02
# @Author  : Qu Yuan
# @Site    : 
# @File    : ZcqybService.py
# @Software: PyCharm
import os
from background.FTPManager import FTPManager
from pip._internal.utils import logging
from apscheduler.schedulers.blocking import BlockingScheduler
global config_path
config_path = r'E:\projects\pycharm\weather_product\Background\docs\ZcqybConfig.ini'
global section_neargoos
section_ftp = 'FTP'
global section_mysql
section_local = 'LOCAL'
class ZcqybService:
    def __init__(self, config_path, section_ftp, section_local):
        self.ftp_Manager = FTPManager(config_path, section_ftp)
        self.config_path = config_path
        self.section_ftp = section_ftp
        self.section_local = section_local
        self.username = ""
        self.password = ""
        self.host = ""
        self.config = self.ftp_Manager.get_config()
        self.host = self.config.get(section_ftp, 'host')
        self.username = self.config.get(section_ftp, 'username')
        self.password = self.config.get(section_ftp, 'password')
        self.target = self.config.get(section_ftp, 'target')

    def get_file_info(self):
        """
        获取数据信息列表
        :return file_infos: 数据信息列表
        """

        # 获取配置文件信息

        self.ftp_Manager.ftp_connect(self.host, self.username, self.password)

        # 获取时间
        # self.ftp_Manager.getCreateTime()
        file_infos = self.ftp_Manager.get_filename("", self.target)
        # for f in file_infos:
        #     print(f)
        return file_infos

    # 判断本地是否有此路径
    def check_file(self, local_dir):

        if not os.path.exists(local_dir):
            logging.debug('no such directory %s.'(local_dir))
            return False
        else:
            # 读入文件
            return True
            # for f in files:

    def upload_files(self):
        # 1.检查是否存在路径
        local_dir = self.config.get(self.section_local, 'dir')
        self.ftp_Manager.ftp_connect(self.host, self.username, self.password)
        if self.check_file(local_dir):
            files = os.listdir(local_dir)
            remote_dir = self.config.get(self.section_ftp, 'target')
            count = 0
            for f in files:
                if '.doc' == os.path.splitext(f)[1] or '.docx' == os.path.splitext(f)[1]:
                    local_path = local_dir + f
                    new_filename = 'NMF_MCP_POMET_CSDT_' + f[5:13] + '00_028d_OCE.doc'
                    remote_path = remote_dir + new_filename
                    is_success = self.ftp_Manager.upload_file(local_path, remote_path)
                    if is_success:
                        print('成功上传: ' + f)
                        count = count + 1
                    else:
                        print('上传失败：' + f)
        else:
            print('没有这个路径，请检查配置文件')
        print('总共上传' + str(count) + '个文件')
        self.ftp_Manager.close_connect()

# 定时任务
def scheduleTask():
    times = 0;
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(task, 'interval', seconds=120, id='task1')
    scheduler.start()

def task():
    zcqybService = ZcqybService(config_path, section_ftp, section_local)
    # zcqybService.check_file(zcqybService.config.get(zcqybService.section_local, 'dir'))
    # zcqybService.get_file_info()
    zcqybService.upload_files()


if __name__ == "__main__":
    scheduleTask()