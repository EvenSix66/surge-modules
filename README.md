# Even Modules

个人 Surge 模块仓库。模块分类统一为 **Even Modules**，各自保留作者、来源和许可说明。

| 模块 | 文件 | 作用 / 许可 |
| --- | --- | --- |
| Even HTTPDNS | [HTTPDNS.sgmodule](Surge/HTTPDNS.sgmodule) | 根据阿里云、腾讯云官方端点事实重新实现，31 条精确规则，无需 MITM；新实现 MIT |
| Even AdBlock | [Advertisers.sgmodule](Surge/Advertisers.sgmodule) | AdGuard 官方清单 + 秋风 Only.Ads，2,179 条域名过滤，无需 MITM；GPLv3 |
| Google 搜索重定向 | [GoogleRedirect.sgmodule](Surge/GoogleRedirect.sgmodule) | google.cn / g.cn 跳转至 www.google.com，保留路径和搜索词；独立编写，尚未选择对外许可 |

## 安装与更新

在 Surge 中通过以下地址安装远程模块；已有安装更新原地址即可：

- HTTPDNS：https://raw.githubusercontent.com/EvenSix66/surge-modules/main/Surge/HTTPDNS.sgmodule
- 广告过滤：https://raw.githubusercontent.com/EvenSix66/surge-modules/main/Surge/Advertisers.sgmodule
- Google 重定向：https://raw.githubusercontent.com/EvenSix66/surge-modules/main/Surge/GoogleRedirect.sgmodule

Even AdBlock 还需要下载外部规则集，更新后可刷新 Surge 外部资源。当前广告模块版本 2026.11.20.5，HTTPDNS 新实现版本 2026.11.20.6。

Google 的 HTTPS 重定向需要开启重写与 MITM，并信任 Surge 证书。当前 HTTPDNS、广告模块均无需 MITM。Google 模块不修改浏览器的默认搜索引擎设置。

## 实现与来源

- [HTTPDNS.md](HTTPDNS.md)：新版覆盖范围、逐条来源、限制和 MIT 许可范围。旧转换实现、上游快照及旧构建逻辑已从当前树移除。
- [ADGUARD.md](ADGUARD.md)：AdGuard 与秋风固定来源、例外保护、转换限制和 GPLv3 范围。它不等同完整 AdGuard，不支持网页元素隐藏或视频贴片处理。
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)：当前文件许可范围及历史来源核对。

模块名称和分类不代表上游作者对本项目的认可。HTTPDNS 并非广告黑名单；阻断后能否回退取决于应用，异常时先停用对应模块排查。

## 重建与检查

运行 `python build.py`，从仓库内固定清单重建 HTTPDNS 和广告模块；构建不请求网络。单独重建可运行 `python build_httpdns.py` 或 `python build_ads.py`。

运行 `python -m unittest test_build_httpdns.py test_build_ads.py`。源清单与构建报告记录端点依据、固定提交、哈希及转换统计。语法检查不能替代实际设备上的功能测试。

本仓库为不同许可内容的集合，没有覆盖所有文件的统一许可。许可按具体文件范围适用。删除当前文件不会清除 Git 历史；此前旧 HTTPDNS 和广告平台转换产物的许可问题仍见历史核对记录。
