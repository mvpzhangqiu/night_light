# 利用区域的圆度来进行检测
import cv2
import numpy as np
import math

cap = cv2.VideoCapture('./MOVA0803.avi')
frame_index = 0
interval = 10
frame_count = 0

if cap.isOpened():
    success = True
else:
    success = False
    print("读取失败!")

while success:
    success, img = cap.read()
    if not success:
        print('video over!')
        break
    if frame_index % interval == 0:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("./gray_img.jpg", gray_img)

        bin_img = cv2.threshold(gray_img, 240, 255, cv2.THRESH_BINARY_INV)[1]
        # cv2.imwrite("./bin_img.jpg", bin_img)

        params = cv2.SimpleBlobDetector_Params()

        # 表示提取白色的色块，若需要提取黑色色块可以用0
        params.filterByColor = True
        params.blobColor = 0
        # 二值化的起始阈值
        params.minThreshold = 240
        # 二值化的终止阈值
        params.maxThreshold = 255

        # params.thresholdStep = 100
        params.thresholdStep = 2

        # 控制blob的区域面积大小
        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 50000
        # blob的圆度限制，默认为不限制，通常不限制，除非找圆形特征
        # params.filterByCircularity = False
        params.filterByCircularity = True
        # blob最小的圆度
        params.minCircularity = 0.001
        # blob的凸性
        # params.filterByConvexity = False
        params.filterByConvexity = True
        params.minConvexity = 0.001

        # blob的惯性率， 圆为1， 线为0， 大多数情况介于[0 ,1]之间
        params.filterByInertia = True
        # params.filterByInertia = False
        params.minInertiaRatio = 0.001

        # params.minDistBetweenBlobs = 5  # 最小的斑点距离，不同的二值图像斑点小于该值时将被认为是同一个斑点
        params.minDistBetweenBlobs = 10  # 最小的斑点距离，不同的二值图像斑点小于该值时将被认为是同一个斑点
        params.minRepeatability = 1

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(bin_img)
        # for keypoint in keypoints:
        #     x, y = np.int64(keypoint.pt[0]), np.int64(keypoint.pt[1])
        #     # cv2.circle(img, (x, y), math.ceil(math.sqrt(keypoint.size / math.pi)), (255, 25, 25), 2)
        #     cv2.circle(img, (x, y), math.ceil(keypoint.size), (255, 25, 25), 2)

        for keypoint in keypoints:
            if keypoint.size < 20:
                continue
            x, y = np.int64(keypoint.pt[0]), np.int64(keypoint.pt[1])
            cv2.circle(img, (x, y), math.ceil(keypoint.size/2), (255, 25, 25), 2)

        cv2.imwrite("./cnl/cnl_night_%d" % frame_count + '.jpg', img)
        cv2.imwrite("./cnl/cnl_night_bin_%d" % frame_count + '.jpg', bin_img)
        frame_count += 1
    frame_index += 1
cap.release()
