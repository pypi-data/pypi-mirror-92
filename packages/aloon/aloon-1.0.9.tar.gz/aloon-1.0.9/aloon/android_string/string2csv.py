from genericpath import exists
import os, collections
from os.path import curdir
from xml.dom import minidom
import codecs
import io
from .ordered_set import OrderedSet

class Convert:

  DEBUG = False

  def unescapeAndroidChar(self, text):
      text = text.replace("\\'", '\'')
      return text

  def getLangsFromDir(self, res_path):
    curdir = os.getcwd()
    os.chdir(res_path)
    langs = []
    for x in os.walk('.'):
        code = self.getLangDir(x[0])
        if code is not None:
            langs.append(code)
    os.chdir(curdir)
    return langs
  
  def getLangDir(self, dir_name):
    """
    Supported langauge directories follow one of three patterns:
    https://support.google.com/googleplay/android-developer/table/4419860
    1) values-**
    2) values-**-**
    3) values-**-***
    returns code for language or None if not a language directory
    """
    if dir_name[2:].startswith('values-'):
        code = [dir_name[9:]][0]
        if (len(code) == 2) or (len(code) == 5 and code[2] == '-') \
                or (len(code) == 6 and code[2] == '-'):
            return code

    # not a language dir
    return None

  def fetchLanguageFromInput(self, resourcePath):
      language = input('export language list. if don\'t input, export all. (e.g.: \'zh-rCN es-rCL\'):')
      allLans = self.getLangsFromDir(resourcePath)
      if not language:
        exportLans = allLans
      else:
        exportLans = language.split(' ')
        if set(exportLans) <= set(allLans):
          pass
        else:
          print('language input error, can\'t find these languages, please input again.')
          exportLans = self.fetchLanguageFromInput(resourcePath)
      return exportLans
  
  def fetchResourcePathFromInput(self):
      path = input('Path to Android project resource directory. (e.g.: \'/root/user/project/module/src/main/res\':')
      if not os.path.exists(path):
        print('input path isn\'t exsit, make sure path is correct')
        path = self.fetchResourcePathFromInput()
      return path

  def fetchOutputFilePathFromInput(self):
      path = input('Path to CSV file (output). (e.g.: \'/root/user/directory/csvname.csv\')')
      if not path:
        curdir = os.getcwd()
        path = curdir + "/android-string.csv"
      self.create_file(path)
      return path
  
  def create_file(self, filename):
        path = filename[0:filename.rfind("/")]
        if not os.path.isdir(path):
            os.makedirs(path)
        if not os.path.isfile(filename):
            fd = io.open(filename, mode="w", encoding="utf-8")
            fd.close()
        else:
            pass

  def run(self):
    print('************** attention: input content use \'\'**********************')
    resourcePath = self.fetchResourcePathFromInput()
    exportLans = self.fetchLanguageFromInput(resourcePath)
    outputFilePath = self.fetchOutputFilePathFromInput()
    self.convert(exportLans, resourcePath, outputFilePath)
    pass

  def convert(self, lans, resourcePath, outputFilePath):
    csvSep = "\t"
    resourcePath = resourcePath
    outputFilePath = outputFilePath
    exportLanguages = lans
    folderList = os.listdir(resourcePath)
    languageDict = dict()
    for f in folderList:
      if f.startswith("values"):
        if f == 'values':
          curLanguage = 'default' 
        else:
          curLanguage = f.replace('values-', '')
        if curLanguage in exportLanguages or curLanguage == 'default':
          languageDict[curLanguage] = dict()
          stringsDict = languageDict[curLanguage]
          valuesPath = os.path.join(resourcePath,f)
          if os.path.isdir(valuesPath):
            filePath = os.path.join(valuesPath, "strings.xml")
            if os.path.exists(filePath):
              #Open String XML
              #print(filePath)
              xmldoc = minidom.parse(filePath)
              rootNode = xmldoc.getElementsByTagName("resources")
              if len(rootNode) == 1:          
                nodeList = rootNode[0].childNodes
                for n in nodeList:
                  attr = n.attributes
                  if attr != None:
                    tag = n.tagName
                    if tag == 'string':
                      key = attr['name'].nodeValue
                      value = n.childNodes[0].nodeValue
                      stringsDict[key] = value.strip()
                      #print(key + " = " + value)
                    elif tag == 'string-array':
                      name = attr['name'].nodeValue
                      itemList = n.getElementsByTagName("item")
                      for idx, item in enumerate(itemList):
                        key = str(name)+","+str(idx)
                        value = item.childNodes[0].nodeValue
                        #print(key + " = " + value)
                        stringsDict[key] = value.strip()
                    else:
                      if self.DEBUG:
                        print("Unknown node")
            else:
              if self.DEBUG:
                print('Invalid ressource file. We expect a ressources node')
            #for s in itemlist :          
              #print(s)

    #Get all key list
    uniqueKeys = set()
    for k in languageDict:
      stringsDict = languageDict[k]
      for keys in stringsDict:
        uniqueKeys.add(keys)
    uniqueKeys = OrderedSet(sorted(uniqueKeys))

    #Write CSV
    with codecs.open(outputFilePath, 'w', "utf-8") as f:
      f.write(u'\ufeff') #UTF8 Marker
      f.write("key" + csvSep)
      for k in languageDict:
        f.write(k + csvSep)
      for key in uniqueKeys:
        f.write("\n")
        f.write(key+csvSep)
        totalCount = len(languageDict)
        for k in languageDict:
          stringsDict = languageDict[k]
          if key in stringsDict:
              f.write(self.unescapeAndroidChar(stringsDict[key]) + csvSep) 
          else:
              f.write(" " + csvSep)
    print('string convert success, csv file saved path: ' + outputFilePath)

  def test(self):
      # lans = 'zh-rCN es-rCL'
      outpath = os.getcwd() + "/android-string.csv"
      resPath = '/Users/didi/DidiProjects/PassengerSug-dev/global_sug/src/main/res'
      lans = self.getLangsFromDir(resPath)
      Convert().convert(lans, resPath, outpath)
      pass

if __name__ == "__main__":
    Convert().run()
    pass