import paramiko
from .base import *

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

def exp_ssh_connect_mul():
    ssh_client = create_ssh_client()
    key = "urls_ssh_connect/key"
    save_dir = f"urls_ssh_connect/urls_connect_ssh_{nowTime()}"
    user = "root"
    urls = readFile("urls_ssh_connect/urls.txt")
    port = "22"
    res = ""
    count = 0
    for url in urls:
        ip = only_domain(url)
        if test_ssh_connection(ssh_client, key, user, ip, port):
            count += 1
            res += f"No: {count}\n{ip}\n\n"
            print(greenStr(f"{url}成功连接ssh --> 编号: {count}\n"))
    writeFile(save_dir, res)
    if count:
        print(f"批量连接ssh成功， 一共有 {count} 个服务器可连接")
        return
    print(f"没有服务器可连接， 行不行啊， 菜狗！！")
