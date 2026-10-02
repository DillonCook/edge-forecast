"""Hero conversion contract without fabricated popularity or rankings."""
from pathlib import Path
import re, unittest
ROOT=Path(__file__).resolve().parents[1]
class HeroOffer(unittest.TestCase):
    def test_live_counter_and_free_offer_are_in_hero(self):
        html=(ROOT/'docs/index.html').read_text(encoding='utf-8')
        hero=re.search(r'<section class="hero wrap".*?</section>',html,re.S).group()
        self.assertIn('id="download-stats"',hero)
        self.assertEqual(html.count('id="download-stats"'),1)
        self.assertIn('tracked downloads',hero)
        self.assertIn('all versions',hero)
        self.assertRegex(hero,r'id="download-count">…</strong>')
        self.assertIn('For free.',hero)
        self.assertIn('I think it’s the best watch face on the market.',hero)
        self.assertIn('Preview release',hero)
        self.assertIn('Check compatibility',hero)
if __name__=='__main__':unittest.main()
