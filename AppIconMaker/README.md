# 自动化视图工具操作提示：


#### 环境要求：（请提前配置好软件运行环境，添加相应的依赖库）
##### （1）操作系统：Linux或者Windows
##### （2）软件环境：Python2.7
##### （3）需要的插件：PLI（图像处理）【后期优化为OpenCV，环境升级为Python3.0以上】

## 说明：本工具提供了iOS和安卓的icon和LaunchImage切图功能，可通过一行命令快速获取所需要规格的切图。

##### 使用方法：
###### 首先进入工程文件路径：cd /Users/用户名/Desktop/AppIconMaker/
###### 一键切图标：python AutoProcessor.py icon
###### 一键切带有角标的图标（需要提前添加角标）：python AutoProcessor.py FloatIcon
###### 一键切LaunchImage：python AutoProcessor.py  screenshot



##  一、目录结构

#### 1、upload文件夹  包括APPIcon、LaunchImage、FloatIcon（角标）

##### upload文件夹用于存储上传文件，文件为覆盖安装，所以需要指定文件名称.
##### 图片上传规则:
    ① APPIcon名称为APPIcon.png
    ② LaunchImage闪屏图片两张，为防止转换失真，规格要求为2436x1125 和 1125x2436,
    命名为LaunchImageP.png 和 LaunchImageL.png 表示竖屏和横屏文件
    ③ FloatIcon为角标文件，命名为FloatIcon.png

#### 2、temp文件夹

#####temp文件夹是用于存放操作过程中的临时处理文件，作为一个中转站功能。此处的文档结构不需要理会。


#### 3、cache文件夹

##### cache文件夹用于存放处理过的闪屏和icon，文件夹内部区分AppIcon和LaunchImage文件夹，文件以日期（20191109140810.zip）的形式保存，保证文件名称的唯一性，服务端要对文件做名称的标注，便于后期查找下载。


#### 帮助支持：
##### pip 安装PLI库  python的库一般都用pip安装。安装命令：  pip install Pillow 
##### 目前版本只允许上传规定尺寸的LaunchImage图片，请上传之前提前做好处理，后期
会优化相关功能，支持更多格式的文件
