import importlib
import subprocess
import sys
import pkg_resources
from mytools.base import *


def check_and_upgrade_package(package_name, required_version):
    try:
        installed_version = pkg_resources.get_distribution(package_name).version
        print(f"✔️ 已安装: {package_name}=={installed_version}")
        if pkg_resources.parse_version(installed_version) < pkg_resources.parse_version(required_version):
            print(f"⚠️  {package_name} 版本过低 (当前: {installed_version}, 要求: {required_version})")
            return True
        return False
    except pkg_resources.DistributionNotFound:
        print(f"❌ 未安装: {package_name}")
        return True


def install_or_upgrade(package):
    print(f"正在安装/升级 {package} ...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", package],
            check=True
        )
        print(f"✅ 成功安装/升级 {package}")
    except subprocess.CalledProcessError:
        print(f"❌ 安装失败: {package}")
        print("💡 请检查网络连接或开启 tun 模式的小猫咪（VPN）后重试")


def read_requirements():
    lines = readFile(read_pack_file("requirements.txt"))
    packages = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if '==' in line:
            name, version = line.split('==')
            packages[name.strip()] = version.strip()
        else:
            packages[line] = "0.0.0"  # 最低版本
    return packages


def pre_env_main():
    packages = read_requirements()
    to_upgrade = []

    for pkg, ver in packages.items():
        if check_and_upgrade_package(pkg, ver):
            to_upgrade.append(f"{pkg}=={ver}" if ver != "0.0.0" else pkg)

    if to_upgrade:
        print("\n以下模块需要安装/升级：")
        for p in to_upgrade:
            print(f" - {p}")
        consent = input("\n是否执行安装/升级？请输入 yes 确认（其他内容将取消操作）: ").strip().lower()
        if consent == 'yes':
            for p in to_upgrade:
                install_or_upgrade(p)
        else:
            print(f"❌ 用户取消了组件升级，程序无法继续运行。\n")
            sys.exit(1)
    else:
        print(f"🎉 所有依赖项已满足，可继续执行程序。\n")


if __name__ == "__main__":
    pre_env_main()
