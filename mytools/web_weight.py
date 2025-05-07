from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import re
from time import sleep

sys.path.append("/base_tool/base_tool/")
from mytools.base import *  # 自定义工具模块
import os

# 相对路径
chrome_page = "Chrome/Application/chrome.exe"
chrome_path = getFile(chrome_page)
# chrome_options.add_argument("--headless")  # 如需后台运行可启用此项

# 初始化 Chrome 配置
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path


def wait_for_weight(xpath, timeout=10):
    """等待目标图片加载并提取src中的权重数字"""
    # 用抑制报错的方式, 去检测图片 x.png 是否加载, 来拿到我们的权重值
    for i in range(timeout):
        try:
            img = browser.find_element(By.XPATH, xpath)
            src = img.get_attribute("src")
            # print(f"[debug] 第{i + 1}秒 - src={src}")
            match = re.search(r'/(\d)\.png', src)
            if match:
                return int(match.group(1))
        except Exception as e:
            print(f"[debug] 等待异常: {e}")
        sleep(1)
    return None


def into_page():
    """等待首页加载完成"""
    while True:
        content = browser.page_source
        if "百度" in content and "移动" in content:
            print("已进入目标页面")
            break
        sleep(2)


def send_query(url):
    """将URL输入并提交查询"""
    input_element = browser.find_element(By.XPATH, '//*[@id="domain"]')
    input_element.clear()
    input_element.send_keys(url)

    submit_button = browser.find_element(By.XPATH, '//*[@id="c0"]/div[2]/form/input[2]')
    submit_button.click()


# 全局变量
count = 0
have_weight = 0


def woker(url):
    global have_weight
    """等待并提取所有搜索引擎权重"""
    baidu = wait_for_weight('/html/body/div[5]/div[2]/div[2]/table/tbody/tr[2]/td/ul/li[1]/a/img') or 0
    sogou = wait_for_weight('/html/body/div[5]/div[2]/div[2]/table/tbody/tr[2]/td/ul/li[3]/a/img') or 0
    so360 = wait_for_weight('/html/body/div[5]/div[2]/div[2]/table/tbody/tr[2]/td/ul/li[4]/a/img') or 0
    google = wait_for_weight('/html/body/div[5]/div[2]/div[2]/table/tbody/tr[2]/td/ul/li[7]/a/img') or 0

    if sum([baidu, sogou, so360, google]) > 0:
        have_weight += 1
        res = f"\nNo: {have_weight}\nurl: {url}\n百度权重: {baidu}\n搜狗权重: {sogou}\n360权重: {so360}\n谷歌权重: {google}\n"
        print(greenStr(res))
        return res
    res = f"\n百度权重: {baidu}\n搜狗权重: {sogou}\n360权重: {so360}\n谷歌权重: {google}\n"
    print(yellowStr(res))
    return ""


def find_weight(url, total):
    global count
    """主查询逻辑"""
    try:
        print(f"\n[{count + 1} / {total}] 查询: {url}")
        count += 1
        send_query(url)
        res = woker(url)
        if res and len(res.strip()):
            return res
        return ""
    except Exception as e:
        print(f"[错误] 查询失败: {e}")


def web_weight_main():
    global browser
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://www.aizhan.com/cha/guiyang.tgjyjt.com/')

    into_page()
    urls = readFile("input/urls.txt")
    urls = format_domains(urls)[2]
    total = len(urls)
    result = ""
    for url in urls:
        url = str(url).strip().replace("\n", "")
        if not url:
            continue
        res = find_weight(url, total)
        if len(res):
            result += res
    global have_weight
    save_path = f"web_weight_out/{nowTime()}/res.txt"
    if have_weight:
        print(greenStr(f"\n恭喜你, 亲, 一共找到了 {have_weight} 个有权重的网站,已存储至路径: {save_path}"))
        writeFile(save_path, result)
        return
    print(greenStr(f"\n一个有权重的网站都没有, 行不行的, 叼毛"))


if __name__ == '__main__':
    web_weight_main()
