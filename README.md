# Surge Modules

> 许可证核对：HTTPDNS 和广告平台模块的修改、公开再分发授权尚未确认；上游的 CC BY-NC-SA 4.0 标识不能直接视为涵盖这些模块。本仓库没有统一开源许可证。逐文件来源、范围与待办见 [来源与许可证核对](THIRD_PARTY_NOTICES.md)。

个人 Surge 模块仓库。首批包含 HTTPDNS 拦截器和广告平台拦截器。

本仓库模块在 Surge 中统一归类为 `Even Modules`。模块名称使用功能名称；原作者、原项目和转换来源保留在说明和源码备注中，分类不代表原作者署名。Google 重定向为独立编写，注明作者及官方语法来源。

## 来源与当前范围

原作者：可莉，以及 HTTPDNS 模块署名的 VirgilClyne。保留模块内原始署名、图标、主页和日期。

- 原项目索引：https://github.com/luestr/ProxyResource
- 插件中心：https://hub.kelee.one/
- 转换来源：https://github.com/QingRex/LoonKissSurge
- 使用的转换来源提交见 `upstream/commit.txt`，原始转换产物及 SHA-256 分别保存在 `upstream/` 和 `build-report.json`。

官网目前提供 `Block_HTTPDNS.lpx`、`BlockAdvertisers.lpx`；本次下载被站点拒绝，未获得官网当前源文件。因此这里是基于固定版本的 **已有 Surge 转换产物继续适配**，不是重新从最新 Loon 源码完整转换，也不声称与官网当前版本一致。HTTPDNS 上游标注日期为 2026-03-01，广告平台为 2026-03-03。

## 文件与使用

| 模块 | 文件 | 作用 |
| --- | --- | --- |
| HTTPDNS 拦截器 | [HTTPDNS.sgmodule](Surge/HTTPDNS.sgmodule) | 拒绝常见 HTTPDNS 请求，促使支持回退的应用使用正常 DNS |
| 广告平台拦截器 | [Advertisers.sgmodule](Surge/Advertisers.sgmodule) | 拦截广告平台域名及部分广告资源，配合应用专项模块 |
| Google 搜索重定向 | [GoogleRedirect.sgmodule](Surge/GoogleRedirect.sgmodule) | 将 Google 中国搜索域名跳转至 www.google.com，保留路径及搜索参数 |

仓库公开，可以在 Surge 中通过以下直链添加远程模块：

- HTTPDNS：https://raw.githubusercontent.com/EvenSix66/surge-modules/main/Surge/HTTPDNS.sgmodule
- 广告平台：https://raw.githubusercontent.com/EvenSix66/surge-modules/main/Surge/Advertisers.sgmodule
- Google 重定向：https://raw.githubusercontent.com/EvenSix66/surge-modules/main/Surge/GoogleRedirect.sgmodule

Google 重定向为独立编写的模块，遵照 Surge 官方 URL Rewrite 语法，使用 307 和 `$1` 保留路径及参数，仅匹配 google.cn / g.cn 及各自的 www 域名。它不修改浏览器默认搜索引擎设置；需禁用重复的 Google 重定向模块。HTTPS 重定向需要重写与 MITM 生效，且请求经过 Surge。若浏览器允许自定义搜索引擎，也可直接将搜索模板设为 `https://www.google.com/search?q=%s`（占位符以浏览器要求为准），避免先请求 .cn。

使用当前稳定版 Surge。规则中包含 `pre-matching`（官方注明 iOS 5.14.0+ / Mac 5.9.0+）；HTTPDNS 模块还包含内联 Map Local。将广告平台模块置于模块列表靠前位置，具体优先级以 Surge 合并后的配置为准。两个模块并不替代各应用专项规则。

HTTPS URL 重写和 Map Local 需要启用重写、MITM，并在设备信任 Surge 的 MITM 证书；普通域名/IP 拦截不依赖 HTTPS 解密。导入不会自动创建或信任证书。

## 本次适配

模块头遵循 [Surge 官方模块说明](https://manual.nssurge.com/profile/module.html)：文件以连续的 `#!` 元数据开始，`#!name`、`#!desc` 位于最前，普通来源注释放到元数据之后。版本 2026.11.20.2 将作者、适配版本、上游日期及使用条件写入 `#!desc`，方便在模块说明中查看。`author`、`homepage`、`version` 等额外字段供参考，官方并未保证在所有客户端界面单独展示。已有安装请手动更新远程模块；本地导入需重新下载。

1. 移除仅适用于 Loon 的 `#!loon_version` 元数据；保留全部请求规则及其顺序，包括上游 DIRECT 例外。
2. 将 HTTPDNS 描述改为 Surge 语境。
3. 补齐 HTTPDNS HTTPS 规则所需的 MITM 主机：虎牙、喜马拉雅，以及 UC 正则覆盖的 `ucdc-upaas` 与 `ucdc0` 至 `ucdc9-upaas`。未添加整个父域的通配解密。
4. 不增加远程脚本，不设置自动更新任务。
5. 将上游非规范网段 `118.89.204.198/23` 规范为 `118.89.204.0/23`，保持 CIDR 实际覆盖范围；构建检查对全部 IP 网段做严格校验。

HTTPDNS 拒绝后能否回退取决于应用；某些应用可能出现重试或网络异常。上游广告列表同时含统计、推送和配置域名，出现功能异常时先停用相关模块并查看 Surge 请求日志。

## 验证与重建

运行 `python build.py`，从本地固定快照重建模块，并校验规则保留、章节、IPv4/IPv6 网段、正则表达式和 Map Local 空 JSON 响应配置。

这些是静态检查；未在真实 Surge 引擎或 iOS/Mac 设备导入运行，不能替代实际兼容性与去广告效果测试。

参考：[Surge 规则](https://manual.nssurge.com/rules/overview.html)、[预匹配](https://manual.nssurge.com/policies/reject.html)、[Map Local](https://manual.nssurge.com/http/map-local.html)。

## 权利说明

原始模块及规则的权利属于各自作者，本仓库不将其重新许可。上游网站声明限制修改和公开分发，索引仓库也说明仅配置模板开源。本仓库公开不代表已取得原作者额外授权。转换来源仓库也不主张拥有模块版权。

截至 2026-11-20，尚未取得两个基础模块具体版本的公开再分发授权证明。保留署名和来源属于来源记录，不等于授权已齐备。独立编写的 Google 模块及构建脚本尚未选择对外许可证；没有为全仓库擅自套用上游的 CC 许可。详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
