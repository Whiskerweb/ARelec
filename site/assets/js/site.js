(function(){
var d=document.documentElement,rm=matchMedia("(prefers-reduced-motion: reduce)").matches;
// apparitions au scroll (fondu + flou)
var els=document.querySelectorAll(".r");
if("IntersectionObserver" in window&&!rm){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px",threshold:.1});els.forEach(function(el){io.observe(el)})}
else els.forEach(function(el){el.classList.add("in")});
// compteurs
if("IntersectionObserver" in window&&!rm){var co=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;co.unobserve(e.target);var el=e.target,to=+el.dataset.count,suf=el.dataset.suffix||"",t0=performance.now();(function step(t){var p=Math.min(1,(t-t0)/1600),v=Math.round(to*(1-Math.pow(1-p,3)));el.textContent=v+suf;if(p<1)requestAnimationFrame(step)})(t0)})},{threshold:.6});document.querySelectorAll("[data-count]").forEach(function(el){co.observe(el)})}
// navigation
var nav=document.querySelector(".nav");function onS(){nav&&nav.classList.toggle("scrolled",scrollY>24)}addEventListener("scroll",onS,{passive:true});onS();
// tiroir mobile
var dr=document.getElementById("drawer"),bt=document.querySelector(".burger");if(!dr||!bt)return;
function open(){dr.hidden=false;requestAnimationFrame(function(){dr.classList.add("open")});document.body.classList.add("menu-open");bt.setAttribute("aria-expanded","true");dr.querySelector(".drawer-close").focus()}
function close(){dr.classList.remove("open");document.body.classList.remove("menu-open");bt.setAttribute("aria-expanded","false");setTimeout(function(){dr.hidden=true},300)}
bt.addEventListener("click",open);dr.querySelector(".drawer-close").addEventListener("click",close);
dr.addEventListener("click",function(e){if(e.target.closest("a"))close()});
addEventListener("keydown",function(e){if(e.key==="Escape"&&!dr.hidden)close()});
})();
