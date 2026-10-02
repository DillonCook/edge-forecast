"""Routine QA must not inflate public release-download statistics."""
from pathlib import Path
import ast,sys,unittest
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
class QADownloadPolicy(unittest.TestCase):
    def enabled(self,args):
        tree=ast.parse((ROOT/'scripts/browser_qa.py').read_text())
        nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='VERIFY_DOWNLOAD' for t in n.targets)]
        self.assertEqual(len(nodes),1,'Actual APK download must be explicit opt-in')
        env={'sys':SimpleNamespace(argv=['browser_qa.py','https://example.test/']+args)}
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'<download-policy>','exec'),env)
        return env['VERIFY_DOWNLOAD']
    def test_default_does_not_download(self):self.assertFalse(self.enabled([]))
    def test_opt_in_is_explicit(self):self.assertTrue(self.enabled(['--verify-apk-download']))
    def test_legacy_skip_remains_safe(self):self.assertFalse(self.enabled(['--skip-download']))
    def test_network_guard_and_metadata_checks_present(self):
        code=(ROOT/'scripts/browser_qa.py').read_text()
        self.assertIn('Unexpected APK request during routine QA',code)
        self.assertIn("asset['digest']=='sha256:'+release['sha256']",code)
        self.assertNotIn('if not SKIP_DOWNLOAD:',code)
if __name__=='__main__':unittest.main()
