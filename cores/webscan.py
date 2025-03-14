import hashlib
import json
import requests
import chardet
import requests
import re
import subprocess
import socket
import os
from cores.title import title
from plugins.TideFinger import Tide_cms
from plugins.subdomain import run_subdomain_bruteforce, site_site138
from cores.ExpScan import run_pocs


def web_scan(server_name,scan_ip):
    ss = get_url2(scan_ip)
    domain = []
    if ss:
        domain_list = site_site138(ss)
    #get domain_list : www.example.com
    #cms = cms_cms(domain)
    for domain in domain_list:
        scan_url, banner, res, code = title(f"{server_name}://{domain}/")
        cms_list = Tide_cms(f"{server_name}://{domain}/")
        print(f"scan_url: {scan_url}")
        print(f"banner: {banner}")
        print(f"res: {res}")
        print(f"code: {code}")
        print(f"cms_list: {cms_list}")
        #run_pocs(f"{server_name}://{domain}/")

    """domain = clean_domain(domain)
    # 获取当前脚本所在目录（script.py所在的目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建subdomains.txt的路径（相对于当前目录）
    dictionary_file = os.path.join(current_dir, "../plugins/subdomains.txt")
    # run_subdomain_bruteforce("wtu.edu.cn",dictionary_file)
    results = run_subdomain_bruteforce(domain, dictionary_file)
    # 打印所有找到的子域名和状态码
    print("\nFound Subdomains:")
    for url, code in results:
        print(f"{url} - Status Code: {code}")
        #cms = cms_cms(url)
        title(url)
        run_pocs(url)"""



def clean_domain(domain):
    domain = domain.lower().strip()
    # 去掉 http:// 或 https://
    domain = re.sub(r'^https?://', '', domain)
    # 去掉 www. 前缀
    domain = re.sub(r'^www\.', '', domain)
    return domain



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
                    return i["cms"]


def get_url(scan_ip):
    try:
        # 使用 subprocess.run 来获取输出
        result = subprocess.run(["nslookup", scan_ip], capture_output=True, text=True)
        output = result.stdout
        # 获取命令的标准输出
        if result.returncode == 0:
            match = re.search(r'name\s*=\s*([^\r\n]+)\.', output)
            if match:
                domain = match.group(1)
                #print(f"geturl:  {scan_ip}: {domain}")
                return domain
            else:
                domain = scan_ip
                #print(f"ip : {domain}")
                return domain
        else:
            pass
            #print("Error:", result.stderr)

    except Exception as e:
        print(f"An error occurred: {e}")

def get_url2(ip):
    try:
        # 进行反向 DNS 查找
        host, alias, ips = socket.gethostbyaddr(ip)
        #print(f"The host for IP {ip} is: {host}")
        return host
    except socket.herror:
        host = ip
        return host
    except Exception as e:
        print(f"An error occurred: {e}")
