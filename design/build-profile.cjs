/* Run: node design/build-profile.cjs
 * Dependencies: npm install --no-save sharp playwright marked
 * Optional: PROFILE_NODE_MODULES points to an existing dependency directory.
 */
const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
const { pathToFileURL } = require('node:url');
const deps = process.env.PROFILE_NODE_MODULES
  ? createRequire(path.join(process.env.PROFILE_NODE_MODULES, '__profile__.cjs')) : require;
const sharp = deps('sharp');
const { chromium } = deps('playwright');
const root = path.resolve(__dirname, '..');
const out = path.join(root, 'github-profile-assets', 'flow');
const esc = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const svg = (w,h,title,body,desc='') => `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-labelledby="title desc"><title id="title">${esc(title)}</title><desc id="desc">${esc(desc||title)}</desc>${body}</svg>`;
const text = (x,y,t,size=14,color='#202020',extras='') => `<text x="${x}" y="${y}" fill="${color}" font-family="Arial,Helvetica,sans-serif" font-size="${size}" ${extras}>${esc(t)}</text>`;
// Explicit serif helper keeps generated SVGs standalone without web fonts.
const display = (x,y,t,size=36,color='#202020',italic=false) => `<text x="${x}" y="${y}" fill="${color}" font-family="Georgia,Times New Roman,serif" font-size="${size}"${italic?' font-style="italic"':''}>${esc(t)}</text>`;
const line = (x1,y1,x2,y2,stroke='#d6d6d6',extra='') => `<path d="M${x1} ${y1}L${x2} ${y2}" stroke="${stroke}" fill="none" ${extra}/>`;
function ribbons(x=0,y=0,scale=1,stroke='#bebebe',opacity=.55) {
  let curves='';
  for(let i=0;i<12;i++) curves+=`<path d="M ${-40+i*4} ${80+i*6} C ${75+i*8} ${-40+i*7},${155+i*6} ${200-i*8},${260+i*6} ${86+i*3} S ${395+i*4} ${5+i*8},${470+i*5} ${120+i*6}"/>`;
  return `<g transform="translate(${x} ${y}) scale(${scale})" fill="none" stroke="${stroke}" stroke-width=".8" opacity="${opacity}">${curves}</g>`;
}
function section(file,number,label,title) {
  const content=`<rect width="1200" height="132" fill="#f2f2f2"/>${ribbons(810,-9,.8,'#a5a5a5',.42)}${text(36,37,`${number} / ${label.toUpperCase()}`,12,'#595959','letter-spacing="2.5"')}${display(34,88,title,38)}${line(36,113,1164,113)}`;
  fs.writeFileSync(path.join(out,`section-${file}.svg`),svg(1200,132,`${number} / ${label} — ${title}`,content));
  const mobile=`<rect width="720" height="166" fill="#f2f2f2"/>${ribbons(410,20,.6,'#a5a5a5',.35)}${text(26,41,`${number} / ${label.toUpperCase()}`,15,'#595959','letter-spacing="2"')}${display(24,105,title,39)}${line(26,144,694,144)}`;
  fs.writeFileSync(path.join(out,`section-${file}-mobile.svg`),svg(720,166,`${number} / ${label} — ${title}`,mobile));
}
const cards=[
  ['cdr','01','DATA & ANALYTICS','MyCDR','From records to understanding.'],
  ['portal','02','CUSTOMER OPERATIONS','EaseDial','A clearer view of operations.'],
  ['opensips','03','DEPLOYMENT ENGINEERING','OpenSIPS','Make the next deploy repeatable.'],
  ['freeswitch','04','FLEET AUTOMATION','FreeSWITCH','Bring consistency to the fleet.'],
  ['routeforge','05','WHOLESALE VOICE','RouteForge','Precision in every rate deck.'],
  ['health','06','PRODUCT ENGINEERING','Health Tracker','Make everyday progress visible.']
];
function diagram(kind) {
  const p='#707070',q='#b9b9b9';
  if(kind==='cdr') return `<g fill="none" stroke="${q}">${[0,1,2,3].map(i=>`<ellipse cx="462" cy="${54+i*22}" rx="44" ry="12"/>`).join('')}${line(418,54,418,120,q)}${line(506,54,506,120,q)}<path d="M360 112C387 112 381 76 407 76"/><path d="M519 98h26"/></g><circle cx="545" cy="98" r="3" fill="${p}"/>`;
  if(kind==='portal')return `<g fill="none" stroke="${q}"><rect x="356" y="48" width="178" height="102" rx="4"/><path d="M356 69h178M399 69v81M367 60h3m6 0h3m6 0h3"/><rect x="413" y="84" width="31" height="22"/><rect x="452" y="84" width="31" height="22"/><rect x="491" y="84" width="28" height="22"/><path d="M413 136l22-11 20 7 23-17 21 7 20-11"/></g>`;
  if(kind==='opensips')return `<g fill="none" stroke="${q}"><rect x="355" y="49" width="177" height="103" rx="4"/><path d="M355 72h177"/><path d="M373 90l8 7-8 7m15 0h23M373 119h46m-46 10h83m-83 10h65"/></g>${text(450,100,'SIP',15,p,'letter-spacing="3"')}`;
  if(kind==='freeswitch')return `<g fill="none" stroke="${q}">${[0,1,2].map(i=>`<rect x="${365+i*59}" y="${65-i*8}" width="44" height="81" rx="3"/><path d="M${373+i*59} ${81-i*8}h28m-28 10h28m-28 10h28"/><circle cx="${387+i*59}" cy="${131-i*8}" r="3"/>`).join('')}<path d="M387 156v10h118v-26m-59 26v-16"/></g>`;
  if(kind==='routeforge')return `<g fill="none" stroke="${q}"><path d="M368 103h32m0 0c35 0 27-45 61-45h47m-108 45h108m-108 0c35 0 27 45 61 45h47"/><circle cx="361" cy="103" r="7"/><circle cx="515" cy="58" r="7"/><circle cx="515" cy="103" r="7" fill="#202020" stroke="#202020"/><circle cx="515" cy="148" r="7"/></g>${text(446,91,'LCR 2',11,p,'letter-spacing="1"')}`;
  return `<g fill="none" stroke="${q}"><path d="M357 116h35l13-37 19 63 17-47 11 21h78"/><circle cx="446" cy="104" r="62" opacity=".6"/><path d="M364 153h165"/></g>`;
}
function card([file,num,label,title,subtitle]) {
  const content=`<rect width="560" height="206" fill="#eeeeee"/>${ribbons(260,83,.65,'#bebebe',.22)}${text(26,33,`${num} / ${label}`,10,'#626262','letter-spacing="1.8"')}${display(24,104,title,38)}${text(26,141,subtitle,13,'#565656')}${line(26,177,81,177,'#7e7e7e')}${text(530,183,num,12,'#7e7e7e','text-anchor="end"')}${diagram(file)}`;
  fs.writeFileSync(path.join(out,`project-${file}.svg`),svg(560,206,`${num} / ${title} — ${subtitle}`,content));
}
function systems() {
 const cols=[['01','ROUTE','Carrier traffic','SIP / RTP / Interconnects'],['02','OPERATE','Voice infrastructure','OpenSIPS / FreeSWITCH'],['03','UNDERSTAND','CDR & analytics','Quality / Cost / Margin'],['04','DELIVER','Customer operations','Portals / Reports / Tools']];
 let content=`<rect width="1200" height="300" fill="#f2f2f2"/>${ribbons(755,140,1,'#b4b4b4',.3)}`;
 cols.forEach(([n,label,title,sub],i)=>{const x=36+i*294;content+=text(x,46,n,12,'#6b6b6b','letter-spacing="2"')+text(x,85,label,13,'#202020','letter-spacing="2.2"')+display(x,133,title,24)+text(x,164,sub,13,'#595959');if(i<3)content+=line(x+218,80,x+270,80,'#a0a0a0')+`<path d="M${x+263} 76l7 4-7 4" fill="none" stroke="#a0a0a0"/>`;});
 content+=line(36,211,1164,211,'#acacac')+text(36,253,'OBSERVE / AUTOMATE / SECURE',12,'#595959','letter-spacing="2.4"')+text(1164,253,'Across every layer.',15,'#595959','text-anchor="end"');
 fs.writeFileSync(path.join(out,'systems-map.svg'),svg(1200,300,'From signal to understanding',content,'Carrier traffic → Voice infrastructure → CDR and analytics → Customer operations. Observability, automation, and security run across every layer.'));
 let mobile=`<rect width="720" height="474" fill="#f2f2f2"/>${ribbons(320,220,.8,'#b4b4b4',.3)}`;
 cols.forEach(([n,label,title,sub],i)=>{const x=28+(i%2)*352,y=Math.floor(i/2)*184;mobile+=text(x,y+36,`${n} / ${label}`,17,'#595959','letter-spacing="1.6"')+display(x,y+87,title,29)+text(x,y+122,sub,18,'#595959');});
 mobile+=line(28,382,692,382,'#acacac')+text(28,426,'OBSERVE / AUTOMATE / SECURE',17,'#595959','letter-spacing="1.8"');
 fs.writeFileSync(path.join(out,'systems-map-mobile.svg'),svg(720,474,'From signal to understanding',mobile));
}
function footer() {
 let content=`<rect width="1200" height="282" fill="#1c1c1c"/>${ribbons(701,9,1.2,'#bfbfbf',.34)}${ribbons(769,31,1.1,'#e4e4e4',.18)}${text(42,46,'A CONVERSATION IS A GOOD PLACE TO START.',11,'#b5b5b5','letter-spacing="2.4"')}${display(39,113,'Let’s build something',45,'#f1f1f1')}${display(39,166,'that lasts.',45,'#f1f1f1',true)}${text(42,227,'INFRASTRUCTURE / SECURITY / THOUGHTFUL SOFTWARE',12,'#c0c0c0','letter-spacing="1.5"')}${text(1158,241,'↗',38,'#e8e8e8','text-anchor="end"')}`;
 fs.writeFileSync(path.join(out,'footer-dark.svg'),svg(1200,282,'Let’s build something that lasts.',content,'Open a conversation about infrastructure, security, or thoughtful software.'));
 const mobile=`<rect width="720" height="346" fill="#1c1c1c"/>${ribbons(350,70,.9,'#bfbfbf',.26)}${text(28,44,'A CONVERSATION IS A GOOD PLACE TO START.',14,'#b5b5b5','letter-spacing="1.7"')}${display(26,119,'Let’s build something',49,'#f1f1f1')}${display(26,184,'that lasts.',49,'#f1f1f1',true)}${text(28,259,'INFRASTRUCTURE / SECURITY',16,'#c0c0c0','letter-spacing="1.5"')}${text(28,291,'THOUGHTFUL SOFTWARE',16,'#c0c0c0','letter-spacing="1.5"')}${text(670,302,'↗',40,'#e8e8e8','text-anchor="end"')}`;
 fs.writeFileSync(path.join(out,'footer-mobile-dark.svg'),svg(720,346,'Let’s build something that lasts.',mobile));
 const lightPalette={'#1c1c1c':'#f2f2f2','#bfbfbf':'#999999','#e4e4e4':'#b9b9b9','#b5b5b5':'#595959','#f1f1f1':'#202020','#c0c0c0':'#565656','#e8e8e8':'#202020'};
 const light=source=>source.replace(/#[0-9a-f]{6}/gi,color=>lightPalette[color.toLowerCase()]||color);
 fs.writeFileSync(path.join(out,'footer.svg'),svg(1200,282,'Let’s build something that lasts.',light(content),'Open a conversation about infrastructure, security, or thoughtful software.'));
 fs.writeFileSync(path.join(out,'footer-mobile.svg'),svg(720,346,'Let’s build something that lasts.',light(mobile)));
}
function darkVariants() {
 // Only authored vector colors change. Preserve every shape and text position.
 const palette={
  '#f2f2f2':'#171717','#eeeeee':'#1b1b1b','#202020':'#ededed',
  '#595959':'#bdbdbd','#626262':'#b4b4b4','#565656':'#c0c0c0',
  '#6b6b6b':'#b0b0b0','#707070':'#aaaaaa','#7e7e7e':'#999999',
  '#d6d6d6':'#3b3b3b','#a5a5a5':'#707070','#bebebe':'#666666',
  '#b9b9b9':'#737373','#b4b4b4':'#777777','#a0a0a0':'#808080',
  '#acacac':'#656565'
 };
 for(const file of fs.readdirSync(out).filter(f=>/^(section-|project-|systems-map)/.test(f)&&f.endsWith('.svg')&&!f.endsWith('-dark.svg'))) {
  const source=fs.readFileSync(path.join(out,file),'utf8');
  const themed=source.replace(/#[0-9a-f]{6}/gi,color=>palette[color.toLowerCase()]||color);
  fs.writeFileSync(path.join(out,file.replace('.svg','-dark.svg')),themed);
 }
}
async function main() {
 fs.mkdirSync(out,{recursive:true});
 if(fs.existsSync(path.join(__dirname,'hero-art.png'))) await sharp(path.join(__dirname,'hero-art.png')).jpeg({quality:90,mozjpeg:true}).toFile(path.join(__dirname,'hero-art.jpg'));
 section('practice','01','The practice','Clarity beneath complexity.');
 section('work','02','Selected work','Systems with a purpose.');
 section('systems','03','The throughline','From signal to understanding.');
 section('toolkit','04','The toolkit','Tools chosen for the work.');
 section('experiments','05','Beyond the day-to-day','Stay curious. Keep building.');
 cards.forEach(card);systems();footer();darkVariants();
 const markedModule=await import(pathToFileURL(deps.resolve('marked')).href);
 const readme=fs.readFileSync(path.join(root,'README.md'),'utf8');
 const markup=markedModule.marked.parse(readme).replaceAll('./github-profile-assets/','../github-profile-assets/');
 const style=fs.readFileSync(path.join(__dirname,'preview.css'),'utf8');
 fs.mkdirSync(path.join(root,'preview'),{recursive:true});
 // The preview control simulates prefers-color-scheme for picture sources as
 // well as page chrome. GitHub uses the unmodified README media queries.
 const themeScript=`function setTheme(dark){document.documentElement.dataset.theme=dark?'dark':'light';const button=document.querySelector('.preview-tools button');button.setAttribute('aria-pressed',String(dark));button.textContent=dark?'Light preview':'Dark preview';for(const source of document.querySelectorAll('picture source')){source.dataset.originalMedia ||= source.media;source.media=source.dataset.originalMedia.replace('(prefers-color-scheme: dark)',dark?'(min-width: 0px)':'(max-width: 0px)');}}setTheme(matchMedia('(prefers-color-scheme: dark)').matches);`;
 fs.writeFileSync(path.join(root,'preview','index.html'),`<!doctype html><html lang="en" data-theme="light"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Adityasiig — GitHub profile preview</title><style>${style}</style><nav class="preview-tools" aria-label="Preview controls"><span>ADITYASIIG <small>/ PROFILE PREVIEW</small></span><button type="button" aria-pressed="false" onclick="setTheme(document.documentElement.dataset.theme!=='dark')">Dark preview</button></nav><main class="markdown-body">${markup}</main><script>${themeScript}</script></html>`);
 const browser=await chromium.launch({headless:true,...(process.env.PROFILE_BROWSER_PATH?{executablePath:process.env.PROFILE_BROWSER_PATH}:{})});
 try {
  const page=await browser.newPage({viewport:{width:1440,height:830},deviceScaleFactor:1});
  await page.goto(pathToFileURL(path.join(__dirname,'hero.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  await page.locator('.cover').screenshot({path:path.join(out,'hero.png')});
  await page.setViewportSize({width:720,height:880});
  await page.locator('.cover').screenshot({path:path.join(out,'hero-mobile.png')});
  await page.goto(pathToFileURL(path.join(__dirname,'hero.html')).href+'?theme=dark');
  await page.evaluate(()=>document.fonts.ready);
  await page.locator('.cover').screenshot({path:path.join(out,'hero-mobile-dark.png')});
  await page.setViewportSize({width:1440,height:830});
  await page.locator('.cover').screenshot({path:path.join(out,'hero-dark.png')});
  await page.close();
  for(const [name,width,dark] of [['desktop',1120,false],['mobile',390,false],['dark',1120,true],['mobile-dark',390,true]]) {
   const p=await browser.newPage({viewport:{width,height:900},deviceScaleFactor:1});
   const errors=[];p.on('pageerror',e=>errors.push(String(e)));
   await p.emulateMedia({colorScheme:dark?'dark':'light'});
   await p.goto(pathToFileURL(path.join(root,'preview','index.html')).href);
   await p.evaluate(()=>document.fonts.ready);
   await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
   const audit=await p.evaluate(()=>({images:[...document.images].length,broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),overflow:document.documentElement.scrollWidth>innerWidth,theme:document.documentElement.dataset.theme,mobileArt:document.images[0].currentSrc.includes('hero-mobile'),footer:document.images[document.images.length-1].currentSrc.split('/').pop(),wrongTheme:[...document.querySelectorAll('.markdown-body img')].filter(i=>i.currentSrc.includes('-dark.')!==(document.documentElement.dataset.theme==='dark')).map(i=>i.currentSrc)}));
   await p.screenshot({path:path.join(root,'preview',`${name}.png`),fullPage:true});
   console.log(name,JSON.stringify({...audit,errors}));
   if(audit.broken.length||audit.overflow||errors.length||audit.wrongTheme.length) throw new Error(`${name} preview failed`);
   await p.getByRole('button',{name:dark?'Light preview':'Dark preview'}).click();
   await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
   const toggled=await p.evaluate(()=>[...document.images].every(i=>i.currentSrc.includes('-dark.')===(document.documentElement.dataset.theme==='dark')));
   if(!toggled)throw new Error(`${name} theme toggle failed`);
   // Restore the exact README media queries and verify native browser selection
   // independently of the local preview control.
   await p.evaluate(()=>{for(const s of document.querySelectorAll('picture source'))s.media=s.dataset.originalMedia;});
   await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
   const nativeSelection=await p.evaluate(expectedDark=>[...document.images].every(i=>i.currentSrc.includes('-dark.')===expectedDark),dark);
   if(!nativeSelection)throw new Error(`${name} native picture selection failed`);
   await p.close();
  }
 }finally{await browser.close();}
 console.log('Profile assets and previews generated.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
