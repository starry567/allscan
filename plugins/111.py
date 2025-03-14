import requests
import sys
from queue import Queue
from threading import Thread

# 处理每个子域名的函数
def check_subdomain(subdomain, target_domain, q, results):
    url = f"http://{subdomain}.{target_domain}"
    try:
        response = requests.get(url, timeout=5)
        status_code = response.status_code
        print(f"响应状态码：{status_code}")  # 打印状态码
        if status_code == 200:
            print(f"[+] Found: {url}")
            results.append((url, status_code))  # 保存找到的子域名和状态码
        q.put(subdomain)

    except requests.exceptions.Timeout:
        print(f"请求超时：{url}")
    except requests.exceptions.ConnectionError:
        print(f"连接错误：{url}")
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")  # 捕获其他请求相关的异常

# 多线程爆破的函数
def worker(q, target_domain, results):
    while True:
        subdomain = q.get()
        if subdomain is None:  # 如果拿到结束信号，退出线程
            break
        check_subdomain(subdomain, target_domain, q, results)

# 运行爆破的主函数
def run_subdomain_bruteforce(target_domain, dictionary_file):
    # 创建队列和线程
    q = Queue()
    threads = []
    results = []  # 存储发现的子域名和状态码
    print("subdomain启动线程")

    # 从字典文件读取子域名
    try:
        with open(dictionary_file, 'r') as file:
            subdomains = file.read().splitlines()
    except FileNotFoundError:
        print(f"字典文件 {dictionary_file} 未找到")
        sys.exit(1)

    # 启动线程
    for _ in range(10):  # 启动10个线程，可以根据需要调整
        t = Thread(target=worker, args=(q, target_domain, results))
        t.start()
        threads.append(t)

    # 将子域名加入队列
    for subdomain in subdomains:
        q.put(subdomain)

    # 等待所有线程完成后，添加结束信号
    for _ in range(10):  # 这里添加10个结束信号，确保每个线程都能接收到
        q.put(None)

    # 等待所有线程完成
    for t in threads:
        t.join()

    print("爆破完成")
    return results  # 返回所有找到的子域名和状态码

# 测试函数：
if __name__ == "__main__":
    target_domain = "wtu.edu.cn"
    dictionary_file = "subdomains.txt"
    results = run_subdomain_bruteforce(target_domain, dictionary_file)

    # 打印所有找到的子域名和状态码
    print("\nFound Subdomains:")
    for url, code in results:
        print(f"{url} - Status Code: {code}")
