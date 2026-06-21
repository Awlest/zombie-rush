/* Zombie Rush - service worker (offline + maj automatique) */
var CACHE='zr-v2';
var ASSETS=['./','./index.html','./manifest.json','./icon-192.png','./icon-512.png'];

self.addEventListener('install',function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(ASSETS);}).catch(function(){}));
});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.map(function(k){if(k!==CACHE)return caches.delete(k);}));
  }).then(function(){return self.clients.claim();}));
});
self.addEventListener('fetch',function(e){
  if(e.request.method!=='GET')return;
  var isDoc=(e.request.mode==='navigate'||e.request.destination==='document');
  if(isDoc){
    // network-first : on prend la derniere version en ligne, cache en secours hors-ligne
    e.respondWith(
      fetch(e.request).then(function(res){
        var copy=res.clone();
        caches.open(CACHE).then(function(c){try{c.put('./index.html',copy);}catch(_){}});
        return res;
      }).catch(function(){return caches.match('./index.html').then(function(h){return h||caches.match('./');});})
    );
    return;
  }
  // cache-first pour le reste (icones, manifest)
  e.respondWith(
    caches.match(e.request).then(function(hit){
      return hit || fetch(e.request).then(function(res){
        var copy=res.clone();
        caches.open(CACHE).then(function(c){try{c.put(e.request,copy);}catch(_){}});
        return res;
      });
    })
  );
});
