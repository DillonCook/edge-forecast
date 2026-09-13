"""Publication contract: usable phone-only setup and honest preview limitations."""
from pathlib import Path
from html.parser import HTMLParser
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)
class InstallRelease(unittest.TestCase):
    def test_app_requirements_and_pairing_steps_are_explicit(self):
        html=(ROOT/'docs/index.html').read_text(encoding='utf-8');p=Text();p.feed(html);text=' '.join(' '.join(p.parts).split())
        for term in ('Apps you need','Wear Installer 2','Android phone only','Phone Battery Complication','optional','Software information','Software version','ADB debugging','Wireless debugging','Pair with watch','Pair new device','pairing code','pairing port','connection port','Custom APK','Install','Turn off','both your Android phone and Wear OS watch'):
            self.assertIn(term,text)
        for id in ('required-apps','enable-debugging','pair-watch','connect-watch','install-apk','phone-battery-setup','release-limitations'):
            self.assertIn(f'id="{id}"',html)
        self.assertIn('not the pairing port',text)
        self.assertIn('org.freepoc.wearinstaller2',html)
        self.assertIn('com.weartools.phonebattcomp',html)
    def test_current_release_and_cross_version_count_disclosure(self):
        html=(ROOT/'docs/index.html').read_text(encoding='utf-8');meta=json.loads((ROOT/'docs/release.json').read_text())
        self.assertEqual(meta['version'],'1.5.21');self.assertEqual(meta['versionCode'],36)
        self.assertEqual(meta['trackingStartedAt'],'2026-09-12T19:39:23Z')
        self.assertIn('all versions',html)
        for term in ('text-based phone battery stays','extra %','centering','on-watch','Flat settings'):
            self.assertIn(term,html)
if __name__=='__main__':unittest.main()
