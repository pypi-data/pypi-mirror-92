# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Cit']

package_data = \
{'': ['*']}

install_requires = \
['python-string-utils>=1.0.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.56.0,<5.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['cit = Cit.main:app']}

setup_kwargs = {
    'name': 'cit',
    'version': '0.4.1',
    'description': '让github的下载速度比之前快一千倍',
    'long_description': '## 序言\ngithub上有很多好项目,但是国内用户连github却非常的慢.每次都要用插件或者其他工具来解决.\n这次自己做一个小工具,输入github原地址后,就可以自动替换为代理地址,方便大家更快速的下载.\n\n<!-- more -->\n## 安装\n```shell\npip install cit\n```\n## 主要功能与用法\n\n### 主要功能\n* change 将目标地址转换为加速后的地址\n* clone 常见的git加速,最快10M/s,有时候慢一点\n* sub git子模块加速,等同于git submodule add\n* get 就是单纯的下载功能\n\n\n### 示例用法\n\n1. `clone`功能:等效于 `git clone <url>`\n```shell\ncit clone <url>\n# 示例\ncit clone https://github.com/solider245/cit.git\n```\n\n![20210117184201_a0bb88c0f05074e9936d59be10ee1f7f.png](https://images-1255533533.cos.ap-shanghai.myqcloud.com/20210117184201_a0bb88c0f05074e9936d59be10ee1f7f.png)\n\n如上图所示,输入一个数字,选择一个链接即可开始下载.默认使用0.\n\n2. `sub`功能:  等效于`git submodule add <url>`\n```shell \ncit sub <url>\n# 案例\ncit sub https://github.com/solider245/cit.git\n```\n逻辑和git clone一样,这里就不放图了.\n\n3. `get`功能:  等效于 `wget`下载\nget功能会根据你的输入,智能判定下载raw文件或者release文件\n使用示例:\n```shell\ncit get <url>\n# 案例\ncit get https://github.com/cheat/cheat/archive/4.2.0.zip   \n```\n\n* 下载raw文件\n![20210117195105_c1631ea82365332e2fa165f347a9bf96.png](https://images-1255533533.cos.ap-shanghai.myqcloud.com/20210117195105_c1631ea82365332e2fa165f347a9bf96.png)\n\n\n\n![20210117194012_574bf5e906eb1b18b3b9615d7e8b295d.png](https://images-1255533533.cos.ap-shanghai.myqcloud.com/20210117194012_574bf5e906eb1b18b3b9615d7e8b295d.png)\n\n下载安装包.\n![20210119184535_9e6b84fa7e79b955d6b2c8928a50ee1e.png](https://images-1255533533.cos.ap-shanghai.myqcloud.com/20210119184535_9e6b84fa7e79b955d6b2c8928a50ee1e.png)\n\n如上图所示,因为是使用https下载,所以速度快点惊人,如果下载速度太慢可以选择别的地址.我目前测试下来,基本都能用.\n\n## 其他功能\n\n- [x ] 常用软件下载,类似python,go等下载\n- [x ] 常用系统加速,类似ubuntu或者centos等加速\n- [] 其他常用功能\n\n欢迎询问或者给我[邮箱](mailto:solider245@gmail.com)发邮件.\n',
    'author': '中箭的吴起',
    'author_email': 'solider245@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/solider245/cit.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
