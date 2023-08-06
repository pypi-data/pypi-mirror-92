
# -*- coding: UTF-8 -*-
import sys
from .utils import Utils
from .build_component import BuildComponent

def build(projectName, op):
    if op is not None:
        option = op
    else:
        option = 'u'

    if projectName is not None:
        buildComponent = BuildComponent(projectName)
        buildComponent.build(option)
    else:

        print('')
        print('general commands:')
        print('sug                      build Sug library')
        print('map                      build MapCompoent library')
        print('mapflow                  build MapFlow library')
        print('99                       build GlobalPassenger apk')

        print('')
        print('global options:')
        print('default                  same as -u')
        print('-i                       build and install apk')
        print('-u                       upload library to maven')




