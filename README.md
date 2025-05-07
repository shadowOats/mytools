# mytools

一个用于简化python开发流程的工具

## 安装 git 工具

```bash
1. 安装 git 工具
2. 向 shadowOats 申请python脚本拉取权限
3. pip install git+https://github.com/shadowOats/mytools.git
```

## 安装 依赖包

```
pip install -r requirements.txt
```



## 谷歌脚本使用前提

```
将github仓库中， Releases 中的两个压缩包下载下来
```



```
1. 将 chromedriver.zip 解压出来
```

```
2. 在终端使用 py -0p, 查找你pycharm中使用的python的安装路径
3. 将解压出来的 chromedriver 复制到安装路径下
```

![image-20250506220728220](image/image-20250506220728220.png)

![image-20250506220741962](image/image-20250506220741962.png)

```
4. 将 Chrome.zip 解压出来, 通过 from mytools import * 进入 __init__.py 目录
5. 将 Chrome, 放入 __init__.py 同级目录中
```

![image-20250506221408655](image/image-20250506221408655.png)

![image-20250506221413719](image/image-20250506221413719.png)

![image-20250506221424291](image/image-20250506221424291.png)



## 备忘录

```
git add .
git commit -m "你也不想被调查吧"
git push
```



## 更新仓库

```
git status
git init
git remote add origin https://github.com/shadowOats/mytools.git
git remote -v
git pull origin main
```

