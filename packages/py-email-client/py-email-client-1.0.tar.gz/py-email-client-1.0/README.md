# py-email-client

email client python版

[python的目录结构参考](https://marlous.github.io/2019/04/03/Python-%E8%BD%AF%E4%BB%B6%E9%A1%B9%E7%9B%AE%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84%E7%BB%84%E7%BB%87/)

python约束的目录结构如下：
```text
weibo-friends-analysis/
|-- bin/ 或 Scripts/
|   |-- ...
|
|-- src/
|   |-- tests/
|   |   |-- __init__.py
|   |   |-- test_main.py
|   |
|   |-- one/
|   |   |-- __init__.py
|   |   |-- one.py
|   |
|   |-- __init__.py
|   |-- main.py
|   |-- fun.py
|   |-- setting.py
|
|-- docs/
|   |-- abc.rst
|   |-- conf.py
|
|-- setup.py
|-- requirements.txt
|-- README
```

参考了一些python项目，可以简化为现在这样子：
```text
├── README.md
├── email_client
│   ├── __init__.py
│   └── email_client.py
├── requirements.txt
└── setup.py
```

### 创建~/.pypirc文件，用于上传包认证

### 安装setuptools用于打包和上传
>pip3 install setuptools

### 编写setup.py，用于发布仓库
```python
# coding:utf-8

from setuptools import setup

setup(
    name='py-email-client',  # 包名字
    version='1.0',  # 包版本
    description='send email_client python',  # 简单描述
    author='leonming',  # 作者
    author_email='13725911495@163.com',  # 作者邮箱
    url='https://github.com/leon-ming94/py-email-client.git',  # 包的主页
    packages=['email_client'],  # 包
    install_requires=[]
)

```

### 发布源码包
>python3 setup.py sdist upload -r pipy

### 安装包
>pip3 install monkey-email_client

### 使用方法
```python
import email_client


if __name__ == "__main__":
    
    mail_cfgs = {
                 # smtp发送邮件服务器
                 'smtp_server': 'your smtp_server',
                 # 发件人邮箱
                 'msg_from': 'your email',
                 # 发件人授权码(不是密码)
                 'password': 'your email password',
                 # 发件人格式化显示文案   效果：DataWorks对账系统 <your email>
                 'msg_from_format': 'your email format <%s>',
                 # 收件人邮箱列表
                 'msg_to': ['receiver email 1', 'receiver email 2'],
                 # 邮件主题
                 'msg_subject': 'your email subject',
                 # 邮件内容
                 'msg_content': 'your email content',
                 # 邮件附件
                 'attach_files': ['attach_file_1','attach_file_2'],
                 # 邮件发送时间
                 'msg_date': time.ctime()
                 }

    manager = email_client.create(**mail_cfgs)
    manager.send()
```

