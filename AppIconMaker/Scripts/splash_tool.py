# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 11:09
# @Author  : ZhiMa_Maker
# @Email   :  yongtao_vip@163.com
# @File    : splash_tool.py
# @Software : PyCharm
#  splash处理程序
import log_utils,file_manager,Index
from PIL import Image, ImageDraw
import os
import os.path
import sys
import zipfile
import datetime
import shutil

def make_archiveWithInfo():
    """压缩文件到指定文件夹"""
    nowtimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    temp_splash_path = file_manager.createFilePath(file_manager.getFullPath(Index.temp_splash))
    new_path = shutil.make_archive(file_manager.getFullPath(Index.output_splash) + nowtimestr, 'zip', temp_splash_path)
    log_utils.printf()
    log_utils.info("打包结束之后的zip路径为:" + new_path)


def processingWithSplash(image_path,platform="ios",ImageList=[]):
    # 加载图形
    origin_image = Image.open(image_path)
    w = float(origin_image.size[0])
    h = float(origin_image.size[1])
    # 先处理图片，然后根据需求进行图片的裁剪
    for i in range(0, len(ImageList)):

        if i == 0:
            file_manager.joinFilePath(file_manager.getFullPath(Index.temp_splash), platform)
            temp_splash_path = file_manager.createFilePath(file_manager.getFullPath(Index.temp_splash) + platform + "/LaunchImage.launchimage/")
            content_path = file_manager.getFullPath("upload/splash/jsonfile")
            file_manager.copyFiles(content_path, temp_splash_path)


        (dest_w, dest_h) = ImageList[i][1]
        if w > h:
            print("------------------检测到是横屏的图片，进行处理--------------------------")
            # 宽大于高，说明是横屏闪屏，切图以高为基准
            if dest_w > dest_h:
                print(origin_image.size)
                print((dest_w, dest_h))
                # 压缩图片（计算宽高）
                resizeH = dest_h
                resizeW = int(float(dest_h / h) * w)
                # 原始坐标为0 ，计算放大后的图像 左右的间距
                originx = 0
                if resizeW > dest_w:
                    originx = (resizeW - dest_w) / 2
                else:
                    originx = (dest_w - resizeW) / 2
                # 原图根据目标图进行缩放，传入的比较大分辨率，缩小
                origin_image = origin_image.resize((resizeW, resizeH), Image.ANTIALIAS)
                # 创建一张白色背景
                bgimageview = Image.new('RGBA', (dest_w, dest_h), (255, 255, 255))
                # 粘贴压缩之后的图到背景上准备裁剪
                bgimageview.paste(origin_image, (int(-originx), 0))
                # 保存到临时目录文件中
                file_manager.joinFilePath(file_manager.getFullPath(Index.temp_splash), platform)
                bgimageview.save(file_manager.createFilePath(file_manager.getFullPath(Index.temp_splash) + platform + "/LaunchImage.launchimage/" )+ ImageList[i][0] + ".png", "png")
                print(file_manager.getFullPath(Index.temp_splash) + platform + "/LaunchImage.launchimage/" + ImageList[i][0] + ".png")
        else:

            # 宽小于高，说明是竖屏闪屏，切图以宽为基准
            print("------------------检测到是竖屏的图片，进行处理--------------------------")
            if dest_w < dest_h:
                # 压缩图片（计算宽高）
                resizeH = int(float(dest_w / w) * h)
                resizeW = dest_w
                if resizeH > dest_h:
                    originy = (resizeH - dest_h) / 2
                else:
                    originy = (dest_h - resizeH) / 2
                # 原图根据目标图进行缩放，传入的比较大分辨率，缩小
                origin_image = origin_image.resize((resizeW, resizeH), Image.ANTIALIAS)
                # 创建一张白色背景
                bgimageview = Image.new('RGBA', (dest_w, dest_h), (255, 255, 255))
                # 粘贴压缩之后的图到背景上准备裁剪
                bgimageview.paste(origin_image, (0, int(-originy)))

                # 保存到临时目录文件中
                file_manager.joinFilePath(file_manager.getFullPath(Index.temp_splash), platform)
                bgimageview.save(file_manager.createFilePath(file_manager.getFullPath(Index.temp_splash) + platform + "/LaunchImage.launchimage/" )+ ImageList[i][0] + ".png", "png")
                print(file_manager.getFullPath(Index.temp_splash) + platform + "/LaunchImage.launchimage/" + ImageList[i][0] + ".png")


