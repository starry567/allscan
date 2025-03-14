import os
import importlib.util
import traceback

# 获取上一级目录，并设置 POC 脚本的目录路径
POC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'allexp')

def load_poc(poc_name, poc_path):
    """动态加载指定的 POC 脚本路径"""
    try:
        # 动态加载模块
        spec = importlib.util.spec_from_file_location(poc_name, poc_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Failed to load POC '{poc_name}': {e}")
        traceback.print_exc()
    return None

def run_pocs(url):
    """遍历 POC 脚本并运行"""
    # 使用 os.walk() 遍历 POC 脚本目录及其子目录
    for root, dirs, files in os.walk(POC_DIR):
        for poc_name in files:
            if poc_name.endswith(".py"):
                poc_path = os.path.join(root, poc_name)
                poc_name_without_extension = os.path.splitext(poc_name)[0]
                print(f"Loading and running POC: {poc_name_without_extension}...")  # 输出当前执行的POC
                try:
                    # 加载和执行POC
                    module = load_poc(poc_name_without_extension, poc_path)
                    if module and hasattr(module, 'poc'):
                        print(f"Running {poc_name_without_extension} on {url}...")
                        result = module.poc(url)
                        if result:
                            print(f"++++++{url} :POC {poc_name_without_extension} found vulnerability!")
                        else:
                            print(f"{url} :POC {poc_name_without_extension} did not find vulnerability.")
                except Exception as e:
                    print(f"Error running POC '{poc_name_without_extension}': {e}")
                    traceback.print_exc()

if __name__ == "__main__":
    target_url = "http://139.159.140.130/"  # 目标 URL
    print(f"Starting vulnerability scan on: {target_url}")
    run_pocs(target_url)
    # 可以继续扫描其他目标
    #print("Starting vulnerability scan on 'vulnerable' target")
    #run_pocs("vulnerable")
