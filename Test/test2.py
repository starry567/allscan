import requests
import yaml
import re


def load_yaml_template(file_path):
    """加载 YAML 模板文件"""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def send_request(request_details, base_url):
    """发送 HTTP 请求"""
    # 检查请求格式是否是 raw 或 http
    if 'raw' in request_details:
        request_details = request_details['raw'][0]
        url = f"{base_url}{request_details['path']}"
        headers = request_details.get('headers', {})
        method = request_details.get('method', 'GET')
        body = request_details.get('body', '')

        # 发送请求
        if method == "GET":
            response = requests.get(url, headers=headers, params=body)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=body)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    elif 'http' in request_details:
        # 处理 'http' 请求类型
        for req in request_details['http']:
            url = f"{base_url}{req['path'][0]}"
            method = req.get('method', 'GET')
            headers = req.get('headers', {})
            body = req.get('body', '')

            # 发送请求
            if method == "GET":
                response = requests.get(url, headers=headers, params=body)
            elif method == "POST":
                response = requests.post(url, headers=headers, data=body)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            break  # 这里只取第一个请求

    else:
        raise ValueError("Unsupported request format, must be either 'raw' or 'http'")

    return response


def check_matchers(response, matchers):
    """根据模板中的匹配规则检查响应"""
    for matcher in matchers:
        matcher_type = matcher.get('type')

        if matcher_type == 'status':
            if response.status_code not in matcher['status']:
                return False

        elif matcher_type == 'word':
            for word in matcher['words']:
                if word not in response.text:
                    return False

        elif matcher_type == 'dsl':
            # 解析 DSL 表达式，简单的例子
            for dsl in matcher['dsl']:
                if eval(dsl.replace('body', f'"{response.text}"')):
                    return True
            return False

        # 可以根据需要扩展更多的匹配器类型

    return True


def run_scan(vulnerability_template, base_url):
    """执行漏洞扫描"""
    for request in vulnerability_template['requests']:
        # 获取请求详细信息
        response = send_request(request, base_url)

        # 检查响应是否符合漏洞条件
        if check_matchers(response, request['matchers']):
            print(f"漏洞匹配成功：{vulnerability_template['info']['name']}")
        else:
            print(f"未发现漏洞：{vulnerability_template['info']['name']}")


if __name__ == "__main__":
    # 模板文件路径
    templates = [
        '../allexp/1.yaml',
        '../allexp/2.yaml',
        '../allexp/3.yaml'
    ]

    # 目标URL（请根据实际情况修改）
    base_url = "http://example.com"

    # 遍历并执行每个漏洞模板的扫描
    for template_path in templates:
        vulnerability_template = load_yaml_template(template_path)
        run_scan(vulnerability_template, base_url)
