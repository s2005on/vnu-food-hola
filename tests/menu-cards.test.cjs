const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const app=fs.readFileSync('server/web/app.js','utf8');
const page=fs.readFileSync('server/web/index.html','utf8');
const style=fs.readFileSync('server/web/menu-cards.css','utf8');
const dishes=JSON.parse(fs.readFileSync('server/seed.json','utf8'));
test('menu renders tagged prices and add buttons without changing API availability',()=>{
 assert.match(app,/class=\"price-tag\"/);
 assert.match(app,/money\(d\.price\)/);
 assert.match(app,/d\.available\?/);
 assert.match(app,/data-add/);
});
test('Versioned menu CSS loads after v7 styles and before customer script',()=>{
 assert.ok(page.indexOf('href=\"v7.css?v=7.3\"') < page.indexOf('menu-cards.css?v=7.3'));
 assert.ok(page.indexOf('menu-cards.css?v=7.3') < page.indexOf('app.js?v=7.3'));
 assert.match(style,/#menu-section \.dish/);
 assert.match(style,/#menu-section \.price-tag/);
});
test('all sixteen seeded dishes have valid photos and are available initially',()=>{
 assert.equal(dishes.length,16);
 for(const d of dishes){assert.equal(d.available,true);assert.ok(fs.existsSync('server/web/'+d.image));}
});
