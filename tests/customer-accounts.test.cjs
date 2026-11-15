// Customer account workflow: exercise the actual frontend with a small DOM/network harness.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');

const customerApp=fs.readFileSync('server/web/app.js','utf8');
const loginHTML=fs.readFileSync('server/web/login.html','utf8');
const indexHTML=fs.readFileSync('server/web/index.html','utf8');
const tick=()=>new Promise(resolve=>setImmediate(resolve));

function harness(){
 const elements=new Map(), calls=[],savedKeys=[];
 const element=id=>{
  if(!elements.has(id))elements.set(id,{
   id,value:'',hidden:false,open:false,textContent:'',innerHTML:'',
   addEventListener(){},append(){},showModal(){this.open=true;},close(){this.open=false;},
   setAttribute(){},setCustomValidity(){},reportValidity(){},
  });
  return elements.get(id);
 };
 const session={trial:false,customer_id:42,customer_name:'Minh Anh',customer_phone:'0900000000',customer_csrf:'csrf-42'};
 const order={code:'VJU-AABBCCDDEEFF',status:'pending',paid:false,name:'Minh Anh',date:'2026-11-15T13:00:00+07:00',pickup:'KTX VJU',time:'13:30',items:[],total:35000};
 const state={order};
 const document={hidden:false,addEventListener(){},getElementById:element,createElement:()=>({})};
 const context=vm.createContext({
  document,window:{addEventListener(){}},Intl,AbortSignal,
  localStorage:{getItem:()=>null,setItem:key=>savedKeys.push(key)},
  setInterval(){},setTimeout:()=>0,clearTimeout(){},confirm:()=>true,
  fetch:async(url,options)=>{
   calls.push({url,options});
   if(url==='api/session')return {ok:true,json:async()=>session};
   if(url==='api/menu')return {ok:true,json:async()=>({dishes:[],shop:{opens:'10:00',closes:'22:00'},slots:[]})};
   if(url==='api/customer/orders')return {ok:true,json:async()=>[state.order]};
   if(url==='api/customer/orders/claim')return {ok:true,json:async()=>({...state.order})};
   throw Error('Unexpected URL: '+url);
  }
 });
 vm.runInContext(customerApp,context);
 return {element,calls,savedKeys,session,state};
}

test('login screen contains real registration and login forms, with demo separated',()=>{
 assert.match(loginHTML,/id="customer-register"/);
 assert.match(loginHTML,/id="customer-login"/);
 assert.match(loginHTML,/name="confirm"/);
 assert.match(loginHTML,/id="customer-profile"/);
 assert.match(loginHTML,/id="trial-login"/);
 assert.match(indexHTML,/id="customer-logout"/);
});

test('signed-in customer reads server history and storage is account scoped',async()=>{
 const h=harness();await tick();await tick();
 assert.equal(h.element('phone').value,'0900000000');
 assert.equal(h.element('phone').readOnly,true);
 h.element('history-open').onclick();
 await tick();await tick();
 assert.match(h.element('orders').innerHTML,/VJU-AABBCCDDEEFF/);
 assert.match(h.element('orders').innerHTML,/35.000/);
 assert.equal(h.element('history-count').textContent,1);
 assert.equal(h.element('history-clear').hidden,true);
 assert.ok(h.calls.some(x=>x.url==='api/customer/orders'));
 assert.ok(h.savedKeys.some(key=>key==='vju-food-hola-account-42-v1'));
 assert.doesNotMatch(h.element('orders').innerHTML,/Mã tra cứu bí mật/);
});

test('logged-in customer uses CSRF-protected claim for a guest order',async()=>{
 const h=harness();await tick();await tick();
 h.element('lookup-code').value='VJU-AABBCCDDEEFF';
 h.element('lookup-token').value='secret-token-123456789';
 await h.element('lookup-form').onsubmit({preventDefault(){}});
 const request=h.calls.find(x=>x.url==='api/customer/orders/claim');
 assert.ok(request);
 assert.equal(request.options.method,'POST');
 assert.equal(request.options.headers['X-CSRF-Token'],'csrf-42');
 assert.equal(JSON.parse(request.options.body).token,'secret-token-123456789');
 assert.equal(h.element('lookup-token').value,'');
});
