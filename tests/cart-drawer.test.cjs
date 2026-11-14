const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const script = fs.readFileSync('server/web/cart-drawer.js', 'utf8');
const html = fs.readFileSync('server/web/index.html', 'utf8');

function setup() {
  const listeners = {};
  const history = {open:false};
  const trigger = {
    attributes:{},
    focusCount:0,
    setAttribute(key,value){this.attributes[key]=value;},
    addEventListener(type,fn){listeners['trigger:'+type]=fn;},
    focus(){this.focusCount++;document.activeElement=this;},
  };
  const closeButton = {
    addEventListener(type,fn){listeners['close:'+type]=fn;},
    focusCount:0,
    focus(){this.focusCount++;document.activeElement=this;},
  };
  const drawer = {
    open:false,
    showModal(){this.open=true;},
    close(){this.open=false;listeners['drawer:close']();},
    getBoundingClientRect(){return {left:600,right:1000,top:0,bottom:900};},
    addEventListener(type,fn){listeners['drawer:'+type]=fn;},
  };
  const elements={'basket':drawer,'cart-open':trigger,'cart-close':closeButton,'history-dialog':history};
  const document={getElementById:id=>elements[id],activeElement:trigger};
  const window={};
  vm.runInNewContext(script,{document,window});
  return {listeners,trigger,closeButton,drawer,history,window};
}

test('header login and cart stay together, original form remains in modal',()=>{
  assert.match(html,/<div class="header-actions">[\s\S]*id="account-link"[\s\S]*id="cart-open"/);
  assert.match(html,/<dialog id="basket"[\s\S]*<form id="order-form">/);
  assert.match(html,/id="time"/);
  assert.match(html,/id="pickup"/);
});

test('cart opens from header and closes with close button',()=>{
  const h=setup();h.listeners['trigger:click']();
  assert.equal(h.drawer.open,true);
  assert.equal(h.trigger.attributes['aria-expanded'],'true');
  assert.equal(h.closeButton.focusCount,1);
  h.listeners['close:click']();
  assert.equal(h.drawer.open,false);
  assert.equal(h.trigger.attributes['aria-expanded'],'false');
  assert.equal(h.trigger.focusCount,1);
});

test('click on the backdrop closes modal; inside clicks do not',()=>{
  const h=setup();h.window.VJUCartDrawer.open();
  h.listeners['drawer:click']({target:h.drawer,clientX:850,clientY:500});
  assert.equal(h.drawer.open,true);
  h.listeners['drawer:click']({target:h.drawer,clientX:100,clientY:500});
  assert.equal(h.drawer.open,false);
});

test('does not steal focus from the order history opened after checkout',()=>{
  const h=setup();h.window.VJUCartDrawer.open();h.history.open=true;
  h.window.VJUCartDrawer.close();
  assert.equal(h.trigger.focusCount,0);
});
