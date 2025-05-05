import random
from time import sleep
from lxml import etree
from .base import *
from .deal_url import *
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
}

urls = ['baidu.com', 'taobao.com', 'jingdong.com', 'xiaomi.com']


def find_url(url, count):
    try:
        query_url = 'https://www.aizhan.com/cha/' + url.replace('\n', "")
        flag = 1
        res = ""
        while 1:
            response = requests.get(query_url, headers=headers, verify=False, timeout=5)
            txt = response.text
            html = etree.HTML(txt)
            content1 = html.xpath(f'/html/body/div[5]/div[2]/div[2]/table/tr[2]/td/ul/li[1]/a/img/@alt')
            content2 = html.xpath(f'/html/body/div[5]/div[2]/div[2]/table/tr[2]/td/ul/li[3]/a/img/@alt')
            content3 = html.xpath(f'/html/body/div[5]/div[2]/div[2]/table/tr[2]/td/ul/li[4]/a/img/@alt')
            content4 = html.xpath(f'/html/body/div[5]/div[2]/div[2]/table/tr[2]/td/ul/li[7]/a/img/@alt')
            if "n" not in content1 and "n" not in content2 and "n" not in content3 and "n" not in content4 and "n" not in content1:
                count += 1
                res = f"No: {count}\n{url} 的权重如下所示: \n百度 的权重为: {content1[0]}\n搜狗 的权重为: {content2[0]}\n360 的权重为: {content3[0]}\n谷歌 的权重为: {content4[0]}\n\n"
                print(f"{url} 的权重如下所示: ")
                print(greenStr(f"百度 的权重为: {content1[0]}"))
                print(greenStr(f"搜狗 的权重为: {content2[0]}"))
                print(greenStr(f"360 的权重为: {content3[0]}"))
                print(greenStr(f"谷歌 的权重为: {content4[0]}\n"))
                return res
            sleep(1 + random.random(1, 2))
            print(f"正在查询中, 请稍等...{flag}秒")
            flag += 1
        return res
    except Exception as e:
        if "Max retries" in str(e):
            print(pinkStr(f"请关闭代理, 亲~"))
        else:
            print(redStr(e))


def main():
    try:
        urls = readFile('input/urls.txt')
        urls = format_domains(urls)[2]
        count = 0
        save_path = f"output/{nowTime()}/result.txt"
        mkdir(os.path.dirname(save_path))  # 只传入目录部分
        result = ""
        for url in urls:
            res = find_url(url, count)
            if res:
                result += f"{res}"
                count += 1
        writeFile(save_path, result)
        if count == 0:
            print(yellowStr(f"一个有权重的域名都没有!!!"))
            return
        print(greenStr(f"恭喜你, 找到了 {count} 个有权重的域名."))
        print(greenStr(f"域名列表已保存至路径: {save_path}"))
    except Exception as e:
        print(redStr(e))


if __name__ == '__main__':
    main()
