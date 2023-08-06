# -*- coding: UTF-8 -*-
from re import findall
import sys
import os
from .utils import Utils, Replace
from . import global_var
from . import Config, Module, Dependency

class BuildComponent:

    def __init__(self, projectName):
        self.config: Config = global_var.get_value(global_var.CONFIG)
        self.module: Module = self.findModule(self.config.projects, projectName)
        print(self.module)
        self.suffix = self.config.suffix
        self.outputs = self.config.outputs
        self.projectDir = self.module.path
        if os.path.exists:
            Utils.del_files(self.outputs)
        else:
            Utils.create_dir(self.outputs)
    
    def findModule(self, projects: list, projectName):
      for project in projects:
          module: Module = project
          if (module.name == projectName or module.alias == projectName):
            return module
      return None
   
    def buildComponent(self, module: Module, option):
        # 只有执行upload时候，修改版本号
        version = module.upload_version
        if option == 'u':
            curVersion = ''
            if version:
                curVersion = Utils.generate_verison_with_suffix(version, self.suffix)
                print('config upload component version:' + version)
            else:
                oldVersion = self.getGradlePlaceHolderValue(module, module.upload_version_placeholder)
                print("oldVersion: " + oldVersion)
                if oldVersion != '':
                    newVersion = Utils.generate_verison(oldVersion, self.suffix)
                    curVersion = newVersion
                    print('don\'t config component upload version, need generate version, old version:' + oldVersion + ',generateVersion:' + newVersion)
                else:
                    print('can\'t fetch version code, check command right')
            self.setGradlePlaceHolderValue(module, module.upload_version_placeholder, curVersion)
        result = self.executeShell(option)
        if result != 0:
            sys.exit(0)
    
    def executeShell(self, option):
        print('execute component shell, option:' + option)
        # 当前文件所在目录
        file_path = os.path.dirname(os.path.realpath(__file__))
        return os.system(file_path + '/shell/build_component.sh ' + self.projectDir + ' ' + file_path + ' ' + option + ' ' + self.outputs)

    def handleDependencies(self):
        print('handle component dependencies')
        for dependency in self.module.dependencies:
            depend: Dependency = dependency
            self.handleDependencyModule(depend)
        
    def handleDependencyModule(self, dependency: Dependency):
        module: Module = self.findModule(self.config.projects, dependency.name)
        if module.build == 'false':
            return
        upload_version = module.upload_version
        if upload_version == '':
            # 没有指定module version时，先编译上传module，然后取module工程版本号
            buildComponent = BuildComponent(module.name)
            buildComponent.build('u')
            moduleVersion = buildComponent.getGradlePlaceHolderValue(module, module.upload_version_placeholder)
            print('don\'t config %s sdk version, fetch from sug project' % moduleVersion)
        else:
            moduleVersion = upload_version
        moduleVersion = Utils.generate_verison_with_suffix(moduleVersion, self.suffix)
        self.setGradlePlaceHolderValue(self.module, dependency.gradle_placeholder, moduleVersion)
        print('used %s sdk version:' % module.name + moduleVersion) 

    def setGradlePlaceHolderValue(self, module: Module, placeHolder, value):
        fileType = [".gradle", ".properties"]
        lookup_table=[[r'(^\s*e?x?t?\.?' + placeHolder + '[\s]*[=][\s]*)\'?[1-9]+.*\'?$', "\\1\'%s\'" %value]]
        Replace.replace_strings(self.projectDir, fileType, lookup_table)

    def getGradlePlaceHolderValue(self, module: Module, placeHolder):
        fileType = [".gradle", ".properties"]
        lookup_str = '^\s*e?x?t?\.?' + placeHolder + '[\s]*[=][\s]*\'?([1-9]+.*)\'?$'
        return Replace.get_string(self.projectDir, fileType, lookup_str)

    def build(self, option): 
        print('build module name: ' + self.module.name + ' ,build switch: ' + str(self.module.build))
        if self.module.build == 'true':
            print('buid component start...')
            self.handleDependencies()
            self.buildComponent(self.module, option)
            print('buid comonent end.')
        else:
            print('build closed, you can open it in config.')

    


