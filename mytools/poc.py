import json
import requests
import queue
import threading
import urllib3
from .base import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

lock = threading.Lock()


def sand(config, url):
    session = requests.Session()
    return session.post(url + config["pocUrl"], headers=config["headers"], data=config["data"], verify=False,
                        timeout=config["waitTime"])


def write_res(current, total, url, content, config, counter):
    print(greenStr(f"[+] {current} / {total} 漏洞识别: {url}"))
    result_dir = config['save_dir']
    os.makedirs(result_dir, exist_ok=True)
    counter[1] += 1
    res = f"No: {counter[1]}\nurl: {url}\n{content}\n"
    print(greenStr(res))

    appenFile(result_dir + "/content.txt", res)
    appenFile(result_dir + "/res.txt", url)


def get_scan(url, headers, config, counter, total):
    with lock:
        counter[0] += 1
        current = counter[0]
    url = url if "://" in url else "http://" + url
    try:
        session = requests.Session()
        resp = session.get(url + config["pocUrl"], headers=headers, verify=False, timeout=config["waitTime"])
        content = resp.text

        for white in config["whiteList"]:
            if all(black not in content for black in config["blackList"]) and white in content:
                with lock:
                    print(greenStr(f"[+] {current} / {total} 漏洞识别: {url}"))
                    result_dir = config['save_dir']
                    os.makedirs(result_dir, exist_ok=True)
                    appenFile(result_dir + "/res.txt", url)
                return
        with lock:
            print(yelloStr(f"[-] {current} / {total} 未识别: {url}"))
    except Exception as e:
        with lock:
            print(redStr(f"[!] {current} / {total} 请求失败: {url}"), e)


def get_worker(q, headers, config, counter, total):
    while not q.empty():
        url = q.get()
        get_scan(url, headers, config, counter, total)
        q.task_done()


def run_get_poc(config, urls):
    q = queue.Queue()
    for url in urls:
        q.put(url)

    counter = [0]

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    total = len(urls)
    for _ in range(config["threadingNum"]):
        threading.Thread(target=get_worker, args=(q, headers, config, counter, total)).start()


def post_scan(url, config, counter, total):
    with lock:
        counter[0] += 1
        current = counter[0]
    url = url if "://" in url else "http://" + url
    try:
        session = requests.Session()
        resp = session.post(url + config["pocUrl"], headers=config["headers"], data=config["data"], verify=False,
                            timeout=config["waitTime"])
        content = resp.text
        # print(content)
        # 根据 whiteBoolean 选择匹配逻辑
        if config["whiteBoolean"] == "AND":
            # 所有白名单都需要匹配
            if all(white in content for white in config["whiteList"]) and all(
                    black not in content for black in config["blackList"]):
                with lock:
                    write_res(current, total, url, content, config, counter)
                return
        elif config["whiteBoolean"] == "OR":
            # 至少一个白名单匹配
            if any(white in content for white in config["whiteList"]) and all(
                    black not in content for black in config["blackList"]):
                with lock:
                    write_res(current, total, url, content, config, counter)
                return
        with lock:
            print(yelloStr(f"[-] {current} / {total} 未识别: {url}"))
    except Exception as e:
        with lock:
            print(redStr(f"[!] {current} / {total} 请求失败: {url}"), e)


def post_worker(q, config, counter, total):
    while not q.empty():
        with lock:
            url = q.get()
        post_scan(url, config, counter, total)
        q.task_done()

    # while not q.empty():
    #     try:
    #         with lock:
    #             url = q.get(timeout=3)  # 如果3秒没有任务则跳出
    #         print(f"[INFO] 线程开始处理: {url}")  # 调试输出
    #     except queue.Empty:
    #         print("[INFO] 队列已空，退出线程")  # 调试输出
    #         break  # 队列为空，退出


def run_post_poc(config, urls):
    q = queue.Queue()

    # 将URLs放入队列中
    for url in urls:
        q.put(url)

    counter = [0, 0]

    total = len(urls)

    # 使用线程池来限制并发线程数量
    threads = []
    for _ in range(config["threadingNum"]):
        t = threading.Thread(target=post_worker, args=(q, config, counter, total))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    print("[+] 所有任务完成")


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def poc(vul_path="1-input/poc.txt"):
    config = load_config(vul_path)
    urls = readFile("1-input/urls.txt")
    urls = list(set(url.strip() for url in urls if url.strip()))
    config["save_dir"] = f"2-poc_output/{config['targetName']}_{nowTime()}"

    if config["method"].upper() == "GET":
        run_get_poc(config, urls)
    elif config["method"].upper() == "POST":
        run_post_poc(config, urls)


def poc_ssh_connect_mul():
    ssh_client = create_ssh_client()
    key = "urls_ssh_connect/key"
    save_dir = f"urls_ssh_connect/urls_connect_ssh_{nowTime()}"
    user = "root"
    urls = readFile("urls_ssh_connect/urls.txt")
    port = "22"
    res = ""
    count = 0
    for url in urls:
        ip = only_domain(url)
        if test_ssh_connection(ssh_client, key, user, ip, port):
            count += 1
            res += f"No: {count}\n{ip}\n\n"
            print(greenStr(f"{url}成功连接ssh --> 编号: {count}\n"))
    writeFile(save_dir, res)
    if count:
        print(f"批量连接ssh成功， 一共有 {count} 个服务器可连接")
        return
    print(f"没有服务器可连接， 行不行啊， 菜狗！！")
