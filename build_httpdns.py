# SPDX-License-Identifier: MIT
# Copyright (c) 2026 EvenSix66
"""Generate precise HTTPDNS endpoint rules from vendor technical facts."""
import hashlib
import ipaddress
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data/httpdns-endpoints.json'


def render(manifest):
    entries = {}
    counts = {'DOMAIN': 0, 'IP-CIDR': 0, 'IP-CIDR6': 0}
    for source in manifest['sources']:
        assert source['url'].startswith('https://')
        for domain in source['domains']:
            assert re.fullmatch(r'[a-z0-9-]+(?:\.[a-z0-9-]+)+', domain), domain
            entries.setdefault(('DOMAIN', domain), []).append(source['id'])
        for key, version, kind in [('ipv4', 4, 'IP-CIDR'), ('ipv6', 6, 'IP-CIDR6')]:
            for value in source[key]:
                address = ipaddress.ip_address(value)
                assert address.version == version and address.is_global, value
                cidr = str(ipaddress.ip_network(f'{address}/{address.max_prefixlen}'))
                entries.setdefault((kind, cidr), []).append(source['id'])
    header = r'''#!name=Even HTTPDNS
#!desc=精确拦截阿里云和腾讯云官方公开的 HTTPDNS 接入端点。\n\n作者：EvenSix66 · 2026.11.20.6\n依据：服务商官方技术文档，逐条来源见仓库 HTTPDNS.md。\n无需 MITM；不含关键字匹配、伪造响应或第三方模块规则。\n仅覆盖已列端点，无法清除应用缓存或保证应用回退；异常时停用。\n许可：MIT（本仓库新实现）。\n项目：https://github.com/EvenSix66/surge-modules
#!author=EvenSix66
#!homepage=https://github.com/EvenSix66/surge-modules/blob/main/HTTPDNS.md
#!category=Even Modules
#!version=2026.11.20.6

# SPDX-License-Identifier: MIT
# Copyright (c) 2026 EvenSix66. See LICENSES/MIT-EvenSix66.txt.
# New implementation based on vendor endpoint facts, not the prior converted module.
# Alibaba Cloud: https://help.aliyun.com/en/document_detail/2868011.html
# Tencent Cloud: https://cloud.tencent.com/document/product/379/95497
[Rule]
'''
    lines, evidence = [], []
    for (kind, target), sources in sorted(entries.items()):
        counts[kind] += 1
        line = f'{kind},{target},REJECT'
        if kind != 'DOMAIN':
            line += ',no-resolve'
        lines.append(line)
        evidence.append({'rule': line, 'sources': sorted(set(sources))})
    return header + '\n'.join(lines) + '\n', {'counts': counts, 'rules': evidence}


def main():
    manifest = json.loads(DATA.read_text(encoding='utf-8'))
    module, report = render(manifest)
    assert sum(report['counts'].values()) > 0
    report['checked_on'] = manifest['checked_on']
    report['manifest_sha256'] = hashlib.sha256(DATA.read_bytes()).hexdigest()
    report['source_documents'] = manifest['sources']
    (ROOT / 'Surge/HTTPDNS.sgmodule').write_text(module, encoding='utf-8', newline='\n')
    (ROOT / 'httpdns-build-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'HTTPDNS rebuilt: {report["counts"]}')


if __name__ == '__main__':
    main()
