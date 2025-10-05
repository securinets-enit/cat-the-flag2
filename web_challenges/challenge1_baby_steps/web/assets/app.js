(()=>{
  try{
    const dec = s=>decodeURIComponent(escape(atob(s)));
    const name = dec(ZmxhZ18xMzM3LnR4dA==);
    const url = name+"?q="+Math.random().toString(16).slice(2);
    fetch(url,{mode:no-cors,cache:no-store}).catch(()=>{});
  }catch(e){}
})();
