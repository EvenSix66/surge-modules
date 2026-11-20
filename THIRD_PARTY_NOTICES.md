# 来源与许可证核对

更新日期：2026-11-20。本文件记录各文件的具体授权范围，不是对全仓库重新许可。

## 当前内容

| 范围 | 作者 / 来源 | 许可 |
| --- | --- | --- |
| 新 HTTPDNS 模块、端点清单、生成器、测试、报告及新构建入口的本仓库贡献 | EvenSix66；依据阿里云、腾讯云公开文档中的端点事实编写 | MIT，范围见 [HTTPDNS.md](HTTPDNS.md)，文本见 [LICENSES/MIT-EvenSix66.txt](LICENSES/MIT-EvenSix66.txt) |
| 当前广告模块、规则、生成器、对应测试、源清单及报告 | AdGuard、TG-Twilight 及贡献者；EvenSix66 转换 | GPLv3，具体范围、原始声明见 [ADGUARD.md](ADGUARD.md)、sources/ 和 LICENSES/ |
| Google 重定向 | EvenSix66 独立编写，参考 Surge 官方语法 | 尚未选择对外许可 |

HTTPDNS 的厂商技术文档只作为端点事实依据，没有复制全文或 SDK 实现。新实现的 MIT 许可不涵盖厂商文档，也不为历史第三方模块补授许可。此前接触过旧实现，不声称严格净室开发。Even Modules 是界面分类，不表示取得上游背书。

## 历史转换内容

早期 HTTPDNS 与广告模块来自 QingRex/LoonKissSurge 提交 `913ec005f544221e6c56a7d0ecec81c4b3b914bb`，原作者署名为可莉，HTTPDNS 另有 VirgilClyne。

- [原作者仓库 README](https://github.com/luestr/ProxyResource/blob/b7f70ce6ed207a2225851f0a2827675a3a538fe3/README.md)说明仅配置模板开源；该仓库虽有 CC BY-NC-SA 4.0 标识，但不能直接认定其涵盖两个具体模块。
- [转换来源 README](https://github.com/QingRex/LoonKissSurge/blob/913ec005f544221e6c56a7d0ecec81c4b3b914bb/README.md)不对 Surge 目录内模块主张版权，要求遵循原作者分发要求。
- 本次核对未取得旧模块具体版本的额外修改及公开分发授权证明。署名和公开下载能力不能替代授权。

2026-11-20 已先后替换两个模块，旧 `upstream/HTTPDNS.sgmodule`、`upstream/Advertisers.sgmodule`、旧源提交标记及旧报告均已从当前树移除，构建入口不再使用旧数据。旧图标和旧 MITM/重写配置也不再用于当前 HTTPDNS。

旧内容仍存在于 Git 提交历史，不能因此宣称历史分发问题已解决。本次没有重写历史或强制推送，亦不能收回已下载或 fork 的外部副本。

参考：[GitHub 仓库许可说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。没有覆盖全部文件的统一许可证，不能把某一组件的 MIT/GPL 扩展到其他组件。
