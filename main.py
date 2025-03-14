import concurrent.futures.thread
from cores.scan import *

'''
#### need to change

'''


def start(scan_ip):
    #print(scan_ip)
    scan_nmap(scan_ip)
    scan_masscan(scan_ip)
    ##test
    #return ok

#### get ip.     too large
def get_ip():
    ip_list = []
    #for i in range(5):
        #for j in range(256):
            #for k in range(256):
                #for l in range(256):
                    #j=k=l=1
                    #ip = f"{i}.{j}.{k}.{l}"
                    #ip_list.append(ip)
    ip_list = ['211.67.48.2', '139.159.140.130:8081']
    return ip_list



def main():
    list = get_ip()
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=10) as executor:
        mytasks = [executor.submit(start,i) for i in list]   #提交了10个任务
        for mytask in concurrent.futures.as_completed(mytasks):
            try:
                #print(mytask.result())
                mytask.result()
            except Exception as e:
                print(e)




if __name__ == '__main__':
    main()

