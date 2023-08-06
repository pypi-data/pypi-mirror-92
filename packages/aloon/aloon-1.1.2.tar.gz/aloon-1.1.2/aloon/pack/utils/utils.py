# -*- coding: UTF-8 -*-

import re
import shutil
import os

class Utils:

    # 最后数值加1，然后加上后缀
    @staticmethod
    def generate_verison(version, suffix):
        versions = re.findall(r"\d+", version)
        lastVersion = versions[-1]
        num = int(lastVersion) + 1
        newNum = str(num).zfill(3)
        versions[-1] = newNum
        return '.'.join(versions) + '-' + suffix

    # 使用指定后缀
    @staticmethod
    def generate_verison_with_suffix(version, suffix):
        versions = re.findall(r"\d+", version)
        return '.'.join(versions) + '-' + suffix

    @staticmethod
    def get_file_list(dir, fileType):
        file_list = []
        for home, dirs, files in os.walk(dir):
            for file_name in files:
                if(file_name[-len(fileType):] == fileType):
                    file_list.append(os.path.join(home, file_name))
        return file_list

    # 删除某一目录下的所有文件或文件夹 filepath: 路径
    @staticmethod
    def del_files(file_dir):
        if os.path.isdir(file_dir):
            del_list = os.listdir(file_dir)
            for f in del_list:
                file_path = os.path.join(file_dir, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        else:
            print(file_dir + ' not exsit')
    
    def create_dir(dir):
        if os.path.exists(dir):
            return
        else:
            os.mkdir(dir)   


if __name__ == '__main__':

    # version = Utils.generate_verison("1.2.222", "david")
    # print(version)
    # version = Utils.generate_verison_with_suffix('1.2.222-fix', 'david')
    # print(version)

    Utils.del_files("/Users/didi/Tools/outputs")

    Utils.create_dir("/Users/didi/Tools/outputs")