// Execute the actual customer script with a minimal DOM/network harness.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const source=fs.readFileSync('server/web/app.js','utf8');
const tick=()=>new Promise(resolve=>setImmediate(resolve));
function harness(){
 const elements=new Map(), intervals=[];
 const element=id=>{
  if(!elements.has(id))elements.set(id,{id,hidden:false,open:false,value:'',textContent:'',innerHTML:'',
   addEventListener(){},append(e){elements.set(e.id,e);},showModal(){this.open=true;},close(){this.open=false;}});
  return elements.get(id);
 };
 const order={code:'VJU-TEST',status:'pending',paid:false,name:'Khách',date:'2026-11-11T12:00:00+07:00',pickup:'Quán',time:'12:30',items:[],total:0};
 const state={order,fail:false,count:0,hold:null};
 const document={addEventListener(){},hidden:false,getElementById:element,createElement:()=>({})};
 const context=vm.createContext({document,window:{addEventListener(){}},Intl,AbortSignal,
  localStorage:{getItem:()=>JSON.stringify({refs:[{code:order.code,token:'secret'}]}),setItem(){}},
  setInterval:(fn,ms)=>intervals.push({fn,ms}),setTimeout:()=>0,clearTimeout(){},confirm:()=>true,
  fetch:async url=>{
   if(url==='api/session')return {ok:true,json:async()=>({trial:false})};
   if(url==='api/menu')return {ok:true,json:async()=>({dishes:[],shop:{name:'Quán'},slots:[]})};
   state.count++;
   if(state.hold)await state.hold;
   if(state.fail)throw new Error('offline');
   return {ok:true,json:async()=>({...state.order})};
  }
 });
 vm.runInContext(source,context);
 return {element,document,intervals,state};
}
test('polls open visible order history and shows updated server status',async()=>{
 const h=harness();await tick();
 h.element('history-open').onclick();await tick();
 assert.match(h.element('orders').innerHTML,/Chờ xác nhận/);
 h.state.order.status='ready';
 assert.equal(h.intervals[0].ms,60000);
 h.intervals[0].fn();await tick();
 assert.match(h.element('orders').innerHTML,/Sẵn sàng nhận/);
 const count=h.state.count;
 h.document.hidden=true;h.intervals[0].fn();await tick();assert.equal(h.state.count,count);
 h.document.hidden=false;h.element('history-dialog').close();h.intervals[0].fn();await tick();assert.equal(h.state.count,count);
});
test('network failure preserves previous order details and reports stale data',async()=>{
 const h=harness();await tick();h.element('history-open').onclick();await tick();
 const before=h.element('orders').innerHTML;
 h.state.fail=true;h.intervals[0].fn();await tick();
 assert.equal(h.element('orders').innerHTML,before);
 assert.match(h.element('order-message').textContent,/chưa cập nhật được/);
});
test('forgetting history during a request does not restore forgotten orders',async()=>{
 const h=harness();await tick();
 let release;h.state.hold=new Promise(resolve=>release=resolve);
 h.element('history-open').onclick();await tick();
 h.element('history-clear').onclick();release();await tick();await tick();
 assert.match(h.element('orders').innerHTML,/Chưa có đơn hàng/);
 assert.equal(h.element('history-count').textContent,0);
});

test('order card presents pickup details, real status and expandable content',async()=>{
 const h=harness();await tick();
 h.state.order.items=[{id:1,name:'Cơm gà',qty:2,price:30000}];
 h.state.order.total=60000;
 h.state.order.status='preparing';
 h.element('history-open').onclick();await tick();
 const html=h.element('orders').innerHTML;
 assert.match(html,/60.000/);
 assert.match(html,/Cơm gà/);
 assert.match(html,/Đang chuẩn bị/);
 assert.match(html,/Giờ nhận/);
 assert.match(html,/Xem chi tiết/);
 assert.match(html,/order-steps/);
 const detail=h.element('detail-VJU-TEST');detail.hidden=true;
 const button={dataset:{details:'VJU-TEST'},innerHTML:'',setAttribute(key,value){this[key]=value}};
 h.element('orders').onclick({target:{closest(selector){return selector==='[data-details]'?button:null;}}});
 assert.equal(detail.hidden,false);
 assert.equal(button['aria-expanded'],'true');
});
