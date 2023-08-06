# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_simdraw']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-alpha.8,<3.0.0', 'ujson>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-simdraw',
    'version': '0.1.2',
    'description': 'A phonegame draw simulator plugin for nonebot2',
    'long_description': '<h1 align="center">nonebot-plugin-simdraw</h1>\n\n## 使用方式\n\n- 方式一：\n\n发送`[gamename]抽卡（来一发）`来模拟手游抽卡（目前仅有Fgo与明日方舟卡池文件、欢迎提交其他游戏卡池文件娱乐大家~）\n\n指令后带参数`图`可以抽卡附带你们老婆们和老公们的头像\n\n- 方式二：\n\n使用以下方式调用抽卡函数\n\n```python\nnonebot.require("nonebot_plugin_simdraw").draw(times: int, game: str, noimg=True):\n    return [Messages]\n```\n\n## 配置项\n\n使用本插件需要将在bot.py同级目录下新建/cache/simdraw文件夹，并在文件夹内配置congfig.json与其他游戏卡池信息文件\n\ncongfig.json范例：\n\n```json\n{\n    "fgo": [         //游戏名\n        [0.01,5],    //[概率,类别]\n        [0.03,4],\n        [0.04,-1]\n    ],\n    "fgomsgs": [     //游戏名+msgs\n        "五星从者：", //用于生成抽卡信息\n        "四星从者：",\n        "五星礼装："\n    ],\n    "fgocards": "fgo.json" //游戏名+cards:卡池信息文件名\n}\n```\n\n游戏卡池信息文件范例：\n\n```json\n[\n    {\n        "name": "\\u5f17\\u6817\\u591a",   //角色名\n        "url": "https:\\/\\/fgo.wiki\\/images\\/3\\/3e\\/Servant300.jpg", //图片url\n        "star": 5  //类别\n    }\n]\n```\n\n本仓库内有fgo与明日方舟的卡池文件与配置文件，欢迎取用~',
    'author': 'abrahumlink',
    'author_email': '307887491@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abrahum/nonebot_plugin_simdraw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
