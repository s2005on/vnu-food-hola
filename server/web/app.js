'use strict';
let dishes=[];
function normalize(s){return String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/Đ/g,'D').toLowerCase();}
function cleanCart(value){const out={};if(!value||typeof value!=='object'||Array.isArray(value))return out;for(const d of dishes){const n=value[d.id];if(d.available&&Number.isInteger(n)&&n>0)out[d.id]=Math.min(n,20);}return out;}
function cartTotal(cart){const safe=cleanCart(cart);return dishes.reduce((sum,d)=>sum+d.price*(safe[d.id]||0),0);}
function changeQuantity(cart,id,delta){const out=cleanCart(cart);const d=dishes.find(x=>x.id===Number(id));if(!d||!d.available||!Number.isInteger(delta))return out;const n=Math.max(0,Math.min(20,(out[d.id]||0)+delta));if(n)out[d.id]=n;else delete out[d.id];return out;}
function filterDishes(query,category,sort,favs){let list=dishes.filter(d=>(category==='Tất cả'||(category==='Yêu thích'?favs.includes(d.id):d.category===category))&&normalize(d.name+' '+d.desc).includes(normalize(query).trim()));if(sort==='asc')list.sort((a,b)=>a.price-b.price);if(sort==='desc')list.sort((a,b)=>b.price-a.price);return list;}
if(typeof module!=='undefined')module.exports={dishes,cleanCart,cartTotal,changeQuantity,filterDishes};
if(typeof document!=='undefined'){
async function bootCustomer(){
const sessionResponse=await fetch('api/session',{cache:'no-store'});
if(!sessionResponse.ok)throw new Error('Không kiểm tra được phiên. Vui lòng tải lại trang.');
const session=await sessionResponse.json();
const $=id=>document.getElementById(id),money=n=>new Intl.NumberFormat('vi-VN',{style:'currency',currency:'VND',maximumFractionDigits:0}).format(n);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const key=session.trial?'vju-food-hola-trial-'+session.trial_id:'vju-food-hola-live-v1';let storageAvailable=true;
function read(){try{const value=JSON.parse(localStorage.getItem(key)||'{}');return value&&typeof value==='object'?value:{};}catch{storageAvailable=false;return {};}}
const saved=read();
let cart={}, favorites=Array.isArray(saved.favorites)?saved.favorites:[],orders=[];
let refs=Array.isArray(saved.refs)?saved.refs.filter(x=>x&&typeof x.code==='string'&&typeof x.token==='string').slice(0,20):[];
let shop=null,slots=[],busy=false, menuReady=false;
async function api(path,options={}){const r=await fetch('api/'+path,{...options,signal:AbortSignal.timeout(15000),headers:{'Content-Type':'application/json','X-VJU-Request':'1',...(session.trial?{'X-VJU-Trial':session.trial_id}:{'X-VJU-Mode':'guest'}),...(options.headers||{})}});let data;try{data=await r.json();}catch{throw new Error('Máy chủ trả dữ liệu không hợp lệ.');}if(!r.ok){const err=new Error(typeof data.detail==='string'?data.detail:'Dữ liệu chưa hợp lệ. Kiểm tra lại các ô nhập.');err.status=r.status;throw err;}return data;}
async function loadMenu(initial=false){
 try{const previousSlot=$('time').value;const data=await api('menu');dishes=data.dishes;shop=data.shop;slots=data.slots;cart=cleanCart(initial?saved.cart:cart);menuReady=true;

 $('time').innerHTML=slots.map(x=>`<option value="${esc(x.id)}">${esc(x.label)}</option>`).join('');
 if(slots.some(x=>x.id===previousSlot))$('time').value=previousSlot;
 $('shop-status').textContent=slots.length?`Giờ nhận ${shop.opens}–${shop.closes} · Hôm nay & ngày mai`:'Quán đang tạm ngừng nhận đơn.';
 renderCategories();renderMenu();renderCart();save();
 }catch(e){menuReady=false;$('shop-status').textContent='Không tải được thực đơn. '+e.message;$('submit').disabled=true;}
}
function remember(code,token){refs=[{code,token},...refs.filter(x=>x.code!==code)].slice(0,20);save();}
let pending=saved.pending||null;
let category='Tất cả',query='',sort='default',toastTimer,clearArmed=false,clearTimer;
function save(){try{localStorage.setItem(key,JSON.stringify({cart,favorites,refs,pending}));}catch{storageAvailable=false;}$('storage-warning').hidden=storageAvailable;}
function toast(s){$('toast').textContent=s;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,2500);}
function renderCategories(){$('categories').innerHTML=['Tất cả','Cơm','Bún & mì','Ăn nhẹ','Đồ uống','Yêu thích'].map(c=>`<button class="category ${c===category?'active':''}" data-category="${esc(c)}" aria-pressed="${c===category}">${c==='Yêu thích'?'♡ ':''}${esc(c)}</button>`).join('');}
function renderMenu(){const list=filterDishes(query,category,sort,favorites);$('result-count').textContent=list.length+' món';$('empty').hidden=!!list.length;$('menu').innerHTML=list.map(d=>`<article class="dish"><div class="dish-art" style="--dish-bg:${d.bg}"><span class="dish-label">${esc(d.tag)}</span>${d.image?`<img class="food-photo" src="${esc(d.image)}" alt="${esc(d.name)} — ảnh minh họa" loading="lazy" width="512" height="512">`:`<span class="food-emoji" aria-hidden="true">${esc(d.emoji)}</span>`}<button class="fav ${favorites.includes(d.id)?'selected':''}" data-fav="${d.id}" aria-label="${favorites.includes(d.id)?'Bỏ yêu thích':'Yêu thích'} ${esc(d.name)}" aria-pressed="${favorites.includes(d.id)}">${favorites.includes(d.id)?'♥':'♡'}</button></div><div class="dish-body"><h3>${esc(d.name)}</h3><p class="dish-desc">${esc(d.desc)}</p><div class="dish-bottom"><span class="price-tag"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 12.5 12 21 3 12V3h9l8.5 8.5a1.4 1.4 0 0 1 0 1z"/><circle cx="7.6" cy="7.6" r="1.3"/></svg><strong>${money(d.price)}</strong></span>${d.available?`<button class="add" data-add="${d.id}" aria-label="Thêm ${esc(d.name)}">+</button>`:'<span class="sold">Tạm hết món</span>'}</div></div></article>`).join('');}
function renderCart(){cart=cleanCart(cart);let count=0;$('cart').innerHTML=dishes.filter(d=>cart[d.id]).map(d=>{count+=cart[d.id];return `<div class="cart-row"><div class="cart-line"><span class="cart-name">${esc(d.emoji)} ${esc(d.name)}</span><span class="cart-price">${money(d.price*cart[d.id])}</span></div><div class="qty"><button data-qty="${d.id}" data-delta="-1" aria-label="Giảm ${esc(d.name)}">−</button><span aria-label="Số lượng">${cart[d.id]}</span><button data-qty="${d.id}" data-delta="1" ${cart[d.id]>=20?'disabled':''} aria-label="Tăng ${esc(d.name)}">+</button><button class="remove" data-remove="${d.id}" aria-label="Xóa ${esc(d.name)} khỏi giỏ">Xóa</button></div></div>`;}).join('')||'<div class="empty-cart"><span aria-hidden="true">🥣</span><b>Giỏ hàng đang chờ món ngon</b><br>Chọn dấu + bên cạnh món bạn thích.</div>';$('cart-count').textContent=count;$('subtotal').textContent=$('total').textContent=money(cartTotal(cart));$('submit').disabled=!count||!menuReady||!slots.length||busy||session.expired;}
const statuses={pending:'Chờ xác nhận',confirmed:'Đã xác nhận',preparing:'Đang chuẩn bị',ready:'Sẵn sàng nhận',completed:'Hoàn thành',cancelled:'Đã hủy'};
const statusDescriptions={pending:'Quán sẽ kiểm tra và xác nhận đơn.',confirmed:'Quán đã nhận đơn và sắp chuẩn bị.',preparing:'Món ăn đang được chuẩn bị.',ready:'Món đã sẵn sàng, hãy đến điểm nhận.',completed:'Đơn đã hoàn tất.',cancelled:'Đơn đã được hủy.'};
const progressSteps=[['confirmed','Xác nhận'],['preparing','Chuẩn bị'],['ready','Sẵn sàng'],['completed','Hoàn thành']];
function orderDate(value){const d=new Date(value);return Number.isNaN(d.getTime())?'—':d.toLocaleString('vi-VN',{timeZone:'Asia/Ho_Chi_Minh',day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'});}
function orderPhoto(items){const dish=dishes.find(d=>d.id===items?.[0]?.id);return dish?.image?`<img src="${esc(dish.image)}" alt="${esc(dish.name)}" loading="lazy">`:`<span aria-hidden="true">${esc(dish?.emoji||'🍽️')}</span>`;}
function renderOrders(){
 $('history-count').textContent=refs.length;
 $('history-clear').hidden=!refs.length;
 $('history-summary').textContent=refs.length?`${refs.length} đơn hàng trên thiết bị này`:'Xem trạng thái đơn hàng của bạn';
 if(!orders.length){$('orders').innerHTML='<div class="order-empty"><span aria-hidden="true">🧾</span><h3>Chưa có đơn hàng</h3><p>Đặt món từ thực đơn hoặc tra cứu bằng mã ở bên dưới.</p><a class="secondary" href="#menu-section" id="go-menu">Khám phá thực đơn →</a></div>';return;}
 $('orders').innerHTML=orders.map(o=>{
  const ref=refs.find(x=>x.code===o.code);
  const label=statuses[o.status]||o.status;
  const current=progressSteps.findIndex(([status])=>status===o.status);
  const done=o.status==='completed'?4:current<0?0:current+1;
  const cancelled=o.status==='cancelled';
  const items=Array.isArray(o.items)?o.items:[];
  const itemSummary=items.map(i=>`${i.qty} × ${esc(i.name)}`).join(' · ');
  const detailItems=items.map(i=>`<li><span>${esc(i.name)} <b>×${i.qty}</b></span><strong>${money(i.price*i.qty)}</strong></li>`).join('');
  const steps=cancelled?'<p class="cancel-note">Đơn đã hủy, không tiếp tục xử lý.</p>':`<ol class="order-steps">${progressSteps.map(([status,name],idx)=>`<li class="${idx<done?'is-done':''} ${idx===done-1?'is-current':''}"><span class="step-dot">${idx<done?'✓':idx+1}</span><span>${name}</span></li>`).join('')}</ol>`;
  return `<article class="order order-card">
    <div class="order-card-top"><div class="order-code"><span class="code-label">MÃ ĐƠN</span><h3>${esc(o.code)}</h3></div><span class="order-status status-${esc(o.status)}">${cancelled?'✕':o.status==='completed'?'✓':o.status==='ready'?'✓':'◷'} ${esc(label)}</span></div>
    <div class="order-card-main"><div class="order-thumbnail">${orderPhoto(items)}</div><div class="order-info"><div class="ordered-items">${itemSummary}</div><div class="order-info-line"><span aria-hidden="true">📍</span><span>${esc(o.pickup)}</span></div><div class="order-info-line"><span aria-hidden="true">🕒</span><span>Giờ nhận: ${esc(o.time)}</span></div><div class="order-info-line"><span aria-hidden="true">📅</span><span>Đặt lúc: ${esc(orderDate(o.date))}</span></div></div><div class="order-price"><small>Tổng cộng</small><strong>${money(o.total)}</strong><span class="payment-status ${o.paid?'paid':''}">${o.paid?'✓ Đã thanh toán':'Tiền mặt khi nhận'}</span></div></div>
    ${steps}
    <div class="order-card-footer"><span class="order-support-text">${esc(statusDescriptions[o.status]||'Theo dõi tình trạng đơn bên dưới.')}</span><button type="button" class="order-detail-button" data-details="${esc(o.code)}" aria-expanded="false">Xem chi tiết <span>⌄</span></button></div>
    <div class="order-extra" id="detail-${esc(o.code)}" hidden><h4>Chi tiết món ăn</h4><ul>${detailItems}</ul>${o.note?`<p><b>Ghi chú:</b> ${esc(o.note)}</p>`:''}${o.cancel_reason?`<p><b>Lý do hủy:</b> ${esc(o.cancel_reason)}</p>`:''}<details class="order-secret"><summary>Mã tra cứu bí mật (giữ riêng)</summary><p>${esc(ref?.token||'Không lưu mã trên thiết bị này')}</p></details><button class="secondary reorder-btn" type="button" data-reorder="${esc(o.code)}">↻ Thêm lại vào giỏ</button></div>
  </article>`;
 }).join('');
}

let ordersRefreshing=false, refreshAgain=false;
async function refreshOrders(){
 if(ordersRefreshing){refreshAgain=true;return;}
 ordersRefreshing=true;
 const requested=refs.slice();
 try {
  $('order-message').textContent='Đang cập nhật…';
  const result=await Promise.allSettled(requested.map(x=>api('orders/'+encodeURIComponent(x.code),{headers:{Authorization:'Bearer '+x.token}})));
  // Ignore responses for lookup codes the user has since forgotten/changed.
  if(JSON.stringify(requested)!==JSON.stringify(refs)){refreshAgain=true;return;}
  const previous=new Map(orders.map(o=>[o.code,o]));
  const updated=result.map((r,i)=>r.status==='fulfilled'?r.value:previous.get(requested[i].code)).filter(Boolean);
  if(JSON.stringify(updated)!==JSON.stringify(orders)){orders=updated;}renderOrders();
  const failures=result.filter(x=>x.status==='rejected');
  $('order-message').textContent=failures.length?'Giữ thông tin lần trước; một số đơn chưa cập nhật được: '+failures[0].reason.message:refs.length?'Đã cập nhật · Tự làm mới mỗi phút':'Bạn có thể tra cứu đơn bằng mã bên dưới.';
 } finally {
  ordersRefreshing=false;
  if(refreshAgain){refreshAgain=false;await refreshOrders();}
 }
}
// At most 20 saved orders, once per minute: below the 60/min lookup limit.
setInterval(()=>{if(!document.hidden&&$('history-dialog').open&&refs.length)refreshOrders();},60000);
$('menu').addEventListener('click',e=>{const add=e.target.closest('[data-add]'),fav=e.target.closest('[data-fav]');if(add){const id=Number(add.dataset.add);if(cart[id]>=20){toast('Mỗi món tối đa 20 phần trong một đơn.');return;}cart=changeQuantity(cart,id,1);save();renderCart();toast('Đã thêm món vào giỏ');}if(fav){const id=Number(fav.dataset.fav);favorites=favorites.includes(id)?favorites.filter(x=>x!==id):[...favorites,id];save();renderMenu();}});
$('cart').addEventListener('click',e=>{const qty=e.target.closest('[data-qty]'),remove=e.target.closest('[data-remove]');if(qty)cart=changeQuantity(cart,Number(qty.dataset.qty),Number(qty.dataset.delta));if(remove)delete cart[remove.dataset.remove];if(qty||remove){save();renderCart();}});
$('categories').addEventListener('click',e=>{const b=e.target.closest('[data-category]');if(b){category=b.dataset.category;renderCategories();renderMenu();}});
$('search').addEventListener('input',e=>{query=e.target.value;renderMenu();});$('sort').addEventListener('change',e=>{sort=e.target.value;renderMenu();});$('reset-filter').onclick=()=>{query='';category='Tất cả';sort='default';$('search').value='';$('sort').value='default';renderCategories();renderMenu();};
$('name').addEventListener('input',()=>$('name').setCustomValidity(''));
$('order-form').addEventListener('submit',async e=>{
 e.preventDefault();if(busy||!menuReady||session.expired)return;
 const name=$('name').value.trim();if(!name){$('name').setCustomValidity('Nhập tên người nhận.');$('name').reportValidity();return;}
 const payload={name,phone:$('phone').value.trim(),pickup:$('pickup').value.trim(),slot:$('time').value,note:$('note').value.trim(),items:dishes.filter(d=>cart[d.id]).map(d=>({id:d.id,qty:cart[d.id],price:d.price}))};
 if(!payload.items.length)return;
 const fingerprint=JSON.stringify(payload);
 if(pending&&pending.fingerprint!==fingerprint){$('checkout-error').hidden=false;$('checkout-error').textContent='Lần gửi trước chưa rõ kết quả. Bấm “Kiểm tra lần đặt trước” trước khi tạo đơn khác.';return;}
 if(!pending){pending={fingerprint,payload,key:typeof crypto.randomUUID==='function'?crypto.randomUUID():Array.from(crypto.getRandomValues(new Uint8Array(24)),b=>b.toString(16).padStart(2,'0')).join('')};save();}
 await sendPending();
});
async function sendPending(){
 if(!pending||busy)return;
 busy=true;renderCart();$('checkout-error').hidden=true;
 try{const result=await api('orders',{method:'POST',body:JSON.stringify({...pending.payload,key:pending.key})});remember(result.code,result.token);pending=null;cart={};save();renderCart();$('note').value='';window.VJUCartDrawer?.close();$('history-dialog').showModal();await refreshOrders();toast('Đã lưu đơn trên máy chủ.');}
 catch(e){if([409,422].includes(e.status)){pending=null;save();await loadMenu();}$('checkout-error').hidden=false;$('checkout-error').textContent=e.message+' Nếu mất kết nối, dùng nút kiểm tra lần đặt trước để tránh đặt trùng.';}
 finally{busy=false;renderCart();$('retry-order').hidden=!pending;$('reset-pending').hidden=!pending;}
}
const retry=document.createElement('button');retry.id='retry-order';retry.type='button';retry.className='secondary';retry.textContent='Kiểm tra lần đặt trước';retry.hidden=!pending;retry.onclick=sendPending;$('order-form').append(retry);
const reset=document.createElement('button');reset.id='reset-pending';reset.type='button';reset.className='secondary';reset.textContent='Bỏ yêu cầu đang chờ';reset.hidden=!pending;reset.onclick=()=>{if(confirm('Chỉ bỏ khi máy chủ đã từ chối đơn hoặc bạn đã xác nhận đơn chưa được tạo. Nếu mất mạng, hãy kiểm tra lần đặt trước trước.')){pending=null;save();retry.hidden=reset.hidden=true;}};$('order-form').append(reset);
$('history-open').onclick=()=>{window.VJUCartDrawer?.close();$('history-dialog').showModal();refreshOrders();};
$('lookup-form').onsubmit=async e=>{e.preventDefault();try{const code=$('lookup-code').value.trim().toUpperCase(),token=$('lookup-token').value.trim();await api('orders/'+encodeURIComponent(code),{headers:{Authorization:'Bearer '+token}});remember(code,token);$('lookup-token').value='';await refreshOrders();}catch(e){$('order-message').textContent=e.message;}};
$('orders').onclick=async e=>{const detail=e.target.closest('[data-details]');if(detail){const box=document.getElementById('detail-'+detail.dataset.details);if(box){box.hidden=!box.hidden;detail.setAttribute('aria-expanded',String(!box.hidden));detail.innerHTML=box.hidden?'Xem chi tiết <span>⌄</span>':'Thu gọn <span>⌃</span>';}return;}const go=e.target.closest('#go-menu');if(go){$('history-dialog').close();return;}const b=e.target.closest('[data-reorder]');if(!b)return;const order=orders.find(x=>x.code===b.dataset.reorder);await loadMenu();if(!menuReady)return;let skipped=false;for(const item of order.items){const d=dishes.find(x=>x.id===item.id&&x.available);if(d)cart=changeQuantity(cart,d.id,item.qty);else skipped=true;}save();renderCart();$('history-dialog').close();window.VJUCartDrawer?.open();toast(skipped?'Đã thêm món còn bán. Một số món không còn khả dụng.':'Đã thêm vào giỏ theo giá hiện tại. Kiểm tra trước khi đặt.');};
$('reload-menu').onclick=()=>loadMenu();
$('history-close').onclick=()=>$('history-dialog').close();$('history-dialog').addEventListener('click',e=>{if(e.target===$('history-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
$('history-clear').onclick=()=>{if(confirm('Quên mã tra cứu trên thiết bị này? Đơn trên máy chủ vẫn giữ nguyên. Hãy lưu mã tra cứu nếu cần xem lại.')){refs=[];orders=[];save();renderOrders();$('order-message').textContent='Đã quên danh sách trên máy này.';}};
window.addEventListener('storage',e=>{if(e.key===key)toast('Dữ liệu đã thay đổi ở tab khác. Tải lại để xem bản mới.');});
const demoFill=$('demo-fill');
if(demoFill){demoFill.hidden=!session.trial;demoFill.onclick=()=>{
 $('pickup').value='Sảnh KTX VJU, cổng chính';$('name').value='Khách Demo';$('phone').value='0900000000';$('note').value='Đơn demo — không chế biến thực tế';
 if(!Object.keys(cart).length)for(const dish of dishes.filter(d=>d.available).slice(0,2))cart[dish.id]=1;
 save();renderCart();window.VJUCartDrawer?.open();toast('Đã điền dữ liệu demo. Kiểm tra giỏ rồi bấm Đặt món.');
};}
document.addEventListener('visibilitychange',()=>{if(!document.hidden&&!busy)loadMenu();});
setInterval(()=>{if(!document.hidden&&!busy)loadMenu();},60000);
renderOrders();loadMenu(true);$('storage-warning').hidden=storageAvailable;
}
bootCustomer().catch(e=>{document.getElementById('shop-status').textContent=e.message;document.getElementById('submit').disabled=true;});
}

