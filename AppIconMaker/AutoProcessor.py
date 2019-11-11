# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import os
import os.path
import sys
import shutil
import zipfile
import datetime
#import matplotlib.pyplot as plt


rootdir=os.path.abspath('.') 
temp_path = rootdir + "/temp/"
temp_icon_path = rootdir + "/temp/AppIcon/"
temp_screenshot_path = rootdir + "/temp/LaunchScreen/"

icon_path = rootdir + '/upload/AppIcon/AppIcon.png'
Float_Path = rootdir + '/upload/FloatIcon/FloatIcon.png'
screenshotP_path = rootdir + '/upload/LaunchScreen/LaunchScreenP.png'
screenshotL_path = rootdir + '/upload/LaunchScreen/LaunchScreenL.png'



os.path.join(temp_path,'ios')
os.path.join(temp_path,'android')


cache_path  = rootdir + "/cache/"    #缓存文件 文件列表
upload_path = rootdir + "/upload/"  #上传文件 APPIcon 或者 LaunchImage




def circle_corner(img, radii):
    """
        圆角处理
        :param img: 源图象。
        :param radii: 半径，如：30。
        :return: 返回一个圆角处理后的图象。
        """
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
    
    # 原图
    img = img.convert("RGBA")
    w, h = img.size
    if w == h:
        pass
    else:
        print('请输入一张1024x1024像素的icon图片')
        return {"error_code":101,"msg":"please upload a square image！"}
    
    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()
    
    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img






def auto_process_appicon(image_path,floatIcon_Path,platform = "ios",is_add_floatIcon = False):

    ''' 

    自动化处理APPIcon

    需要传入参数（图片路径，平台，是否切圆角状态）

    '''
     
     # 加载图形
    origin_image = Image.open(image_path).convert("RGBA")

    if origin_image.size[0] != origin_image.size[1]:

        print 'Icon file must be a rectangle!'
        
        return



    #处理icon
    if is_add_floatIcon == True:

        #获取角标
        float_icon = Image.open(floatIcon_Path)
        #处理角标问题
        if origin_image.size[0] != origin_image.size[1]:
            print 'FloatIcon file must be a rectangle!'
            return

        #获取图片宽高
        origin_imageW = origin_image.size[0]
        
        #角标大小跟icon保持一致
        float_icon = float_icon.resize((origin_imageW,origin_imageW), Image.BILINEAR)

        # #粘贴角标到icon
        # origin_image.paste(float_icon,(0,0,origin_imageW,origin_imageW))

        iconImage = Image.alpha_composite(origin_image, float_icon) # 能看到 float_icon 的黑色背景

        # #接收传来的image
        # iconImage = origin_image

        print ("已经处理完角标----------")

        
    else:
        #接收传来的image
         iconImage = origin_image

    # 定义Icon大小的元组列表
    if  platform == "ios":

        IconList = [("AppIcon-20x20@2x", 40), ("AppIcon-20x20@3x", 60), ("AppIcon-29x29@2x", 58), ("AppIcon-29x29@3x", 87), ("AppIcon-40x40@2x", 80), ("AppIcon-40x40@3x", 120), ("AppIcon-60x60@2x", 120), ("AppIcon-60x60@3x", 180),("AppIcon-1024x1024",1024),("AppIcon-20x20",20),("AppIcon-40x40",40),("AppIcon-72x72",72),("AppIcon-72x72@2x",144),("AppIcon-76x76",76),("AppIcon-76x76@2x",152),("AppIcon-83.5x83.5@2x",167)]
    
    elif platform == "android":

        IconList = [("ldpi", 32),("mdpi", 48),("hdpi", 72),("xhdpi", 96),("xxhdpi", 144),("xxxhdpi",192),("AppIcon",512)]

        print ("aaaaa----------")

    else:

        print("平台名称填写错误，请重新填写")

        return False



    for x in xrange(0, len(IconList)):

        width = IconList[x][1]

        # 调整图像大小
        out_iconImage = iconImage.resize((width, width), Image.BILINEAR)
        
        imgName =  IconList[x][0] + ".png"

        out_iconImage.save(temp_icon_path + platform + "/" + imgName , "png") 

        print(temp_icon_path + imgName)

    return True








