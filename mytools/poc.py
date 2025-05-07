import json
import requests
import queue
import threading
import urllib3
from mytools.base import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

lock = threading.Lock()

res1 = []  # 保存完整响应内容
res2 = []  # 保存 URL


def write_final_results(config):
    result_dir = f"output/poc_output/(len={len(res2)})_{str(config['targetName']).strip()}_{nowTime()}"
    other_save_dir = "input/urls"

    config["save_dir"] = result_dir
    config["other_save_dir"] = other_save_dir

    mkdir(result_dir)
    writeFile(f"{result_dir}/content.txt", res1)
    writeFile(f"{result_dir}/res.txt", res2)
    writeFile(f"{other_save_dir}/poc_res_urls.txt", res2)


def write_res(current, total, url, content, config, counter):
    counter[1] += 1
    res = f"No: {counter[1]}\nurl: {url}\n{content}\n"
    print(greenStr(f"\n[+] {current} / {total} 漏洞识别: {url}"))
    print(greenStr(res))

    res1.append(res)
    res2.append(url)


def get_scan(url, headers, config, counter, total):
    with lock:
        counter[0] += 1
        current = counter[0]

    url = url if "://" in url else "http://" + url

    try:
        session = requests.Session()
        resp = session.get(url + config["require_path"], headers=headers, verify=False, timeout=config["waitTime"])
        content = resp.text

        for white in config["whiteList"]:
            if all(black not in content for black in config["blackList"]) and white in content:
                with lock:
                    write_res(current, total, url, content, config, counter)
                return
        with lock:
            print(yellowStr(f"[-] {current} / {total} 未识别: {url}"))
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

    counter = [0, 0]
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': '*/*', 'Connection': 'keep-alive'}
    total = len(urls)

    threads = []
    for _ in range(config["threadingNum"]):
        t = threading.Thread(target=get_worker, args=(q, headers, config, counter, total))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    write_final_results(config)


def post_scan(url, config, counter, total):
    with lock:
        counter[0] += 1
        current = counter[0]

    url = url if "://" in url else "http://" + url
    try:
        session = requests.Session()
        resp = session.post(url + config["require_path"], headers=config["headers"], data=config["data"], verify=False,
                            timeout=config["waitTime"])
        content = resp.text

        if config["whiteBoolean"] == "AND":
            if all(white in content for white in config["whiteList"]) and all(
                    black not in content for black in config["blackList"]):
                with lock:
                    write_res(current, total, url, content, config, counter)
                return
        elif config["whiteBoolean"] == "OR":
            if any(white in content for white in config["whiteList"]) and all(
                    black not in content for black in config["blackList"]):
                with lock:
                    write_res(current, total, url, content, config, counter)
                return
        with lock:
            print(yellowStr(f"[-] {current} / {total} 未识别: {url}"))
    except Exception as e:
        with lock:
            print(redStr(f"[!] {current} / {total} 请求失败: {url}"), e)


def post_worker(q, config, counter, total):
    while not q.empty():
        with lock:
            url = q.get()
        post_scan(url, config, counter, total)
        q.task_done()


def run_post_poc(config, urls):
    print(f"------------------ poc模块 ------------------")
    q = queue.Queue()
    for url in urls:
        q.put(url)

    counter = [0, 0]
    total = len(urls)

    threads = []
    for _ in range(config["threadingNum"]):
        t = threading.Thread(target=post_worker, args=(q, config, counter, total))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    write_final_results(config)
    print(greenStr(f"\n[+] 所有任务完成, 完成时间  -->  {nowTime()}"))
    print(greenStr(f"[+] 一共 poc 到 {len(res2)} 个url"))
    print(f"------------------ poc模块 ------------------")


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def poc_main(vul_path="input/poc/json/raw1.json"):
    try:
        readFile(vul_path)
    except Exception as e:
        print(yellowStr(f"请检查 {vul_path} 文件是否创建， 并且里面是否有值"))
        return

    config = load_config(vul_path)

    urlsPath = "input/urls/urls.txt"
    try:
        urls = readFile(urlsPath)
    except Exception as e:
        print(yellowStr(f"请检查 input/urls/urls.txt 文件是否创建， 并且里面是否有值"))
        return

    urls = list(set(url.strip() for url in urls if url.strip()))

    if config["method"].upper() == "GET":
        run_get_poc(config, urls)
    elif config["method"].upper() == "POST":
        run_post_poc(config, urls)


if __name__ == '__main__':
    poc_main()
