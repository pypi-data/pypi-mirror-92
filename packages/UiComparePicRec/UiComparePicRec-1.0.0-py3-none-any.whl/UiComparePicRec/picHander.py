#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import os
from pathlib import Path
import cv2
from skimage.metrics import mean_squared_error, structural_similarity
import numpy as np
from numpy import average,dot,linalg
import copy
from PIL import Image
"""
实现下两幅图片的差异性比较的过程，简答的实验下这个里面的过程：
  - 1. 先找到两幅图片的来源；
    - a.构建原始图片的路径信息：original_path
    - b.构建待比较图片的路径信息：save_path

  - 2.使用SSIM（结构相似性函数）比较两幅图片的相似性：
    - a.先定义下compare的数据结构：[{org:filename,save:filename}]
    - b.对原始图像以及待比较的图像进行resize的放缩操作，使图像的尺度保持一致，方便进行比较操作：
        - 处理的方法是：定义一个标准的尺度值：2000
        - 比较一下图片的长和宽的相关的信息，对比较中值大的进行参数话处理，值小的直接等于2000这个尺度的值，图像放缩的插值方法为：INTER_CUBIC，三次样条插值方法；
        - 参数话处理的过程：需要注意的是resize后，原始图像的宽变成新图像的高了，因此在进行计算放缩的时候需要注意这部分的情况；
        - 待对比的照片进行处理：处理的过程仅仅是resize到和原始图片处理到2000的过程的size大小进行放缩就行，不用进行计算的过程；
        - 进行SSIM算法的比较过程
  - 3.相似性系数得到之后，我们关心的是要能看到完整的不同的图像之间的不同的部分到底是那些；
    - a.找出不同图片的不同之处
"""
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 
logger = logging.getLogger("PicHander")
class PicHander:
    PICORDER = 2000
    PICORDER_Vec = 64
    def __init__(self,compare_res,original_path = None,save_path = None):
        # current_path = os.getcwd()
        # self.original_path = Path(current_path).joinpath('org/*.png') if original_path is None else original_path + r'/*.png'
        # self.save_path = Path(current_path).joinpath('sap/')
        self.compare_result = compare_res
    
    @staticmethod
    def get_thum(image,size=(128,256),greyscale=False):
        image = image.resize(size, Image.ANTIALIAS)
        if greyscale:
            image = image.convert('L')
        return image


    def generate_diff_pic_between_vector(self,path_name,save_diff_dir=None):
        result_vector = {}
        for index,result in enumerate(self.compare_result):
            org_pic = Image.open(result['org'])
            save_pic = Image.open(result['sap'])
            image1 = PicHander.get_thum(org_pic)
            image2 = PicHander.get_thum(save_pic)
            logger.info('org pic and save pic have completed to resize.')
            images = [image1,image2]
            vectors = []
            norms = []
            for image in images:
                vector = []
                for pixel_tuple in image.getdata():
                    vector.append(average(pixel_tuple))
                vectors.append(vector)
                norms.append(linalg.norm(vector,2))
            a,b = vectors
            a_norm,b_norm = norms
            res = dot(a/a_norm,b/b_norm)
            logger.info(f"Diff Pic Over Come...")
            logger.info(f'Path:{path_name[index]}')
            logger.info(f'{res}')
            result_vector[f'{path_name[index]}']= res
        return result_vector
    def generate_diff_pic_between_ssim(self,path_name,save_diff_dir=None):
        """
        save_diff_dir: save result dir
        :return 
        """
        result_ssim = {}
        for index,result in enumerate(self.compare_result):
            org_pic = cv2.imread(result['org'])
            save_pic = cv2.imread(result['sap'])
            if org_pic.shape[0] > PicHander.PICORDER or org_pic.shape[1] > PicHander.PICORDER:
                org_pic = PicHander.compare_pic_diff_pic(org_pic,PicHander.PICORDER)
            org_pic_size = (org_pic.shape[1],org_pic.shape[0])
            save_pic_size = (save_pic.shape[1],save_pic.shape[0])
            if not save_pic_size == org_pic_size:
                save_pic = cv2.resize(save_pic,org_pic_size,interpolation=cv2.INTER_CUBIC)
            else:
                save_pic = save_pic
            logger.info('org pic and save pic have completed to resize.')
            ssim_struction_result = structural_similarity(
                cv2.cvtColor(org_pic,cv2.COLOR_BGR2GRAY),
                cv2.cvtColor(save_pic,cv2.COLOR_BGR2GRAY),
                full=True
            )

            if not os.path.exists("diff/"+path_name[index]):
                logger.info('Path:%s',str("diff/"+path_name[index]))
                os.mkdir("diff/"+path_name[index])

            logger.info(f'Path:{path_name[index]}')
            result_ssim_score = ssim_struction_result[0]
            logger.info(f'Similarity score:{result_ssim_score}') 
            #logger.info(Path(os.getcwd()).joinpath('self/diff/org.png'))
            
            ssim_pic = ssim_struction_result[1]

            org_pic_result,save_pic_result = PicHander.get_diff_pic_org_sap(ssim_pic,org_pic,save_pic)
            orgPath = "diff/"+path_name[index]+"/org.png"
            sapPath = "diff/"+path_name[index]+"/sap.png"
            #创建目录
            
            cv2.imwrite(
                str(Path(os.getcwd()).joinpath(orgPath)),
                org_pic_result,
                [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
            )
            cv2.imwrite(
                str(Path(os.getcwd()).joinpath(sapPath)),
                save_pic_result,
                [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
            )
            logger.info(f"Diff Pic Over Come...")
            result_ssim[f'{path_name[index]}']=result_ssim_score
        return result_ssim

    @staticmethod
    def compare_pic_diff_pic(img,picorder = 2000):
        if img.shape[0] > img.shape[1]:
            new_size = (int(img.shape[1] / img.shape[0] * picorder),int(picorder)) # resize后的变换过程
        else:
            new_size = (int(picorder),int(img.shape[0] / img.shape[1] * picorder))
        img = cv2.resize(copy.deepcopy(img),new_size,interpolation=cv2.INTER_CUBIC)
        return img  
    @staticmethod
    def get_diff_pic_org_sap(result_pic,org_pic,sap_pic):
        org_pic_tmp = copy.deepcopy(org_pic)
        sap_pic_tmp = copy.deepcopy(sap_pic)
        result_pic = (result_pic*255).astype("uint8")
        """
        转换成黑白图像，然后在进行不同区域的画图的过程
        """
        oneblack_result_pic = cv2.threshold(result_pic,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
        Rectange_result_pic = cv2.findContours(oneblack_result_pic.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]

        for rect in Rectange_result_pic:
            (x,y,w,h) = cv2.boundingRect(rect)
            cv2.rectangle(org_pic_tmp,(x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(sap_pic_tmp,(x, y), (x + w, y + h), (0, 0, 255), 2)

        return org_pic_tmp,sap_pic_tmp
"""
    附加的构造原始图片和新生成图片的过程，在两个文件夹下保存同名的图像即可
    :return compare_result的数据对象
"""

def compare_result_pic_data():
    current_path = Path(os.getcwd())
    compare_res={}
    compare_res_line=[]
    file_name_org_list = []
    file_name_org = None
    for root1,dirs,files in os.walk(Path(current_path).joinpath('org')):
        for file in files:
            if os.path.splitext(file)[1] == '.png':
                file_name_org = os.path.splitext(file)[0]
                file_path_org = os.path.join(root1,file)
                for root,dirs,files in os.walk(Path(current_path).joinpath('sap')):
                    for file1 in files:
                        if os.path.splitext(file1)[0] == file_name_org and os.path.splitext(file1)[1] == '.png':
                            file_name_sap = os.path.splitext(file1)[0]
                            file_path_sap = os.path.join(root,file1)
                            compare_res['org']=file_path_org
                            compare_res['sap']=file_path_sap
                            compare_res_line.append(compare_res)
                            file_name_org_list.append(file_name_org)
                            break
                    break
            compare_res={}
    #logger.info(f'Compare_res_line is {compare_res_line}')
    return compare_res_line, file_name_org_list  




if __name__ == "__main__":
    logger.info(f"Staring ...")
    compare_res,file_name_org = compare_result_pic_data()
    logger.info(file_name_org)
    logger.info(f"Starting SSIM Progress ...")
    
    result_score = PicHander(compare_res).generate_diff_pic_between_ssim(file_name_org)

    