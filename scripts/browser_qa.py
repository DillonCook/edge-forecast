"""Exercise the real static page in isolated headless Chrome; local or live URL.
Requires websocket-client and psutil. Screenshots/downloads stay in ignored .qa/.
"""
from pathlib import Path
import os,sys,subprocess,tempfile,time,json,urllib.request,base64,hashlib,shutil
import websocket,psutil
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8874/docs/'
QA=ROOT/'.qa'/('live' if URL.startswith('https:') else 'local');QA.mkdir(parents=True,exist_ok=True)
CHROME=shutil.which('google-chrome') or str(Path(os.environ.get('PROGRAMFILES',''))/'Google/Chrome/Application/chrome.exe')
assert Path(CHROME).exists(),'Install Chrome or expose google-chrome on PATH'
assert urllib.request.urlopen(URL,timeout=20).status==200,'Page unavailable'
with tempfile.TemporaryDirectory(prefix='hermes-website-qa-',ignore_cleanup_errors=True) as profile:
    process=subprocess.Popen([CHROME,'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    ws=None;exceptions=[];network=[];seq=0
    try:
        active=Path(profile)/'DevToolsActivePort';deadline=time.monotonic()+20
        while not active.exists():
            assert process.poll() is None
            if time.monotonic()>deadline:raise TimeoutError('Chrome readiness')
            time.sleep(.1)
        port=int(active.read_text().splitlines()[0]);tabs=json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list',timeout=5))
        tab=next(t for t in tabs if t['type']=='page');ws=websocket.create_connection(tab['webSocketDebuggerUrl'],origin='http://localhost',timeout=20)
        def rpc(method,params=None):
            global seq
            seq+=1;ws.send(json.dumps({'id':seq,'method':method,'params':params or {}}))
            while True:
                message=json.loads(ws.recv())
                if message.get('method')=='Runtime.exceptionThrown':exceptions.append(message['params'])
                if message.get('method')=='Network.responseReceived':network.append(message['params']['response'])
                if message.get('id')==seq:
                    assert 'error' not in message,message
                    return message.get('result',{})
        def js(expression,gesture=False):
            result=rpc('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':True,'userGesture':gesture})
            assert 'exceptionDetails' not in result,result
            return result.get('result',{}).get('value')
        def wait(expression,seconds=15):
            deadline=time.monotonic()+seconds
            while not js(expression):
                if time.monotonic()>deadline:raise AssertionError('Browser condition failed: '+expression)
                time.sleep(.05)
        def settle():js('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
        def shot(name):
            settle();r=rpc('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False});(QA/(name+'.png')).write_bytes(base64.b64decode(r['data']))
        rpc('Page.enable');rpc('Runtime.enable');rpc('Network.enable')
        rpc('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1000,'deviceScaleFactor':1,'mobile':False})
        rpc('Page.navigate',{'url':URL});wait('document.readyState==="complete"')
        assert js('document.querySelector(".enhancement").hidden===false'),'Style controls must be usable after enhancement loads'
        wait('document.querySelector(".hero-product img").complete && document.querySelector(".hero-product img").naturalWidth>0')
        shot('desktop-hero')
        # One public end-to-end flow: choose any of the six styles with either trail.
        choices=[]
        for style in 'abcdef':
            for mode in ('following','fixed'):
                js(f'document.querySelector("[data-style={style}]").click();document.querySelector("input[value={mode}]").click()')
                wait(f'document.getElementById("style-image").getAttribute("aria-busy")==="false" && document.getElementById("style-image").src.endsWith("/{style}-{mode}.webp")')
                assert js('document.querySelectorAll(".style-choice[aria-pressed=true]").length')==1
                assert js('document.getElementById("style-image").naturalWidth')==720
                choices.append(style+'-'+mode)
        # Keyboard activation is real input, not an onclick-only control.
        js('document.querySelector("[data-style=a]").focus()')
        assert js('document.activeElement.dataset.style')=='a'
        rpc('Input.dispatchKeyEvent',{'type':'keyDown','key':'Enter','code':'Enter','windowsVirtualKeyCode':13,'text':'\r','unmodifiedText':'\r'})
        rpc('Input.dispatchKeyEvent',{'type':'keyUp','key':'Enter','code':'Enter','windowsVirtualKeyCode':13})
        wait('document.querySelector("[data-style=a]").getAttribute("aria-pressed")==="true"')
        js('document.querySelector("input[value=following]").click()');wait('document.getElementById("style-image").src.endsWith("/a-following.webp")')
        viewports=[]
        for width in (1440,768,390,320):
            rpc('Emulation.setDeviceMetricsOverride',{'width':width,'height':1000,'deviceScaleFactor':1,'mobile':False});settle()
            dims=js('({width:innerWidth,scroll:document.documentElement.scrollWidth})');assert dims['width']==width and dims['scroll']<=width,dims
            assert js('Array.from(document.querySelectorAll(".style-choice,.mode-picker label")).every(e=>e.getBoundingClientRect().height>=44)')
            viewports.append(dims)
            if width in (1440,390):
                js('scrollTo({top:0,behavior:"instant"})');shot(f'hero-{width}')
                for section in ('styles','download','install'):
                    js(f'scrollTo({{top:document.getElementById("{section}").getBoundingClientRect().top+scrollY,behavior:"instant"}})');shot(f'{section}-{width}')
        rpc('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
        assert js('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
        assert js('!document.querySelector("video").autoplay')
        js('document.querySelector(".faq-list summary").click()');assert js('document.querySelector(".faq-list details").open')
        js('document.querySelector("video").play().then(()=>true)',gesture=True)
        wait('document.querySelector("video").currentTime>0.1')
        video=js('({duration:document.querySelector("video").duration,width:document.querySelector("video").videoWidth,height:document.querySelector("video").videoHeight})')
        assert video=={'duration':8,'width':800,'height':890},video
        js('document.querySelector("video").pause()')
        downloads=QA/'downloads';downloads.mkdir(exist_ok=True)
        rpc('Browser.setDownloadBehavior',{'behavior':'allow','downloadPath':str(downloads.resolve()),'eventsEnabled':True})
        js('document.getElementById("apk-download").click()',gesture=True)
        release=json.loads((ROOT/'docs/release.json').read_text());filename=Path(release['file']).name;target=downloads/filename;deadline=time.monotonic()+30
        while not target.exists() or target.stat().st_size!=release['bytes']:
            if time.monotonic()>deadline:raise AssertionError('Actual browser APK download did not finish')
            time.sleep(.1)
        assert hashlib.sha256(target.read_bytes()).hexdigest()==release['sha256']
        failures=[{'url':r['url'],'status':r['status']} for r in network if r['status']>=400]
        assert not failures,failures
        assert not exceptions,exceptions
        assert all(r['url'].startswith(URL) for r in network if not r['url'].startswith('data:')),'Unexpected third-party request'
        result={'url':URL,'styleModeCases':choices,'viewports':viewports,'keyboard':'PASS','reducedMotion':'PASS','faq':'PASS','video':video,'actualBrowserDownloadSha256':release['sha256'],'consoleExceptions':exceptions,'httpErrors':failures}
        (QA/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    finally:
        if ws:ws.close()
        try:children=psutil.Process(process.pid).children(recursive=True)
        except psutil.Error:children=[]
        process.terminate()
        try:process.wait(timeout=8)
        except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
        for child in children:
            try:child.terminate()
            except psutil.Error:pass
