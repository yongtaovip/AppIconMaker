# -*- coding: utf-8 -*-
# @Time    : 2020/3/14 16:41
# @Author  : ZhiMa_Maker
# @Email   :  yongtao_vip@163.com
# @File    : test.py
# @Software : PyCharm
from pygments.util import xrange


if __name__ == '__main__':
    AndroidIconList = [("mipmap-ldpi", 36, "icon-36"), ("mipmap-mdpi", 48, "icon-48"), ("mipmap-hdpi", 72, "icon-72"),
                       ("mipmap-xhdpi", 96, "icon-96"), ("mipmap-xxhdpi", 144, "icon-144"),
                       ("mipmap-xxxhdpi", 192, "icon-192"), ("AppIcon512", 512, "icon-512")]

    for x in xrange(0, len(AndroidIconList)):
        print(AndroidIconList[x][2])