/* Offline shell, plus content cached by the Save offline button. */
const SHELL='japao-pocket-shell-v2';
const CONTENT='japao-pocket-content-v2';
const ASSETS=['./','./index.html','./assets/style.css','./assets/app.js','./icons/icon.svg','./manifest.webmanifest','./data/days.json'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(SHELL).then(cache=>cache.addAll(ASSETS)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',event=>{event.waitUntil(Promise.all([caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('japao-pocket-') && ![SHELL,CONTENT].includes(k)).map(k=>caches.delete(k)))),self.clients.claim()]))});
self.addEventListener('fetch',event=>{const request=event.request;if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;event.respondWith((async()=>{const url=new URL(request.url);const content=await caches.open(CONTENT);const shell=await caches.open(SHELL);const isData=url.pathname.includes('/data/');if(isData){try{const response=await fetch(request);if(response.ok)await content.put(request,response.clone());return response}catch{return await content.match(request)||await shell.match(request)||Response.error()}}
return await content.match(request)||await shell.match(request)||await fetch(request).then(response=>{if(response.ok)shell.put(request,response.clone());return response}).catch(()=>shell.match('./index.html')||Response.error())})())});
