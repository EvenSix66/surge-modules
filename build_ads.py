# SPDX-License-Identifier: GPL-3.0-only
"""Convert conservative subsets of pinned AdGuard and AWAvenue sources.

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
    awa = ROOT / 'sources/awavenue'
    commit = (source / 'commit.txt').read_text().strip()
    dns_commit = (dns / 'commit.txt').read_text().strip()
    awa_commit = (awa / 'commit.txt').read_text().strip()
    texts = {name: (source / name).read_text(encoding='utf-8-sig') for name in SOURCES}
    exceptions = (dns / 'exceptions.txt').read_text(encoding='utf-8-sig')
    exclusions = (dns / 'exclusions.txt').read_text(encoding='utf-8-sig')
    baseline, _ = convert(texts, exceptions, exclusions)
    texts['awavenue/ads.txt'] = (awa / 'ads.txt').read_text(encoding='utf-8-sig')
    domains, report = convert(texts, exceptions, exclusions)
    report['china_enhancement'] = {
        'source': 'AWAvenue Only.Ads', 'baseline_domains': len(baseline),
        'merged_domains': len(domains),
        'new_output_domains': sorted(set(domains) - set(baseline)),
        'removed_or_superseded_domains': sorted(set(baseline) - set(domains)),
    }
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
    report['sources'].append({
        'url': f'https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/{awa_commit}/Filters/AWAvenue-Ads-Rule-Adguard-Only.Ads.txt',
        'file': 'sources/awavenue/ads.txt',
        'sha256': hashlib.sha256((awa / 'ads.txt').read_bytes()).hexdigest()})
    header = ('# SPDX-License-Identifier: GPL-3.0-only\n'
              '# Sources: AdGuard Filters / DNS filter; AWAvenue Ads Rule Only.Ads.\n'
              '# Original authors: AdGuard and contributors; TG-Twilight and AWAvenue contributors.\n'
              '# Modified by EvenSix66 on 2026-11-20: conservative domain conversion.\n'
              '# Full corresponding sources, converter and license: https://github.com/EvenSix66/surge-modules\n')
    (ROOT / 'rules/AdGuardAds.list').write_text(
        header + ''.join(f'DOMAIN-SUFFIX,{d}\n' for d in domains), encoding='utf-8', newline='\n')
    module = r'''#!name=Even AdBlock
#!desc=AdGuard 基础、移动、中文广告域名过滤，加入秋风纯广告清单增强中国应用覆盖。\n\n上游作者：AdGuard、TG-Twilight 及贡献者\n来源：github.com/AdguardTeam/AdguardFilters\n中国增强：github.com/TG-Twilight/AWAvenue-Ads-Rule（Only.Ads）\n例外来源：github.com/AdguardTeam/AdGuardSDNSFilter\n转换维护：EvenSix66 · 2026.11.20.5\n许可：GPLv3，原始清单及转换脚本随仓库提供。\n不需要 MITM；不含网页元素隐藏或视频贴片处理，不等同完整 AdGuard。\n项目：https://github.com/EvenSix66/surge-modules
#!author=AdGuard, TG-Twilight and contributors; Surge conversion by EvenSix66
#!homepage=https://github.com/EvenSix66/surge-modules
#!category=Even Modules
#!version=2026.11.20.5

# SPDX-License-Identifier: GPL-3.0-only
# Modified 2026-11-20. Derived rules: AdGuard, TG-Twilight and contributors.
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