def processingAndroidSplash(image_path,platform="android",ImageList=[]):
    # 加载图形
    origin_image = Image.open(image_path)

    w = float(origin_image.size[0])
    h = float(origin_image.size[1])
    # 先处理图片，然后根据需求进行图片的裁剪
    for i in range(0, len(ImageList)):

        (dest_w, dest_h) = ImageList[i][1]
        splashfilename = ImageList[i][0]

        if w > h:
            print("------------------检测到是横屏的图片，进行处理--------------------------")
            # 宽大于高，说明是横屏闪屏，切图以高为基准
            if dest_w > dest_h:
                print(origin_image.size)
                print((dest_w, dest_h))

                # 压缩图片（计算宽高）
                resizeH = dest_h
                resizeW = int(float(dest_h / h) * w)


                # 原始坐标为0 ，计算放大后的图像 左右的间距
                originx = 0
                if resizeW > dest_w:
                    originx = (resizeW - dest_w) / 2
                else:
                    originx = (dest_w - resizeW) / 2

                # 原图根据目标图进行缩放，传入的比较大分辨率，缩小
                origin_image = origin_image.resize((resizeW, resizeH), Image.ANTIALIAS)

                # 创建一张白色背景
                bgimageview = Image.new('RGBA', (dest_w, dest_h), (255, 255, 255))
                # 粘贴压缩之后的图到背景上准备裁剪
                bgimageview.paste(origin_image, (int(-originx), 0))

                # 保存到临时目录文件中
                file_manager.joinFilePath(file_manager.getFullPath(Index.temp_splash), platform)
                bgimageview.save(file_manager.createFilePath(file_manager.getFullPath(Index.temp_splash) + platform +"/"   +splashfilename ) + "/splash.png", "png")
                log_utils.info("保存Splash" + file_manager.getFullPath(Index.temp_splash) + platform +"/"  + splashfilename + "splash.png")


        else:

            # 宽小于高，说明是竖屏闪屏，切图以宽为基准
            print("------------------检测到是竖屏的图片，进行处理--------------------------")


            if dest_w < dest_h:

                # 压缩图片（计算宽高）
                resizeH = int(float(dest_w / w) * h)
                resizeW = dest_w

                originy = 0
                if resizeH > dest_h:
                    originy = (resizeH - dest_h) / 2
                else:
                    originy = (dest_h - resizeH) / 2

                # 原图根据目标图进行缩放，传入的比较大分辨率，缩小
                origin_image = origin_image.resize((resizeW, resizeH), Image.ANTIALIAS)

                # 创建一张白色背景
                bgimageview = Image.new('RGBA', (dest_w, dest_h), (255, 255, 255))
                # 粘贴压缩之后的图到背景上准备裁剪
                bgimageview.paste(origin_image, (0, int(-originy)))

                # 保存到临时目录文件中
                file_manager.joinFilePath(file_manager.getFullPath(Index.temp_splash), platform)
                bgimageview.save(file_manager.createFilePath(file_manager.getFullPath(Index.temp_splash) + platform +"/"  +splashfilename ) + "/splash.png", "png")
                print("保存Splash" + file_manager.getFullPath(Index.temp_splash) + platform +"/"  + splashfilename + "splash.png")






def dealWithSplashPath():
    log_utils.info("进入splash处理程序---开始处理splash")
    # 检查资源
    tempfile = file_manager.getFullPath("upload/splash/ios");
    file_manager.clear(tempfile) #去掉DS_Store文件

    # 1、获取icon的全路径文件夹
    iosIconPath = file_manager.getFullPath(Index.root_splash+"/ios")
    androidIconPath = file_manager.getFullPath(Index.root_splash+"/android")

    # 2、获取该路径下的所有文件
    icons = file_manager.list_files(iosIconPath, [], ".DS_Store");
    if len(icons) == 0:
        log_utils.info("还没有上传splash资源文件，请上传之后操作！")
        return 101
    else:
        # 如果数组不为空，取出第一个元素
        # 获取到icon文件
        for filename in icons:
            if "L.png" in filename:
                launchimageL = filename;
            elif "P.png" in filename:
                launchimageP = filename;

    log_utils.info(launchimageL)
    log_utils.info(launchimageP)

    # ios 需要提供尺寸 1125x2436  和 2436x1125
    # android 需要提供 1920x1080 和 1080x1920

    iOSSplashSizes = [("Default-Portrait-2436h", (1125,2436)), ("Default-Landscape-2436h", (2436,1125)),
          ("Default-Portrait@3x", (1242 , 2208)), ("Default-667h@2x", (750 ,1334)),
          ("Default-Landscape@3x", (2208 ,1242)), ("Default-Portrait@2x", (1536 ,2048)),
            ("Default-Landscape", (1024 , 768)), ("Default-Landscape@2x", (2048 , 1536)),
            ("Default", (320 , 480)) , ("Default@2x", (640 , 960)),("Default-568h@2x", (640 , 1136)),
            ("Default-Portrait", ( 768 , 1024))]


    AndroidSplashList =  [("drawable_ldpi", (320,240)), ("drawable_mdpi",(480,320)),
                          ("drawable_hdpi", (800,480)), ("drawable_xhdpi",(1280,720)),
                          ("drawable_xxhdpi", (1920,1080)),("drawable_ldpi", (240,320)),
                          ("drawable_mdpi",(320,480)), ("drawable_hdpi", (480,800)),
                          ("drawable_xhdpi",(720,1280)), ("drawable_xxhdpi", (1080,1920))]

    processingWithSplash(launchimageL,"ios",iOSSplashSizes)
    processingWithSplash(launchimageP,"ios",iOSSplashSizes)

    processingAndroidSplash(launchimageL,"android",AndroidSplashList)
    processingAndroidSplash(launchimageP,"android",AndroidSplashList)

    log_utils.printf()
    print("所有闪屏图片处理完毕，接下来是打包过程，请稍后....")

    make_archiveWithInfo()

