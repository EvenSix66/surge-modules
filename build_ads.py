# SPDX-License-Identifier: GPL-3.0-only
"""Convert a conservative subset of pinned AdGuard sources to Surge domains.

Copyright (C) 2026 EvenSix66. See LICENSES/GPL-3.0.txt.
No LoonKissSurge/iKelee rule data is used by this converter.
"""
import hashlib
import ipaddress
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'base.txt': 'BaseFilter/sections/adservers.txt',
    'mobile.txt': 'MobileFilter/sections/adservers.txt',
    'chinese.txt': 'ChineseFilter/sections/adservers.txt',
}
DOMAIN = r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?'
BLOCK = re.compile(r'\|\|(' + DOMAIN + r')\^', re.I)


def domain_valid(value):
    if len(value) > 253 or not re.fullmatch(DOMAIN, value, re.I):
        return False
    try:
        ipaddress.ip_address(value)
        return False
    except ValueError:
        return True


def exception_domain(line):
    """Deliberately widen path/conditional exceptions to domain safeguards."""
    text = line.removeprefix('@@').lstrip('|')
    host = re.split(r'[\^/$|]', text, maxsplit=1)[0].lower()
    if '*' in host:
        # Widen wildcard exceptions to their fixed suffix, never to a block.
        host = host.split('*')[-1].lstrip('.')
    if host.startswith('-'):
        host = host.split('.', 1)[1]
    if not domain_valid(host):
        raise ValueError(f'Unrecognized exception; stop instead of dropping it: {line}')
    return host


def overlap(a, b):
    return a == b or a.endswith('.' + b) or b.endswith('.' + a)


def convert(texts, exception_text, exclusion_text):
    domains, safeguards, exclusions = set(), set(), []
    skipped, provenance = Counter(), {}
    for name, text in texts.items():
        for number, raw in enumerate(text.splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith(('!', '#')):
                continue
            if line.startswith('@@'):
                safeguards.add(exception_domain(line))
                continue
            match = BLOCK.fullmatch(line)
            if match and domain_valid(match[1]):
                domain = match[1].lower()
                domains.add(domain)
                provenance.setdefault(domain, []).append(f'{name}:{number}')
            else:
                skipped['conditional' if '$' in line else 'other_syntax'] += 1
    for raw in exception_text.splitlines():
        line = raw.strip()
        if line and not line.startswith(('!', '#')):
            if not line.startswith('@@'):
                raise ValueError(f'Unexpected allow rule: {line}')
            safeguards.add(exception_domain(line))
    for raw in exclusion_text.splitlines():
        line = raw.strip()
        if not line or line.startswith(('!', '#')):
            continue
        if line.startswith('/'):
            exclusions.append(re.compile(line[1:-1] if line.endswith('/') else line[1:]))
        elif re.fullmatch(r'\|\|[0-9.]+', line):
            # IP-prefix exclusions cannot intersect our hostname-only candidates.
            skipped['ip_exclusion_not_applicable'] += 1
        else:
            safeguards.add(exception_domain(line))
    removed = {}
    for domain in sorted(domains):
        guards = [item for item in safeguards if overlap(domain, item)]
        if guards or any(pattern.search(value) for pattern in exclusions
                         for value in (domain, '.' + domain + '^', '||' + domain + '^')):
            removed[domain] = sorted(guards) or ['exclusion_regex']
    domains.difference_update(removed)
    # Remove redundant child blocks only after all safeguards were applied.
    kept = []
    for domain in sorted(domains, key=lambda x: (x.count('.'), x)):
        if not any('.'.join(domain.split('.')[i:]) in domains
                   for i in range(1, len(domain.split('.')))):
            kept.append(domain)
    return sorted(kept), {
        'candidates': len(provenance), 'skipped': dict(skipped),
        'safeguard_domains': len(safeguards), 'safeguard_regexes': len(exclusions),
        'removed_for_safety': removed, 'output_domains': len(kept),
        'provenance': {d: provenance[d] for d in sorted(kept)},
    }


def main():
    source = ROOT / 'sources/adguard'
    dns = ROOT / 'sources/adguard-dns'
    commit = (source / 'commit.txt').read_text().strip()
    dns_commit = (dns / 'commit.txt').read_text().strip()
    domains, report = convert(
        {name: (source / name).read_text(encoding='utf-8-sig') for name in SOURCES},
        (dns / 'exceptions.txt').read_text(encoding='utf-8-sig'),
        (dns / 'exclusions.txt').read_text(encoding='utf-8-sig'))
    assert len(domains) > 100, 'Unexpectedly empty source or conversion result'
    report['sources'] = [
        {'url': f'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/{commit}/{path}',
         'file': f'sources/adguard/{name}',
         'sha256': hashlib.sha256((source / name).read_bytes()).hexdigest()}
        for name, path in SOURCES.items()]
    report['sources'] += [
        {'url': f'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/{dns_commit}/Filters/{name}',
         'file': f'sources/adguard-dns/{name}',
         'sha256': hashlib.sha256((dns / name).read_bytes()).hexdigest()}
        for name in ('exceptions.txt', 'exclusions.txt')]
    report['license'] = 'GPL-3.0-only'
    header = ('# SPDX-License-Identifier: GPL-3.0-only\n'
              '# Source: AdGuard Filters / AdGuard DNS filter, AdGuard and contributors.\n'
              '# Modified by EvenSix66 on 2026-11-20: conservative domain conversion.\n'
              '# Full corresponding sources, converter and license: https://github.com/EvenSix66/surge-modules\n')
    (ROOT / 'rules/AdGuardAds.list').write_text(
        header + ''.join(f'DOMAIN-SUFFIX,{d}\n' for d in domains), encoding='utf-8', newline='\n')
    module = r'''#!name=Even AdBlock
#!desc=基于 AdGuard 官方基础、移动及中文广告清单的保守域名过滤。\n\n上游作者：AdGuard 及贡献者\n来源：github.com/AdguardTeam/AdguardFilters\n例外来源：github.com/AdguardTeam/AdGuardSDNSFilter\n转换维护：EvenSix66 · 2026.11.20.4\n许可：GPLv3，源码及转换脚本随仓库提供。\n不需要 MITM；不包含网页元素隐藏或视频贴片处理；不等同完整 AdGuard。\n项目：https://github.com/EvenSix66/surge-modules
#!author=AdGuard and contributors; Surge conversion by EvenSix66
#!homepage=https://github.com/EvenSix66/surge-modules
#!category=Even Modules
#!version=2026.11.20.4

# SPDX-License-Identifier: GPL-3.0-only
# Modified 2026-11-20. Derived rules: AdGuard and contributors.
# Corresponding source, changes and full license: repository sources/, build_ads.py, LICENSES/.
# Original Advertisers.sgmodule was replaced; no old module rules are used here.
[Rule]
RULE-SET,https://raw.githubusercontent.com/EvenSix66/surge-modules/main/rules/AdGuardAds.list,REJECT,update-interval=86400
'''
    (ROOT / 'Surge/Advertisers.sgmodule').write_text(module, encoding='utf-8', newline='\n')
    (ROOT / 'adguard-build-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'AdGuard: {len(domains)} domains, {len(report["removed_for_safety"])} safeguards removed, skipped {report["skipped"]}')


if __name__ == '__main__':
    main()
