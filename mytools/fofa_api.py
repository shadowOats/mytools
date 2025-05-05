import base64
from .base import *
import requests
import json
import re

def is_valid_ip(ip):
    return re.fullmatch(r'(?:\d{1,3}\.){3}\d{1,3}', ip) is not None


def is_valid_domain(domain):
    return re.fullmatch(r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$', domain) is not None


def deal_domain(url):
    if "://" in url:
        # 将第一次出现的 :// 作为分隔符, 拿下标 1 的值
        url = url.split("://", 1)[1]
    if ":" in url:
        # 将第一次出现的 : 作为分隔符, 拿下标 0 的值
        url = url.split(":", 1)[0]
    if is_valid_domain(url):
        return url
    return ""


def deal_ip(ip):
    ip = ip.split(":", 1)[0]
    return ip if is_valid_ip(ip) else ""


def build_url(domain_or_ip, port):
    scheme = "https" if port == "443" else "http"
    return f"{scheme}://{domain_or_ip}:{port}"


def fofa_gogogo(main_url="http://fofa.xmint.cn", email="", key="45d8cfcccaf45289ca2cc204642543ff", query="", size=0):
    if not main_url:
        print(f"main_url is empty")
        return
    if not key:
        print(f"key is empty")
        return
    if not query:
        print(f"query is empty")
        return
    if not size:
        print(f"size is empty")
        return

    try:
        if str(main_url) or str(key) or str(size):
            print(f"请检查参数 main_url/key/query/size 是否可以正常使用.")
        query1 = str(base64.b64encode(query.encode('utf-8')), "utf-8")
        if '@' in email:
            url = f'{main_url}/api/v1/search/all?key={key}&email={email}&qbase64={query1}&page=1&size={size}'
        else:
            url = f'http://fofa.xmint.cn/api/v1/search/all?key={key}&qbase64={query1}&page=1&size={size}'

        # 请求数据
        response = requests.get(url).content.decode('utf-8')
        resJson = json.loads(response)
        datas = resJson.get('results')
        print(f"共搜索到 {len(datas)} 条记录！")

        print(datas)

        # 创建输出目录
        timestamp = nowTime()
        dir = f"output/{timestamp}"
        os.makedirs(dir)

        # 准备数据
        domains, ips, urls = '', '', ''
        for data in datas:
            domain_or_ip = data[0]
            ip_raw = data[1]
            port = data[2]

            domain = deal_domain(domain_or_ip)
            ip = deal_ip(ip_raw)

            if domain:
                domains += domain + "\n"
                url_entry = build_url(domain, port)
                urls += url_entry + "\n"
            elif ip:
                ips += ip + "\n"
                url_entry = build_url(ip, port)
                urls += url_entry + "\n"

        log = f"查询语句为: {query}\n查询条数为: {size}"

        # 写入文件
        writeFile(f"{dir}/log.txt", log)
        writeFile(f"{dir}/domains.txt", domains)
        writeFile(f"{dir}/ips.txt", ips)
        writeFile(f"{dir}/urls.txt", urls)

        print(pinkStr(f"老公~~ 人家已经帮你把资产找出来了噢, 存放在目录 {dir} 下啦~~ 今晚记得奖励人家噢 QAQ"))
    except Exception as e:
        print(pinkStr(f"老公~~ 出现报错了呢... 这边建议检查一下小猫咪有没有关噢~~\n") + e)
