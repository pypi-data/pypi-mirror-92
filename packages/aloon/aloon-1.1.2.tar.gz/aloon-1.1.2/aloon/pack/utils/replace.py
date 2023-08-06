# -*- coding: UTF-8 -*-

from logging import PlaceHolder
import os
import re
# from utils import Utils

class Replace:

    @staticmethod
    def get_file_list(dir, file_type):
        file_list = []
        for home, dirs, files in os.walk(dir):
            for file_name in files:
                if(file_name[-len(file_type):] == file_type):
                    file_list.append(os.path.join(home, file_name))
        return file_list

    @staticmethod
    def replace_strings(dir, file_type, lookup_table):
        for type in file_type:
            print("开始处理" + type + "类型文件")
            file_list = Replace.get_file_list(dir, type)
            print("共发现" + str(len(file_list)) + "个" + type + "类型文件")
            replace_count = 0
            file_count = 0
            for file in  file_list:
                file_count = file_count + 1
                if(file_count % 100 == 0):
                    print("修改到第" + str(file_count) + "个文件")
                file_data = ""
                with open(file, "r", encoding = "utf-8") as f:
                    for line in f:
                        for item in lookup_table:
                            if re.search(item[0], line):
                                print("--------------- line" + line)
                                #print("正在修改从"+item[0]+"到"+item[1])
                                line = re.sub(item[0], item[1], line)
                                replace_count = replace_count + 1
                        file_data += line
                with open(file, "w", encoding="utf-8") as f:
                    f.write(file_data)
            print("一共进行了" + str(replace_count) + "处替换")
            print("结束处理" + type + "类型文件")
        print("全部结束")
    
    @staticmethod
    def get_string(dir, file_type, lookup_str):
        for type in file_type:
            print("开始处理" + type + "类型文件")
            file_list = Replace.get_file_list(dir, type)
            print("共发现" + str(len(file_list)) + "个" + type + "类型文件")
            file_count = 0
            for file in  file_list:
                file_count = file_count + 1
                if(file_count % 100 == 0):
                    print("修改到第" + str(file_count) + "个文件")
                with open(file, "r", encoding = "utf-8") as f:
                    for line in f:
                        if re.search(lookup_str, line):
                            print(line + '--------------')
                            return re.findall(lookup_str, line)[0]
        return ''

if __name__ == "__main__":
    fileType = [".gradle", ".properties"]

    placeHolder = 'VERSION'
    # projectDir = '/Users/didi/DidiProjects/PassengerSug-dev'
    # projectDir = '/Users/didi/DidiProjects/PassengerMapFlow'
    # lookup_str = '^\s*e?x?t?\.?' + placeHolder + '[\s]*[=][\s]*)\'?[1-9]+.*\'?$'
    # version = Replace.get_string(projectDir, fileType, lookup_str)
    # print(version + '+++++++')

    # newVersion = Utils.generate_verison(version, 'test')
    # print('new verison:' + newVersion)

    
    # placeHolder = 'map_global_sdk_version'
    
    # lookup_table=[[r'(^\s*e?x?t?\.?' + placeHolder + '[\s]*[=][\s]*)\'?[1-9]+.*\'?$', "\\1\'%s\'" %newVersion]]
    # Replace.replace_strings(projectDir, fileType, lookup_table)
    
    pass



