from setuptools import setup, find_packages

setup(
    name='mytools',
    version='0.2.0',
    description='My personal tools',
    author='Oats',
    author_email='1008611@qq.com',
    packages=find_packages(),  # 自动找到 mytools 包
    python_requires='>=3.6',
    install_requires=[],
)
