import os
import shutil

class FileUtils(object):
    '''
    用于操作文件的工具类
    :version 1.0
    :Python version : 3.6
    :author : YJK923

    '''

    @staticmethod
    def read(self,file_name,mode):
        '''
        读取文件内容，返回文件内容，类型为字符串，若文件不存在，则返回空
        ：prarm file_name : 文件名
                mode : 打开模式，常用方式 r 或 rb
                    r : 以读方式打开，只能读文件
                    rb : 以二进制读方式打开，只能读文件
                    rt : 以文本读方式打开，只能读文件
                    rb+ : 以二进制方式打开，可以读写文件
        '''
        try:
            with open(file_name,mode) as f:
                f.seek(0) # 移动文件指针
                content = f.read()
                return content
        except Exception as e :
            print(e)

    @staticmethod
    def readline(self,file_name):
        '''
        一行一行的读取文件
        :param : file_name : 文件名
        '''
        try:
            with open(file_name,'r') as f:
                for line in f:
                    print(line)
        except Exception as e:
            print(e)

    @staticmethod
    def write(self,file_name,content,mode):
        '''
        清空文件并写入 content
        :param file_name : 文件名
               content : 写入内容
               mode : 打开模式，常用方式 w 或 wb 
                   w : 以写的方式打开，只能写文件，若文件不存在，先创建，再写
                   wb : 以二进制写方式打开，只能写文件，若文件不存在，先创建再写，反之，清空之后再写
                   wt : 以文本方式打开，只能写文件，若文件不存在，先创建再写，反之，清空之后再写
        '''         
        with open(file_name,mode) as f:
            f.write(str(content))

    @staticmethod
    def append_write(self,file_name,content):
        '''
        追加文件写入 content
        :param file_name : 文件名
               content : 追加内容
        '''
        with open(file_name,'a+') as f:
            f.write(str(content))

    @staticmethod
    def clear(self,file_name):
        '''
        清空文件内容
        :param: file_name : 文件名
        '''
        with open(file_name,'wb') as f:
            f.truncate() # 清空文件内容

    @staticmethod
    def remove(self,file_name):
        '''
        删除文件
        :param : file_name : 文件名
        '''
        try:
            os.remove(file_name)
        except Exception as e:
            print(e)

    @staticmethod
    def tell(self,file_name):
        '''
        获取文件中指针的值
        :param : file_name : 文件名
        '''
        try:
            with open(file_name,'a+') as f:
                L = f.tell()
                return L
        except Exception as e:
            print(e)

    @staticmethod
    def copyfile(self,source_name,target_name):
        '''
        复制文件，复制之后的文件在同一级目录中
        :param : source_name : 原文件名
                 target_name : 复制之后的文件名 
        '''
        try:
            with open(source_name,'rb') as f1, open(target_name,'wb') as f2:
                f2.write(f1.read())
        except Exception  as e:
            print(e)

    @staticmethod
    def movefile(self,source_name,path):
        '''
        移动文件到 path 路径下 示例：movefile('users.txt','D:\\FTPTest')
        :param : source_name : 原文件名称
                 path : 移动之后的目录信息
        '''
        try:
            with open(source_name,'rb') as f1, open(path+'\\'+source_name,'wb') as f2:
                f2.write(f1.read())
            os.remove(source_name)
        except Exception as e:
            print(e)
    
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
