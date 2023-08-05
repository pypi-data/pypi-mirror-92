#！/usr/bin/env python
#_*_coding:utf-8_*_
import os
import argparse
import textwrap
from dataclasses import dataclass
from typing import *
from pathlib import Path
import tempfile
from .android_string import Convert
from .simple_parsing import ArgumentParser, field, subparsers
from .pack import Config
from .pack import global_var
from .pack import build
from .simple_parsing.helpers import Serializable

Version = '1.0.6'

General_Description = '''
Common operation tools
Version %s
''' % Version

tmpdir = tempfile.gettempdir()
Cache_Path = os.path.join(tmpdir, 'aloon_cache.json')

@dataclass
class LocalCache(Serializable):
    configPath: str = ''

@dataclass
class Str2csv:
    """Covert android string to csv file, you can specified language, or export all by default."""

    def execute(self):
        Convert().run()


@dataclass
class Build:
    """A command to compile your project according to configuration.
       Start: 1、 aloon build -c 'Your JSON PATH'
              2、 aloon build -n 'Your project name or alias' -o 'i, u or other gradle task(e.g. assembleDebug)'
    """

    # name: input the name or alias configured in the JSON file 
    name:   str = field(alias=["-n"], default='')

    # option: i: installDebug  u: uploadArchives or gradle task name
    option:  str = field(alias=["-o"], default='')

    # config: specifies the path to the JSON file 
    config:  str = field(alias=["-c"], default='')

    def execute(self):
        if os.path.exists(Cache_Path):
            try:
                print(Cache_Path)
                localCache = LocalCache.load_json(Cache_Path)
                config = Config.load_json(localCache.configPath)
                global_var.set_value(global_var.CONFIG, config)
            except:
                os.remove(Cache_Path)
                print('json config error, please check and re-associated, run aloon build -c JSON path')
        else:
            if self.config is '':
                print('please associated json config file. run aloon build -c JSON path.')
                return
            else:
                config = Config.load_json(self.config)
                global_var.set_value(global_var.CONFIG, config)
                loaclCache = LocalCache()
                loaclCache.configPath = self.config
                loaclCache.save_json(Cache_Path)
                return

        if self.name is not '' and self.option is not '':
            build.build(self.name, self.option)
        else:
            print('Command need -n and -o, For details, please enter aloon build -h')

@dataclass
class Program:
    """Some top-level command"""
    command: Union[Str2csv, Build]

    # log additional messages in the console.
    verbose: bool = field(alias=["-v"], default=False)  
    
    def execute(self):
        print(f"Program (verbose: {self.verbose})")
        return self.command.execute()

def main():
    global_var._init()
    parser = ArgumentParser()
    parser.add_arguments(Program, dest="aloon")
    args = parser.parse_args()
    prog: Program = args.aloon

    prog.execute()
    
if __name__ == "__main__":
    main()