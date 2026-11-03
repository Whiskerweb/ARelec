(function(){
var d=document.documentElement,rm=matchMedia("(prefers-reduced-motion: reduce)").matches;
// apparitions au scroll (fondu + flou)
var els=document.querySelectorAll(".r");
if("IntersectionObserver" in window&&!rm){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px",threshold:.1});els.forEach(function(el){io.observe(el)})}
else els.forEach(function(el){el.classList.add("in")});
// compteurs
if("IntersectionObserver" in window&&!rm){var co=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;co.unobserve(e.target);var el=e.target,to=+el.dataset.count,suf=el.dataset.suffix||"",t0=performance.now();(function step(t){var p=Math.min(1,(t-t0)/1600),v=Math.round(to*(1-Math.pow(1-p,3)));el.textContent=v+suf;if(p<1)requestAnimationFrame(step)})(t0)})},{threshold:.6});document.querySelectorAll("[data-count]").forEach(function(el){co.observe(el)})}
// carrousels
document.querySelectorAll(".carousel").forEach(function(c){
 var t=c.querySelector(".c-track"),pv=c.querySelector(".prev"),nx=c.querySelector(".next"),fill=c.querySelector(".c-fill"),cnt=c.querySelector(".c-count"),items=t.children,n=items.length,timer=null,hover=false;
 function step(){return items.length>1?items[1].offsetLeft-items[0].offsetLeft:t.clientWidth}
 function perView(){return Math.max(1,Math.round(t.clientWidth/step()))}
 function idx(){return Math.round(t.scrollLeft/step())}
 function max(){return t.scrollWidth-t.clientWidth-2}
 function upd(){var i=idx(),pvw=perView(),last=Math.min(n,i+pvw);pv.disabled=t.scrollLeft<=2;nx.disabled=t.scrollLeft>=max();fill.style.transform="scaleX("+(last/n)+")";cnt.textContent=String(last).padStart(2,"0")+" / "+String(n).padStart(2,"0")}
 function go(d){t.scrollBy({left:d*step(),behavior:rm?"auto":"smooth"})}
 pv.addEventListener("click",function(){go(-1);rest()});nx.addEventListener("click",function(){go(1);rest()});
 t.addEventListener("scroll",function(){requestAnimationFrame(upd)},{passive:true});addEventListener("resize",upd);
 t.addEventListener("keydown",function(e){if(e.key==="ArrowRight"){e.preventDefault();go(1)}if(e.key==="ArrowLeft"){e.preventDefault();go(-1)}});
 // glisser à la souris (le tactile défile nativement)
 var down=false,x0=0,s0=0,moved=false;
 t.addEventListener("pointerdown",function(e){if(e.pointerType!=="mouse")return;down=true;moved=false;x0=e.clientX;s0=t.scrollLeft});
 addEventListener("pointermove",function(e){if(!down)return;var dx=e.clientX-x0;if(Math.abs(dx)>4){moved=true;t.classList.add("drag")}t.scrollLeft=s0-dx});
 addEventListener("pointerup",function(){if(!down)return;down=false;if(!moved)return;t.classList.remove("drag");var i=Math.round(t.scrollLeft/step());t.scrollTo({left:i*step(),behavior:"smooth"});rest()});
 t.addEventListener("click",function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
 // défilement automatique, en pause au survol, au focus, et quand le carrousel n'est pas visible
 function tick(){if(hover||document.hidden)return;if(t.scrollLeft>=max())t.scrollTo({left:0,behavior:"smooth"});else go(1)}
 function start(){if(rm||timer)return;timer=setInterval(tick,5500)}
 function stop(){clearInterval(timer);timer=null}
 function rest(){stop();start()}
 c.addEventListener("mouseenter",function(){hover=true});c.addEventListener("mouseleave",function(){hover=false});
 c.addEventListener("focusin",function(){hover=true});c.addEventListener("focusout",function(){hover=false});
 if("IntersectionObserver" in window)new IntersectionObserver(function(es){es[0].isIntersecting?start():stop()},{threshold:.3}).observe(c);
 upd();
});
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
