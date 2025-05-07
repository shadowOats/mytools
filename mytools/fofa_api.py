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
    main_url = str(main_url)
    email = str(email)
    key = str(key)
    query = str(query)
    size = str(size)

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
        if str(main_url)=="" or str(key)=="" or str(size)=="":
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

        # print(datas)

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

        print(pinkStr(f"\n老公~~ 人家已经帮你把资产找出来了噢, 存放在目录 {dir} 下啦~~ 今晚记得奖励人家噢 QAQ"))
    except Exception as e:
        print(pinkStr("\n老公~~ 出现报错了呢... 这边建议检查一下小猫咪有没有关噢~~\n") + str(e))


def fofa_api_main():
    # 基本参数
    # 使用不正规的 fofa
    main_url = 'http://fofa.xmint.cn'
    email = ""
    key = '45d8cfcccaf45289ca2cc204642543ff'

    # 适用正规的 fofa
    # main_url = 'https://fofa.info'
    # email = '18563245634@163.com'
    # key = '59746060c289b3edd58a60d9c9d09b91'

    # query = 'title="Vite App" || body="Powered by Vite" || header="vite"'
    query = str(input("请输入fofa语句(请尽量不要开代理): "))
    size = str(input("请输入你要的结果条数(最大10000条，输入 -1 给你拿 10000 条): "))
    if size == '-1':
        size = '10000'

    fofa_gogogo(main_url, email, key, query, size)


if __name__ == '__main__':
    fofa_api_main()