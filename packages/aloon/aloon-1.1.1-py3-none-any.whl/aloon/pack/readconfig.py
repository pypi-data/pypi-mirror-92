# -*- coding: UTF-8 -*-

import configparser
import os

'''定义一个读取配置文件的类'''
class ReadConfig:
     
    def __init__(self, configName=None):
        root_dir = os.path.dirname(os.path.abspath('.'))
        # 当前文件所在目录
        filePath = os.path.dirname(os.path.realpath(__file__))
        print('root_dir:' + root_dir + ', filePath:' + filePath)
        if configName:
            self.configPath = os.path.join(root_dir, filePath + "/config/" + configName)
        else:
            self.configPath = os.path.join(root_dir, filePath + "/config/config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(self.configPath)

    def get_value(self, section, key):
        if self.cf.has_option(section, key):
            value = self.cf.get(section, key)
        else:
            value = ''
        return value

    def set_value(self, section, key, value):
        self.cf.set(section, key, value)
        with open(self.configPath, 'w') as configFile:
             self.cf.write(configFile)


if __name__ == '__main__':
    test = ReadConfig('init.ini')
    # t = test.get_value("Version", "SugVersion")
    # print(t)
    # if t:
    #     print('is not null')
    # else:
    #     print('is null')

    test.set_value("INIT", "NeedInit", "false")


