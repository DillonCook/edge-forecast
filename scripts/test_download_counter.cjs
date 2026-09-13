// Synthetic fixtures test counter behavior; they are never published as statistics.
const test=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');
const path=require('node:path');const modulePath=path.join(__dirname,'../docs/download-counter.js');
const ROOT='https://api.github.com/repos/DillonCook/edge-forecast/releases';
const asset=(id,count,name='edge-forecast-1.5.17.apk')=>({id,name,state:'uploaded',download_count:count});
const response=(data,link=null)=>({ok:true,headers:{get:name=>name==='Link'?link:null},json:async()=>data});
function counter(){assert.ok(fs.existsSync(modulePath),'Shared GitHub counter implementation is missing');return require(modulePath);}

test('shared count sums only published APK downloads across pages, without double-counting assets',async()=>{
  const {getTotal}=counter();const calls=[];
  const next=ROOT+'?per_page=100&page=2';
  const fetcher=async(url,options)=>{
    calls.push(url);assert.equal(options.credentials,'omit');assert.equal(options.referrerPolicy,'no-referrer');assert.ok(!options.headers.Authorization);
    if(calls.length===1)return response([{draft:false,assets:[asset(1,7),asset(2,99,'SHA256SUMS.txt')]},{draft:true,assets:[asset(5,40)]}],`<${next}>; rel="next"`);
    assert.equal(url,next);return response([{draft:false,prerelease:true,assets:[asset(1,8),asset(3,2,'edge-forecast-1.5.18.apk')]}]);
  };
  assert.equal(await getTotal(fetcher),10);assert.equal(calls.length,2);
});
test('a real zero is allowed, but no matching APK is not a fabricated zero',async()=>{
  const {getTotal}=counter();assert.equal(await getTotal(async()=>response([{draft:false,assets:[asset(1,0)]}])),0);
  await assert.rejects(()=>getTotal(async()=>response([])));
});
test('rate limits, malformed/negative counts and unsafe pagination fail without partial totals',async()=>{
  const {getTotal}=counter();
  for(const count of [-1,NaN,'3',null])await assert.rejects(()=>getTotal(async()=>response([{draft:false,assets:[asset(1,count)]}])));
  await assert.rejects(()=>getTotal(async()=>({ok:false,status:403})));
  await assert.rejects(()=>getTotal(async()=>response([{draft:false,assets:[asset(1,4)]}],'<https://example.com/other>; rel="next"')));
  let i=0;await assert.rejects(()=>getTotal(async()=>++i===1?response([{draft:false,assets:[asset(1,4)]}],`<${ROOT}?page=2>; rel="next"`):({ok:false,status:500})));
});
test('UI renders server totals and honest unavailable state, never locally increments clicks',async()=>{
  const {renderCounter}=counter();const number={textContent:'…'},status={textContent:''},container={dataset:{},setAttribute(){}};
  await renderCounter(container,number,status,async()=>response([{draft:false,assets:[asset(1,1234)]}]));
  assert.equal(container.dataset.state,'ready');assert.equal(container.dataset.total,'1234');assert.match(number.textContent,/1.?234/);
  await renderCounter(container,number,status,async()=>{throw Error('offline')});
  assert.equal(container.dataset.state,'unavailable');assert.equal(number.textContent,'—');assert.match(status.textContent,/unavailable/i);assert.equal(container.dataset.total,undefined);
});

test('publishing a new version at zero preserves all previous asset downloads',async()=>{
  const {getTotal}=counter();
  const releases=[{draft:false,prerelease:true,assets:[asset(21,0,'edge-forecast-1.5.21.apk')]},{draft:false,prerelease:true,assets:[asset(17,3,'edge-forecast-1.5.17.apk')]}];
  assert.equal(await getTotal(async()=>response(releases)),3);
  releases[0].assets[0].download_count=2;
  assert.equal(await getTotal(async()=>response(releases)),5);
});
test('counter labels the project total as all versions',async()=>{
  const {renderCounter}=counter();const number={},status={},container={dataset:{},setAttribute(){}};
  await renderCounter(container,number,status,async()=>response([{draft:false,assets:[asset(17,3)]}]));
  assert.match(status.textContent,/All versions/);
});
