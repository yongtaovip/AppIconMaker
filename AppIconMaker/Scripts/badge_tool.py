# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 11:35
# @Author  : ZhiMa_Maker
# @Email   :  yongtao_vip@163.com
# @File    : badge_tool.py
# @Software : PyCharm

import log_utils
import Index
import file_manager
from PIL import Image, ImageDraw
import icon_tool


def composeIconWithBadge(floatIcon_Path,appIcon_path):

    # 获取icon原图
    origin_image = Image.open(appIcon_path).convert("RGBA")

    # 获取角标
    float_icon = Image.open(floatIcon_Path)

    # 处理角标问题
    if origin_image.size[0] != origin_image.size[1]:
        print('FloatIcon file must be a rectangle!')
        return

    # 获取图片宽高
    origin_imageW = origin_image.size[0]

    # 角标大小跟icon保持一致
    float_icon = float_icon.resize((origin_imageW, origin_imageW), Image.BILINEAR)

    # #粘贴角标到icon
    # origin_image.paste(float_icon,(0,0,origin_imageW,origin_imageW))

    iconImage = Image.alpha_composite(origin_image, float_icon)  # 能看到 float_icon 的黑色背景

    # file_manager.joinFilePath(file_manager.getFullPath(Index.temp_badge))
    temp_badge_path = file_manager.createFilePath(file_manager.getFullPath(Index.temp_badge))
    iconImage.save(temp_badge_path + "/badge_icon.png" , "png")
    print(temp_badge_path + "/badge_icon.png")

    print("已经处理完角标----------")


def getpath(dir):
    # 2、获取该路径下的所有文件
    icons = file_manager.list_files(dir, [], ".DS_Store");
    if len(icons) == 0:
        log_utils.info("还没有上传appicon资源文件，请上传之后操作！")
        return 101
    else:
        # 如果数组不为空，取出第一个元素
        # 获取到icon文件
        for filename in icons:
            if ".png" in filename:
                appIconDir = filename
                return  appIconDir




def dealWithBadgePath():
    log_utils.info("进入badge处理程序---开始处理badge")

    # 检查资源
    tempfile = file_manager.getFullPath("upload/badge");
    file_manager.clear(tempfile)

    # 1、获取badge的全路径文件夹
    badgePath = file_manager.getFullPath(Index.root_badge)
    badgeIcon_path = getpath(badgePath)

    icon_path = file_manager.getFullPath(Index.root_icon)
    appIcon_path = getpath(icon_path)

    # 获取角标 对icon进行处理
    composeIconWithBadge(badgeIcon_path,appIcon_path)

    iOSIconSizes = [("icon-20@2x", 40), ("icon-20@3x", 60), ("icon-29@2x", 58), ("icon-29@3x", 87),
                    ("icon-40@2x", 80), ("icon-40@3x", 120), ("icon-60@2x", 120),
                    ("icon-60@3x", 180), ("icon-1024", 1024), ("icon-20", 20), ("icon-40", 40),
                    ("icon-72", 72), ("icon-29", 29), ("icon-72@2x", 144), ("icon-76", 76), ("icon-76@2x", 152),
                    ("icon-83.5@2x", 167), ("icon-57", 57), ("icon-57@2x", 114), ("icon-20-ipad", 20),
                    ("icon-20-ipad@2x", 40), ("icon-50", 50), ("icon-50@2x", 100)]
    AndroidIconList = [("drawable-ldpi", 36,"icon-36"), ("drawable-mdpi", 48,"icon-48"), ("drawable-hdpi", 72,"icon-72"),
                       ("drawable-xhdpi", 96,"icon-96"),
                       ("drawable-xxhdpi", 144,"icon-144"), ("drawable-xxxhdpi", 192,"icon-192"),
                       ("drawable", 512,"icon-512")]

    # 获取添加角标的icon位置
    tempIcon_path = file_manager.getFullPath(Index.temp_badge)
    tempBadgeIconDir = getpath(tempIcon_path)

    # 调用icon的生成器
    icon_tool.processingIcons(tempBadgeIconDir,"ios",iOSIconSizes)
    icon_tool.processingIcons(tempBadgeIconDir,"android",AndroidIconList)
    icon_tool.make_archiveWithInfo()