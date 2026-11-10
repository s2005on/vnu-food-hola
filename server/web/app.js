'use strict';
let dishes=[];
function normalize(s){return String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/Đ/g,'D').toLowerCase();}
function cleanCart(value){const out={};if(!value||typeof value!=='object'||Array.isArray(value))return out;for(const d of dishes){const n=value[d.id];if(d.available&&Number.isInteger(n)&&n>0)out[d.id]=Math.min(n,20);}return out;}
function cartTotal(cart){const safe=cleanCart(cart);return dishes.reduce((sum,d)=>sum+d.price*(safe[d.id]||0),0);}
function changeQuantity(cart,id,delta){const out=cleanCart(cart);const d=dishes.find(x=>x.id===Number(id));if(!d||!d.available||!Number.isInteger(delta))return out;const n=Math.max(0,Math.min(20,(out[d.id]||0)+delta));if(n)out[d.id]=n;else delete out[d.id];return out;}
function filterDishes(query,category,sort,favs){let list=dishes.filter(d=>(category==='Tất cả'||(category==='Yêu thích'?favs.includes(d.id):d.category===category))&&normalize(d.name+' '+d.desc).includes(normalize(query).trim()));if(sort==='asc')list.sort((a,b)=>a.price-b.price);if(sort==='desc')list.sort((a,b)=>b.price-a.price);return list;}
if(typeof module!=='undefined')module.exports={dishes,cleanCart,cartTotal,changeQuantity,filterDishes};
if(typeof document!=='undefined'){
const $=id=>document.getElementById(id),money=n=>new Intl.NumberFormat('vi-VN',{style:'currency',currency:'VND',maximumFractionDigits:0}).format(n);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const key='vju-food-hola-live-v1';let storageAvailable=true;
function read(){try{const value=JSON.parse(localStorage.getItem(key)||'{}');return value&&typeof value==='object'?value:{};}catch{storageAvailable=false;return {};}}
const saved=read();
let cart={}, favorites=Array.isArray(saved.favorites)?saved.favorites:[],orders=[];
let refs=Array.isArray(saved.refs)?saved.refs.filter(x=>x&&typeof x.code==='string'&&typeof x.token==='string').slice(0,20):[];
let shop=null,slots=[],busy=false, menuReady=false;
async function api(path,options={}){const r=await fetch('api/'+path,{...options,signal:AbortSignal.timeout(15000),headers:{'Content-Type':'application/json','X-VJU-Request':'1',...(options.headers||{})}});let data;try{data=await r.json();}catch{throw new Error('Máy chủ trả dữ liệu không hợp lệ.');}if(!r.ok){const err=new Error(typeof data.detail==='string'?data.detail:'Dữ liệu chưa hợp lệ. Kiểm tra lại các ô nhập.');err.status=r.status;throw err;}return data;}
async function loadMenu(initial=false){
 try{const data=await api('menu');dishes=data.dishes;shop=data.shop;slots=data.slots;cart=cleanCart(initial?saved.cart:cart);menuReady=true;
 $('pickup').innerHTML='<option>'+esc(shop.name)+'</option>';
 $('time').innerHTML=slots.map(x=>`<option value="${esc(x.id)}">${esc(x.label)}</option>`).join('');
 $('shop-status').textContent=slots.length?`${shop.name} · Nhận món hôm nay · ${shop.opens}–${shop.closes}`:'Quán đang nghỉ hoặc đã hết khung giờ nhận hôm nay.';
 renderCategories();renderMenu();renderCart();save();
 }catch(e){menuReady=false;$('shop-status').textContent='Không tải được thực đơn. '+e.message;$('submit').disabled=true;}
}
function remember(code,token){refs=[{code,token},...refs.filter(x=>x.code!==code)].slice(0,20);save();}
let pending=saved.pending||null;
let category='Tất cả',query='',sort='default',toastTimer,clearArmed=false,clearTimer;
function save(){try{localStorage.setItem(key,JSON.stringify({cart,favorites,refs,pending}));}catch{storageAvailable=false;}$('storage-warning').hidden=storageAvailable;}
function toast(s){$('toast').textContent=s;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,2500);}
function renderCategories(){$('categories').innerHTML=['Tất cả','Cơm','Bún & mì','Ăn nhẹ','Đồ uống','Yêu thích'].map(c=>`<button class="category ${c===category?'active':''}" data-category="${esc(c)}" aria-pressed="${c===category}">${c==='Yêu thích'?'♡ ':''}${esc(c)}</button>`).join('');}
function renderMenu(){const list=filterDishes(query,category,sort,favorites);$('result-count').textContent=list.length+' món';$('empty').hidden=!!list.length;$('menu').innerHTML=list.map(d=>`<article class="dish"><div class="dish-art" style="--dish-bg:${d.bg}"><span class="dish-label">${esc(d.tag)}</span><span class="food-emoji" aria-hidden="true">${esc(d.emoji)}</span><button class="fav ${favorites.includes(d.id)?'selected':''}" data-fav="${d.id}" aria-label="${favorites.includes(d.id)?'Bỏ yêu thích':'Yêu thích'} ${esc(d.name)}" aria-pressed="${favorites.includes(d.id)}">${favorites.includes(d.id)?'♥':'♡'}</button></div><div class="dish-body"><h3>${esc(d.name)}</h3><p class="dish-desc">${esc(d.desc)}</p><div class="dish-bottom"><strong>${money(d.price)}</strong>${d.available?`<button class="add" data-add="${d.id}" aria-label="Thêm ${esc(d.name)}">+</button>`:'<span class="sold">Tạm hết món</span>'}</div></div></article>`).join('');}
function renderCart(){cart=cleanCart(cart);let count=0;$('cart').innerHTML=dishes.filter(d=>cart[d.id]).map(d=>{count+=cart[d.id];return `<div class="cart-row"><div class="cart-line"><span class="cart-name">${esc(d.emoji)} ${esc(d.name)}</span><span class="cart-price">${money(d.price*cart[d.id])}</span></div><div class="qty"><button data-qty="${d.id}" data-delta="-1" aria-label="Giảm ${esc(d.name)}">−</button><span aria-label="Số lượng">${cart[d.id]}</span><button data-qty="${d.id}" data-delta="1" ${cart[d.id]>=20?'disabled':''} aria-label="Tăng ${esc(d.name)}">+</button><button class="remove" data-remove="${d.id}" aria-label="Xóa ${esc(d.name)} khỏi giỏ">Xóa</button></div></div>`;}).join('')||'<div class="empty-cart"><span aria-hidden="true">🥣</span><b>Giỏ hàng đang chờ món ngon</b><br>Chọn dấu + bên cạnh món bạn thích.</div>';$('cart-count').textContent=count;$('subtotal').textContent=$('total').textContent=money(cartTotal(cart));$('submit').disabled=!count||!menuReady||!slots.length||busy;}
const statuses={pending:'Chờ xác nhận',confirmed:'Đã xác nhận',preparing:'Đang chuẩn bị',ready:'Sẵn sàng nhận',completed:'Hoàn thành',cancelled:'Đã hủy'};
function renderOrders(){
 $('history-count').textContent=refs.length;$('history-clear').hidden=!refs.length;
 $('orders').innerHTML=orders.map(o=>{const ref=refs.find(x=>x.code===o.code);return `<article class="order"><h3>${esc(o.code)}</h3><span class="order-status">${statuses[o.status]||esc(o.status)} · ${o.paid?'Đã thu tiền':'Chưa thu tiền'}</span><p>${esc(o.name)} · ${esc(new Date(o.date).toLocaleString('vi-VN',{timeZone:'Asia/Ho_Chi_Minh'}))}</p><p>${esc(o.pickup)} · ${esc(o.time)}</p><ul>${o.items.map(i=>`<li>${i.qty} × ${esc(i.name)} — ${money(i.price*i.qty)}</li>`).join('')}</ul>${o.note?`<p>Ghi chú: ${esc(o.note)}</p>`:''}${o.cancel_reason?`<p>Lý do hủy: ${esc(o.cancel_reason)}</p>`:''}<p><b>Tổng cộng: ${money(o.total)}</b></p><details><summary>Mã tra cứu bí mật (giữ riêng)</summary><p style="overflow-wrap:anywhere">${esc(ref?.token||'')}</p></details><button class="secondary" data-reorder="${esc(o.code)}">Thêm lại vào giỏ</button></article>`;}).join('');
}
async function refreshOrders(){
 $('order-message').textContent='Đang cập nhật…';
 const result=await Promise.allSettled(refs.map(x=>api('orders/'+encodeURIComponent(x.code),{headers:{Authorization:'Bearer '+x.token}})));
 orders=result.filter(x=>x.status==='fulfilled').map(x=>x.value);renderOrders();
 const failures=result.filter(x=>x.status==='rejected');
 $('order-message').textContent=failures.length?'Một số đơn không tải được: '+failures[0].reason.message:refs.length?'Đã cập nhật trạng thái từ máy chủ.':'Chưa có đơn trên thiết bị này. Bạn có thể tra cứu bằng mã.';
}
$('menu').addEventListener('click',e=>{const add=e.target.closest('[data-add]'),fav=e.target.closest('[data-fav]');if(add){const id=Number(add.dataset.add);if(cart[id]>=20){toast('Mỗi món tối đa 20 phần trong demo.');return;}cart=changeQuantity(cart,id,1);save();renderCart();toast('Đã thêm món vào giỏ');}if(fav){const id=Number(fav.dataset.fav);favorites=favorites.includes(id)?favorites.filter(x=>x!==id):[...favorites,id];save();renderMenu();}});
$('cart').addEventListener('click',e=>{const qty=e.target.closest('[data-qty]'),remove=e.target.closest('[data-remove]');if(qty)cart=changeQuantity(cart,Number(qty.dataset.qty),Number(qty.dataset.delta));if(remove)delete cart[remove.dataset.remove];if(qty||remove){save();renderCart();}});
$('categories').addEventListener('click',e=>{const b=e.target.closest('[data-category]');if(b){category=b.dataset.category;renderCategories();renderMenu();}});
$('search').addEventListener('input',e=>{query=e.target.value;renderMenu();});$('sort').addEventListener('change',e=>{sort=e.target.value;renderMenu();});$('reset-filter').onclick=()=>{query='';category='Tất cả';sort='default';$('search').value='';$('sort').value='default';renderCategories();renderMenu();};
$('name').addEventListener('input',()=>$('name').setCustomValidity(''));
$('order-form').addEventListener('submit',async e=>{
 e.preventDefault();if(busy||!menuReady)return;
 const name=$('name').value.trim();if(!name){$('name').setCustomValidity('Nhập tên người nhận.');$('name').reportValidity();return;}
 const payload={name,phone:$('phone').value.trim(),slot:$('time').value,note:$('note').value.trim(),items:dishes.filter(d=>cart[d.id]).map(d=>({id:d.id,qty:cart[d.id],price:d.price}))};
 if(!payload.items.length)return;
 const fingerprint=JSON.stringify(payload);
 if(pending&&pending.fingerprint!==fingerprint){$('checkout-error').hidden=false;$('checkout-error').textContent='Lần gửi trước chưa rõ kết quả. Bấm “Kiểm tra lần đặt trước” trước khi tạo đơn khác.';return;}
 if(!pending){pending={fingerprint,payload,key:crypto.randomUUID()};save();}
 await sendPending();
});
async function sendPending(){
 if(!pending||busy)return;
 busy=true;renderCart();$('checkout-error').hidden=true;
 try{const result=await api('orders',{method:'POST',body:JSON.stringify({...pending.payload,key:pending.key})});remember(result.code,result.token);pending=null;cart={};save();renderCart();$('note').value='';$('history-dialog').showModal();await refreshOrders();toast('Đã lưu đơn trên máy chủ.');}
 catch(e){if([409,422].includes(e.status)){pending=null;save();}$('checkout-error').hidden=false;$('checkout-error').textContent=e.message+' Nếu mất kết nối, dùng nút kiểm tra lần đặt trước để tránh đặt trùng.';}
 finally{busy=false;renderCart();$('retry-order').hidden=!pending;$('reset-pending').hidden=!pending;}
}
const retry=document.createElement('button');retry.id='retry-order';retry.type='button';retry.className='secondary';retry.textContent='Kiểm tra lần đặt trước';retry.hidden=!pending;retry.onclick=sendPending;$('order-form').append(retry);
const reset=document.createElement('button');reset.id='reset-pending';reset.type='button';reset.className='secondary';reset.textContent='Bỏ yêu cầu đang chờ';reset.hidden=!pending;reset.onclick=()=>{if(confirm('Chỉ bỏ khi máy chủ đã từ chối đơn hoặc bạn đã xác nhận đơn chưa được tạo. Nếu mất mạng, hãy kiểm tra lần đặt trước trước.')){pending=null;save();retry.hidden=reset.hidden=true;}};$('order-form').append(reset);
$('history-open').onclick=()=>{$('history-dialog').showModal();refreshOrders();};
$('lookup-form').onsubmit=async e=>{e.preventDefault();try{const code=$('lookup-code').value.trim().toUpperCase(),token=$('lookup-token').value.trim();await api('orders/'+encodeURIComponent(code),{headers:{Authorization:'Bearer '+token}});remember(code,token);$('lookup-token').value='';await refreshOrders();}catch(e){$('order-message').textContent=e.message;}};
$('orders').onclick=async e=>{const b=e.target.closest('[data-reorder]');if(!b)return;const order=orders.find(x=>x.code===b.dataset.reorder);await loadMenu();if(!menuReady)return;let skipped=false;for(const item of order.items){const d=dishes.find(x=>x.id===item.id&&x.available);if(d)cart=changeQuantity(cart,d.id,item.qty);else skipped=true;}save();renderCart();$('history-dialog').close();toast(skipped?'Đã thêm món còn bán. Một số món không còn khả dụng.':'Đã thêm vào giỏ theo giá hiện tại. Kiểm tra trước khi đặt.');};
$('reload-menu').onclick=()=>loadMenu();
$('history-close').onclick=()=>$('history-dialog').close();$('history-dialog').addEventListener('click',e=>{if(e.target===$('history-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
$('history-clear').onclick=()=>{if(confirm('Quên mã tra cứu trên thiết bị này? Đơn trên máy chủ vẫn giữ nguyên. Hãy lưu mã tra cứu nếu cần xem lại.')){refs=[];orders=[];save();renderOrders();$('order-message').textContent='Đã quên danh sách trên máy này.';}};
window.addEventListener('storage',e=>{if(e.key===key)toast('Dữ liệu đã thay đổi ở tab khác. Tải lại để xem bản mới.');});
renderOrders();loadMenu(true);$('storage-warning').hidden=storageAvailable;
}
