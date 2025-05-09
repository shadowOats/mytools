import datetime
import os
import json


def yellowStr(str): return f"\033[0;93m{str}\033[0m"


def redStr(str): return f"\033[0;91m{str}\033[0m"


def greenStr(str): return f"\033[0;92m{str}\033[0m"


def pinkStr(str): return f"\033[0;95m{str}\033[0m"


def mkdir(path):
    # 如果是文件路径（包含文件名），取上级目录；如果是目录路径，直接创建
    dir_path = path if path.endswith(("/", "\\")) or "." not in os.path.basename(path) else os.path.dirname(path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def appenFile(filePath, fileContent):
    dir_path = os.path.dirname(filePath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(filePath, "a", encoding="utf-8") as f:
        if isinstance(fileContent, list):
            f.writelines(fileContent)
        else:
            f.write(fileContent + "\n")


def writeFile(filePath, fileContent):
    dir_path = os.path.dirname(filePath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(filePath, 'w', encoding='utf-8') as f:
        if isinstance(fileContent, list):
            # 如果是列表，逐行写入，每项自动添加换行符
            f.writelines([str(line).rstrip() + "\n" for line in fileContent])
            # print(f"列表类型数据保存成功, 保存路径为: {filePath}")
        else:
            # 如果是字符串，直接写
            f.write(str(fileContent) + "\n")
            # print(f"字符串类型数据保存成功, 保存路径为: {filePath}")


def readFile(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        return f.readlines()


def nowTime(): return datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")


# 获取包路径下的文件内容
def read_pack_file(path):
    # 获取当前脚本所在目录（不是运行目录）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, path)
