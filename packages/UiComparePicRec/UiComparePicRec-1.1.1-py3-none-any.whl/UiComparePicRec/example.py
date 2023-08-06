from selenium.webdriver import Chrome,ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import logging
from pathlib import Path
from findHander import FindHander
from picHander import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 
logger = logging.getLogger("Example")
chrome_driver='/Users/lijishuang/Downloads/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
dr = webdriver.Chrome(executable_path=chrome_driver,chrome_options=options)

def function_pic(dr,path_self):
    pt = FindHander(dr.save_screenshot)

    dr.set_window_size(1920, 1080)
    origin_url = 'https://www.baidu.com/'
    dr.get(origin_url)
    dr.implicitly_wait(10)

    pt.get_pic_traverse(path_self)

    elem = dr.find_element_by_name("wd")
    elem.send_keys('今日头条'+ Keys.RETURN)
    time.sleep(5)
    # 截
    pt.get_pic_traverse(path_self)
"""
path_self:定义保存截图的目录，使用 --from pathlib import Path-- 定义路径
使用get_pic_traverse进行需要保存截图的地方使用
"""
path_self_org = Path(os.getcwd()).joinpath('org')
path_self_sap = Path(os.getcwd()).joinpath('sap')
function_pic(dr,path_self_org)
function_pic(dr,path_self_sap)

logger.info(f"Staring ...")
compare_res,file_name_org = compare_result_pic_data()
logger.info(file_name_org)
logger.info(f"Starting SSIM Progress ...")
    
result_score = PicHander(compare_res).generate_diff_pic_between_ssim(file_name_org)

print(result_score)


logger.info(f"Staring ...")
compare_res,file_name_org = compare_result_pic_data()
logger.info(file_name_org)
logger.info(f"Starting Vector Progress ...")
    
result_score = PicHander(compare_res).generate_diff_pic_between_vector(file_name_org)

print(result_score)