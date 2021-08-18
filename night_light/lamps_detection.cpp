#include "lamps_detection.h"
#include <vector>
using namespace std;
CLampsDetection::CLampsDetection()
{
	
	m_nStructElementSize = 2;
}
void CLampsDetection::LampsDetectProcess(cv::Mat& img,long long time_stamp,std::vector<Object>& detections_list)
{
	if(img.empty())
	{
		return;
	}
	/*cv::cvtColor(img,m_image_gray,CV_BGR2GRAY);
	//cv::resize(m_image_gray,m_image_gray,cv::Size(m_imgW,m_imgH));	
	cv::threshold(m_image_gray,m_image_gray , 150, 255, cv::THRESH_BINARY);
	cv::Mat element = getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(2 * m_nStructElementSize + 1, 2 * m_nStructElementSize + 1), cv::Point(m_nStructElementSize, m_nStructElementSize));
	cv::erode(m_image_gray, m_image_gray, element); 
	cv::dilate(m_image_gray, m_image_gray, element); */
	cv::SimpleBlobDetector::Params pDefaultBLOB;
	//二值化
	pDefaultBLOB.minThreshold = 150;                 //二值化的起始阈值 40	
    pDefaultBLOB.maxThreshold = 255;  
    pDefaultBLOB.thresholdStep = 2;
	
    pDefaultBLOB.minRepeatability = 1;
    pDefaultBLOB.minDistBetweenBlobs = 10;
	//斑点颜色
    pDefaultBLOB.filterByColor = true;
    pDefaultBLOB.blobColor = 255;
	//面积控制
    pDefaultBLOB.filterByArea = true;
    pDefaultBLOB.minArea = 1000;
    pDefaultBLOB.maxArea = 3000000;
	//形状圆
    pDefaultBLOB.filterByCircularity = true;
    pDefaultBLOB.minCircularity = 0.3f;	
    pDefaultBLOB.maxCircularity =  std::numeric_limits<float>::max();
	//凹
	pDefaultBLOB.filterByConvexity = true;
	pDefaultBLOB.minConvexity = 0.8;                                    //0.05f//斑点的最小凹度  
	pDefaultBLOB.maxConvexity = std::numeric_limits<float>::max();    //斑点的最大凸度  

	//惯性比
	pDefaultBLOB.filterByInertia = true;
	pDefaultBLOB.minInertiaRatio = 0.3f;                                 //斑点的最小惯性率  圆的值为1，直线的值为0  //.05f
	pDefaultBLOB.maxInertiaRatio = 1;    //斑点的最大惯性率    

	//凸
	pDefaultBLOB.filterByConvexity = true;
	pDefaultBLOB.minConvexity = 0.3f;
	pDefaultBLOB.maxConvexity = std::numeric_limits<float>::max();
	//*用参数创建对象
	cv::Ptr<cv::SimpleBlobDetector> blob=cv::SimpleBlobDetector::create(pDefaultBLOB);

	vector<cv::KeyPoint> key_points;
	blob->detect(img,key_points);
	cv::Mat outImg;
	static int i=0;
	if(key_points.size()>0)
	{
		for(int i=0;i<key_points.size();i++)
		{
			cout << "Blob_size 直径：" << key_points[i].size << endl;
			cout << "Blob_response 点强度:" << key_points[i].response << endl;
			cout << "Blob_pt 点位置：" << key_points[i].pt << endl;
			cout << "keypoints _angle" << key_points[i].angle << endl;
			cout << "keypoints_octave" << key_points[i].octave << endl;

		}
		cout<<"size ="<<key_points.size()<<endl;
		outImg =img.clone();
		//绘制结果
		cv::drawKeypoints(img,key_points,outImg,cv::Scalar(0,0,255),cv::DrawMatchesFlags::DRAW_RICH_KEYPOINTS);
		char str[50];
	
		sprintf(str,"%d.jpg",i);
		i++;
		imwrite(str,outImg);
		cout<<str<<endl;
		//sprintf(str,"---%d.jpg",i);
		
		//imwrite(str,m_image_gray);
	}

	

}