#-*- coding:utf-8 –*-
#author:yuanly
#data:2021.5.18
#Description:读取目录下的录像文件，隔帧保存图片
# -*- coding: utf-8 -*-
import os
import cv2

videos_src_path = '/home/yly/work/night'  # 录像文件路径
frames_save_path ='/home/yly/work/suizhong_night'#图片路径


video_formats = [".mp4", ".avi",".MOV"]

width = 1920
height = 1080
time_interval = 30
 
 
def video2frame(video_src_path, formats, frame_save_path, frame_width, frame_height, interval):
    """
    将视频按固定间隔读取写入图片
    :param video_src_path: 视频存放路径
    :param formats:　包含的所有视频格式
    :param frame_save_path:　保存路径
    :param frame_width:　保存帧宽
    :param frame_height:　保存帧高
    :param interval:　保存帧间隔
    :return:　帧图片
    """
    videos = os.listdir(video_src_path)
 
    def filter_format(x, all_formats):
        if x[-4:] in all_formats:
            return True
        else:
            return False
 
    videos = filter(lambda x: filter_format(x, formats), videos)
    frame_count = 0
    for each_video in videos:
        print ("正在读取视频：", each_video) 
        cap = cv2.VideoCapture(videos_src_path+'/'+each_video)
        frame_index = 0

        if cap.isOpened():
            success = True
        else:
            success = False
            print("读取失败!")
 
        while(success):
            success, frame = cap.read()
            #print("---> 正在读取第%d帧:" % frame_index, success)
            if success==False:
                print('video over!')
                break
            if frame_index % interval == 0:
               # filename =each_video.split("/")[-1].split(".")[0]+"_%d" % frame_count+'.jpg'
                filename ="cnl_night_%d" % frame_count + '.jpg'
                print('save-----'+filename)
                #resize_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
                # cv2.imwrite(each_video_save_full_path + each_video_name + "_%d.jpg" % frame_index, resize_frame)
                cv2.imwrite(frames_save_path +'/'+ filename, frame)
                frame_count += 1 
            frame_index += 1
           
 
        cap.release()
 
 
if __name__ == '__main__':
    video2frame(videos_src_path, video_formats, frames_save_path, width, height, time_interval)