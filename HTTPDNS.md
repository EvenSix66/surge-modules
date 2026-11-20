# Even HTTPDNS — rebuilt

版本：2026.11.20.6。作者：EvenSix66。分类：Even Modules。

## 本次替换

移除旧 HTTPDNS 转换实现、`upstream/HTTPDNS.sgmodule`、旧提交标记及旧构建报告；构建过程不再读取旧数据。安装地址 `Surge/HTTPDNS.sgmodule` 保持不变。

新实现依据厂商公开技术资料中的服务端点事实编写，没有复制旧模块规则清单、注释、描述、图标或接口响应。我们此前接触过旧模块，因此不声称进行过严格净室开发。公开文档链接是端点事实依据，不表示文档作者为本模块背书或文档获得 MIT 许可。

当前提交移除旧内容，不会删除旧 Git 提交；历史版本的许可问题仍保留记录。此次没有重写或强制推送 Git 历史，也无法收回外部副本。

## 覆盖范围及逐条依据

| 来源 | 用途 | 规则数量 |
| --- | --- | --- |
| [阿里云官方 HTTPDNS 启动端点](https://help.aliyun.com/en/document_detail/2868011.html) | 中国大陆、香港、新加坡、美洲、欧洲的启动/调度及解析端点 | 5 个精确域名、14 个 IPv4、10 个去重后的 IPv6 |
| [腾讯云官方 HTTPDNS 接口](https://cloud.tencent.com/document/product/379/95497) | 文档公布的 HTTP 和 HTTPS 接入地址 | 2 个 IPv4 |

合计 **31 条规则**。端点清单、文档日期及 URL 在 `data/httpdns-endpoints.json`；每条规则对应的来源 ID 和清单 SHA-256 在 `httpdns-build-report.json`。官方公布的启动端点不是完整动态解析服务器集合，其他服务商及应用私有解析接口不在本版覆盖范围。

只使用精确 `DOMAIN`、IPv4 `/32` 和 IPv6 `/128`。IP 规则带 `no-resolve`，不会主动解析其他请求域名来寻找匹配。未使用宽泛关键词、整个云服务网段、User-Agent、路径猜测、远程脚本或伪造接口响应。

没有拦截腾讯公共 DNS `119.29.29.29`。腾讯[官方公告](https://cloud.tencent.com/document/product/379/56885)说明其旧 HTTPDNS 服务下线不影响同地址的公共 DNS。本版也没有把阿里云 HTTPDNS 管理 API 当作客户端解析入口。

## 使用与限制

- 无需重写或 MITM；移除旧模块中本模块曾添加的解密主机，仅需更新模块后重新载入配置。若你曾手动把旧主机写进主配置，该部分需要自行移除。
- 拒绝请求后，支持回退的应用可能改用系统 DNS；不支持回退的应用可能重试或连接失败。不能清除应用内 DNS 缓存，也不能保证接管全部 DNS、阻止所有 DoH/DoT、或提高网速。
- IP 阻断作用于列出的端点连接，并非通过查看加密内容确认请求用途；同一 IP 如被复用于其他服务，也可能受到影响。遇到异常先停用本模块，对照 Surge 请求日志定位。
- 规则基于核对日的公开资料固定生成，不会自动跟踪服务商端点变动；更新须重新核对来源。

## 重建、验证与许可

`python build_httpdns.py` 重建本模块；`python build.py` 重建 HTTPDNS 和广告模块；`python -m unittest test_build_httpdns.py test_build_ads.py` 运行检查。

MIT 许可范围：新 `Surge/HTTPDNS.sgmodule`、`build_httpdns.py`、`test_build_httpdns.py`、`data/httpdns-endpoints.json`、`httpdns-build-report.json`、此说明及新构建入口 `build.py` 中本仓库的贡献。完整文本见 [LICENSES/MIT-EvenSix66.txt](LICENSES/MIT-EvenSix66.txt)。该范围不包含广告模块及其 GPL 数据，也不为旧模块补授许可。

未在实际 iOS/macOS Surge 流量上验证回退行为。

2026-11-20：14 项 HTTPDNS/广告构建测试通过；将本模块 31 条规则组成完整测试配置提交 Surge 官方校验服务，返回 `valid: true`。
