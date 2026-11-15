'use strict';
(async()=>{
 const $=id=>document.getElementById(id);
 async function api(path,body){const response=await fetch('api/'+path,{method:body?'POST':'GET',headers:{'Content-Type':'application/json','X-VJU-Request':'1'},...(body?{body:JSON.stringify(body)}:{})});const data=await response.json();if(!response.ok)throw new Error(data.detail||'Không kết nối được máy chủ.');return data;}
 async function leave(){try{await api('trial/logout',{});location.href='./';}catch(e){alert(e.message);}}
 function banner(text,expired=false){const el=$('trial-banner');if(!el)return;el.hidden=false;el.replaceChildren();const label=document.createElement('span');label.textContent=text;const link=document.createElement('a');link.href='admin.html';link.textContent='Quản trị quán ↗';const button=document.createElement('button');button.className='secondary';button.textContent='Tiếp tục với vai trò khách';button.onclick=event=>{event.preventDefault();leave();};el.append(label,link,button);}
 let info;
 try{info=await api('session');if(info.trial){banner('Đang dùng tài khoản demo · Phiên riêng 2 giờ');if($('account-link'))$('account-link').innerHTML='<span class="nav-symbol" aria-hidden="true">♙</span> Demo đang bật';}else if(info.expired){banner('Phiên demo đã hết hạn. Bạn vẫn có thể xem thực đơn.',true);}}
 catch(e){banner('Không thể kiểm tra phiên demo. Bạn có thể đăng nhập lại.',true);}
 if($('guest-start'))$('guest-start').onclick=leave;
 const note=document.querySelector('.demo-note');
 if(note&&info){note.hidden=!info.trial&&!info.expired;note.textContent=info.trial?'DEMO · Dữ liệu riêng, không gửi vào danh sách đơn của quán':info.expired?'Phiên demo hết hạn · Chọn tiếp tục với vai trò khách hoặc đăng nhập demo lại':'Đặt món với vai trò khách · Đơn gửi tới quản trị quán · Thanh toán tiền mặt khi nhận';}
 if($('account-link')&&info&&!info.trial){
  $('account-link').textContent=info.customer_id?'Xin chào, '+info.customer_name:'Khách / Đăng nhập';
  if(info.customer_id)$('account-link').setAttribute('aria-label','Tài khoản '+info.customer_name);
 }
 if($('customer-logout')&&info?.customer_id&&!info.trial){
  const button=$('customer-logout');
  button.hidden=false;
  button.onclick=async()=>{
   button.disabled=true;
   try{
    const r=await fetch('api/customer/logout',{method:'POST',headers:{'Content-Type':'application/json','X-VJU-Request':'1','X-CSRF-Token':info.customer_csrf},body:'{}'});
    if(!r.ok)throw new Error('Không đăng xuất được. Vui lòng tải lại trang.');
    location.href='./';
   }catch(e){alert(e.message);button.disabled=false;}
  };
 }
 if($('trial-login')){
  $('trial-login').onsubmit=async event=>{event.preventDefault();const f=event.target,b=f.querySelector('button[type=submit]');b.disabled=true;$('trial-error').textContent='Đang mở phiên demo…';try{await api('trial/login',{username:f.elements.username.value,password:f.elements.password.value});location.href='./';}catch(e){$('trial-error').textContent=e.message;}finally{b.disabled=false;}};
  $('fill-credentials').onclick=()=>{const f=$('trial-login');f.elements.username.value='demo';f.elements.password.value='VjuTest2026!';$('trial-error').textContent='Đã điền tài khoản công khai. Bấm Vào chế độ demo.';};
  if(info&&!info.trial_enabled){$('trial-error').textContent='Chế độ demo hiện không khả dụng.';$('trial-login').querySelector('button[type=submit]').disabled=true;}
 }
})();