def auto_process_launchimage(image_path,platform="ios"):

    '''
        对闪屏进行处理：
            区分设备：ios ，安卓 ，小米
            横竖屏，需要传入两张图，横向和纵向的，根据尺寸来进行处理
            按照要求存入两张规格最大的横竖图,所有平台统一
            规格要求：2436x1125   1125x2436
    '''
     # 定义LaunchImage大小的元组列表
    if platform == "ios":
        ImageList = [("iPhoneXsMaxPortrait-1242x2688", (1242,2688)), ("iPhoneXRPortrait-828x1792",
         (828,1792)), ("iPhoneXsMaxLandscape-2688x1242", (2688,1242)), ("iPhoneXRLandscape-1792x828", 
         (1792,828)), ("iPhoneXsPortrait-1125x2436", (1125,2436)), ("iPhoneXsLandscape-2436x1125", (2436,1125)),
          ("iPhoneProtrait-1242x2208", (1242 , 2208)), ("iPhoneProtrait-750x1334", (750 ,1334)), 
          ("iPhoneLandscape-2208x1243", (2208 ,1243)), ("iPhonePortrait-640x960@2x", (640 , 960)),
           ("iPhonePortrait-640x1136", (640 ,1136)), ("iPadPortrait-768x1024@2x", (1536 ,2048)),
            ("iPadLandscape-1024x768", (1024 , 768)), ("iPadLandscape-1024x768@2x", (2048 , 1536)), 
            ("iPhonePortrait-320x480", (320 , 480)) , ("iPhonePortrait-320x480@2x", (640 , 960)), 
            ("iPadPortrait-768x1024", ( 768 , 1024))]

    elif platform == "android":

       ImageList = [("iPhoneXsMaxPortrait-1242x2688", (1242,2688)), ("iPhoneXRPortrait-828x1792",
        (828,1792)), ("iPhoneXsMaxLandscape-2688x1242", (2688,1242)), ("iPhoneXRLandscape-1792x828",
        (1792,828)), ("iPhoneXsPortrait-1125x2436", (1125,2436)), ("iPhoneXsLandscape-2436x1125", (2436,1125)),
         ("iPhoneProtrait-1242x2208", (1242 , 2208)), ("iPhoneProtrait-750x1334", (750 ,1334)),
         ("iPhoneLandscape-2208x1243", (2208 ,1243)), ("iPhonePortrait-640x960@2x", (640 , 960)),
          ("iPhonePortrait-640x1136", (640 ,1136)), ("iPadPortrait-768x1024@2x", (1536 ,2048)),
           ("iPadLandscape-1024x768", (1024 , 768)), ("iPadLandscape-1024x768@2x", (2048 , 1536)),
           ("iPhonePortrait-320x480", (320 , 480)) , ("iPhonePortrait-320x480@2x", (640 , 960)),
           ("iPadPortrait-768x1024", ( 768 , 1024))]
    
    else:

        print("平台名称填写错误，请重新填写")

        return {"error_code":"101","msg":"平台名称填写错误，请重新填写"}



    # 加载图形
    origin_image = Image.open(image_path)


    w = float(origin_image.size[0])
    h = float(origin_image.size[1])
    #先处理图片，然后根据需求进行图片的裁剪
    for i in xrange(0, len(ImageList)):

        screenshot_size = ImageList[i][1]

        if w > h:
            print("------------------检测到是横屏的图片，进行处理--------------------------")

        # 宽大于高，说明是横屏闪屏，切图以高为基准
            print(w)
            print(h)

            (dest_w,dest_h) = screenshot_size

            if dest_w > dest_h:
                  
                #压缩图片（计算宽高）
                resizeH = dest_h
                resizeW = int(float(dest_h/h)* w)

                originx = 0
                if resizeW > dest_w:
                    originx = (resizeW - dest_w)/2
                else:
                    originx = (dest_w - resizeW)/2
                
                #原图根据目标图进行缩放，传入的比较大分辨率，缩小
                origin_image = origin_image.resize((resizeW, resizeH),Image.ANTIALIAS)

                #创建一张白色背景
                bgimageview = Image.new('RGBA', (dest_w ,dest_h), (255,255,255)) 
                #粘贴压缩之后的图到背景上准备裁剪
                bgimageview.paste(origin_image, (-originx, 0))


                #保存到临时目录文件中
                bgimageview.save(temp_screenshot_path + platform + "/" + ImageList[i][0]+ ".png", "png") 

                print(temp_screenshot_path + platform + "/" +  ImageList[i][0] + ".png")


        else:
            
             # 宽小于高，说明是竖屏闪屏，切图以宽为基准
            print("------------------检测到是竖屏的图片，进行处理--------------------------")
            print(w)
            print(h)

            (dest_w,dest_h) = screenshot_size

            print(screenshot_size)

            if dest_w < dest_h:

                #压缩图片（计算宽高）
                resizeH = int(float(dest_w/w)* h)
                resizeW = dest_w

                originy = 0
                if resizeH > dest_h:
                    originy = (resizeH - dest_h)/2
                else:
                    originy = (dest_h - resizeH)/2
                


                #原图根据目标图进行缩放，传入的比较大分辨率，缩小
                origin_image = origin_image.resize((resizeW, resizeH),Image.ANTIALIAS)

                print origin_image.size

                #创建一张白色背景
                bgimageview = Image.new('RGBA', (dest_w ,dest_h), (255,255,255)) 
                #粘贴压缩之后的图到背景上准备裁剪
                bgimageview.paste(origin_image, (0, -originy))

                #保存到临时目录文件中
                bgimageview.save(temp_screenshot_path + platform + "/" +  ImageList[i][0] + ".png", "png") 

                print(temp_screenshot_path + platform + "/" +  ImageList[i][0] + ".png")



