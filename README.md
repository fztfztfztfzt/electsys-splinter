# 上海交大抢课插件
[![Software License](https://img.shields.io/badge/license-GPL-brightgreen.svg)](LICENSE)

## 环境
* Python 2.7

## 安装
* 安装 python2.7
* 安装 pip
* 安装 splinter
```bash
  pip install splinter
```
* 安装pytesseract
```bash
  pip install pytesseract
```
* 安装PIL
```bash
  pip install pillow
```
* 将 chromedriver.exe 复制到 [PATH TO PYTHON]/Script/

## Usage
* 打开config.ini
* user后填入你的jaccount用户名
* pass后填入你的jaccount密码的base64编码
* 在path后面填入如何进入到你需要选的课，每一个数字分别代表
* 如暑假小学期的第三门课的第一个老师，xxq=1，path=3>1，xklc=2
* 双击运行electsys.py