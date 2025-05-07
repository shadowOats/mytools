import json
import os
from .base import *

def parse_raw_to_json(raw_file_path, config, output_file_path):
    with open(raw_file_path, "r", encoding="utf-8") as f:
        raw_data = f.read().strip()

    if not raw_data:
        raw_file_path = str(raw_file_path).replace("\\","/")
        print(yellowStr(f"[!] 文件为空，跳过: {raw_file_path}"))
        return

    parts = raw_data.split("\n\n", 1)
    header_block, body = parts if len(parts) == 2 else (raw_data, "")
    lines = header_block.strip().splitlines()

    method, path, _ = lines[0].split(" ", 2)
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value

    try:
        body_json = json.loads(body.strip())
        body_data = json.dumps(body_json, ensure_ascii=False)
    except json.JSONDecodeError:
        # 如果 body 不是标准 JSON，保留原样
        body_data = body.strip()

    output_data = {
        "targetName": config.get("targetName", ""),
        "require_path": path,
        "whiteBoolean": config.get("whiteBoolean", "AND"),
        "whiteList": config.get("whiteList", []),
        "blackBoolean": config.get("blackBoolean", "AND"),
        "blackList": config.get("blackList", []),
        "threadingNum": config.get("threadingNum", 10),
        "waitTime": config.get("waitTime", 5),
        "method": method,
        "headers": headers,
        "data": body_data,
        "discript": config.get("discrip", "")
    }

    mkdir(output_file_path)
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    output_file_path = str(output_file_path).replace("\\","/")
    print(greenStr(f"[+] 已生成: {output_file_path}"))


def is_non_empty_json(file_path):
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return bool(data)
    except Exception:
        return False


def worker(raw_dir="input/poc", config_file="config/config.json", output_dir="input/poc/json"):
    mkdir(output_dir)
    if not os.path.exists(config_file):
        print(yellowStr(f"[!] 配置文件不存在: {config_file}"))
        return

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    for filename in os.listdir(raw_dir):
        if not filename.endswith(".txt"):
            continue

        raw_file_path = os.path.join(raw_dir, filename)
        json_file_name = os.path.splitext(filename)[0] + ".json"
        output_file_path = os.path.join(output_dir, json_file_name)

        if os.path.exists(output_file_path) and is_non_empty_json(output_file_path):
            output_file_path = str(output_file_path).replace("\\","/")
            print(greenStr(f"[-] {raw_dir}/{filename} 的json格式已存在且非空，存储路径为: {output_file_path}"))
            continue

        try:
            parse_raw_to_json(raw_file_path, config, output_file_path)
        except Exception as e:
            print(redStr(f"[!] 处理失败: {raw_file_path} -> {e}"))


def raw_to_json_main():
    print(f"------------------ raw_to_json 模块 ------------------")
    worker()
    worker(raw_dir="input/exp", config_file="config/config.json", output_dir="input/exp/json")
    print(f"------------------ raw_to_json 模块 ------------------")

if __name__ == '__main__':
    raw_to_json_main()
