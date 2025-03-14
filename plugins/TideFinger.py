import subprocess
import re

def Tide_cms(url):
    try:
        # 执行 TideFinger 命令
        result = subprocess.run(
            ['./plugins/TideFinger', '-u', url],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            output = str(result.stdout)
            return extract_info(output)
        else:
            sss = []
            return sss
    except Exception as e:
        return f"Exception: {str(e)}"

def remove_ansi_escape(text):
    ansi_escape = re.compile(r'\x1b\[.*?m')  # 匹配 ANSI 转义序列
    return ansi_escape.sub('', text)  # 替换为空

def extract_info(output):
    output = remove_ansi_escape(output)
    pattern = r'\[\+\] (.*?) http://'
    matched_lines = []
    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            matched_lines.append(f"{match.group(1)}")
    if matched_lines:
        return matched_lines
    else:
        return matched_lines

