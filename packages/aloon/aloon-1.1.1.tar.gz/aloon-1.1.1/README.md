## Getting started

To install run:
```bash
pip install aloon
```

## Usage

### Options

#### -h, --help
aloon命令帮助信息

#### str2csv
导出Android 指定语言的string文件到CVS，根据命令行提示操作。

#### build

##### -h
build命令帮助信息

##### -n --option
指定编译工程名称或者别名（配置文件中配置）

##### -o --option
默认有两个选项 
i: 打包并安装 = installDebug
u: 上传library到maven
其他可以自己指定build任务，.e.g. assembleRelease assembleGlobalDebug 等等

##### -c --config 
指定配置文件路径

##### 配置文件说明
```json
{
	"suffix": "rtl",     // 上传的maven包的版本号后面追加的后缀，方便maven库清理，验证完毕可以根据后缀清理干净
	"outputs": "/Users/didi/Record/outputs",    // build包的输出目录
	"projects": [{
			"name": "GlobalPassenger",          // build -n 后面的参数  编译的工程名称
			"alias": "99",                      // build -n 后面的参数  编译的工程名称，和nane二选一，通常为了输入方便配置简写
			"path": "/Users/didi/DidiProjects/GlobalPassenger",   // 工程在电脑的路径
			"build": "true",     // 是否编译该工程，如果此工程作为library，无修改时候可配置不编译，配置false。
            "dependencies": [{   
				// 该工程的依赖工程，配置依赖工程的工程名和依赖该工程的maven引用版本变量，工程编译时候会先编译依赖工程，只要配置了依赖工程，需要配置依赖工程的完整信息
				"name": "PassengerMapFlow",   // 依赖工程名称
				"gradle_placeholder": "map_global_sdk_version"  // 引用的依赖工程的版本变量
			}]
		},
		{
			"name": "PassengerSug",
			"alias": "sug",
			"path": "/Users/didi/DidiProjects/PassengerSug-dev",
			"build": "false",
			"upload_version": "",            // 如果该工程为library，需要上传maven，则需要配置上传版本号
            "upload_version_placeholder": "VERSION"  // 如果该工程为library，需要上传maven，需要配置版本号的引用变量
		},
		{
			"name": "PassengerMapFlow",
			"alias": "mapflow",
			"path": "/Users/didi/DidiProjects/PassengerMapFlow",
			"build": "false",
			"upload_version": "",
			"upload_version_placeholder": "VERSION",
			"dependencies": [{
				"name": "GlobalMapComponents",
				"gradle_placeholder": "global_map_components_version"
			}, {
				"name": "PassengerSug",
				"gradle_placeholder": "global_sug_sdk_version"
			}]
		},
		{
			"name": "GlobalMapComponents",
			"alias": "component",
			"path": "/Users/didi/DidiProjects/GlobalMapComponent",
			"build": "false",
			"upload_version": "",
			"upload_version_placeholder": "VERSION"
		}
	]

}
```

##### build命令使用示例：
1. aloon build -c 配置文件路径  
2. aloon build -n 99 -o i 打包安装99包  
   aloon build -n 99 -o assembleGlobalDebug  打包99全球版  
   aloon build -n sug -o u  打包并上传sug到maven  

## 上传Python库
```shell
python3 setup.py sdist bdist_wheel                      // 打包
python3 -m twine upload --repository pypi dist/*        // 上传
pip install --upgrade aloon                             // 更新
```

## 常见问题
1. 安装或者使用失败
请使用python3.9以上版本
更新方式:
```shell
brew upgrade 
brew intall python
```
2. python提示行退出：
   CTRL+D

## TODO
1. RTL插件  （避免后续需求做重复的开发）  
   i   自动完成left start, right end的替换  
   ii  自动对TextView, EditView样式插入  
   iii 自动导出自定义TextView, EditView的类进行相关说明  
   iv  对ani drawable的xml文件替换  
   v   根据配置对图片翻转并生成drwable-ldrtl文件，不同清晰度图片根据原有图片存放目录生存不同清晰度目录  
   vi  gradle脚本进行编译检查，输出不满足既定规则项  
   vii 其他根据RTL开发中遇到问题进行补充  

2. Android string分析插件完善，目前只支持导出指定语言的字符串。  
   i  分析并导出各个没有国际化的语言项  
   ii csv文件导入value（做通用工具可以考虑实现，目前公司有相应多语言插件，不做实现）  

3. 其他重复性比较频繁工作，可以立项做成插件形式  

## Release History
* 2020-12-29   v0.1.0  导出指定语言到CSV文件
* 2021-1-7     v1.0.5  多工程打包

## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).
