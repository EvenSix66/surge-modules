# SPDX-License-Identifier: GPL-3.0-only
import unittest
from build_ads import convert


class ConversionTests(unittest.TestCase):
    def test_conditions_never_widened(self):
        result, report = convert({'test': '||ads.example.com^\n||conditional.example^$third-party\n||path.example/banner\n'}, '', '')
        self.assertEqual(result, ['ads.example.com'])
        self.assertEqual(sum(report['skipped'].values()), 2)

    def test_exception_removes_parent_and_child_without_direct(self):
        result, _ = convert({'test': '||example.com^\n||sub.safe.example.com^\n||other.example^'}, '@@||safe.example.com^|', '')
        self.assertEqual(result, ['other.example'])

    def test_scoped_path_exception_widened_for_safety(self):
        result, _ = convert({'test': '||example.com^\n@@||safe.example.com/path$domain=site.example'}, '', '')
        self.assertEqual(result, [])

    def test_wildcard_and_regex_exclusions(self):
        result, _ = convert({'test': '||example.com^\n||minepi.com^\n||other.example^'}, '@@||clk*.example.com^|', r'/^(?:\w+\.)*minepi\.com$/')
        self.assertEqual(result, ['other.example'])

    def test_bad_exception_fails_closed(self):
        with self.assertRaises(ValueError):
            convert({'test': '||example.com^'}, '@@/unknown.*/', '')

    def test_no_superdomain_or_duplicate_expansion(self):
        result, _ = convert({'test': '||ads.example.com^\n||ads.example.com^\n||sub.ads.example.com^\n||badexample.com^'}, '', '')
        self.assertEqual(result, ['ads.example.com', 'badexample.com'])


if __name__ == '__main__':
    unittest.main()
