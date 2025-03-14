import hashlib
import json
import requests
import os
import sys
from plugins.subdomain import run_subdomain_bruteforce
from main import start


def cms_cms(url):
    cms_json = open("../fingers/cms/fingers_simple.json", "r", encoding="utf-8")
    cms_data = json.load(cms_json)
    for i in cms_data["data"]:
        print(i)
        if i["path"]!="":
            respon = requests.get(url+i["path"])
            if str(respon) == "<Response [200]>":
                md5_1 = hashlib.md5()
                md5_1.update(respon.content)
                hash_key = md5_1.hexdigest()
                if hash_key ==i["match_pattern"]:
                    print(i["cms"])

def test():
    cms_cms("http://162.43.117.29")

if __name__ == '__main__':
    #test()
    #title("http://www.wtu.edu.cn")
    #get_url2("211.67.48.2")
    #get_url2("139.159.140.130")
    #web_scan("211.67.48.2")
    #scan_nmap("139.159.140.130")
    #scan_masscan("139.159.140.130")
    #start("211.67.48.2")
    #dictionary_file = "subdomains.txt"

    # 获取当前脚本所在目录（script.py所在的目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建subdomains.txt的路径（相对于当前目录）
    dictionary_file = os.path.join(current_dir, "../plugins/subdomains.txt")
    #run_subdomain_bruteforce("wtu.edu.cn",dictionary_file)
    results = run_subdomain_bruteforce("wtu.edu.cn", dictionary_file)

    # 打印所有找到的子域名和状态码
    print("\nFound Subdomains:")
    for url, code in results:
        print(f"{url} - Status Code: {code}")
