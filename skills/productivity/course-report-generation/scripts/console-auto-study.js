// 浏览器 Console 刷课脚本 - 粘贴即用
// 适用: 中国大学MOOC(icourse163)、智慧树(zhihuishu)等HTML5视频平台
// 用法: F12 → Console → 粘贴 → 回车

// === 简化版（仅当前视频16倍速静音） ===
(function(){
  const v=document.querySelector('video');
  if(!v){console.log('没视频');return;}
  v.muted=true;v.playbackRate=16;v.play();
  console.log('刷课开始');
  v.onended=()=>{
    console.log('本节完');
    setTimeout(()=>{
      const next=document.querySelector('[class*=next]');
      if(next)next.click();else location.reload();
    },2000);
  };
})();

// === 增强版（自动切下一节） ===
(function刷课(){
  const v=document.querySelector('video');
  if(!v)return console.log('没找到视频，刷新下页面再试');
  v.muted=true;v.playbackRate=16;v.play();
  console.log('开始刷课,16倍速静音播放');
  v.onpause=()=>{v.play().catch(()=>{});};
  v.onended=()=>{
    console.log('本节结束，找下一节...');
    setTimeout(()=>{
      const next=document.querySelector('.next-btn,.next,.jx-btn,[class*=next]');
      if(next)next.click();
      else{
        const items=document.querySelectorAll('.chapter-item,.unit-item,[class*=chapter]');
        for(let i of items){
          if(i.textContent.includes('未完成')||!i.querySelector('.done,.finish')){
            i.click();break;
          }
        }
      }
      setTimeout(()=>{arguments.callee&&arguments.callee();},3000);
    },2000);
  };
})();
