# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 23:01
# @Author  : ZhiMa_Maker
# @Email   :  yongtao_vip@163.com
# @File    : file_manager.py
# @Software : PyCharm

import os,sys
import re
import platform
import shutil
import log_utils

# 获取当前脚本工作目录
rootDir = os.getcwd()

def __init__(self):
    pass



def list_files(src, resFiles, igoreFiles):
    if os.path.exists(src):
        if os.path.isfile(src) and src not in igoreFiles:
                resFiles.append(src)
        elif os.path.isdir(src):
            for f in os.listdir(src):
                if src not in igoreFiles:
                    list_files(os.path.join(src, f), resFiles, igoreFiles)

    return resFiles




 #获取当前路径
def getCurrDir(self):
    global currentDir
    retPath = currentDir
    if platform.system() == 'Darwin':  # 判断是否是 mac平台
        retPath = sys.path[0]
        lstPath = os.path.split(retPath)
        if lstPath[1]:
            retPath = lstPath[0]
    return retPath


# 获取完整路径
def getFullPath(filename):
    if os.path.isabs(filename):  # 判断是否是绝对路径
        return filename
    currdir = rootDir
    filename = os.path.join(currdir, filename)
    filename = filename.replace('\\', '/')
    filename = re.sub('/+', '/', filename)
    return filename



# 获取输出路径
def createFilePath(filepath,isClearDir=0):
    outpath = getFullPath(filepath)
    if os.path.exists(outpath):
        if isClearDir == 1:
            # shutil.rmtree(outpath)
            os.makedirs(outpath)
            log_utils.info(outpath + "目录创建成功")
            return outpath
        else:
            log_utils.info("目录已存在" + outpath)
            return outpath
    else:
        os.makedirs(outpath)
        log_utils.info(outpath + "目录创建成功")
        return outpath



def joinFilePath(sourcePath,appendPath):
    path = getFullPath(sourcePath)
    if os.path.exists(path):
        os.path.join(sourcePath, appendPath)
    else:
        log_utils.info("原路径不存在，请检查")






def copyFile(filepath, newPath):
    # 获取当前路径下的文件名，返回List
    fileNames = os.listdir(filepath)
    for file in fileNames:
        # 将文件命加入到当前文件路径后面
        newDir = filepath + '/' + file
        # 如果是文件
        if os.path.isfile(newDir):
            print(newDir)
            newFile = newPath + file
            shutil.copyfile(newDir, newFile)
        #如果不是文件，递归这个文件夹的路径
        else:
            copyFile(newDir,newPath)



def copyFiles(srcPath, dstPath):
    for file in os.listdir(srcPath):
        if file == '.DS_Store':
            continue
        srcFilePath = srcPath + '/' + file
        dstFilePath = dstPath + '/' + file

        # if file.endswith('.plist'):
        #     combineOtherPlist(srcFilePath, dstFilePath)
        # elif
        #文件夹内容copy
        if os.path.isdir(srcFilePath):
            if srcFilePath.endswith('launchimage'):
            	if os.path.exists(dstFilePath):
                    pass
                    #如果目标文件夹存在内容，删除
            		# shutil.rmtree(dstFilePath)
            if os.path.exists(dstFilePath):
                copyFiles(srcFilePath, dstFilePath)
            else:
                shutil.copytree(srcFilePath, dstFilePath, symlinks=False, ignore=None)
        else:
            #文件内容copy
            shutil.copy(srcFilePath, dstFilePath)


def removeFilePath(file_path):
    """删除路径下的所有文件"""
    if os.path.exists(file_path):
        shutil.rmtree(file_path)


# 清理文件函数
def clear(path):
    log_utils.info('正在扫描：' + path)
    # 获取目录中的所有文件和文件夹名字
    dir_list = os.listdir(path)
    # 遍历循环每个目录
    for i in dir_list:
        # 拼接绝对路径
        abspath = os.path.join(os.path.abspath(path), i)
        # 判断是否是文件
        if os.path.isfile(abspath):
            # 判断文件是否是 ._ 开头的文件
            if i.startswith("._"):
                # 删除文件
                # 这是彻底删除 回收站不会存在
                # 这是彻底删除 回收站不会存在
                # 这是彻底删除 回收站不会存在
                os.remove(abspath)
                log_utils.info('清理文件 : ' + abspath)

        else:
            # 不是文件就继续递归
            clear(abspath)

