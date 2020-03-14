# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 11:04
# @Author  : ZhiMa_Maker
# @Email   :  yongtao_vip@163.com
# @File    : icon_tool.py
# @Software : PyCharm
# 处理appicon程序
import os
import os.path
import sys
import zipfile
import datetime
import log_utils, file_manager, Index
from PIL import Image, ImageDraw
import shutil


def make_archiveWithInfo():
    """压缩文件到指定文件夹"""
    nowtimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    temp_icon_path = file_manager.createFilePath(file_manager.getFullPath(Index.temp_icon))
    new_path = shutil.make_archive(file_manager.getFullPath(Index.output_icon) + nowtimestr, 'zip', temp_icon_path)
    log_utils.printf()
    log_utils.info("打包结束之后的zip路径为:" + new_path)



def processingIcons(appicon_path="",platform="ios",sizeArray=[]):
    """APPIcon的处理流程"""
    # 获取icon原图
    origin_image = Image.open(appicon_path).convert("RGBA")

    for x in range(0, len(sizeArray)):
        width = sizeArray[x][1]
        # 调整图像大小
        outImage = origin_image.resize((width, width), Image.BILINEAR)

        if platform == "ios":
            imgName = sizeArray[x][0] + ".png"
            file_manager.joinFilePath(file_manager.getFullPath(Index.temp_icon),platform+"/AppIcon.appiconset")
            temp_ios_path = file_manager.createFilePath(file_manager.getFullPath(Index.temp_icon)+platform+"/AppIcon.appiconset")
            print(temp_ios_path)
            outImage.save(temp_ios_path + "/" + imgName, "png")
            print(temp_ios_path + "/" + imgName)
            if x == 0:
                file_manager.joinFilePath(file_manager.getFullPath(Index.temp_icon), platform)
                temp_ios_path = file_manager.createFilePath(file_manager.getFullPath(Index.temp_icon) + platform +"/AppIcon.appiconset")
                content_path = file_manager.getFullPath("upload/icon/jsonfile")
                log_utils.info(temp_ios_path +"\n" +content_path)
                file_manager.copyFiles(content_path, temp_ios_path)

        elif platform == "android":
            typeFileName = sizeArray[x][0]
            imgName = "ic_launcher.png"
            file_manager.joinFilePath(file_manager.getFullPath(Index.temp_icon),platform + "/" +typeFileName)
            temp_android_path = file_manager.createFilePath(file_manager.getFullPath(Index.temp_icon)+platform+ "/" +typeFileName)
            print(temp_android_path)
            outImage.save(temp_android_path + "/" + imgName, "png")
            print(temp_android_path  + "/" + imgName)
        else:
            log_utils.warning("平台选择错误")











def dealWithIconPath():
    """外部入口"""
    log_utils.info("进入appicon处理程序---开始处理icon")
    # 检查资源
    tempfile = file_manager.getFullPath("upload/icon");
    file_manager.clear(tempfile)

    # 1、获取icon的全路径文件夹
    iconPath = file_manager.getFullPath(Index.root_icon)

    # 2、获取该路径下的所有文件
    icons = file_manager.list_files(iconPath, [], ".DS_Store");
    if len(icons) == 0:
        log_utils.info("还没有上传appicon资源文件，请上传之后操作！")
        return 101
    else:
        # 如果数组不为空，取出第一个元素
        # 获取到icon文件
        for filename in icons:
            if ".png" in filename:
                appIconDir = filename


    iOSIconSizes = [("icon-20@2x", 40), ("icon-20@3x", 60), ("icon-29@2x", 58), ("icon-29@3x", 87),
                    ("icon-40@2x", 80), ("icon-40@3x", 120), ("icon-60@2x", 120),
                    ("icon-60@3x", 180), ("icon-1024", 1024), ("icon-20", 20), ("icon-40", 40),
                    ("icon-72", 72), ("icon-72@2x", 144), ("icon-76", 76), ("icon-76@2x", 152),
                    ("icon-83.5@2x", 167)]
    AndroidIconList = [("drawable-ldpi", 36,"icon-36"), ("drawable-mdpi", 48,"icon-48"), ("drawable-hdpi", 72,"icon-72"),
                       ("drawable-xhdpi", 96,"icon-96"),
                       ("drawable-xxhdpi", 144,"icon-144"), ("drawable-xxxhdpi", 192,"icon-192"),
                       ("drawable", 512,"icon-512")]


    processingIcons(appIconDir,"ios",iOSIconSizes)
    processingIcons(appIconDir,"android",AndroidIconList)
    make_archiveWithInfo()

