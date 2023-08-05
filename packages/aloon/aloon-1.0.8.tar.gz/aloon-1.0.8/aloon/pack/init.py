# -*- coding: UTF-8 -*-

from .readconfig import ReadConfig
from .build_mapflow import BuildMapFlow
from .build_global_passenger import BuildGlobalPassenger
import os
from .utils import *

class Init:
    
    def __init__(self):
        self.config = ReadConfig()
        #要改的文件类型（可以输入多个）
        self.file_type = [".gradle"]

    def init_mapflow(self):
        # sdk-mapflow/build.gradle中api 'com.xiaoju.nova:globalsug:2.2.090' 变更为api "com.xiaoju.nova:globalsug:${global_sug_sdk_version}"
        # sdk-mapflow/build.gradle中api 'com.xiaoju.nova:GlobalMapComponents:2.0.112' 变更为api "com.xiaoju.nova:GlobalMapComponents:${global_map_components_version}"
        #要改的文件夹
        project_dir = self.config.get_value("Project-Dir", "PassengerMapFlow")
        #替换表（可以用python正则表达式）
        lookup_table=[[".*api.+com.xiaoju.nova.globalsug.*", "api \"com.xiaoju.nova:globalsug:${global_sug_sdk_version}\""],
                       [".*api.+com.xiaoju.nova.GlobalMapComponents.*", "api \"com.xiaoju.nova:GlobalMapComponents:${global_map_components_version}\""]]
        utils.Replace.replace_strings(project_dir, self.file_type, lookup_table)

        # sdk-mapflow/gradle.properties中新增global_sug_sdk_version=2.2.131和global_map_components_version=2.0.129-david
        build_mapflow = BuildMapFlow()
        build_mapflow.setProperties("global_sug_sdk_version", "2.2.131")
        build_mapflow.setProperties("global_map_components_version", "2.0.129")

    def init_global_passenger(self):
        # build.gradle中删除ext.map_global_sdk_version = '3.2.355'
        # 要改的文件夹
        project_dir = self.config.get_value("Project-Dir", "GlobalPassenger")
        # 替换表（可以用python正则表达式）
        lookup_table=[[".*ext.map.global.sdk.version.*", ""]]
        utils.Replace.replace_strings(project_dir, self.file_type, lookup_table)
        
        # GlobalPassenger 工程 gradle.properties中新增map_global_sdk_version=3.2.366-david
        buildGlobalPassenger = BuildGlobalPassenger()
        buildGlobalPassenger.setProperties("map_global_sdk_version", "3.2.366")
    
    def init_python_env(self, build_path):
        alias = 'alias didi=\'python3 %s/build.py\'\n' % build_path
        homefolder = os.path.expanduser('~')
        bashrc = os.path.abspath('%s/.bash_profile' % homefolder)
        with open(bashrc, 'r') as f:
          lines = f.readlines()
          if alias not in lines:
            out = open(bashrc, 'a')
            out.write(alias)
            out.close()
          else:
            print('you had set alias didi, please delete the repeat setting.')
              
        os.system('source %s' % bashrc)

    def init(self):
        init_config = ReadConfig('init.ini')
        need_init = init_config.get_value("INIT", "needinit")
        if need_init == 'true':
            print('****************** init python environment ')
            build_path = os.path.dirname(os.path.realpath(__file__))
            print('build path :' + build_path)
            self.init_python_env(build_path)
            print('****************** init project *****************')
            init = Init()
            init.init_mapflow()
            init.init_global_passenger()
            init_config.set_value("INIT", "needinit", "false")
        else:
            print('you had inited, are you sure reinit?')


if __name__ == '__main__':
    Init().init()







