"""Keep the public page concise without dropping setup or release boundaries."""
from pathlib import Path
from html.parser import HTMLParser
import re,unittest
ROOT=Path(__file__).resolve().parents[1]
class Copy(HTMLParser):
    def __init__(self):super().__init__();self.body=False;self.parts=[]
    def handle_starttag(self,t,a):
        if t=='body':self.body=True
    def handle_endtag(self,t):
        if t=='body':self.body=False
    def handle_data(self,data):
        if self.body:self.parts.append(data)
class PageFocus(unittest.TestCase):
    def test_shorter_copy_keeps_the_useful_sections_and_release_limits(self):
        html=(ROOT/'docs/index.html').read_text(encoding='utf-8');copy=Copy();copy.feed(html)
        words=re.findall(r'\S+',' '.join(copy.parts))
        self.assertLessEqual(len(words),1250,f'Too much page copy: {len(words)} words')
        self.assertNotIn('class="chapter-strip"',html)
        self.assertNotRegex(html,r'\d\d / ')
        for id in ('styles','motion','download','install','phone-battery-setup'):
            self.assertIn(f'id="{id}"',html)
        for text in ('Watch Face Format 5','Wear OS 7','on-watch validation is incomplete','10× speed','not watch footage','unresolved','both your Android phone and Wear OS watch'):
            self.assertIn(text,html)
        self.assertEqual(html.count('on-watch validation is incomplete'),1)
if __name__=='__main__':unittest.main()
