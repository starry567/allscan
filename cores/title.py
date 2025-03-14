
import time

import chardet
import requests
import re
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from plugins.TideFinger import Tide_cms

def title(scan_url_port):
    try:
        # 请求网页
        r = requests.get(scan_url_port, timeout=10)
        # 检测页面编码
        r_detectencode = chardet.detect(r.content)
        actual_encode = r_detectencode['encoding']
        # 使用正则表达式提取<title>标签内容
        response = re.findall(b'<title>(.*?)</title>', r.content, re.S)
        # 如果没有找到<title>，则打印消息
        if not response:
            print('[*] Website: ' + scan_url_port + '\t\t' + '\n')
        else:
            #cms_list = Tide_cms(scan_url_port)
            #if cms_list == []:
                #cms_list.append("unknown")
            #print(cms_list)
            #cms = "".join(cms_list)
            # 如果找到了<title>标签的内容，进行解码
            res = response[0].decode(actual_encode)  # 先解码为字符串
            banner = r.headers.get('server', 'Unknown')  # 防止 'server' 头缺失,web服务器信息
            code = str(r.status_code)
            print('[*] Website: (url:)' + scan_url_port + '\t\t(banner)' + banner + '\t\t' + 'Title: ' + res +'\t\t' + "code: " + code +'\n')
            #print(cms)
            return scan_url_port,banner,res,code
    except Exception as e:
        pass
        # 捕获并打印异常
        #print(f"Error: {e}")

