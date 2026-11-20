# SPDX-License-Identifier: MIT
import json
import unittest
from build_httpdns import DATA, render


class HTTPDNSTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(DATA.read_text(encoding='utf-8'))
        self.module, self.report = render(self.manifest)

    def test_no_decryption_or_broad_matching(self):
        body = self.module.split('[Rule]\n')[1]
        for forbidden in ('[MITM]', '[Map Local]', '[URL Rewrite]'):
            self.assertNotIn(forbidden, self.module)
        self.assertFalse(any(x in body for x in ('DOMAIN-KEYWORD', 'DOMAIN-SUFFIX', 'USER-AGENT', 'URL-REGEX')))

    def test_ip_blocks_are_exact_and_no_resolve(self):
        for item in self.report['rules']:
            kind, target, *rest = item['rule'].split(',')
            if kind != 'DOMAIN':
                self.assertTrue(target.endswith('/32' if kind == 'IP-CIDR' else '/128'))
                self.assertEqual(rest, ['REJECT', 'no-resolve'])

    def test_no_public_dns_servers_or_cloud_management_api(self):
        targets = {x['rule'].split(',')[1] for x in self.report['rules']}
        for target in ['119.29.29.29/32', '223.5.5.5/32', '8.8.8.8/32', '1.1.1.1/32', 'httpdns-api.aliyuncs.com']:
            self.assertNotIn(target, targets)

    def test_every_rule_has_document_evidence(self):
        ids = {s['id'] for s in self.manifest['sources']}
        self.assertEqual(len(self.report['rules']), 31)
        for rule in self.report['rules']:
            self.assertTrue(rule['sources'])
            self.assertLessEqual(set(rule['sources']), ids)

    def test_deduplicates_shared_regional_ipv6(self):
        source = self.manifest['sources'][0]
        source['ipv6'].append(source['ipv6'][0])
        _, report = render(self.manifest)
        self.assertEqual(report['counts']['IP-CIDR6'], 10)

    def test_private_endpoint_rejected(self):
        self.manifest['sources'][0]['ipv4'].append('192.168.1.1')
        with self.assertRaises(AssertionError):
            render(self.manifest)


if __name__ == '__main__':
    unittest.main()
