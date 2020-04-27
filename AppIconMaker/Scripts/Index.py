# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 22:09
# @Author  : ZhiMa_Maker
# @Email   :  yongtao_vip@163.com
# @File    : Index.py
# @Software : PyCharm
import log_utils, file_manager, icon_tool, splash_tool, badge_tool, ipa_utils
import json
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])

# 定义预加载路径
root_icon = "upload/icon/"
root_splash = "upload/splash/"
root_badge = "upload/badge/"

temp_icon = "temp/icon/"
temp_splash = "temp/splash/"
temp_badge = "temp/badge/"

output_icon = "output/icon/"
output_splash = "output/splash/"
output_badge = "output/badge/"

def checkResourcesDir():
    log_utils.info("正在检查资源路径,请稍后.....")
    # 检查备用资源
    dirs = [root_icon,root_splash,root_badge,output_icon,output_splash,output_badge]
    for item in dirs:
        log_utils.info(file_manager.createFilePath(item))


def selectFunctionNum():
#    return 3
    array = ["获取APPIcon", "获取Splash闪屏", "给APPIcon添加角标", "ipa包去签名", "请重新选择正确的功能编号"]
    num = int(input("请输入要执行的程序：\n\t0 获取APPIcon\n\t1 获取Splash闪屏\n\t2 给APPIcon添加角标\n\t3 ipa包重签名\n"))
    if num > 3:
        num = 4
        print(array[num])
        return num

    else:
        print("您选择了功能" + array[num])
        return num


if __name__ == '__main__':

    # 0、检查资源路径
    checkResourcesDir()

    # 1、选择程序功能
    i= 0
    num = 5
    while i<5 :
        i+=1
        num=selectFunctionNum()
        print(sys.argv[1])
        log_utils.printf()
        # num= int()
        if [0,1,2,3].__contains__(num):
            break

    # 2、获取预备资源  icon   splash   badge 并进入处理
    result = 0
    if num == 0:
        result = icon_tool.dealWithIconPath()
    elif num == 1:
        result = splash_tool.dealWithSplashPath()
    elif num == 2:
        result = badge_tool.dealWithBadgePath()
    else:
        result = ipa_utils.removeIpaSigning()

    # 3、获取处理结果
    """ 
    result结果定义
        200     处理成功
        101     找不到文件
        500     路径错误
        10000   未知原因   
    """
    if result == 200:
        log_utils.printf("*",5)
        log_utils.info("成功" + "*")
        log_utils.printf("*",3)



