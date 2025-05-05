import re
from urllib.parse import urlparse
from .base import *

def format_url(url):
    url = url.strip()
    # 检测 url 是否为 http:// 或者 https:// 开头的
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    if ':' not in url.split(":")[1]:
        url += ':80'
    # parsed = urlparse(url)
    # url = "https://test.example.com:443/page?id=123"
    # 将  url 进行切割为 对象形式, 分别存储 协议,域名,端口,路径,参数
    # scheme    https
    # netloc    test.example.com:443
    # hostname  example.com
    # port      443
    # path      /page
    # query     id=123
    # url = "https://test.example.com:443/page?id=123"
    # netloc = parsed.netloc

    return f"{url}"


def format_urls(urls, message=0):
    urls_full = []  # http://domain/ip:port
    urls_basic = []  # http://domain/ip
    urls_raw = []  # domain/ip

    for url in urls:
        url = url.replace("\n", "")
        if not url:
            continue
        full = format_url(url)
        parsed = urlparse(full)
        scheme_host_port = f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"
        scheme_host = f"{parsed.scheme}://{parsed.hostname}"
        host = parsed.hostname

        urls_full.append(scheme_host_port)
        urls_basic.append(scheme_host)
        urls_raw.append(host)

    if message:
        print(f"format_urls(urls)[0] --> http://host:8080\n")
        print(f"format_urls(urls)[1] --> http://host\n")
        print(f"format_urls(urls)[2] --> host\n")
    return [urls_full, urls_basic, urls_raw]


def is_ip(s):
    return re.fullmatch(r'(?:\d{1,3}\.){3}\d{1,3}', s) is not None


def is_domain(s):
    return re.fullmatch(r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$', s) is not None


def format_domains(urls, message=0):
    # print(f"format_domains(urls)[0] --> http://domain:8080\n")
    # print(f"format_domains(urls)[1] --> http://domain\n")
    # print(f"format_domains(urls)[2] --> domain\n")
    domains_full = []
    domains_basic = []
    domains_raw = []

    # 确保 urls 是标准的 url
    urls = format_urls(urls)[0]
    for url in urls:
        url = url.replace("\n", "")
        if not url:
            continue
        parsed = urlparse(url)
        host = parsed.hostname
        if is_domain(host):
            domains_full.append(f"{parsed.scheme}://{host}:{parsed.port}")
            domains_basic.append(f"{parsed.scheme}://{host}")
            domains_raw.append(host)
    if message:
        print(f"format_domains(urls)[0] --> http://domain:8080\n")
        print(f"format_domains(urls)[1] --> http://domain\n")
        print(f"format_domains(urls)[2] --> domain\n")
    return [domains_full, domains_basic, domains_raw]


def format_ips(urls, message=0):
    ips_full = []
    ips_basic = []
    ips_raw = []

    urls = format_urls(urls)[0]

    for url in urls:
        url = url.replace("\n", "")
        if not url:
            continue
        parsed = urlparse(url)
        host = parsed.hostname
        if is_ip(host):
            ips_full.append(f"{parsed.scheme}://{host}:{parsed.port}")
            ips_basic.append(f"{parsed.scheme}://{host}")
            ips_raw.append(host)
    if message:
        print(f"format_ips(urls)[0] --> http://ip:8080\n")
        print(f"format_ips(urls)[1] --> http://ip\n")
        print(f"format_ips(urls)[2] --> ip\n")
    return [ips_full, ips_basic, ips_raw]
