// 當service worker在「安裝階段」時會觸發此事件
self.addEventListener('install', function(event) {
    console.log(event);
    //var para =  new URL(location).searchParams.get('para');
    //console.log('Custom parameter:', para);
    self.skipWaiting();    
    console.log("skip waiting");
});

// 當service worker在「激活階段」時會觸發此事件
self.addEventListener('activate', function(event) {
    console.log("activated");
    self.clients.matchAll({type: 'window'}).then(windowClients => {
        windowClients.forEach(windowClient => {
          windowClient.navigate(windowClient.url);
        });
      });
});