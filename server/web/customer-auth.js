'use strict';
(() => {
  const loginForm = document.getElementById('customer-login');
  const registerForm = document.getElementById('customer-register');
  if (!loginForm || !registerForm) return;

  const status = document.getElementById('customer-error');
  const tabs = [...document.querySelectorAll('[data-auth-tab]')];
  const container = document.getElementById('customer-auth-forms');
  const profile = document.getElementById('customer-profile');
  const trialNote = document.getElementById('customer-trial-note');
  const guestArea = document.getElementById('guest-choice');

  function showTab(tab) {
    loginForm.hidden = tab !== 'login';
    registerForm.hidden = tab !== 'register';
    tabs.forEach(button => {
      const selected = button.dataset.authTab === tab;
      button.setAttribute('aria-selected', String(selected));
      button.classList.toggle('selected', selected);
    });
    status.textContent = '';
  }
  tabs.forEach(button => button.addEventListener('click', () => showTab(button.dataset.authTab)));
  showTab('login');

  async function api(path, payload, csrf) {
    const response = await fetch('api/customer/' + path, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-VJU-Request': '1',
        ...(csrf ? {'X-CSRF-Token': csrf} : {})
      },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(typeof data.detail === 'string' ? data.detail : 'Thông tin chưa hợp lệ. Vui lòng kiểm tra lại.');
    }
    return data;
  }

  function handle(form, action) {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const button = form.querySelector('[type=submit]');
      const fields = new FormData(form);
      const password = String(fields.get('password') || '');
      const payload = {phone: String(fields.get('phone') || '').trim(), password};
      if (action === 'register') {
        payload.name = String(fields.get('name') || '').trim();
        if (password !== String(fields.get('confirm') || '')) {
          status.textContent = 'Hai mật khẩu chưa trùng khớp.';
          return;
        }
      }
      button.disabled = true;
      status.textContent = action === 'register' ? 'Đang tạo tài khoản…' : 'Đang đăng nhập…';
      try {
        await api(action, payload);
        window.location.replace('./');
      } catch (error) {
        status.textContent = error.message;
      } finally {
        button.disabled = false;
      }
    });
  }
  handle(registerForm, 'register');
  handle(loginForm, 'login');

  async function init() {
    try {
      const response = await fetch('api/session', {cache: 'no-store'});
      if (!response.ok) throw new Error('Không thể kiểm tra phiên đăng nhập.');
      const session = await response.json();
      if (session.trial || session.expired) {
        container.hidden = true;
        trialNote.hidden = false;
        trialNote.textContent = 'Hãy chọn “Tiếp tục với vai trò khách” để thoát phiên demo trước khi đăng ký hoặc đăng nhập.';
        return;
      }
      if (session.customer_id) {
        container.hidden = true;
        guestArea.hidden = true;
        profile.hidden = false;
        document.getElementById('profile-name').textContent = session.customer_name;
        document.getElementById('profile-phone').textContent = session.customer_phone;
        document.getElementById('customer-signout').onclick = async () => {
          const button = document.getElementById('customer-signout');
          button.disabled = true;
          try {
            await api('logout', {}, session.customer_csrf);
            window.location.replace('./');
          } catch (error) {
            button.disabled = false;
            document.getElementById('profile-message').textContent = error.message;
          }
        };
      }
    } catch (error) {
      status.textContent = error.message;
    }
  }
  init();
})();
