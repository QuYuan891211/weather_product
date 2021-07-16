#!/usr/bin/env python

# encoding: utf-8

# @Time    : 2020/7/25 10:51
# @Author  : Qu Yuan
# @Site    : 
# @File    : HdqxService.py
# @Software: PyCharm
import os
import FTPManager
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

global config_path
config_path = r'E:\projects\pycharm\weather_product\Background\docs\HdqxConfig.ini'
global section_ftp
section_ftp = 'FTP'
global section_local
section_local = 'LOCAL'


class HdqxService:
    def __init__(self, config_path, section_ftp, section_local):
        self.ftp_Manager = FTPManager.FTPManager(config_path, section_ftp)
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
                if '.txt' == os.path.splitext(f)[1] and 18 == len(f):
                    local_path = local_dir + f
                    fileDate = f[6:14]
                    now = datetime.date.today()
                    time_str = datetime.datetime.strftime(now, '%Y%m%d')
                    if time_str == fileDate:
                        new_filename = 'NMF_TRF_RI_CSDT_' + fileDate + '00_072h_OCE.txt'
                        remote_path = remote_dir + new_filename
                        is_success = self.ftp_Manager.upload_file(local_path, remote_path)
                        if is_success:
                            print('成功上传: ' + f)
                            count = count + 1
                        else:
                            print('上传失败：' + f)
        else:
            print('没有这个路径，请检查配置文件')
        print('海岛气象预报总共上传' + str(count) + '个文件')
        # localtime = time.asctime(time.localtime(time.time()))
        print(datetime.datetime.now())
        self.ftp_Manager.close_connect()


def scheduleTask():
    times = 0;
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # scheduler.add_job(task, "cron", day_of_week="0-6", hour=19, minute=30)
    scheduler.add_job(task, "cron", day_of_week="0-6", coalesce=True, misfire_grace_time=3600, hour=20, minute=20)
    # scheduler.add_job(task, 'interval', seconds=120, id='task1')

    scheduler.start()


def task():
    hdqxService = HdqxService(config_path, section_ftp, section_local)

    hdqxService.upload_files()


if __name__ == "__main__":
    scheduleTask()