def main():

    #检测是否存在路径，如果没有就提前创建路径
    if os.path.exists(temp_path) == False:
        os.mkdir(temp_path)
    if os.path.exists(temp_icon_path) == False:
        os.mkdir(temp_icon_path)
    if os.path.exists(temp_screenshot_path) == False:
        os.mkdir(temp_screenshot_path)


    #创建Icon的临时文件目录
    android_path = temp_icon_path + "android/"
    ios_path = temp_icon_path + "ios/"

    if os.path.exists(android_path) == False:
        os.mkdir(android_path)
    if os.path.exists(ios_path) == False:
        os.mkdir(ios_path)


    #创建闪屏的临时文件目录
    screenshot_android_path = temp_screenshot_path + "android/"
    screenshot_ios_path = temp_screenshot_path + "ios/"

    if os.path.exists(screenshot_android_path) == False:
        os.mkdir(screenshot_android_path)
    if os.path.exists(screenshot_ios_path) == False:
        os.mkdir(screenshot_ios_path)



    # # 闪屏和icon
    action = sys.argv[1]#action:icon or screenshot

    if action == "icon":

        print ("一键生成移动端所有Icon图标，如果尺寸不够，可自行添加")

        print("icon所在的路径："+ icon_path)

        if os.path.exists(icon_path):


            #自动处理图片
            auto_process_appicon(icon_path,Float_Path,'ios',False)
            auto_process_appicon(icon_path,Float_Path,'android',False)

            print("已经处理完所有的icon+角标，接下来为您打包，请稍后...")


            #对处理完的icon进行打包处理
            nowtimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            new_path = shutil.make_archive(cache_path + "AppIcon/" + nowtimestr, 'zip', temp_icon_path)
            print("*************已经打包完毕*******************")
            print("打包结束之后的zip路径为:" + new_path)
            return {"error_code":200,"msg":"文件处理完毕"}

        else:
             print('no such file:%s'%icon_path)

             return {"error_code":404,"msg":"文件不存在，请上传文件"}

    elif action == "screenshot":

        print ("需要处理闪屏页，进入处理流程...")

        if os.path.exists(screenshotP_path):
            auto_process_launchimage(screenshotP_path,"ios")
        else:
            print("竖屏闪屏不存在，请上传竖屏闪屏")
            return {"error_code":404,"msg":"竖屏闪屏不存在，请上传文件"}

        if os.path.exists(screenshotL_path):
            auto_process_launchimage(screenshotL_path,"ios")
        else:
            print("竖屏闪屏不存在，请上传竖屏闪屏")
            return {"error_code":404,"msg":"竖屏闪屏不存在，请上传文件"}



        print ("所有闪屏已经处理完毕，准备打包...")
        #对处理完的icon进行打包处理
        nowtimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        new_path = shutil.make_archive(cache_path + "LaunchScreen/" + nowtimestr, 'zip', temp_screenshot_path)
        print("*************已经打包完毕*******************")
        print("打包结束之后的zip路径为:" + new_path)
        return {"error_code":200,"msg":"所有闪屏文件打包处理完毕"}

        

    elif action == "FloatIcon":
        
        print("需要给icon添加角标，进入处理流程...")

        print ("一键生成移动端所有Icon图标，如果尺寸不够，可自行添加")

        print("icon所在的路径："+ icon_path)

        if os.path.exists(icon_path):
            if os.path.exists(Float_Path) == False:
                print ("角标文件不存在，请上传角标文件")
                return {"error_code":404,"msg":"角标文件不存在，请上传角标文件"}
            
            #自动处理图片
            auto_process_appicon(icon_path,Float_Path,'ios',True)
            auto_process_appicon(icon_path,Float_Path,'android',True)



            print("已经处理完所有的icon，接下来为您打包，请稍后...")

            nowtimestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            new_path = shutil.make_archive(cache_path + "FloatIcon/" + nowtimestr, 'zip', temp_icon_path)

            print("*************已经打包完毕*******************")

            print("打包结束之后的zip路径为:" + new_path)

            return {"error_code":200,"msg":"文件处理完毕"}

        else:
             print('no such file:%s'%icon_path)

             return {"error_code":404,"msg":"文件不存在，请上传文件"}

        return {"error_code":200,"msg":"处理icon添加角标..."}


    else:
       
        print("如果处理appicon，请输入格式: python AutoProcessor.py icon")
        print("如果处理LaunchImage，请输入格式: python AutoProcessor.py screenshot")
        print("如果对icon添加角标，请输入格式: python AutoProcessor.py FloatIcon")

        return {"error_code":101,"msg":"请重新选择处理的命令icon/FloatIcon/screenshot"}


if __name__ == '__main__':
       main()  


