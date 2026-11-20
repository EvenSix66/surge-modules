# Even AdBlock

## 中国应用增强（2026.11.20.5）

2026-11-20 加入 [秋风广告规则](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) 的 **Only.Ads 纯广告版本**，原作者 TG-Twilight 及贡献者。固定提交为 `3b96f6337ee05400d5be302f7e9bdd5188839b82`；原文件位于 `Filters/AWAvenue-Ads-Rule-Adguard-Only.Ads.txt`，快照、README 与原许可证存放在 `sources/awavenue/`。许可为 GPLv3，来源和哈希加入构建报告，与现有衍生规则一并按本页 GPL 范围提供。

当前输出 **2,179 条**：相对原 1,697 条，新增 483 个输出域名，1 条原规则被父域覆盖而压缩，净增 482 条。例外保护共排除 32 个候选；跳过 780 条带修饰符规则及 82 条其他语法，其中秋风的 4 条通配规则不直接转成整域名阻断。

没有引入秋风完整版本的独立隐私/不受欢迎分类，也没有合并 anti-AD 或 AdRules 聚合清单。Only.Ads 是上游分类，并不保证所有域名只用于广告；若正常应用功能受影响，可先停用此模块定位。

安装地址、规则集地址和 `Even Modules` 分类保持不变；更新远程模块及外部资源即可。8 项转换测试通过，包括跨来源例外保护。增量和被替代规则明细见 `adguard-build-report.json` 的 `china_enhancement`。

本版 2,179 条域名规则组成的完整测试配置已通过 Surge 官方校验服务（`valid: true`）；未进行实际设备流量测试。

2026-11-20：替换原广告平台模块。安装 URL 仍为 `Surge/Advertisers.sgmodule`，分类为 `Even Modules`，显示名称为 `Even AdBlock`。没有使用旧广告模块的域名、IP、脚本、重写或 MITM 配置。

## 来源与许可

原作者：AdGuard 及项目贡献者；本仓库由 EvenSix66 编写转换脚本并转换为 Surge 域名规则。本项目不属于 AdGuard 官方产品，不暗示其背书。

- AdGuard Filters 固定提交：`0408f180b8d7575254162fc9911302646da2a12a`，文件分别来自 `BaseFilter/sections/adservers.txt`、`MobileFilter/sections/adservers.txt`、`ChineseFilter/sections/adservers.txt`。
- AdGuard DNS filter 固定提交：`c1fdb248eeddaddc543d7341a59c4a49dc6d0d3a`，只采用 `Filters/exceptions.txt` 和 `Filters/exclusions.txt` 作为误杀保护，不直接采用聚合后的阻断清单。
- 原始文件、上游 README（Filters）及许可分别保存在 `sources/adguard/`、`sources/adguard-dns/`。
- 可点击的固定版本 URL、SHA-256、逐域名源文件行号、跳过数量及例外排除记录保存在 `adguard-build-report.json`。

上述源清单保留上游 GPLv3 许可。本次衍生的 `Surge/Advertisers.sgmodule`、`rules/AdGuardAds.list`、`adguard-build-report.json` 以及新增 `build_ads.py`、`test_build_ads.py` 依 GPL-3.0-only 提供；完整文本为 [LICENSES/GPL-3.0.txt](LICENSES/GPL-3.0.txt)。此范围不包含 HTTPDNS 或 Google 模块，亦不为旧第三方内容补授许可。对应源文件和生成脚本均随公开仓库提供，可离线重建。修改已标注日期；无担保。

## 转换方式与限制

1. 只接受无修饰符、无路径的 `||domain^` 整域名规则，转换为 `DOMAIN-SUFFIX,domain`。域名只做小写规范化、去重及冗余子域压缩。
2. `$third-party`、`$domain`、`$popup`、脚本、元素隐藏、正则拦截等规则不会被简化成整域名阻断；跳过并计数。因此不等同完整 AdGuard，也不覆盖所有中国应用开屏广告。
3. 来源中发现的例外以及 DNS 官方例外、排除表用于移除冲突的阻断规则。带路径、条件或通配符的例外会保守扩大成域名保护；无法理解的域名例外使构建失败，不会默默忽略。IP 前缀排除不适用于不接受 IP 的候选集，会单独记录。
4. 若例外子域与父域阻断冲突，删除整个父域阻断；因此部分广告也会被放行，以避免扩大误杀。不会生成 DIRECT 例外去覆盖用户原有的代理分流。
5. 不使用 `extended-matching` 或 `pre-matching`，也不生成 MITM、URL 重写、远程脚本。它按请求主机名过滤，不保证发现 DNS CNAME 后的追踪目标。
6. 模块引用仓库的外部规则集，默认缓存更新间隔 86400 秒。该间隔只更新仓库产物；本次没有设置自动拉取上游的定时任务。

## 首版结果与检查（2026.11.20.4）

输出 1,697 条域名；排除 24 个有例外冲突的候选；跳过 780 条带修饰符规则和 78 条其他语法。报告还记录了 8 个不适用的 IP 前缀排除。

运行 `python -m unittest test_build_ads.py` 验证语义边界；运行 `python build_ads.py` 只重建新版广告模块，或 `python build.py` 重建广告和历史 HTTPDNS 模块。输入快照固定，构建不请求网络。

2026-11-20 已将生成的 1,697 条规则内联到不含个人信息的完整测试配置，提交 Surge 官方配置校验服务，返回 `valid: true`。这验证的是规则语法，不代表真实流量去广告效果，也不验证远程规则集下载是否成功。

安装者更新原远程模块即可。需要同时保证外部规则集下载成功；若列表缓存未更新，请在 Surge 中刷新外部资源。未在实际 iOS/macOS Surge 流量上验证拦截效果。

官方语法参考：[AdGuard DNS 语法](https://adguard-dns.io/kb/general/dns-filtering-syntax/)、[Surge 规则集](https://manual.nssurge.com/rules/ruleset.html)。
