(()=>{
  const status = document.getElementById('network-status');
  const install = document.getElementById('install-app');
  function update(){if(status){status.hidden=navigator.onLine;}}
  window.addEventListener('online',update);window.addEventListener('offline',update);update();
  if('serviceWorker' in navigator && window.isSecureContext){navigator.serviceWorker.register('/service-worker.js').catch(()=>{});}
  let promptEvent;
  window.addEventListener('beforeinstallprompt',ev=>{ev.preventDefault();promptEvent=ev;if(install)install.hidden=false;});
  if(install) install.addEventListener('click',async()=>{if(!promptEvent)return;promptEvent.prompt();await promptEvent.userChoice;promptEvent=null;install.hidden=true;});
  window.addEventListener('appinstalled',()=>{if(install)install.hidden=true;});
})();
