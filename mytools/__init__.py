import datetime
import os
import paramiko
import re
from urllib.parse import urlparse


def yelloStr(str): return f"\033[0;93m {str}\033[0m"


def redStr(str): return f"\033[0;91m {str}\033[0m"


def greenStr(str): return f"\033[0;92m {str}\033[0m"


def pinkStr(str): return f"\033[0;95m {str}\033[0m"


def writeFile(fileName, fileContent):
    with open(fileName, 'w', encoding='utf-8') as f:
        f.write(fileContent + "\n")
        f.close()


def appenFile(filePath, fileContent):
    # 确保父目录存在
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    with open(filePath, "a", encoding="utf-8") as f:
        if isinstance(fileContent, list):
            f.writelines(fileContent)
        else:
            f.write(fileContent + "\n")


def readFile(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        return f.readlines()


def nowTime(): return datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")


def create_ssh_client():
    """创建并返回一个SSH客户端实例"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return client


def test_ssh_connection(client, key_path, username, host, port=22):
    """使用已有的SSH客户端测试连接"""
    try:
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        client.connect(hostname=host, port=port, username=username, pkey=private_key)
        print("SSH连接成功!")
        return True
    except Exception as e:
        print(f"SSH连接失败: {str(e)}")
        return False


def format_url(url):
    url = url.strip()
    # 检测 url 是否为 http:// 或者 https:// 开头的
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    parsed = urlparse(url)
    # url = "https://test.example.com:443/page?id=123"
    # 将  url 进行切割为 对象形式, 分别存储 协议,域名,端口,路径,参数
    # scheme    https
    # netloc    test.example.com:443
    # hostname  example.com
    # port      443
    # path      /page
    # query     id=123
    # url = "https://test.example.com:443/page?id=123"
    netloc = parsed.netloc
    if ':' not in parsed.netloc:
        netloc += ':80'
    return f"{parsed.scheme}://{parsed.netloc}"

def format_urls(urls, message=0):
    urls_full = []  # http://domain/ip:port
    urls_basic = [] # http://domain/ip
    urls_raw = []   # domain/ip

    for url in urls:
        url = url.replace("\n","")
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

def format_domains(urls,message = 0):
    domains_full = []
    domains_basic = []
    domains_raw = []

    # 确保 urls 是标准的 url
    urls = format_urls(urls)[0]

    for url in urls:
        url = url.replace("\n","")
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

def format_ips(urls, message = 0):
    ips_full = []
    ips_basic = []
    ips_raw = []

    urls = format_urls(urls)[0]

    for url in urls:
        url = url.replace("\n","")
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

