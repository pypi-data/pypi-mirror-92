#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
此函数的目的是通过相应的页面数据，通过获取下函数的实例声明，并获取相应的值的过程:

整个页面的历程如下：
 - 1.在主页面中引用子页面的相关的类的实例对象，初始化的部分是通过传入浏览器实例实现；
 search_handler = FindPic(browser=dr)
 - 2.由传入的参数确定是在每个页面都进行截图，还是在固定的页面进行截图，默认是在每个页面都进行截图
 search_handler.get_pic_traverse_url()
 - 3.截图的文件在分别保存着不同的文件夹中同时在相应的文件中保存比较得到的对应结果
FindPic类的作用是进行第一步的初始化作用，同时在其内部进行相应的功能引导作用；
"""
from picHander import PicHander
import picHander
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 
logger = logging.getLogger("FindHander")
class FindHander():
    
    def __init__(self,sava_screen_shot=None,pic_args=None):
        # compare_res = picHander.compare_result_pic_data()
        # self.pichander = PicHander(compare_res)
        self.num = 0
        self.save_pic =[]
        self.screen_shot = sava_screen_shot
        self.pic_args = None
    """
    第一次执行函数的过程，是包括在相应的文件夹生成，初始化org文件夹的内容；
    截图相应的部分图片，使用screenshot函数进行
    """
    def get_pic_traverse(self,path):
        logger.info('Path:%s',path)
        self.fileMkdir(str(path))
        self.save_pic.append(
        self.get_screen_log(self.num,path)
        )
        self.num = self.num+1

    def fileMkdir(self,path):
        if not os.path.exists(path):
            logger.info('Path:%s',path)
            os.mkdir(path)
            logger.info('Org-Dir hava completed and suceed to create it ...')
        else:
            # logger.info('Org-Dir have shutted down it ...')
            # shutil.rmtree(str(path))
            # os.makedirs(str(path))
            logger.info('Org-Dir have succeed to create it ...')

    def get_screen_log(self,num,path,filename = None):
        if path is None:
            return None
        png_file_name = 'pic_'+str(num)+'_'+'.png'
        png_path = os.path.join(path,png_file_name)
        logger.info('this is png path:%s'%png_path)
        self.screenShot(png_path)
        saved = {"screen":png_file_name}
        return saved

    def screenShot(self,file_path = None):
        if file_path:
            self.screen_shot(file_path)
        else:
            file_path = os.path.join(path,"failed.png")
            self.screen_shot(file_path)

if __name__ == "__main__":
    from selenium.webdriver import Chrome,ActionChains
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import os
    import time
    chrome_driver='/Users/lijishuang/Downloads/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    dr = webdriver.Chrome(executable_path=chrome_driver,chrome_options=options)

    pt = FindHander(
        dr.save_screenshot
    )
    dr.set_window_size(1920, 1080)
    origin_url = 'https://www.baidu.com/'
    dr.get(origin_url)
    dr.implicitly_wait(10)
    path_self = Path(os.getcwd()).joinpath('org')
    pt.get_pic_traverse(path_self)
    elem = dr.find_element_by_name("wd")
    elem.send_keys('今日头条'+ Keys.RETURN)
    time.sleep(5)
    # 截
    pt.get_pic_traverse(path_self)

