# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baidupcs_py',
 'baidupcs_py.app',
 'baidupcs_py.baidupcs',
 'baidupcs_py.commands',
 'baidupcs_py.common']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<9.0.0',
 'aget>=0.1.17,<0.2.0',
 'chardet>=4.0.0,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.8.0,<10.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['BaiduPCS-Py = baidupcs_py.app:main']}

setup_kwargs = {
    'name': 'baidupcs-py',
    'version': '0.3.6',
    'description': 'Baidu Pcs App',
    'long_description': '# BaiduPCS-Py\n\n[![PyPI version](https://badge.fury.io/py/baidupcs-py.svg)](https://badge.fury.io/py/baidupcs-py)\n![Build](https://github.com/PeterDing/BaiduPCS-Py/workflows/BaiduPCS-Py%20Build%20&%20Test/badge.svg)\n\nA BaiduPCS API and An App\n\nBaiduPCS-Py 是百度网盘 pcs 的非官方 api 和一个命令行运用程序。\n\n> 也是 https://github.com/PeterDing/iScript/blob/master/pan.baidu.com.py 的重构版。\n\n## 安装\n\n需要 Python 版本大于或等于 3.6\n\n```\npip3 install BaiduPCS-Py\n```\n\n## 用法\n\n```\nBaiduPCS-Py --help\n```\n\n## 添加用户\n\nBaiduPCS-Py 目前不支持用帐号登录。需要使用者在 pan.baidu.com 登录后获取 cookies 和其中的 bduss 值，并用命令 `useradd` 为 BaiduPCS-Py 添加一个用户。\n\n使用者可以用下面的方式获取用户的 cookies 和 bduss 值。\n\n1. 登录 pan.baidu.com\n2. 打开浏览器的开发者工具(如 Chrome DevTools)。\n3. 然后选择开发者工具的 Network 面板。\n4. 在登录后的页面中任意点开一个文件夹。\n5. 在 Network 面板中找到 `list?....` 一行，然后在右侧的 Headers 部分找到 `Cookie:` 所在行，复制 `Cookie:` 后的所有内容作为 cookies 值，其中的 `BDUSS=...;` 的 `...` (没有最后的字符;)作为 bduss 值。\n\n![cookies](./imgs/cookies.png)\n\n现在找到了 cookies 和 bduss 值，我们可以用下面的命令添加一个用户。\n\n交互添加：\n\n```\nBaiduPCS-Py useradd\n```\n\n或者直接添加:\n\n```\nBaiduPCS-Py useradd --cookies "cookies 值" --bduss "bduss 值"\n```\n',
    'author': 'PeterDing',
    'author_email': 'dfhayst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PeterDing/BaiduPCS-Py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
