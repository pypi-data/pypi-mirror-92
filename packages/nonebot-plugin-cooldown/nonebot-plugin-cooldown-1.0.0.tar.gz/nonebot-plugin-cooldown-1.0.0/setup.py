# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_cooldown', 'nonebot_plugin_cooldown.extra']

package_data = \
{'': ['*']}

install_requires = \
['apscheduler>=3.7.0,<4.0.0', 'nonebot2>=2.0.0-alpha.8,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-cooldown',
    'version': '1.0.0',
    'description': 'A Cooldown Event Managing Plugin for Nonebot 2',
    'long_description': '# nonebot-plugin-cooldown\n\n适用于 Nonebot 2 的冷却事件管理插件。\n\n[![time tracker](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_cooldown.svg)](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_cooldown)\n\n> 由于本人 Python 水平低下，因此源码可能会令人不适。\n\n## 关于冷却事件\n\n冷却事件是一种用以限制用户功能调用频率的机制。在该插件中，冷却事件由事件标签所标识，每个事件包含若干个由事件记录，其中事件记录包含群组 ID、用户 ID 和事件结束时间戳三个字段，事件状态由以上字段共同决定。\n\n根据群组 ID 与用户 ID 设定的不同，该插件的冷却事件分为如下四种：\n\n- **全局冷却事件**：限制任何群组的任何成员调用功能；\n- **群组冷却事件**：限制特定群组的任何成员调用功能；\n- **一般冷却事件**：限制特定群组的特定成员调用功能；\n- **用户冷却事件**：限制特定用户调用功能。\n\n事件优先级由上至下依次递减。\n\n## 安装\n\n### 通过 `nb-cli` 安装\n\n````shell\nnb plugin install nonebot-plugin-cooldown\n````\n\n### 通过 Poetry 安装\n\n````shell\npoetry add nonebot-plugin-cooldown\n````\n\n### 通过 `pip` 安装\n\n````shell\npip install nonebot-plugin-cooldown\n````\n\n## 使用\n\n### 加载插件\n\n请参考 Nonebot 2 官方文档的 [加载插件](https://v2.nonebot.dev/guide/loading-a-plugin.html) 章节，在项目中加载该插件。\n\n### CRUD\n\n该插件提供了数种方法对冷却事件进行 CRUD 操作，可在 [该文件](nonebot_plugin_cooldown/cooldown.py) 的方法注释中查看使用方法。\n\n### 自定义匹配规则\n\n该插件提供了自定义匹配规则 `is_cooled_down`，用于判断事件生效状态。可在 [该文件](nonebot_plugin_cooldown/rule.py) 的方法注释中查看使用方法。\n\n关于如何使用匹配规则，参考 Nonebot 2 官方文档的 [自定义 rule](https://v2.nonebot.dev/guide/creating-a-matcher.html#%E8%87%AA%E5%AE%9A%E4%B9%89-rule) 章节。\n\n### 配置\n\n该插件可通过在配置文件中添加如下配置项对部分功能进行配置。关于如何设置插件配置项，参考 Nonebot 2 官方文档的 [基本配置](https://v2.nonebot.dev/guide/basic-configuration.html) 章节。\n\n- **`CD_AUTOBACKUP_PERIOD`**：自动备份事件周期（秒），默认为 `600`；\n- **`CD_AUTOREMOVE_PERIOD`**：自动移除无效事件周期（秒），默认为 `3600`。\n- **`CD_BACKUP_FILE`**：事件备份文件路径（建议在 `bot.py` 文件中使用 `pathlib` 进行配置或使用绝对路径）。\n\n## 许可协议\n\n该项目以 MIT 协议开放源代码，详阅 [LICENSE](LICENSE) 文件。\n',
    'author': 'Satoshi Jek',
    'author_email': 'jks15satoshi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
