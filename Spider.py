# -*- coding: utf-8 -*-

######################
# Author : 高明飞
# Data : 2016-07-25
# Brief : 用于自动检查新信息的爬虫
######################

import time, logging
import logging.handlers

from ZJU_Talk import *
from SJTU_Talk import *
from FD_Talk import *
from YJS import *
from RuanKao import *

# Init
FinanceKeywords = [
    '金融', '投资', '资产', '债券', '证券', '期货', '银行', '保险',
    '基金', '信托', 'analyst', 'Analyst'
]

EngineerKeywords = [
    '编程', 'Linux', 'linux', '嵌入式', '单片机', 'MCU', 'STM32',
    'IT服务', 'Python', 'python', 'C++', 'RTOS', 'firmware', 'Firmware',
    '硬件', '软件', '智能', '驱动', '新能源', '固件',
    '电路', 'ARM', 'arm', '微控制器', '汇编', 'C语言', 'matlab',
    'Matlab', '研发', '算法', 'DSP', 'C#', '微电子', '芯片', '图像处理',
	'模式识别', 'NEON', 'OpenGL', '计算机视觉', '图像识别', 'OpenCV'
]

HardwareKeywords = [
    '硬件', '电路', 'Altium', '单片机', '信号完整性', '电子设计', '系统设计',
    'PCB', '原理图', 'EMC', 'EMI', '电磁兼容', '数字电路', '模拟电路', 
    '数电', '模电', 'Cadence'
]

HardwareSpecialKeywords = [
    '硬件工程师', '电子工程师', '射频工程师', '硬件应用工程师'
]

WebList = []
WebList.append(ZJU_Talk('浙大招聘宣讲会', 'ZJU_Talk_Engineer', 7, HardwareKeywords, HardwareSpecialKeywords))
#    WebList.append(ZJU_Talk('浙大金融宣讲会', 'ZJU_Talk_Finance', 6, FinanceKeywords))
#    WebList.append(SJTU_Talk('交大金融宣讲会', 'SJTU_Talk_Finance', 8, FinanceKeywords))
WebList.append(SJTU_Talk('交大招聘宣讲会', 'SJTU_Talk_Engineer', 9, HardwareKeywords, HardwareSpecialKeywords))
#    WebList.append(FD_Talk('复旦金融宣讲会', 'FD_Talk_Finance', 10, FinanceKeywords))
WebList.append(FD_Talk('复旦招聘宣讲会', 'FD_Talk_Engineer', 11, HardwareKeywords, HardwareSpecialKeywords))
#    WebList.append(YJS('应届生金融招聘', 'YJS_Finance', 12, FinanceKeywords))
WebList.append(YJS('应届生工程师招聘', 'YJS_Engineer', 13, HardwareKeywords, HardwareSpecialKeywords))
WebList.append(RuanKao(5))

LOG_FILE = "Debug.log"
#  logging.basicConfig(
#      filename='%s.log'%(time.strftime("%Y_%m_%d", time.localtime())), level=logging.WARNING,
#      format='%(asctime)s  :  %(message)s')

logger = logging.getLogger()
fh = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='D', interval=1, backupCount=7)
formatter = logging.Formatter('%(asctime)s  :  %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logging.critical('Program Start!\n')
while True:
    logging.warning('Start a new loop~')

    for web in WebList:
        try:
            logging.warning('************************')
            web.GET()

        except Exception as err:
            logging.error('Unexpected ERROR!!!!!!')
            logging.error(repr(err))
            # traceback.print_exc()

            web.err += 1
            if 4 == web.err:
                try:
                    web.ReportErrStatus(repr(err), True)
                    logging.warning('Send Wchat Error Report.')
                except:
                    logging.critical('Send Wchat Error Report Error!!!!!')
        else:
            if web.err >= 4:
                try:
                    web.ReportErrStatus('', False)
                    logging.warning('Send Wchat Recovery Report.')
                except:
                    logging.critical('Send Wchat Recovery Report Error!!!!!')
            web.err = 0

        finally:
            web.Update()

    logging.warning('************************')
    logging.warning('End of a loop~\n')
    time.sleep(900)

logging.critical('Program End!\n')

