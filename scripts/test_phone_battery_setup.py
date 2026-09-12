from pathlib import Path
import re,unittest

class PhoneBatterySetup(unittest.TestCase):
    def test_optional_phone_battery_setup_names_both_apps_and_provider_selection(self):
        html=(Path(__file__).resolve().parents[1]/'docs/index.html').read_text(encoding='utf-8')
        block=re.search(r'<li id="phone-battery-setup">(.*?)</li>',html,re.S)
        self.assertIsNotNone(block,'Phone-battery installation must have a clear setup step')
        text=block.group(1)
        self.assertIn('Install and open',text)
        self.assertIn('both your Android phone and Wear OS watch',text)
        self.assertIn('https://play.google.com/store/apps/details?id=com.weartools.phonebattcomp',text)
        self.assertIn('Phone Battery',text)
        self.assertIn('phone-battery slot',text)
        self.assertIn('optional',text.lower())

if __name__=='__main__':unittest.main()
