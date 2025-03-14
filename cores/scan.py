import os
import nmap
import subprocess
from cores.webscan import cms_cms, title, web_scan

ports = ["22","80","3386","443"]

def scan_nmap(scan_ip):
    nm = nmap.PortScanner()
    try:
        for port in ports:
            ret = nm.scan(scan_ip, port, arguments='-sV')
            service_name = ret['scan'][scan_ip]['tcp'][int(port)]['name']
            print('[*] 主机 ' + scan_ip + ' 的 ' + str(port) + ' 端口服务为：' + service_name)
            if service_name=="http" or service_name=="https":
                web_scan(f"{service_name}",scan_ip)

    except Exception as e:
        print(e)


def scan_masscan(ip):
    ##os.system(f'masscan -p80 {ip} -oJ {ip}.json --rate 1000')
    #os.system(f'masscan -p80 {ip} --rate 100')
    try:
        for port in ports:
            command = f"masscan -p{port} {ip} --rate 100"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            stdout = result.stdout
            stderr = result.stderr
            if stdout:
                print(ip + ":  "+port)
    except Exception as e:
        print(e)






