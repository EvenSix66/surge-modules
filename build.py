"""Reproducible Surge adaptation of pinned, already-converted source modules."""
import csv
import hashlib
import ipaddress
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMIT = (ROOT / 'upstream/commit.txt').read_text().strip()
REPORT = {}
for name in ('HTTPDNS', 'Advertisers'):
    source = ROOT / f'upstream/{name}.sgmodule'
    original = source.read_text(encoding='utf-8-sig')
    output = []
    section = None
    counts = Counter()
    for line in original.splitlines():
        if line.startswith('#!loon_version='):
            continue
        if line.startswith('#!desc='):
            if name == 'HTTPDNS':
                desc = '拦截常见 HTTPDNS 服务，促使支持回退的应用使用系统/Surge DNS。'
                authors = '可莉、VirgilClyne'
                source_date = '2026-03-01'
            else:
                desc = '拦截常见广告平台请求，需搭配应用专项去广告模块；建议置于模块列表靠前位置。'
                authors = '可莉'
                source_date = '2026-03-03'
            line = ('#!desc=' + desc + r'\n\n原作者：' + authors
                    + r'\nSurge 适配：EvenSix66 · 2026.11.20.2'
                    + r'\n上游版本日期：' + source_date
                    + r'\nHTTPS 重写需启用重写与 MITM，并信任证书。'
                    + r'\n项目：https://github.com/EvenSix66/surge-modules')
        if line.startswith(('IP-CIDR,', 'IP-CIDR6,')):
            fields = line.split(',')
            fields[1] = str(ipaddress.ip_network(fields[1], strict=False))
            line = ','.join(fields)
        if line.startswith('['):
            section = line.strip('[]')
        elif line and not line.startswith('#'):
            counts[section] += 1
        if name == 'HTTPDNS' and line.startswith('hostname ='):
            hosts = ['appconf.mail.163.com', 'msglb.91160.com',
                     'cdn.wup.huya.com', 'gslbali.ximalaya.com', 'ucdc-upaas.uc.cn']
            hosts += [f'ucdc{i}-upaas.uc.cn' for i in range(10)]
            line = 'hostname = %APPEND% ' + ', '.join(hosts)
        output.append(line)
    header_end = next(i for i, line in enumerate(output) if not line.startswith('#!'))
    output[header_end:header_end] = [
        '#!version=2026.11.20.2',
        '',
        f'# Adapted from QingRex/LoonKissSurge commit {COMMIT}; original authors retained above.',
    ]
    result = '\n'.join(output).rstrip() + '\n'
    assert result.startswith('#!name=')
    metadata = dict(line[2:].split('=', 1) for line in result.split('\n\n', 1)[0].splitlines())
    assert all(metadata.get(key) for key in ('name', 'desc', 'version'))
    # No request rule may disappear or change order during adaptation.
    def rules(text):
        values = []
        for x in text.splitlines():
            if not x or x.startswith(('#', '[', 'hostname =')):
                continue
            if x.startswith(('IP-CIDR,', 'IP-CIDR6,')):
                fields = x.split(',')
                fields[1] = str(ipaddress.ip_network(fields[1], strict=False))
                x = ','.join(fields)
            values.append(x)
        return values
    assert rules(original) == rules(result), 'Request rule order/content changed'
    section = None
    for line in result.splitlines():
        if line.startswith('['):
            section = line.strip('[]')
            assert section in {'Rule', 'URL Rewrite', 'Map Local', 'MITM'}
        elif line and not line.startswith('#'):
            if section == 'Rule':
                fields = next(csv.reader([line]))
                assert fields[0] in {'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'IP-CIDR', 'IP-CIDR6', 'URL-REGEX', 'USER-AGENT', 'AND', 'OR', 'NOT'}
                assert line.count('(') == line.count(')'), line
                if fields[0] in {'IP-CIDR', 'IP-CIDR6'}:
                    ipaddress.ip_network(fields[1], strict=True)
                if fields[0] == 'URL-REGEX':
                    re.compile(fields[1])
            elif section in {'URL Rewrite', 'Map Local'}:
                re.compile(line.split(' ')[0])
                if section == 'Map Local':
                    assert 'data-type=text data="{}" status-code=200' in line
            else:
                assert line.startswith('hostname = %APPEND% ')
    (ROOT / f'Surge/{name}.sgmodule').write_text(result, encoding='utf-8', newline='\n')
    REPORT[name] = {'source_commit': COMMIT, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'sections': dict(counts)}

(ROOT / 'build-report.json').write_text(json.dumps(REPORT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(REPORT, ensure_ascii=False, indent=2))
