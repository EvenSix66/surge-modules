# 来源与许可证核对

核对日期：2026-11-20。本文件记录来源和发现，不构成授权书，也不授予第三方内容的新许可。

## 后续替换：Even AdBlock

2026-11-20 已将当前 `Surge/Advertisers.sgmodule` 替换为基于 AdGuard 官方清单生成的 Even AdBlock。新版规则、脚本、源文件和 GPLv3 许可范围详见 [ADGUARD.md](ADGUARD.md) 及 [LICENSES/GPL-3.0.txt](LICENSES/GPL-3.0.txt)。旧 `upstream/Advertisers.sgmodule` 已从最新树移除；旧数据仍存在于 Git 历史，下面涉及旧广告模块的结论作为历史记录保留。HTTPDNS 的授权问题尚未解决。Google 模块许可状态不变。

## 文件范围

以下表格为替换前的核对记录；当前广告模块以本页“后续替换”和 ADGUARD.md 为准。

| 文件 | 来源 / 作者 | 本次核对结论 |
| --- | --- | --- |
| `Surge/HTTPDNS.sgmodule` | 可莉、VirgilClyne；经 QingRex/LoonKissSurge 转换 | 原模块再分发及修改授权未确认，不能仅凭索引仓库的 CC 标识认定获准 |
| `Surge/Advertisers.sgmodule` | 可莉；经 QingRex/LoonKissSurge 转换 | 同上 |
| `upstream/HTTPDNS.sgmodule`、`upstream/Advertisers.sgmodule` | 转换仓库固定提交中的原始快照 | 与衍生模块相同，也需要核对复制、分发授权 |
| 上述两模块的远程图标 | `luestr/IconResource` 的链接 | 未复制图像文件；图像自身许可尚未核对，不纳入本仓库许可 |
| `Surge/GoogleRedirect.sgmodule` | 本仓库独立编写；参考 Surge 官方语法文档 | 未复制前述两个第三方模块；仓库所有者尚未选择对外许可 |
| `build.py`、本仓库新增说明文档 | 本仓库新增实现及说明 | 未复制 LoonKissSurge 的 `build.ts` 或 Script-Hub 实现；尚未选择对外许可 |

`Even Modules` 是界面分类，不是版权归属或许可证标识。模块中的原作者署名、主页、图标地址与上游日期继续保留；本仓库所作修改见 README 的适配记录及 Git 历史。

## 原作者项目：luestr/ProxyResource

核对提交：[`b7f70ce6ed207a2225851f0a2827675a3a538fe3`](https://github.com/luestr/ProxyResource/tree/b7f70ce6ed207a2225851f0a2827675a3a538fe3)。

- [LICENSE](https://github.com/luestr/ProxyResource/blob/b7f70ce6ed207a2225851f0a2827675a3a538fe3/LICENSE) 为 CC BY-NC-SA 4.0。
- [README](https://github.com/luestr/ProxyResource/blob/b7f70ce6ed207a2225851f0a2827675a3a538fe3/README.md) 限定仓库只是索引、仅配置模板开源，并另列学习研究、非商业及传播等使用声明。
- [插件中心](https://hub.kelee.one/) 在本次查看时声明限制爬取、二次修改和公开分发。

因此，当前证据不足以将配置模板的 CC 许可直接扩展到上述两个模块。也没有核验到这两个具体源版本曾获有效 CC 授权的历史证据。若找到早期明确适用的授权，应按该授权范围另行审查；不能仅凭目前的限制声明推断历史授权已被撤回。

对确实适用 CC BY-NC-SA 4.0 的材料，应保留适当署名、许可证链接和修改说明，遵守非商业及相同方式共享条件。其条件不能替代确认作品是否在许可范围内。参考：[CC 官方摘要](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)、[法律文本](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)。本仓库未将该许可作为两个模块已获授权的证明。

## 转换来源：QingRex/LoonKissSurge

固定源提交：[`913ec005f544221e6c56a7d0ecec81c4b3b914bb`](https://github.com/QingRex/LoonKissSurge/tree/913ec005f544221e6c56a7d0ecec81c4b3b914bb)。源内容哈希见 `build-report.json`。

- [README](https://github.com/QingRex/LoonKissSurge/blob/913ec005f544221e6c56a7d0ecec81c4b3b914bb/README.md) 对 Surge 文件夹内模块不主张著作权，要求依原作者要求分发。
- README 提到的网站构建代码授权只涉及其相应代码，不能作为 Surge 模块的授权。
- 本仓库没有复制其 `build.ts`，也没有复制或运行 Script-Hub 源码；因此不能把工具的许可证直接套到本仓库模块上。
- GitHub 可访问、可以下载以及存在转换版本，均不足以独立证明原模块允许修改和再分发。

## 本仓库当前状态与待办

核对时仓库公开，根目录没有统一 LICENSE。未为整个仓库添加 MIT、CC 或其他统一授权，避免误授第三方内容权利。独立内容也尚未选择许可；公开可查看不等于已作一般开源授权。参考：[GitHub 许可证说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。

需要补齐的证据：两个模块具体版本的修改和公开再分发授权，或明确适用于这些版本的已有许可证。拿到证据后，应记录授权人、日期、范围、原始链接及证明，并按要求附带许可文本。

在此之前，建议暂停上述两个模块及其快照的公开分发，选择改为私有，或移除这部分内容。仅在最新提交移除文件并不能清除公开 Git 历史，也不能收回已经下载或 fork 的副本。仓库可见性、移除文件及重写历史须由仓库所有者决定，本次核对没有执行这些操作。
