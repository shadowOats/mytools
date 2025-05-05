import requests
from .base import *


def exp2(config1, config2, url, command=""):
    save_dir = f"exp_output/res.txt"

    if config1["method"].upper() == "GET":
        return run_get_exp(config, config2, url, save_dir, command)
    elif config1["method"].upper() == "POST":
        return run_post_exp_mul(config1, config2, url, save_dir, command)


def run_get_exp(config, url, save_dir, command):
    print()


def run_post_exp(config, url, save_dir, command):
    session = requests.Session()
    content = ""
    try:
        resp = session.post(url + config["pocUrl"], headers=config["headers"], data=config["data"], verify=False,
                            timeout=config["waitTime"])
        content = resp.text
        res = f"url: {url}\ncommand: {command}\ntime: {nowTime()}\n{content}\n\n"
        # print(greenStr(res))
        appenFile(save_dir, res)
    except Exception as e:
        print(e)
    return res

def exp(config, url, command=""):
    save_dir = f"3-exp_output/res.txt"

    if config["method"].upper() == "GET":
        return run_get_exp(config, url, save_dir, command)
    elif config["method"].upper() == "POST":
        return run_post_exp(config, url, save_dir, command)


def run_post_exp_mul(config1, config2, url, save_dir, command):
    content1 = sand(config1, url).text
    content2 = sand(config2, url).text

    content = greenStr(f"第一个包的响应为--->:\n {content1}\n\n第二个包的响应为--->:\n {content2}\n\n")

    res = f"url: {url}\ncommand: {command}\ntime: {nowTime()}\n{content}\n\n"
    appenFile(save_dir, res)
    return content


def shell():
    print()