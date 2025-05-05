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
