import base64
import time
from .base import *
import requests
import json
import re
from .base import *

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


def fofa_request_with_retry(url, headers=None, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            result = response.json()  # 正确写法：直接解析 JSON，而不是先 decode

            # 检查是否为频率限制错误
            if result.get("error") and "请求过于频繁" in result.get("errmsg", ""):
                retry_after = result.get("retry_after", 1)
                print(f"[!] 请求过于频繁，等待 {retry_after} 秒后重试...（第 {attempt + 1}/{max_retries} 次）")
                time.sleep(retry_after)
                continue
            else:
                return result  # 成功返回
        except Exception as e:
            print(f"[!] 请求异常：{e}")
            time.sleep(1)

    print("[×] 重试次数已达上限，仍然失败。")
    return None




def fofa_getAllUrls(main_url, email, key, query):
    main_url = str(main_url)
    email = str(email)
    key = str(key)
    query = str(query)
    size = "10000"

    queries = [
        query + ' && port="443"',
        query + ' && port="80"',
        query + ' && port!="80" && port!="443"'
    ]

    if not main_url:
        print("main_url is empty")
        return
    if not key:
        print("key is empty")
        return
    if not query:
        print("query is empty")
        return

    all_datas = []

    try:
        for q in queries:
            q_base64 = str(base64.b64encode(q.encode('utf-8')), "utf-8")
            if '@' in email:
                url = f'{main_url}/api/v1/search/all?key={key}&email={email}&qbase64={q_base64}&page=1&size={size}'
            else:
                url = f'http://fofa.xmint.cn/api/v1/search/all?key={key}&qbase64={q_base64}&page=1&size={size}'

            response = fofa_request_with_retry(url)
            resJson = response
            datas = resJson.get('results', [])
            all_datas.extend(datas)

        print(greenStr(f"\n总共合并查询结果：{len(all_datas)} 条记录"))

        # 创建输出目录
        timestamp = nowTime()
        dir = f"output/fofa_api_output/{timestamp}_({len(all_datas)})"
        mkdir(dir)

        # 准备数据
        domains, ips, urls = '', '', ''
        for data in all_datas:
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

        log = f"你查询本语句的时间是: {nowTime()}\n查询语句为: {query}\n查询总条数为: {len(all_datas)}\n"

        # 写入文件
        appenFile(f"{dir}/log.txt", log)
        writeFile(f"{dir}/domains.txt", domains)
        writeFile(f"{dir}/ips.txt", ips)
        writeFile(f"{dir}/urls.txt", urls)

        print(pinkStr(f"\n老公~~ 人家已经帮你把资产找出来了噢, 存放在目录 {dir} 下啦~~ 今晚记得奖励人家噢 QAQ"))
    except Exception as e:
        print(pinkStr("\n你个叼毛，是不是没关代理 ？？\n") + str(e))


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
        dir = f"output/fofa_api_output/{timestamp}_({len(datas)})"
        # os.makedirs(dir)
        mkdir(dir)

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

        log = f"你查询本语句的时间是: {nowTime()}\n查询语句为: {query}\n查询条数为: {size}\n"

        # 写入文件
        appenFile(f"{dir}/log.txt", log)
        writeFile(f"{dir}/domains.txt", domains)
        writeFile(f"{dir}/ips.txt", ips)
        writeFile(f"{dir}/urls.txt", urls)

        print(pinkStr(f"\n老公~~ 人家已经帮你把资产找出来了噢, 存放在目录 {dir} 下啦~~ 今晚记得奖励人家噢 QAQ"))
    except Exception as e:
        print(pinkStr("\n你个叼毛，是不是没关代理 ？？\n") + str(e))


def fofa_api_main():
    # 基本参数
    # 使用不正规的 fofa
    main_url = 'https://fofoapi.com'
    email = ""
    key = 'nbvbfz9lnikse5w1uvv0gcy9pp6vjyn8'

    # 适用正规的 fofa
    # main_url = 'https://fofa.info'
    # email = '18563245634@163.com'
    # key = '59746060c289b3edd58a60d9c9d09b91'

    # query = 'title="Vite App" || body="Powered by Vite" || header="vite"'
    query = str(input("请输入fofa语句(请尽量不要开代理): "))
    q_base64 = base64.b64encode(query.encode()).decode()

    # 请求只返回数量的接口
    count_url = f"{main_url}/api/v1/search/stats?key={key}&qbase64={q_base64}&fields=count"
    response = requests.get(count_url)
    count_data = response.json()

    print(count_data)
    print(f"当前查询到有: {count_data['count']} 条数据。")

    size = str(input("请输入你要的结果条数(输入 -1 给你拿完): "))
    if size == '-1':
        fofa_getAllUrls(main_url, email, key, query)
    else:
        fofa_gogogo(main_url, email, key, query, size)


if __name__ == '__main__':
    fofa_api_main()