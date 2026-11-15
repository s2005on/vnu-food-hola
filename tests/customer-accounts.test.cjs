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

test('registration form submits name, phone, password and redirects on success',async()=>{
 const script=fs.readFileSync('server/web/customer-auth.js','utf8');
 const handlers={};const calls=[];const redirects=[];
 const submit={disabled:false};
 const makeForm=(id,fields)=>({
  id,fields,hidden:false,
  addEventListener(type,fn){handlers[id+':'+type]=fn;},
  querySelector(){return submit;}
 });
 const login=makeForm('customer-login',{phone:'0900000000',password:'SecurePassword123'});
 const register=makeForm('customer-register',{
  name:'Minh Anh',phone:'0900000000',password:'SecurePassword123',confirm:'SecurePassword123'
 });
 const tabs=['login','register'].map(tab=>({
  dataset:{authTab:tab},setAttribute(){},classList:{toggle(){}},
  addEventListener(type,fn){handlers['tab:'+tab]=fn;}
 }));
 const extra=new Map([
  ['customer-auth-forms',{hidden:false}],['customer-profile',{hidden:true}],
  ['customer-trial-note',{hidden:true}],['guest-choice',{hidden:false}],
  ['customer-error',{textContent:''}]
 ]);
 const document={
  querySelectorAll:()=>tabs,
  getElementById:id=>id==='customer-login'?login:id==='customer-register'?register:extra.get(id)
 };
 const context=vm.createContext({
  document,window:{location:{replace:value=>redirects.push(value)}},
  FormData:class {constructor(form){this.data=form.fields;}get(key){return this.data[key];}},
  fetch:async(url,options)=>{
   calls.push({url,options});
   if(url==='api/session')return {ok:true,json:async()=>({trial:false,customer_id:null})};
   if(url==='api/customer/register')return {ok:true,json:async()=>({id:1})};
   throw Error('unexpected: '+url);
  }
 });
 vm.runInContext(script,context);
 await tick();
 handlers['tab:register']();
 assert.equal(register.hidden,false);
 assert.equal(login.hidden,true);
 await handlers['customer-register:submit']({preventDefault(){}});
 const sent=calls.find(x=>x.url==='api/customer/register');
 assert.ok(sent);
 assert.equal(sent.options.headers['X-VJU-Request'],'1');
 const body=JSON.parse(sent.options.body);
 assert.equal(body.name,'Minh Anh');
 assert.equal(body.phone,'0900000000');
 assert.equal(body.password,'SecurePassword123');
 assert.deepEqual(redirects,['./']);
});
