#!/usr/bin/env python3
# Generateur du site statique ARELEC.
# HOME = scroll-snap (hero photo + metiers + avis + footer).
# SUBPAGES (metier + locales) = layout inspire de traaaction.com/portal :
#   subnav claire sticky, hero 2 colonnes, trust strip, 3 sections numerotees, recap CTA, footer.
import os, html, pathlib, datetime, json
from PIL import Image, ImageOps

ROOT = pathlib.Path("/Users/lucasroncey/Desktop/Projet Saas/Arelec")
SITE = ROOT/"site"; IMG = SITE/"assets/img"; CSS = SITE/"assets/css"
DOMAIN = "https://www.entreprise-arelec.fr"
PHONE_DISP = "02 98 40 20 43"; PHONE_TEL = "0298402043"; EMAIL = "contact@entreprise-arelec.fr"
SVG_PHONE='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
SVG_MAIL='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'
SVG_WA='<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2zm.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23-1.48 0-2.93-.39-4.19-1.15l-.3-.17-3.12.82.83-3.04-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24zM8.53 7.33c-.16 0-.43.06-.66.31-.22.25-.87.86-.87 2.07 0 1.22.89 2.39 1 2.56.14.17 1.76 2.67 4.25 3.73.59.27 1.05.42 1.41.53.59.19 1.13.16 1.56.1.48-.07 1.46-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.07-.1-.23-.16-.48-.27-.25-.14-1.47-.74-1.69-.82-.23-.08-.4-.12-.56.12-.17.25-.64.81-.78.97-.15.17-.29.19-.53.07-.26-.13-1.06-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.12-.24-.01-.39.11-.5.11-.11.27-.29.37-.44.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.11-.56-1.35-.77-1.84-.2-.48-.4-.42-.56-.43-.14 0-.3-.01-.47-.01z"/></svg>'
SVG_FB='<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12.07C22 6.51 17.52 2 12 2S2 6.51 2 12.07c0 5.02 3.66 9.18 8.44 9.93v-7.02H7.9v-2.91h2.54V9.84c0-2.51 1.49-3.89 3.78-3.89 1.09 0 2.24.19 2.24.19v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.88h2.77l-.44 2.91h-2.33V22c4.78-.75 8.43-4.91 8.43-9.93z"/></svg>'
for p in (IMG,CSS): p.mkdir(parents=True, exist_ok=True)

# ---------- images mutualisees ----------
def save(srcname, dst, w):
    im = ImageOps.exif_transpose(Image.open(ROOT/"assets/realisations"/srcname)).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
    im.save(IMG/dst, "JPEG", quality=80, optimize=True)

save("photo-10.jpg","hero.jpg",1800)
for n,name,wpx in [(7,"plomb.jpg",1100),(8,"chantier-plouider.jpg",1100),(10,"maison-bleue.jpg",1100),
                   (12,"eclairage.jpg",1100),(13,"sdb-bois.jpg",1100),(14,"confort.jpg",1100),
                   (15,"sdb-baignoire.jpg",1100),(16,"sdb-marbre.jpg",1100),(17,"douche-marbre.jpg",1100),
                   (18,"escalier-led.jpg",1100),(20,"sdb-bleue.jpg",1100),(21,"cablage.jpg",1100),
                   (22,"reno-cablage.jpg",1100)]:
    save(f"photo-{n:02d}.jpg", name, wpx)
# Logos : blanc (nav photo sombre) + sombre (subnav claire)
wl = Image.open(ROOT/"assets/logo-arelec-white.png").convert("RGBA"); wl.thumbnail((640,640), Image.LANCZOS); wl.save(IMG/"logo.png")
alpha = wl.split()[3]; dark = Image.new("RGBA", wl.size, (12,28,58,255)); dark.putalpha(alpha); dark.save(IMG/"logo-dark.png")

# ---------- CSS partage ----------
CSS_TXT = r"""@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--ink:#0c1c3a;--ink-soft:#46587a;--blue:#1457ff;--cyan:#0bb0ff;--paper:#fbfcfe;--r:28px;--glass-d:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.08))}
*{box-sizing:border-box;margin:0;padding:0}html,body{height:100%}
html,body{overflow-x:clip}img,video,svg{max-width:100%}
body{font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;background:var(--paper);color:var(--ink)}
a{color:inherit}
.snap{height:100vh;height:100svh;overflow-y:scroll;scroll-snap-type:y proximity;scroll-behavior:smooth;scrollbar-width:none}
.snap::-webkit-scrollbar{display:none}
.panel{position:relative;height:100vh;height:100svh;overflow:hidden;scroll-snap-align:start;scroll-snap-stop:always;display:flex;flex-direction:column;padding:clamp(16px,3.2vw,28px) clamp(18px,4vw,48px) clamp(24px,4vw,40px)}
.bg{position:absolute;inset:0;z-index:0;background-size:cover;background-position:center 46%;transform:scale(1.08);opacity:.4;transition:transform 1.1s ease,opacity 1.1s ease;background-image:linear-gradient(to bottom,rgba(8,15,30,.30),rgba(8,15,30,0) 26%,rgba(8,15,30,0) 42%,rgba(6,12,24,.82)),url('/assets/img/hero.jpg')}
.panel.visible .bg{transform:scale(1);opacity:1}
.reveal{opacity:0;transform:translateY(28px);transition:opacity .85s cubic-bezier(.2,.7,.2,1),transform .85s cubic-bezier(.2,.7,.2,1)}
.panel.visible .reveal{opacity:1;transform:none}
.panel.visible .d1{transition-delay:.05s}.panel.visible .d2{transition-delay:.15s}.panel.visible .d3{transition-delay:.27s}.panel.visible .d4{transition-delay:.39s}
.nav{position:relative;z-index:5;display:flex;align-items:center;justify-content:space-between;gap:16px}
.nav>a:first-child,.topnav>a:first-child,.subnav>a:first-child{flex:none;display:block}
.brand-img{height:clamp(40px,5.2vw,54px);width:auto;max-width:none;display:block;filter:drop-shadow(0 2px 12px rgba(0,0,0,.55))}
.topnav .logo-dark,.subnav .logo-dark{flex:none}
.navlinks{display:flex;gap:4px;padding:7px 10px;border-radius:999px;backdrop-filter:blur(20px) saturate(160%);-webkit-backdrop-filter:blur(20px) saturate(160%);background:var(--glass-d);border:1px solid rgba(255,255,255,.35);box-shadow:inset 0 1px 0 rgba(255,255,255,.55),0 12px 30px rgba(0,0,0,.28)}
.navlinks a{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:999px;text-decoration:none;color:#fff;font-size:14.5px;font-weight:500;text-shadow:0 1px 6px rgba(0,0,0,.3);white-space:nowrap;transition:.2s}
.navlinks a:hover,.navlinks a[aria-current]{background:rgba(255,255,255,.2)}
.btn{position:relative;display:inline-flex;align-items:center;justify-content:center;min-height:44px;gap:9px;padding:12px 22px;border-radius:999px;font-size:14.5px;font-weight:600;color:#fff;cursor:pointer;text-decoration:none;overflow:hidden;white-space:nowrap;backdrop-filter:blur(20px) saturate(160%);-webkit-backdrop-filter:blur(20px) saturate(160%);background:var(--glass-d);border:1px solid rgba(255,255,255,.4);box-shadow:inset 0 1px 0 rgba(255,255,255,.6),0 12px 30px rgba(0,0,0,.3)}
.btn::after{content:"";position:absolute;left:0;right:0;top:0;height:48%;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.4),transparent);pointer-events:none}
.btn.primary{padding:14px 26px;font-size:15px;color:#0c2a5e;background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(225,238,255,.78));border:1px solid rgba(255,255,255,.9);box-shadow:inset 0 1px 0 rgba(255,255,255,1),0 16px 36px rgba(0,0,0,.34)}
.btn.solid{color:#fff;background:linear-gradient(180deg,#3a7dff,#1654d8);border:1px solid rgba(255,255,255,.4);box-shadow:0 10px 22px rgba(20,87,255,.22),inset 0 1px 0 rgba(255,255,255,.35);backdrop-filter:none;-webkit-backdrop-filter:none}
.btn.solid::after{display:none}
.btn.line{color:#0c2a5e;background:rgba(255,255,255,.85);border:1px solid rgba(20,60,140,.18);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
.btn.line::after{display:none}
.burger{display:none;width:46px;height:46px;border-radius:14px;align-items:center;justify-content:center;cursor:pointer;backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);background:var(--glass-d);border:1px solid rgba(255,255,255,.4);padding:0;font:inherit;color:inherit}
.burger span{display:block;width:18px;height:2px;background:#fff;border-radius:2px;box-shadow:0 5px 0 #fff,0 -5px 0 #fff;transition:transform .25s,box-shadow .25s,background .25s}
.burger[aria-expanded="true"] span{background:transparent;box-shadow:none;transform:rotate(45deg)}
.burger[aria-expanded="true"] span::before,.burger[aria-expanded="true"] span::after{content:""}
.subnav .burger,.topnav .burger{display:none}
.subnav .burger span,.topnav .burger span{background:#0c1c3a;box-shadow:0 5px 0 #0c1c3a,0 -5px 0 #0c1c3a}
.subnav .burger,.topnav .burger{background:rgba(255,255,255,.6);border-color:rgba(15,40,90,.12)}
.subnav .burger[aria-expanded="true"] span,.topnav .burger[aria-expanded="true"] span{background:transparent;box-shadow:none}
#hero{color:#fff;background:#0a1322}
.spacer{flex:1;min-height:24px;position:relative;z-index:2}.content{position:relative;z-index:2}
.topline{display:flex;align-items:flex-end;justify-content:space-between;gap:clamp(20px,4vw,40px);flex-wrap:wrap}
.kicker{display:inline-flex;align-items:center;gap:9px;font-size:clamp(11.5px,1.6vw,13px);font-weight:600;letter-spacing:.02em;margin-bottom:16px;text-shadow:0 1px 8px rgba(0,0,0,.5)}
.kicker .dot{width:8px;height:8px;border-radius:50%;background:#36e07f;box-shadow:0 0 0 4px rgba(54,224,127,.25);flex:none}
h1{font-size:clamp(34px,7.5vw,66px);line-height:1.0;letter-spacing:-.035em;font-weight:600;text-shadow:0 4px 30px rgba(0,0,0,.5)}
h1 b{font-weight:700}
.hr{height:1px;background:linear-gradient(to right,rgba(255,255,255,.05),rgba(255,255,255,.45),rgba(255,255,255,.05));margin:clamp(20px,3vw,28px) 0 20px}
.bottom{display:flex;align-items:flex-start;justify-content:space-between;gap:clamp(20px,4vw,40px);flex-wrap:wrap}
.meta{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.chip{font-size:13.5px;font-weight:500;padding:11px 14px;min-height:44px;border-radius:999px;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.28);display:inline-flex;gap:7px;align-items:center;color:#fff;text-decoration:none}
.desc{max-width:440px;font-size:clamp(14px,1.8vw,15px);line-height:1.55;color:rgba(255,255,255,.94);text-align:right;text-shadow:0 1px 10px rgba(0,0,0,.5)}
.scrollhint{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);z-index:3;font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:#fff;opacity:.85;display:flex;flex-direction:column;align-items:center;gap:6px;animation:bob 2s ease-in-out infinite}
.scrollhint .arr{width:20px;height:20px;border-right:2px solid #fff;border-bottom:2px solid #fff;transform:rotate(45deg)}
@keyframes bob{0%,100%{transform:translate(-50%,0)}50%{transform:translate(-50%,7px)}}
.light{align-items:center;color:var(--ink);overflow-y:auto;padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(48px,7vh,90px);background:radial-gradient(42% 42% at 12% 8%,rgba(20,87,255,.16),transparent 60%),radial-gradient(46% 46% at 88% 16%,rgba(11,176,255,.16),transparent 62%),linear-gradient(160deg,#fff,#edf3ff)}
.sec{position:relative;z-index:2;max-width:1200px;margin:auto;width:100%}
.sechead{text-align:center;margin-bottom:clamp(36px,4.5vw,60px)}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--blue);padding:8px 16px;border-radius:999px;background:rgba(20,87,255,.07);border:1px solid rgba(20,87,255,.14);margin-bottom:22px}
.sec h2{font-size:clamp(28px,4.4vw,48px);font-weight:700;letter-spacing:-.03em;line-height:1.04}
.sec h2 em{font-style:normal;background:linear-gradient(110deg,var(--blue),var(--cyan));-webkit-background-clip:text;background-clip:text;color:transparent}
.sec .sub{margin:18px auto 0;font-size:clamp(15px,1.8vw,16.5px);color:var(--ink-soft);max-width:620px;line-height:1.6}
/* Trades — split layout: texte+CTA gauche, accordéon image droite */
.sec-split{display:grid;grid-template-columns:1.2fr 1fr;gap:clamp(28px,5vw,56px);align-items:center;max-width:1360px;margin:auto;width:100%}
.lead-col{max-width:720px}
.lead-col .trade-list{display:flex;flex-direction:column;gap:.08em;font-weight:800;letter-spacing:-.05em;line-height:1.04;font-size:clamp(54px,7.6vw,108px);margin:0 0 clamp(32px,3.5vw,44px);text-align:left;color:var(--ink)}
.lead-col .trade-list span{display:block;white-space:nowrap}
.lead-actions{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.lead-actions .btn{min-height:56px;font-size:16px;padding:16px 30px}
.accordion{display:flex;gap:14px;height:clamp(420px,62vh,560px);width:100%;--ease:cubic-bezier(.22,.61,.36,1)}
.acc{position:relative;flex:1;border-radius:26px;overflow:hidden;text-decoration:none;color:inherit;isolation:isolate;cursor:pointer;
 transition:flex .85s var(--ease),box-shadow .5s var(--ease);
 border:1px solid rgba(255,255,255,.55);
 box-shadow:0 30px 60px -28px rgba(20,60,140,.34),0 2px 6px rgba(20,60,140,.08);
 will-change:flex}
.acc::before{content:"";position:absolute;inset:0;border-radius:inherit;z-index:5;pointer-events:none;background:linear-gradient(180deg,rgba(255,255,255,.22),transparent 18%)}
.acc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .95s var(--ease),filter .6s ease;filter:brightness(.86) saturate(1.05);will-change:transform,filter}
.acc-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,16,32,.05) 0%,rgba(6,16,32,.45) 55%,rgba(6,12,24,.88) 100%);transition:opacity .5s ease}
.acc-rail{position:absolute;left:0;top:0;bottom:0;width:64px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:20px 0 22px;z-index:3;
 background:linear-gradient(180deg,rgba(6,18,38,.10),rgba(6,18,38,.55));
 border-right:1px solid rgba(255,255,255,.10);
 opacity:1;transform:none;
 transition:opacity .4s var(--ease) .2s,transform .55s var(--ease) .2s}
.acc-ic{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;font-size:20px;color:#fff;background:linear-gradient(160deg,rgba(255,255,255,.20),rgba(255,255,255,.06));backdrop-filter:blur(14px) saturate(160%);-webkit-backdrop-filter:blur(14px) saturate(160%);border:1px solid rgba(255,255,255,.35);box-shadow:inset 0 1px 0 rgba(255,255,255,.4)}
.acc-vt{writing-mode:vertical-rl;transform:rotate(180deg);color:#fff;font-weight:700;font-size:13.5px;letter-spacing:.22em;text-transform:uppercase;text-shadow:0 2px 12px rgba(0,0,0,.45)}
.acc-open{position:absolute;left:0;right:0;bottom:0;padding:clamp(22px,2.4vw,34px);color:#fff;z-index:3;opacity:0;pointer-events:none;transition:opacity .5s var(--ease);will-change:opacity;text-align:left}
.acc-open>*{opacity:0;transition:opacity .45s var(--ease)}
.acc-ic-lg{width:56px;height:56px;border-radius:17px;display:grid;place-items:center;font-size:24px;margin-bottom:14px;background:linear-gradient(160deg,rgba(255,255,255,.26),rgba(255,255,255,.08));backdrop-filter:blur(18px) saturate(160%);-webkit-backdrop-filter:blur(18px) saturate(160%);border:1px solid rgba(255,255,255,.45);box-shadow:inset 0 1px 0 rgba(255,255,255,.5),0 10px 22px rgba(0,0,0,.25)}
.acc-open h3{font-size:clamp(26px,2.8vw,34px);font-weight:700;letter-spacing:-.02em;line-height:1.06;margin-bottom:8px;text-shadow:0 2px 16px rgba(0,0,0,.4)}
.acc-open p{font-size:14.5px;line-height:1.55;margin-bottom:16px;max-width:380px;text-shadow:0 1px 8px rgba(0,0,0,.4)}
.acc-cta{display:inline-flex;align-items:center;gap:8px;font-size:13.5px;font-weight:700;letter-spacing:.02em;padding:11px 18px;border-radius:999px;color:#0c2a5e;background:linear-gradient(180deg,rgba(255,255,255,.98),rgba(225,238,255,.82));border:1px solid rgba(255,255,255,.95);box-shadow:inset 0 1px 0 #fff,0 10px 22px rgba(0,0,0,.22)}
/* Ouverture: par défaut (.is-open) + hover (le hover suit la souris) */
.acc.is-open,.acc:hover,.acc:focus-visible{flex:2.7}
.acc.is-open .acc-rail,.acc:hover .acc-rail,.acc:focus-visible .acc-rail{opacity:0;transform:translateX(-12px);transition-delay:0s,0s}
.acc.is-open .acc-open,.acc:hover .acc-open,.acc:focus-visible .acc-open{opacity:1;transition-delay:.6s;pointer-events:auto}
.acc.is-open .acc-ic-lg,.acc:hover .acc-ic-lg,.acc:focus-visible .acc-ic-lg{opacity:1;transition-delay:.65s}
.acc.is-open .acc-open h3,.acc:hover .acc-open h3,.acc:focus-visible .acc-open h3{opacity:1;transition-delay:.75s}
.acc.is-open .acc-open p,.acc:hover .acc-open p,.acc:focus-visible .acc-open p{opacity:1;transition-delay:.88s}
.acc.is-open .acc-cta,.acc:hover .acc-cta,.acc:focus-visible .acc-cta{opacity:1;transition-delay:1s}
.acc.is-open img,.acc:hover img,.acc:focus-visible img{transform:scale(1.05);filter:brightness(.78) saturate(1.1)}
/* Override: si on hover une autre carte, la carte par défaut se rétracte proprement */
.accordion:hover .acc.is-open:not(:hover):not(:focus-visible){flex:1}
.accordion:hover .acc.is-open:not(:hover):not(:focus-visible) .acc-rail{opacity:1;transform:none;transition-delay:.22s,.22s}
.accordion:hover .acc.is-open:not(:hover):not(:focus-visible) .acc-open{opacity:0;transition-delay:0s;pointer-events:none}
.accordion:hover .acc.is-open:not(:hover):not(:focus-visible) .acc-open>*{opacity:0;transition-delay:0s}
.accordion:hover .acc.is-open:not(:hover):not(:focus-visible) img{transform:none;filter:brightness(.86) saturate(1.05)}
/* === Carrousel avis Google (compact, hors snap) === */
.band-reviews{scroll-snap-align:none;padding:clamp(36px,5vh,64px) clamp(18px,4vw,48px);background:radial-gradient(60% 100% at 50% 0%,rgba(20,87,255,.06),transparent 60%),linear-gradient(180deg,#fff,#f5f9ff);color:var(--ink);border-top:1px solid rgba(20,87,255,.06);border-bottom:1px solid rgba(20,87,255,.06)}
.sec-reviews{max-width:1080px;margin:auto;width:100%;text-align:center}
.g-head{display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:clamp(18px,2.4vw,28px)}
.g-logo{font-family:'Inter',sans-serif;font-weight:700;font-size:clamp(26px,3vw,34px);letter-spacing:-.02em;line-height:1;display:inline-flex}
.g-stars-big{color:#FBBC05;font-size:clamp(16px,1.8vw,20px);letter-spacing:3px;line-height:1}
.g-sub-big{font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft)}
.g-carousel{position:relative;padding:0 clamp(0px,3vw,44px)}
.g-track{display:flex;gap:clamp(12px,1.4vw,18px);overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;padding:4px 4px 10px;scrollbar-width:none}
.g-track::-webkit-scrollbar{display:none}
.g-card{flex:0 0 clamp(240px,24vw,300px);scroll-snap-align:center;background:#fff;border-radius:14px;padding:16px 18px;text-align:left;border:1px solid rgba(15,40,90,.08);box-shadow:0 10px 22px -12px rgba(20,60,140,.16),0 1px 4px rgba(20,60,140,.05);transition:transform .3s var(--ease,cubic-bezier(.22,.61,.36,1)),box-shadow .3s ease;display:flex;flex-direction:column}
.g-card:hover{transform:translateY(-3px);box-shadow:0 22px 38px -18px rgba(20,60,140,.22)}
.g-card header{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.g-avatar{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;color:#fff;font-weight:700;font-size:15px;flex:none;font-family:'Inter',sans-serif}
.g-meta{display:flex;flex-direction:column;line-height:1.2;min-width:0}
.g-name{font-weight:600;font-size:13.5px;color:var(--ink)}
.g-sub{font-size:11.5px;color:var(--ink-soft);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.g-stars-small{color:#FBBC05;font-size:13px;letter-spacing:2px;margin-bottom:6px;line-height:1}
.g-card blockquote{margin:0;font-size:13px;line-height:1.5;color:var(--ink)}
.g-nav{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;background:#fff;border:1px solid rgba(15,40,90,.1);color:var(--ink);cursor:pointer;display:grid;place-items:center;font-size:22px;line-height:1;box-shadow:0 6px 14px rgba(20,60,140,.12);transition:.2s;z-index:5;font-family:inherit;padding:0 0 3px}
.g-nav:hover{background:var(--blue);color:#fff;border-color:var(--blue);box-shadow:0 8px 18px rgba(20,87,255,.28)}
.g-prev{left:-2px}.g-next{right:-2px}
.g-dots{display:flex;gap:7px;justify-content:center;margin-top:10px}
.g-dots button{width:7px;height:7px;border-radius:50%;border:none;background:rgba(120,140,175,.4);cursor:pointer;padding:0;transition:.25s}
.g-dots button.on{background:var(--blue);transform:scale(1.5);box-shadow:0 0 0 3px rgba(20,87,255,.14)}
@media (max-width:760px){.g-carousel{padding:0}.g-nav{display:none}.g-card{flex:0 0 78vw;max-width:280px}.g-track{padding-left:11vw;padding-right:11vw;scroll-padding-left:11vw;scroll-padding-right:11vw}}
.cta-band{scroll-snap-align:start;padding:clamp(40px,6vw,80px) clamp(20px,5vw,80px);display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;background:radial-gradient(60% 120% at 80% 0%,rgba(20,87,255,.12),transparent 60%),linear-gradient(160deg,#fff,#e9f1ff);border-top:1px solid rgba(20,87,255,.1);color:var(--ink)}
.cta-band h2{font-size:clamp(22px,3vw,34px);font-weight:700;letter-spacing:-.02em;line-height:1.08}
.cta-band p{color:var(--ink-soft);margin-top:8px;font-size:15px}
.cta-actions{display:flex;gap:12px;flex-wrap:wrap}
footer.site{scroll-snap-align:none;color:#dfe8f7;padding:clamp(40px,5vw,64px) clamp(20px,5vw,80px) 0;background:radial-gradient(60% 80% at 85% 0%,rgba(20,87,255,.18),transparent 60%),linear-gradient(160deg,#0c2750,#0a1c39 55%,#06101f)}
footer.site .fgrid{max-width:1320px;margin:0 auto;display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr 1fr;gap:clamp(18px,1.8vw,32px)}
footer.site .blogo{height:44px;width:auto;filter:drop-shadow(0 2px 12px rgba(0,0,0,.5));margin-bottom:16px;display:block}
footer.site .brand p{font-size:14px;line-height:1.6;color:#a9bcd9;max-width:300px}
footer.site .nap{margin-top:16px;font-size:14px;line-height:1.9}
footer.site .nap a{color:#fff;text-decoration:none;font-weight:600}footer.site .nap .muted{color:#8ea3c6}
footer.site h4{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#7fb0ff;margin-bottom:16px;font-weight:700}
footer.site ul{list-style:none;display:flex;flex-direction:column;gap:11px}
footer.site .fcol a{color:#bccbe4;text-decoration:none;font-size:14px;min-height:24px;display:inline-flex;align-items:center;transition:.2s}
footer.site .fcol a:hover{color:#fff}
footer.site .soc{display:inline-flex;gap:8px;margin-top:16px}
footer.site .soc a{width:44px;height:44px;border-radius:13px;display:grid;place-items:center;color:#fff;text-decoration:none;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2)}
footer.site .legal{max-width:1200px;margin:clamp(30px,4vw,48px) auto 0;border-top:1px solid rgba(255,255,255,.1);padding:20px 0 26px;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;font-size:12.5px;color:#8ea3c6}
footer.site .legal a{color:#a9bcd9;text-decoration:none}footer.site .legal a:hover{color:#fff}
.dots{position:fixed;right:18px;top:50%;transform:translateY(-50%);z-index:30;display:flex;flex-direction:column;gap:6px}
.dots button{position:relative;width:40px;height:30px;border:none;cursor:pointer;padding:0;background:transparent}
.dots button::before{content:"";position:absolute;inset:0;margin:auto;width:9px;height:9px;border-radius:50%;background:rgba(120,140,175,.55);transition:.3s}
.dots button.on::before{background:var(--blue);transform:scale(1.5);box-shadow:0 0 0 4px rgba(20,87,255,.16)}
a:focus-visible,button:focus-visible{outline:2px solid var(--blue);outline-offset:3px;border-radius:14px}
#hero a:focus-visible{outline-color:#fff}
@media (max-width:980px){.sec-split{grid-template-columns:1fr;gap:32px;max-width:560px}.lead-col{max-width:100%;text-align:center;margin:0 auto}.lead-col .trade-list{text-align:center;align-items:center;font-size:clamp(46px,12vw,78px)}.lead-actions{justify-content:center}.accordion{flex-direction:column;height:auto;gap:14px}.acc{flex:none!important;height:230px}.acc .acc-rail{opacity:0!important;transform:none!important;width:100%;height:auto;flex-direction:row;justify-content:flex-start;gap:14px;padding:14px 18px;background:linear-gradient(90deg,rgba(6,18,38,.55),rgba(6,18,38,.15));border-right:none;border-bottom:1px solid rgba(255,255,255,.1)}.acc .acc-vt{writing-mode:horizontal-tb;transform:none}.acc .acc-open{left:0;right:0;padding:20px;opacity:1!important;transform:none!important}.acc .acc-open>*{opacity:1!important;transition:none}.acc img{transform:scale(1.02);filter:brightness(.72) saturate(1.12)}.reviews{grid-template-columns:1fr;max-width:520px;margin:0 auto}footer.site .fgrid{grid-template-columns:1fr 1fr}footer.site .brand{grid-column:1/-1}}
@media (max-width:900px){.navlinks{display:none}.burger{display:flex}.nav>.btn{display:none}.desc{text-align:left}}
@media (max-width:760px){.dots{display:none}.scrollhint{display:none}}
@media (max-width:560px){.topline{flex-direction:column;align-items:stretch}.topline .btn.primary{width:100%}.bottom{flex-direction:column-reverse;gap:18px}.desc{text-align:left;max-width:100%}h1{font-size:clamp(30px,9vw,46px)}.cta-band{flex-direction:column;align-items:flex-start}.cta-actions{width:100%}.cta-band .btn{flex:1}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition-duration:.001ms!important;scroll-behavior:auto!important}.reveal{opacity:1!important;transform:none!important}.bg{transform:none!important;opacity:1!important}}

/* ===== SUBPAGES (Traaction-inspired) ===== */
.sub-shell{background:var(--paper);min-height:100vh}
.subnav{position:sticky;top:0;z-index:40;backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);background:rgba(255,255,255,.78);border-bottom:1px solid rgba(15,40,90,.08);padding:12px clamp(18px,4vw,40px);display:flex;align-items:center;justify-content:space-between;gap:16px}
.subnav .logo-dark{height:38px;width:auto;display:block}
.subnav nav{display:flex;align-items:center;gap:4px}
.subnav nav a{display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border-radius:999px;text-decoration:none;color:var(--ink);font-size:14px;font-weight:500;transition:.2s}
.subnav nav a:hover,.subnav nav a[aria-current]{background:rgba(20,87,255,.08);color:var(--blue)}
.subnav .ctas{display:flex;gap:10px;align-items:center}
.subnav .ctas a.tel{font-size:14px;font-weight:600;color:var(--ink);text-decoration:none;padding:0 10px;min-height:44px;display:inline-flex;align-items:center}
.subnav .ctas a.tel:hover{color:var(--blue)}
.subhero{padding:clamp(40px,7vh,90px) clamp(18px,5vw,80px) clamp(40px,6vh,80px);background:radial-gradient(42% 60% at 12% -10%,rgba(20,87,255,.055),transparent 60%),radial-gradient(40% 50% at 95% 110%,rgba(11,176,255,.055),transparent 60%),var(--paper);position:relative;overflow:hidden}
.subhero .wrap{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(28px,5vw,60px);align-items:center}
.crumb{font-size:12.5px;color:var(--ink-soft);margin-bottom:16px}
.crumb a{color:var(--ink-soft);text-decoration:none}.crumb a:hover{color:var(--blue)}
.eyebrow-blue{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--blue);padding:7px 14px;border-radius:999px;background:rgba(20,87,255,.07);border:1px solid rgba(20,87,255,.14);margin-bottom:18px}
.subhero h1{font-size:clamp(34px,5.6vw,64px);line-height:1.02;letter-spacing:-.035em;color:var(--ink);text-shadow:none;font-weight:600}
.subhero h1 b{font-weight:800;color:var(--ink)}
.subhero .lead{margin-top:18px;font-size:clamp(15px,1.8vw,17.5px);color:var(--ink-soft);line-height:1.6;max-width:520px}
.subhero .lead a{color:var(--blue);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1.5px;font-weight:600;transition:color .2s}
.subhero .lead a:hover{color:#0a3eb8;text-decoration-thickness:2px}
.feat p a{color:var(--blue);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1.5px;font-weight:600;transition:color .2s}
.feat p a:hover{color:#0a3eb8}
.subhero .actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.imgcard{position:relative;border-radius:28px;overflow:hidden;background:linear-gradient(165deg,rgba(255,255,255,.7),rgba(255,255,255,.42));border:1px solid rgba(255,255,255,.85);box-shadow:inset 0 1px 0 rgba(255,255,255,.95),0 30px 60px -28px rgba(20,60,140,.26)}
.imgcard img{width:100%;height:100%;object-fit:cover;display:block}
.imgcard::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(10,20,40,.25),transparent 50%)}
.subhero .imgcard{aspect-ratio:4/5}
.subhero .float{position:absolute;left:-18px;bottom:24px;padding:12px 16px;border-radius:16px;font-size:13px;font-weight:600;color:var(--ink);background:linear-gradient(165deg,rgba(255,255,255,.9),rgba(255,255,255,.62));backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);border:1px solid rgba(255,255,255,.95);box-shadow:0 18px 36px rgba(20,60,140,.22);display:flex;align-items:center;gap:8px}
.subhero .float .stars{color:#ffb400}
.trust{padding:22px clamp(18px,5vw,80px);background:#fff;border-top:1px solid rgba(15,40,90,.06);border-bottom:1px solid rgba(15,40,90,.06)}
.trust .wrap{max-width:1200px;margin:0 auto;display:flex;flex-wrap:wrap;justify-content:space-between;gap:18px}
.trust .item{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:var(--ink)}
.trust .item .ic{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:rgba(20,87,255,.1);color:var(--blue);font-size:14px;font-weight:800}
.feat{padding:clamp(50px,8vh,100px) clamp(18px,5vw,80px)}
.feat:nth-of-type(even){background:linear-gradient(180deg,rgba(20,87,255,.018),transparent)}
.feat .wrap{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,5vw,70px);align-items:center}
.feat.flip .wrap > :first-child{order:2}
.feat .num{display:inline-flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;letter-spacing:.16em;color:var(--blue);padding:8px 14px;border-radius:999px;background:linear-gradient(165deg,rgba(255,255,255,.78),rgba(255,255,255,.46));backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);border:1px solid rgba(20,87,255,.22);box-shadow:inset 0 1px 0 #fff,0 8px 18px rgba(20,60,140,.10);margin-bottom:16px}
.feat h2{font-size:clamp(28px,3.6vw,40px);font-weight:700;letter-spacing:-.025em;line-height:1.08;margin-bottom:16px;color:var(--ink)}
.feat p{font-size:16px;line-height:1.65;color:var(--ink-soft);margin-bottom:22px;max-width:520px}
.feat ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:11px 18px;max-width:560px}
.feat li{display:flex;gap:9px;align-items:flex-start;font-size:14.5px;color:var(--ink);font-weight:500;line-height:1.45}
.feat li::before{content:"";width:7px;height:7px;border-radius:50%;background:#16c172;margin-top:7px;flex:none;box-shadow:0 0 0 3px rgba(22,193,114,.16)}
.feat .imgcard{aspect-ratio:5/4}
.feat .tag{position:absolute;top:18px;left:18px;font-size:12px;font-weight:700;padding:7px 12px;border-radius:999px;color:#0c2a5e;background:linear-gradient(165deg,rgba(255,255,255,.92),rgba(255,255,255,.7));backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.9);z-index:2}
.recap{padding:clamp(50px,8vh,90px) clamp(18px,5vw,80px);text-align:center;background:radial-gradient(60% 80% at 50% 0%,rgba(20,87,255,.08),transparent 60%),linear-gradient(160deg,#fff,#edf3ff)}
.recap h2{font-size:clamp(28px,4vw,46px);font-weight:700;letter-spacing:-.03em;line-height:1.04;max-width:780px;margin:0 auto 16px;color:var(--ink)}
.recap p{font-size:16px;color:var(--ink-soft);max-width:560px;margin:0 auto 28px;line-height:1.55}
.recap .actions{display:inline-flex;gap:12px;flex-wrap:wrap;justify-content:center}
.faq{padding:clamp(50px,8vh,90px) clamp(18px,5vw,80px);background:#fff;border-top:1px solid rgba(15,40,90,.06)}
.faq .wrap-faq{max-width:860px;margin:0 auto}
.faq .eyebrow-blue{margin-bottom:10px}
.faq h2{font-size:clamp(26px,3.6vw,40px);font-weight:700;letter-spacing:-.028em;line-height:1.1;color:var(--ink);margin-bottom:28px}
.faq-list{display:flex;flex-direction:column;gap:10px}
.faq-q{border:1px solid rgba(15,40,90,.1);border-radius:14px;background:linear-gradient(180deg,#fff,#fafcff);transition:border-color .2s}
.faq-q[open]{border-color:rgba(20,87,255,.32);box-shadow:0 4px 18px rgba(20,87,255,.06)}
.faq-q summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:18px;padding:18px 22px;font-weight:600;font-size:clamp(15.5px,1.6vw,17px);color:var(--ink);line-height:1.4;min-height:44px}
.faq-q summary::-webkit-details-marker{display:none}
.faq-q-icon{flex:0 0 auto;width:28px;height:28px;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;background:rgba(20,87,255,.08);color:var(--blue);font-weight:700;font-size:18px;line-height:1;transition:transform .25s}
.faq-q[open] .faq-q-icon{transform:rotate(45deg);background:var(--blue);color:#fff}
.faq-a{padding:0 22px 20px;font-size:15.5px;line-height:1.65;color:var(--ink-soft)}
@media (max-width:560px){.faq-q summary{padding:16px 18px;font-size:15px}.faq-a{padding:0 18px 18px;font-size:14.5px}}
@media (max-width:980px){.subnav nav{display:none}.subhero .wrap,.feat .wrap{grid-template-columns:1fr}.subhero .imgcard{aspect-ratio:16/11;max-width:560px;margin:0 auto}.feat .imgcard{aspect-ratio:16/11}.feat.flip .wrap > :first-child{order:0}.feat ul{grid-template-columns:1fr}.feat .num{font-size:88px}}
@media (max-width:560px){.subhero{padding-left:18px;padding-right:18px}.recap .actions .btn{width:100%}}
.areas{padding:clamp(50px,8vh,90px) clamp(18px,5vw,80px);background:#fff;border-top:1px solid rgba(15,40,90,.06)}
.areas .wrap{max-width:900px;margin:0 auto;text-align:center}
.areas h2{font-size:clamp(26px,3.6vw,38px);font-weight:700;letter-spacing:-.025em;line-height:1.12;margin-bottom:18px;color:var(--ink)}
.areas p{font-size:clamp(15.5px,1.9vw,17.5px);line-height:1.75;color:var(--ink-soft);max-width:720px;margin:0 auto 12px}
.areas p a{color:var(--blue);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1.5px;font-weight:600;transition:color .2s}
.areas p a:hover{color:#0a3eb8;text-decoration-thickness:2px}
.areas .pills{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:22px}
.areas .pills a{font-size:14px;font-weight:600;color:var(--blue);padding:9px 16px;border-radius:999px;background:rgba(20,87,255,.08);border:1px solid rgba(20,87,255,.18);text-decoration:none;transition:.2s}
.areas .pills a:hover{background:var(--blue);color:#fff}
.topnav{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px clamp(18px,4vw,40px);backdrop-filter:blur(22px) saturate(180%);-webkit-backdrop-filter:blur(22px) saturate(180%);background:rgba(255,255,255,.78);border-bottom:1px solid rgba(15,40,90,.08);transform:translateY(-100%);transition:transform .45s cubic-bezier(.2,.7,.2,1);will-change:transform}
.topnav.visible{transform:translateY(0)}
.topnav .logo-dark{height:36px;width:auto;display:block}
.topnav nav{display:flex;align-items:center;gap:4px}
.topnav nav a{display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border-radius:999px;text-decoration:none;color:var(--ink);font-size:14px;font-weight:500;transition:.2s}
.topnav nav a:hover{background:rgba(20,87,255,.08);color:var(--blue)}
.topnav .ctas{display:flex;gap:10px;align-items:center}
.topnav .ctas .tel{font-size:14px;font-weight:600;color:var(--ink);text-decoration:none;padding:0 10px;min-height:44px;display:inline-flex;align-items:center}
.topnav .ctas .tel:hover{color:var(--blue)}
@media (max-width:980px){.topnav nav{display:none}.topnav .burger{display:flex}.subnav .burger{display:flex}}
@media (max-width:560px){.topnav .ctas .tel span.tel-label,.subnav .ctas .tel span.tel-label{display:none}.topnav .ctas .tel,.subnav .ctas .tel{min-width:44px;justify-content:center;padding:0 8px}
  /* Bottom CTA bar prend déjà tel+estimer en mobile → on libère la place dans la nav */
  .topnav .ctas .tel,.subnav .ctas .tel,.topnav .ctas .btn.solid,.subnav .ctas .btn.solid{display:none}
  .topnav,.subnav{padding-left:14px;padding-right:14px}
}
.contact-hero{padding:clamp(50px,8vh,90px) clamp(18px,5vw,80px) clamp(20px,4vh,40px);text-align:center;background:radial-gradient(42% 60% at 50% 0%,rgba(20,87,255,.06),transparent 60%),var(--paper)}
.contact-hero .wrap-c{max-width:760px;margin:0 auto}
.contact-hero .crumb{justify-content:center;display:flex;margin-bottom:14px}
.contact-hero h1{font-size:clamp(34px,5.2vw,58px);line-height:1.04;letter-spacing:-.035em;color:var(--ink);font-weight:600;text-shadow:none}
.contact-hero h1 b{font-weight:800;color:var(--ink)}
.contact-hero .lead{margin-top:16px;font-size:clamp(15px,1.8vw,17px);color:var(--ink-soft);line-height:1.55}
.contact-methods{padding:clamp(20px,3vh,40px) clamp(18px,5vw,80px) clamp(40px,5vh,60px);background:var(--paper)}
.contact-methods .wrap-c{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2vw,24px)}
.cmethod{display:flex;align-items:center;gap:18px;padding:clamp(20px,2.2vw,28px);border-radius:24px;text-decoration:none;color:var(--ink);
 background:linear-gradient(165deg,rgba(255,255,255,.66),rgba(255,255,255,.4));backdrop-filter:blur(26px) saturate(180%);-webkit-backdrop-filter:blur(26px) saturate(180%);
 border:1px solid rgba(255,255,255,.85);box-shadow:inset 0 1px 0 rgba(255,255,255,.95),0 24px 50px -28px rgba(20,60,140,.28);
 transition:transform .3s cubic-bezier(.2,.7,.2,1),box-shadow .3s ease}
.cmethod:hover{transform:translateY(-4px);box-shadow:inset 0 1px 0 rgba(255,255,255,.95),0 36px 64px -30px rgba(20,60,140,.36)}
.cm-icon{width:54px;height:54px;border-radius:16px;display:grid;place-items:center;font-size:24px;flex:none;background:linear-gradient(160deg,rgba(20,87,255,.12),rgba(11,176,255,.12));border:1px solid rgba(20,87,255,.18);color:var(--blue)}
.cmethod-whatsapp .cm-icon{background:linear-gradient(160deg,rgba(37,211,102,.18),rgba(37,211,102,.10));border-color:rgba(37,211,102,.30);color:#22a85a}
.cm-label{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft);font-weight:700;margin-bottom:4px}
.cm-value{font-size:17px;font-weight:700;color:var(--ink)}
.ic{flex:none;display:inline-block;vertical-align:middle}
.cm-icon .ic{width:26px;height:26px;display:block}
.soc a .ic{width:18px;height:18px;display:block}
.chip .ic,.tel .ic{width:14px;height:14px;display:inline-block}
.btn .ic,.mca .ic,.md-tel-ic .ic{width:16px;height:16px;display:inline-block;flex:none}
.contact-form-section{padding:clamp(40px,6vh,80px) clamp(18px,5vw,80px) clamp(60px,8vh,100px);background:linear-gradient(180deg,rgba(20,87,255,.025),transparent),var(--paper)}
.contact-form-section .wrap-c{max-width:720px;margin:0 auto;text-align:center}
.contact-form-section h2{font-size:clamp(26px,3.6vw,38px);font-weight:700;letter-spacing:-.025em;line-height:1.12;margin-bottom:12px;color:var(--ink)}
.contact-form-section .sub{font-size:15px;color:var(--ink-soft);margin-bottom:32px}
.cform{display:flex;flex-direction:column;gap:16px;text-align:left}
.cfrow{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.cform label{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:600;color:var(--ink);letter-spacing:.02em}
.cform input,.cform textarea{font:inherit;font-size:16px;font-weight:400;padding:13px 16px;min-height:48px;border-radius:14px;border:1px solid rgba(15,40,90,.12);background:rgba(255,255,255,.85);color:var(--ink);transition:border .2s,box-shadow .2s,background .2s;outline:none}
.cform input:focus,.cform textarea:focus{border-color:var(--blue);box-shadow:0 0 0 4px rgba(20,87,255,.12);background:#fff}
.cform textarea{resize:vertical;min-height:130px;line-height:1.5;font-family:inherit}
.cform button{align-self:flex-start;margin-top:8px;font-size:15px}
.cform-foot{font-size:12.5px;color:var(--ink-soft);text-align:center;margin-top:8px}
@media (max-width:880px){.contact-methods .wrap-c{grid-template-columns:1fr;max-width:520px}}
@media (max-width:560px){.cfrow{grid-template-columns:1fr}.cform button{align-self:stretch;width:100%}}
.gallery-section{position:relative;padding:clamp(40px,6vh,80px) clamp(18px,5vw,80px) clamp(60px,8vh,100px);background:var(--paper)}
.gallery-section .wrap-g{max-width:1280px;margin:0 auto;position:relative;z-index:1}
.gradual-blur{isolation:isolate;overflow:hidden;pointer-events:none}
.gradual-blur[data-target="page"]{opacity:0;transition:opacity .28s ease-out}
.gradual-blur[data-target="page"].on{opacity:1}
.gradual-blur-inner{position:relative;width:100%;height:100%;pointer-events:none}
.gradual-blur-inner>div{position:absolute;inset:0;pointer-events:none}
@media (max-width:760px){.gradual-blur[data-pos="bottom"],.gradual-blur[data-pos="top"]{height:7rem!important}.gradual-blur[data-target="page"]{display:none!important}}
@media (max-width:560px){.gradual-blur[data-pos="bottom"],.gradual-blur[data-pos="top"]{height:5rem!important}}
.gallery{column-count:3;column-gap:clamp(16px,1.8vw,24px)}
.rcard{break-inside:avoid;margin:0 0 clamp(16px,1.8vw,24px);border-radius:22px;overflow:hidden;
 background:linear-gradient(165deg,rgba(255,255,255,.66),rgba(255,255,255,.4));backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);
 border:1px solid rgba(255,255,255,.85);box-shadow:inset 0 1px 0 rgba(255,255,255,.95),0 22px 44px -24px rgba(20,60,140,.24);
 transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s ease;position:relative;display:block}
.rcard:hover{transform:translateY(-6px);box-shadow:inset 0 1px 0 rgba(255,255,255,.95),0 36px 60px -24px rgba(20,60,140,.34)}
.rcard img{display:block;width:100%;height:auto}
.rcard figcaption{padding:14px 18px 16px;display:flex;flex-direction:column;gap:4px}
.rcard .rkind{font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--blue)}
.rcard .rloc{font-size:14px;color:var(--ink);font-weight:600;line-height:1.4}
@media (max-width:880px){.gallery{column-count:2}}
@media (max-width:560px){.gallery{column-count:1;max-width:480px;margin:0 auto}}

/* ===== FALLING TEXT PANEL (matter-js physics on panel background) ===== */
.panel.falling{height:clamp(360px,46vh,480px);min-height:360px;max-height:520px;justify-content:stretch;align-items:stretch;overflow:hidden;padding:0;position:relative;flex-shrink:0}
.panel.falling .falling-stage{position:absolute;inset:0;pointer-events:none}
.panel.falling .falling-text{position:absolute;inset:0;padding:clamp(32px,5vh,60px) clamp(32px,6vw,100px);font-size:clamp(20px,2.8vw,38px);font-weight:700;letter-spacing:-.02em;line-height:1.25;color:var(--ink);display:flex;align-items:flex-start;justify-content:center;flex-wrap:wrap;text-align:center;pointer-events:none;z-index:2;gap:6px 12px}
.panel.falling .falling-text .word{display:inline-block;user-select:none;will-change:transform;pointer-events:none}
.panel.falling .falling-text .word.hl{background:linear-gradient(110deg,var(--blue),var(--cyan));-webkit-background-clip:text;background-clip:text;color:transparent}
.panel.falling .falling-stage canvas{position:absolute;inset:0;z-index:1;pointer-events:auto;display:block;cursor:grab;touch-action:none}
.panel.falling .falling-stage.grabbing canvas{cursor:grabbing}
@media (max-width:760px){.panel.falling{height:clamp(320px,42vh,420px)}.panel.falling .falling-text{font-size:clamp(18px,4.4vw,28px);padding:24px 20px;gap:5px 10px}}
@media (max-width:560px){.panel.falling{height:clamp(280px,38vh,360px)}.panel.falling .falling-text{font-size:clamp(16px,5vw,22px);padding:20px 14px;gap:4px 8px}}

/* ===== MOBILE: scroll naturel (snap désactivé) + section physics masquée ===== */
@media (max-width:760px){
  .snap{height:auto;overflow:visible;scroll-snap-type:none;scroll-behavior:auto}
  .panel{height:auto;min-height:auto;scroll-snap-align:none;scroll-snap-stop:normal;overflow:visible}
  #hero{min-height:100svh}
  .panel.light{padding-top:clamp(56px,9vh,90px);padding-bottom:clamp(56px,9vh,90px)}
  .panel.falling{display:none}
  .cta-band,footer.site,.band-reviews{scroll-snap-align:none}
}

/* ===== MOBILE DRAWER (refonte premium ARELEC) ===== */
.mdrawer{position:fixed;inset:0;z-index:60;display:flex;flex-direction:column;gap:18px;padding:calc(18px + env(safe-area-inset-top)) 16px calc(18px + env(safe-area-inset-bottom));background:radial-gradient(60% 40% at 90% -10%,rgba(20,87,255,.24),transparent 62%),radial-gradient(50% 40% at -10% 105%,rgba(11,176,255,.18),transparent 62%),linear-gradient(160deg,#0c2750,#0a1c39 55%,#06101f);backdrop-filter:blur(30px) saturate(160%);-webkit-backdrop-filter:blur(30px) saturate(160%);transform:translateY(-100%);transition:transform .38s cubic-bezier(.2,.7,.2,1);overflow-y:auto;will-change:transform;color:#fff}
.mdrawer.open{transform:translateY(0)}
.md-head{display:flex;align-items:center;justify-content:space-between;gap:12px;flex:none}
.md-logo{height:32px;width:auto;filter:drop-shadow(0 2px 12px rgba(0,0,0,.5));display:block}
.mdrawer-close{position:static;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.06);color:#fff;font-size:24px;line-height:1;cursor:pointer;display:grid;place-items:center;padding:0 0 2px;transition:background .2s,border-color .2s}
.mdrawer-close:hover,.mdrawer-close:focus-visible{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.32)}
.md-tagline{font-size:11.5px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.55);display:flex;align-items:center;gap:9px;padding:0 4px}
.md-tagline .pulse{width:7px;height:7px;border-radius:50%;background:#36e07f;box-shadow:0 0 0 3px rgba(54,224,127,.22);flex:none}
.md-section{display:flex;flex-direction:column;gap:8px}
.md-label{font-size:11px;font-weight:700;letter-spacing:.20em;text-transform:uppercase;color:#7fb0ff;padding:0 6px 4px;display:flex;align-items:center;gap:10px}
.md-label::after{content:"";flex:1;height:1px;background:linear-gradient(to right,rgba(127,176,255,.35),transparent)}
.md-trade{display:flex;align-items:center;gap:14px;padding:12px 14px 12px 12px;border-radius:18px;text-decoration:none;color:#fff;background:linear-gradient(165deg,rgba(255,255,255,.10),rgba(255,255,255,.025));border:1px solid rgba(255,255,255,.12);box-shadow:inset 0 1px 0 rgba(255,255,255,.10),0 6px 14px rgba(0,0,0,.18);transition:transform .25s cubic-bezier(.2,.7,.2,1),background .25s,border-color .25s;min-height:64px}
.md-trade:active{transform:scale(.985)}
.md-trade:hover,.md-trade:focus-visible{background:linear-gradient(165deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border-color:rgba(255,255,255,.22)}
.md-ic{width:44px;height:44px;flex:none;border-radius:13px;display:grid;place-items:center;font-size:20px;background:linear-gradient(160deg,rgba(20,87,255,.42),rgba(11,176,255,.20));border:1px solid rgba(255,255,255,.22);box-shadow:inset 0 1px 0 rgba(255,255,255,.30),0 4px 10px rgba(20,87,255,.18)}
.md-trade-txt{display:flex;flex-direction:column;gap:2px;flex:1;min-width:0}
.md-trade-name{font-size:16px;font-weight:600;letter-spacing:-.01em;line-height:1.2}
.md-trade-sub{font-size:12.5px;color:rgba(255,255,255,.6);line-height:1.3;letter-spacing:.005em}
.md-arr{font-size:18px;color:rgba(255,255,255,.45);flex:none;transition:transform .25s,color .25s;line-height:1}
.md-trade:hover .md-arr,.md-trade:focus-visible .md-arr{transform:translateX(4px);color:#7fb0ff}
.md-link{display:flex;align-items:center;justify-content:space-between;min-height:48px;padding:0 16px;border-radius:14px;text-decoration:none;color:rgba(255,255,255,.88);font-size:15px;font-weight:500;letter-spacing:-.005em;border:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.025);transition:background .2s,color .2s,border-color .2s}
.md-link:hover,.md-link:focus-visible{background:rgba(255,255,255,.09);color:#fff;border-color:rgba(255,255,255,.14)}
.md-link .md-arr{font-size:15px}
.md-foot{margin-top:auto;display:flex;flex-direction:column;gap:10px;padding-top:14px;border-top:1px solid rgba(255,255,255,.10)}
.md-cta{justify-content:center;min-height:54px;font-size:16px;letter-spacing:-.01em}
.md-tel{display:flex;align-items:center;gap:14px;padding:10px 14px;border-radius:16px;text-decoration:none;color:#fff;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.10);transition:background .2s,border-color .2s;min-height:60px}
.md-tel:hover,.md-tel:focus-visible{background:rgba(255,255,255,.10);border-color:rgba(255,255,255,.20)}
.md-tel-ic{width:42px;height:42px;flex:none;border-radius:12px;display:grid;place-items:center;background:linear-gradient(160deg,rgba(54,224,127,.24),rgba(54,224,127,.06));border:1px solid rgba(54,224,127,.32);color:#52e896}
.md-tel-txt{display:flex;flex-direction:column;gap:1px;line-height:1.15;flex:1;min-width:0}
.md-tel-num{font-size:16.5px;font-weight:700;letter-spacing:.005em}
.md-tel-sub{font-size:11.5px;color:rgba(255,255,255,.55);letter-spacing:.04em;margin-top:2px}
body.menu-open{overflow:hidden;touch-action:none}

/* ===== BOTTOM ACTION BAR (mobile thumb zone) ===== */
.mobile-cta{display:none}
@media (max-width:760px){
  .mobile-cta{display:flex;position:fixed;left:8px;right:8px;z-index:45;bottom:calc(8px + env(safe-area-inset-bottom));gap:8px;padding:8px;border-radius:20px;background:linear-gradient(165deg,rgba(255,255,255,.94),rgba(255,255,255,.82));backdrop-filter:blur(22px) saturate(180%);-webkit-backdrop-filter:blur(22px) saturate(180%);border:1px solid rgba(255,255,255,.95);box-shadow:0 18px 40px rgba(20,60,140,.22)}
  .mca{flex:1;min-height:52px;display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:14px;text-decoration:none;font-weight:700;font-size:15px;letter-spacing:-.01em}
  .mca.call{color:#0c2a5e;background:rgba(20,87,255,.08);border:1px solid rgba(20,87,255,.18)}
  .mca.quote{color:#fff;background:linear-gradient(180deg,#3a7dff,#1654d8);border:1px solid rgba(255,255,255,.25);box-shadow:0 8px 18px rgba(20,87,255,.28)}
  .mca .ic{width:16px;height:16px}
  .snap{scroll-padding-bottom:80px}
  body.menu-open .mobile-cta{display:none}
}
"""
(CSS/"styles.css").write_text(CSS_TXT)

# ---------- composants HOME ----------
NAV_LINKS=[("/electricite","Électricité"),("/chauffage","Chauffage"),("/plomberie","Plomberie"),
           ("/realisations","Réalisations"),("/entreprise","L'entreprise"),("/contact","Contact")]
def nav_home(active):
    links="".join(f'<a href="{u}"{" aria-current=\"page\"" if u==active else ""}>{t}</a>' for u,t in NAV_LINKS)
    return ('<nav class="nav reveal d1"><a href="/"><img class="brand-img" alt="ARELEC" src="/assets/img/logo.png"></a>'
            f'<div class="navlinks">{links}</div>'
            '<a href="/estimation" class="btn">Faire une estimation</a>'
            '<button class="burger" type="button" aria-expanded="false" aria-controls="mdrawer" aria-label="Ouvrir le menu"><span></span></button></nav>')

def mobile_drawer():
    trades=[
        ("/electricite","⚡","Électricité","Tableau, rénovation, éclairage LED"),
        ("/chauffage","🌡️","Chauffage","Installation, remplacement, entretien"),
        ("/plomberie","💧","Plomberie","Sanitaire, salle de bain, fuites"),
    ]
    trade_html="".join(
        f'<a class="md-trade" href="{u}"><span class="md-ic" aria-hidden="true">{ic}</span>'
        f'<span class="md-trade-txt"><span class="md-trade-name">{n}</span>'
        f'<span class="md-trade-sub">{s}</span></span>'
        f'<span class="md-arr" aria-hidden="true">→</span></a>'
        for u,ic,n,s in trades
    )
    sec_links=[("/realisations","Réalisations"),("/entreprise","L'entreprise"),("/contact","Contact")]
    link_html="".join(
        f'<a class="md-link" href="{u}">{t}<span class="md-arr" aria-hidden="true">→</span></a>'
        for u,t in sec_links
    )
    return ('<div class="mdrawer" id="mdrawer" hidden aria-label="Menu mobile">'
            '<div class="md-head">'
            '<img class="md-logo" src="/assets/img/logo.png" alt="ARELEC">'
            '<button class="mdrawer-close" type="button" aria-label="Fermer le menu">×</button>'
            '</div>'
            '<div class="md-tagline"><span class="pulse" aria-hidden="true"></span>Plouzané · Bassin brestois · Devis gratuit</div>'
            f'<div class="md-section"><div class="md-label">Nos métiers</div>{trade_html}</div>'
            f'<div class="md-section"><div class="md-label">L\'entreprise</div>{link_html}</div>'
            '<div class="md-foot">'
            '<a class="btn solid md-cta" href="/estimation">Faire une estimation →</a>'
            f'<a class="md-tel" href="tel:{PHONE_TEL}" aria-label="Appeler {PHONE_DISP}">'
            f'<span class="md-tel-ic" aria-hidden="true">{SVG_PHONE}</span>'
            f'<span class="md-tel-txt"><span class="md-tel-num">{PHONE_DISP}</span>'
            '<span class="md-tel-sub">Lun–Ven · 8h–18h</span></span></a>'
            '</div></div>')

def mobile_cta_bar():
    return ('<nav class="mobile-cta" aria-label="Actions rapides">'
            f'<a class="mca call" href="tel:{PHONE_TEL}">{SVG_PHONE} <span>Appeler</span></a>'
            '<a class="mca quote" href="/estimation">✏️ <span>Estimer</span></a>'
            '</nav>')
def trades_panel(heading_em, sub):
    cards=[("/electricite","escalier-led.jpg","⚡","Électricité","Du tableau à l'éclairage soigné — le cœur de métier ARélec.",True),
           ("/chauffage","confort.jpg","🌡️","Chauffage","Le confort toute l'année, sans faire flamber la facture.",False),
           ("/plomberie","plomb.jpg","💧","Plomberie","Sanitaire et réseau d'eau, propre et durable.",False)]
    c=""
    for i,(href,img,ic,t,p,is_open) in enumerate(cards):
        d=["d2","d3","d4"][i]; oc=" is-open" if is_open else ""
        c+=(f'<a class="acc reveal {d}{oc}" href="{href}" aria-label="{t}">'
            f'<img src="/assets/img/{img}" alt="{t} — ARÉLEC" loading="lazy">'
            f'<div class="acc-shade" aria-hidden="true"></div>'
            f'<div class="acc-rail" aria-hidden="true"><span class="acc-ic">{ic}</span><span class="acc-vt">{t}</span></div>'
            f'<div class="acc-open"><div class="acc-ic-lg">{ic}</div><h3>{t}</h3><p>{p}</p>'
            f'<span class="acc-cta">En savoir plus →</span></div></a>')
    return (f'<section class="panel light"><div class="sec sec-split">'
            f'<div class="lead-col">'
            f'<h2 class="trade-list reveal d1"><span>Électricité.</span><span>Chauffage.</span><span>Plomberie.</span></h2>'
            f'<div class="lead-actions reveal d3">'
            f'<a class="btn solid" href="/estimation">Faire une estimation →</a>'
            f'</div></div>'
            f'<div class="accordion reveal d2">{c}</div></div></section>')
REVS=[("Intervention de très bonne qualité. Chantier propre et rapide. Je recommande ARÉLEC.","Philippe C.","Rénovation électrique"),
 ("Super entreprise, travail de qualité et toujours dans la bonne humeur. Merci pour la rénovation de notre maison&nbsp;!","Mélanie Hautecoeur","Rénovation complète"),
 ("Très pro, Arnaud et son collègue font du bon travail, propre, et en plus ils sont sympas.","Yvon Riou","Installation électrique"),
 ("Super dépannage… rapide, efficace, au top — avec de l'humour en prime&nbsp;;)","Carole Yven","Dépannage"),
 ("Sympa et efficace, je recommande sans problème.","Ronan Madec","Client ARÉLEC"),
 ("J'ai fait refaire ma salle de bain et l'électricité avec eux. Je conseille.","JL le grand","Salle de bain + élec")]
AVATAR_COLORS=["#1a73e8","#34a853","#ea4335","#fbbc04","#9334e8","#e8710a"]
def avis_panel(sub):
    cards=""
    for i,(q,w,c) in enumerate(REVS):
        init=w[0].upper(); col=AVATAR_COLORS[i%len(AVATAR_COLORS)]
        cards+=(f'<article class="g-card"><header><div class="g-avatar" style="background:{col}">{init}</div>'
                f'<div class="g-meta"><span class="g-name">{w}</span><span class="g-sub">Avis Google · {c}</span></div></header>'
                f'<div class="g-stars-small" aria-label="5 sur 5">★★★★★</div><blockquote>{q}</blockquote></article>')
    logo=('<span class="g-logo" aria-label="Google">'
          '<span style="color:#4285F4">G</span><span style="color:#EA4335">o</span>'
          '<span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span>'
          '<span style="color:#34A853">l</span><span style="color:#EA4335">e</span></span>')
    return ('<section class="band-reviews"><div class="sec sec-reviews">'
            f'<div class="g-head">{logo}'
            '<div class="g-stars-big" aria-hidden="true">★★★★★</div>'
            '<div class="g-sub-big">Avis clients vérifiés</div></div>'
            '<div class="g-carousel">'
            '<button class="g-nav g-prev" aria-label="Avis précédent" type="button">‹</button>'
            f'<div class="g-track" id="gtrack">{cards}</div>'
            '<button class="g-nav g-next" aria-label="Avis suivant" type="button">›</button>'
            '</div><div class="g-dots" id="gdots"></div></div></section>')

FALL_TEXT="Électricité Chauffage Plomberie Tableau Radiateurs Sanitaires Câblage Éclairage Chaudière Robinetterie"
FALL_HL=["Électricité","Chauffage","Plomberie"]
def falling_panel():
    return ('<section class="panel light falling" id="fallingPanel">'
            '<div class="falling-stage" id="fallingStage">'
            f'<div class="falling-text" data-text="{html.escape(FALL_TEXT, quote=True)}" data-hl="{html.escape("|".join(FALL_HL), quote=True)}">{html.escape(FALL_TEXT)}</div>'
            '</div></section>')

# ---------- GradualBlur (vanilla port of React Bits component) ----------
def gradual_blur(position="bottom", height="11rem", strength=2.5, divCount=6, curve="bezier", exponential=True, opacity=1, target="parent"):
    direction = {"top":"to top","bottom":"to bottom","left":"to left","right":"to right"}.get(position,"to bottom")
    def cv(p):
        if curve == "bezier": return p*p*(3-2*p)
        if curve == "ease-in": return p*p
        if curve == "ease-out": return 1-(1-p)**2
        return p
    increment = 100/divCount
    divs = []
    for i in range(1, divCount+1):
        progress = cv(i/divCount)
        if exponential:
            blur_value = (2**(progress*4))*0.0625*strength
        else:
            blur_value = 0.0625*(progress*divCount+1)*strength
        p1 = round((increment*i - increment)*10)/10
        p2 = round(increment*i*10)/10
        p3 = round((increment*i + increment)*10)/10
        p4 = round((increment*i + increment*2)*10)/10
        grad = f"transparent {p1}%, black {p2}%"
        if p3 <= 100: grad += f", black {p3}%"
        if p4 <= 100: grad += f", transparent {p4}%"
        mask = f"linear-gradient({direction}, {grad})"
        bv = f"{blur_value:.3f}rem"
        st = (f"position:absolute;inset:0;"
              f"-webkit-mask-image:{mask};mask-image:{mask};"
              f"-webkit-backdrop-filter:blur({bv});backdrop-filter:blur({bv});"
              f"opacity:{opacity}")
        divs.append(f'<div style="{st}"></div>')
    pos_kind = "fixed" if target == "page" else "absolute"
    z = 1100 if target == "page" else 5
    if position in ("top","bottom"):
        pos = f"position:{pos_kind};left:0;right:0;{position}:0;width:100%;height:{height}"
    else:
        pos = f"position:{pos_kind};top:0;bottom:0;{position}:0;height:100%;width:{height}"
    return (f'<div class="gradual-blur" data-pos="{position}" data-target="{target}" style="{pos};z-index:{z}">'
            f'<div class="gradual-blur-inner">{"".join(divs)}</div></div>')
EXTRA_COMMUNES=[
 ("le-conquet","Le Conquet"),("saint-renan","Saint-Renan"),("guipavas","Guipavas"),
 ("le-relecq-kerhuon","Le Relecq-Kerhuon"),("guilers","Guilers"),("plougonvelin","Plougonvelin"),
 ("locmaria-plouzane","Locmaria-Plouzané"),("lannilis","Lannilis"),("plabennec","Plabennec"),
 ("landerneau","Landerneau"),
]
EXISTING_COMMUNES=[("brest","Brest"),("plouzane","Plouzané"),("plouider","Plouider")]
ALL_COMMUNES=sorted(EXISTING_COMMUNES+EXTRA_COMMUNES, key=lambda c:c[1])
def _li(metier_slug): return "".join(f'<li><a href="/{metier_slug}-{s}">{l}</a></li>' for s,l in ALL_COMMUNES)
FCITY_E=_li("electricien"); FCITY_P=_li("plombier"); FCITY_C=_li("chauffagiste")
FOOTER=('<section class="cta-band"><div><h2>Un projet, une panne, une question&nbsp;?</h2>'
 '<p>Estimez vos travaux en ligne, ou appelez-nous. Devis gratuit.</p></div>'
 '<div class="cta-actions"><a href="/estimation" class="btn solid">Faire une estimation →</a>'
 f'<a href="tel:{PHONE_TEL}" class="btn line">Contacter</a></div></section>'
 '<footer class="site"><div class="fgrid">'
 '<div class="brand"><a href="/"><img class="blogo" src="/assets/img/logo.png" alt="ARELEC"></a>'
 '<p>Électricité, chauffage et plomberie dans le bassin brestois. Un seul interlocuteur, depuis 2010.</p>'
 f'<div class="nap"><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a><br><span class="muted">{EMAIL}</span><br>'
 '<span class="muted">Plouzané (29280) — Finistère</span></div>'
 f'<div class="soc"><a href="https://www.facebook.com/people/AR%C3%A9lec/100089481862657/" target="_blank" rel="noopener" aria-label="Facebook">{SVG_FB}</a><a href="https://wa.me/33678020424" target="_blank" rel="noopener" aria-label="WhatsApp">{SVG_WA}</a></div></div>'
 '<div class="fcol"><h4>Nos métiers</h4><ul><li><a href="/electricite">Électricité</a></li><li><a href="/chauffage">Chauffage</a></li><li><a href="/plomberie">Plomberie</a></li><li><a href="/realisations">Réalisations</a></li></ul></div>'
 f'<div class="fcol"><h4>Électricien à…</h4><ul>{FCITY_E}</ul></div>'
 f'<div class="fcol"><h4>Plombier à…</h4><ul>{FCITY_P}</ul></div>'
 f'<div class="fcol"><h4>Chauffagiste à…</h4><ul>{FCITY_C}</ul></div>'
 '<div class="fcol"><h4>Entreprise</h4><ul><li><a href="/entreprise">L\'entreprise</a></li><li><a href="/avis">Avis clients</a></li><li><a href="/contact">Contact</a></li><li><a href="/estimation">Faire une estimation</a></li></ul></div>'
 '</div><div class="legal"><span>© 2026 SARL ARélec — SIREN 790 223 036 — Plouzané</span>'
 '<span><a href="/mentions-legales">Mentions légales</a> · <a href="/politique-confidentialite">Confidentialité</a></span></div></footer>')
JS=r'''<script>
const s=document.getElementById("snap");
if(s){const ps=[...document.querySelectorAll(".panel")],ds=[...document.querySelectorAll(".dots button")],tn=document.querySelector(".topnav"),hero=document.getElementById("hero");
const isMobile=window.matchMedia("(max-width: 760px)").matches;
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("visible");const i=ps.indexOf(e.target);ds.forEach((d,k)=>d.classList.toggle("on",k===i));if(tn&&e.target===hero)tn.classList.remove("visible")}else if(tn&&e.target===hero){tn.classList.add("visible")}}),{root:isMobile?null:s,threshold:.55});
ps.forEach(p=>io.observe(p));ds.forEach(d=>d.addEventListener("click",()=>{const i=+d.dataset.go;if(ps[i])ps[i].scrollIntoView({behavior:"smooth"})}));}
(function(){
 const burgers=document.querySelectorAll(".burger");
 const drawer=document.getElementById("mdrawer");
 if(!drawer||!burgers.length)return;
 const closeBtn=drawer.querySelector(".mdrawer-close");
 const open=()=>{drawer.hidden=false;requestAnimationFrame(()=>drawer.classList.add("open"));burgers.forEach(b=>b.setAttribute("aria-expanded","true"));document.body.classList.add("menu-open");};
 const close=()=>{drawer.classList.remove("open");burgers.forEach(b=>b.setAttribute("aria-expanded","false"));document.body.classList.remove("menu-open");setTimeout(()=>{if(!drawer.classList.contains("open"))drawer.hidden=true;},350);};
 burgers.forEach(b=>b.addEventListener("click",()=>{b.getAttribute("aria-expanded")==="true"?close():open();}));
 closeBtn&&closeBtn.addEventListener("click",close);
 drawer.addEventListener("click",e=>{const a=e.target.closest("a");if(a&&drawer.contains(a))close();});
 document.addEventListener("keydown",e=>{if(e.key==="Escape")close();});
})();
(function(){
 const panel=document.getElementById("fallingPanel");if(!panel)return;
 const stage=document.getElementById("fallingStage");if(!stage)return;
 const reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
 const isMobile=window.matchMedia("(max-width: 760px)").matches;
 if(reduce||isMobile)return;
 const textEl=stage.querySelector(".falling-text");
 const text=textEl.dataset.text||"";
 const hl=(textEl.dataset.hl||"").split("|").filter(Boolean);
 textEl.innerHTML=text.split(" ").map(w=>{const k=hl.some(h=>w.startsWith(h));return '<span class="word'+(k?" hl":"")+'">'+w+"</span>";}).join(" ");
 let started=false;
 function loadMatter(){return new Promise(r=>{if(window.Matter)return r();const sc=document.createElement("script");sc.src="https://cdn.jsdelivr.net/npm/matter-js@0.19.0/build/matter.min.js";sc.onload=r;document.head.appendChild(sc);});}
 async function start(){if(started)return;started=true;await loadMatter();
  const M=window.Matter,{Engine,Render,World,Bodies,Runner,Mouse,MouseConstraint,Events}=M;
  const rect=stage.getBoundingClientRect();const W=rect.width,H=rect.height;if(W<=0||H<=0){started=false;return;}
  const engine=Engine.create();engine.world.gravity.y=0.9;
  const render=Render.create({element:stage,engine,options:{width:W,height:H,background:"transparent",wireframes:false,pixelRatio:window.devicePixelRatio||1}});
  const bo={isStatic:true,render:{fillStyle:"transparent"}};
  World.add(engine.world,[Bodies.rectangle(W/2,H+25,W,50,bo),Bodies.rectangle(-25,H/2,50,H,bo),Bodies.rectangle(W+25,H/2,50,H,bo),Bodies.rectangle(W/2,-25,W,50,bo)]);
  const words=[...textEl.querySelectorAll(".word")];
  const bodies=words.map(el=>{const r=el.getBoundingClientRect();const x=r.left-rect.left+r.width/2;const y=r.top-rect.top+r.height/2;const b=Bodies.rectangle(x,y,r.width,r.height,{render:{fillStyle:"transparent"},restitution:.74,frictionAir:.013,friction:.22,chamfer:{radius:6}});M.Body.setVelocity(b,{x:(Math.random()-.5)*4,y:0});M.Body.setAngularVelocity(b,(Math.random()-.5)*.05);return{el,body:b};});
  textEl.style.display="block";textEl.style.padding="0";textEl.style.maxWidth="none";textEl.style.margin="0";textEl.style.pointerEvents="none";
  bodies.forEach(({el,body})=>{el.style.position="absolute";el.style.left=body.position.x+"px";el.style.top=body.position.y+"px";el.style.transform="translate(-50%,-50%)";el.style.margin="0";el.style.pointerEvents="none";});
  World.add(engine.world,bodies.map(o=>o.body));
  const mouse=Mouse.create(render.canvas);
  mouse.pixelRatio=window.devicePixelRatio||1;
  if(mouse.element){mouse.element.removeEventListener("mousewheel",mouse.mousewheel);mouse.element.removeEventListener("DOMMouseScroll",mouse.mousewheel);}
  const mc=MouseConstraint.create(engine,{mouse,constraint:{stiffness:.22,damping:.08,render:{visible:false}}});
  World.add(engine.world,mc);render.mouse=mouse;
  Events.on(mc,"startdrag",()=>{stage.classList.add("grabbing")});
  Events.on(mc,"enddrag",()=>{stage.classList.remove("grabbing")});
  Runner.run(Runner.create(),engine);Render.run(render);
  (function loop(){bodies.forEach(({body,el})=>{el.style.left=body.position.x+"px";el.style.top=body.position.y+"px";el.style.transform="translate(-50%,-50%) rotate("+body.angle+"rad)";});requestAnimationFrame(loop);})();
 }
 const snapRoot=document.getElementById("snap")||null;
 const io2=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting && e.intersectionRatio>=0.85){setTimeout(start,400);io2.disconnect();}}),{root:snapRoot,threshold:[0.85,0.95]});
 io2.observe(panel);
})();
(function(){
 const track=document.getElementById("gtrack");if(!track)return;
 const dotsWrap=document.getElementById("gdots");
 const cards=[...track.querySelectorAll(".g-card")];
 if(!cards.length)return;
 cards.forEach((_,i)=>{const b=document.createElement("button");b.type="button";b.dataset.i=i;b.setAttribute("aria-label","Avis "+(i+1));dotsWrap.appendChild(b);});
 const dots=[...dotsWrap.querySelectorAll("button")];
 const setActive=i=>dots.forEach((b,j)=>b.classList.toggle("on",j===i));
 const step=()=>cards[0].getBoundingClientRect().width+parseFloat(getComputedStyle(track).columnGap||"24");
 dots.forEach(b=>b.addEventListener("click",()=>{const i=+b.dataset.i;cards[i].scrollIntoView({inline:"center",behavior:"smooth",block:"nearest"});}));
 const prev=document.querySelector(".g-prev"),next=document.querySelector(".g-next");
 prev&&prev.addEventListener("click",()=>track.scrollBy({left:-step(),behavior:"smooth"}));
 next&&next.addEventListener("click",()=>track.scrollBy({left:step(),behavior:"smooth"}));
 const io3=new IntersectionObserver(es=>{let best=null;es.forEach(e=>{if(e.isIntersecting&&(!best||e.intersectionRatio>best.intersectionRatio))best=e;});if(best){const i=cards.indexOf(best.target);if(i>=0)setActive(i);}},{root:track,threshold:[.5,.7,.9]});
 cards.forEach(c=>io3.observe(c));
 setActive(0);
})();
</script>'''

def hero_home(kicker,h1,desc):
    return ('<section class="panel visible" id="hero"><div class="bg"></div>'+nav_home("")+
     '<div class="spacer"></div><div class="content"><div class="topline"><div>'
     f'<div class="kicker reveal d2"><span class="dot"></span>{kicker}</div>'
     f'<h1 class="reveal d2">{h1}</h1></div>'
     '<a href="/estimation" class="btn primary reveal d3">Faire une estimation →</a></div>'
     '<div class="hr reveal d3"></div><div class="bottom"><div class="meta reveal d4">'
     f'<a class="chip" href="tel:{PHONE_TEL}">{SVG_PHONE} {PHONE_DISP}</a><span class="chip">📍 Plouzané · bassin brestois</span><span class="chip">✓ Devis gratuit</span></div>'
     f'<p class="desc reveal d4">{desc}</p></div></div>'
     '<div class="scrollhint">Nos métiers<div class="arr"></div></div></section>')

# ---------- SUBPAGE (Traaction-inspired) ----------
def subnav(active):
    nv="".join(f'<a href="{u}"{" aria-current=\"page\"" if u==active else ""}>{t}</a>' for u,t in NAV_LINKS)
    return (f'<header class="subnav"><a href="/" aria-label="ARELEC accueil"><img class="logo-dark" src="/assets/img/logo-dark.png" alt="ARELEC"></a>'
            f'<nav>{nv}</nav>'
            f'<div class="ctas"><a class="tel" href="tel:{PHONE_TEL}" aria-label="Appeler {PHONE_DISP}">{SVG_PHONE} <span class="tel-label">{PHONE_DISP}</span></a>'
            '<a class="btn solid" href="/estimation">Faire une estimation</a>'
            '<button class="burger" type="button" aria-expanded="false" aria-controls="mdrawer" aria-label="Ouvrir le menu"><span></span></button></div></header>')

def trust_strip():
    items=[("✓","Artisan depuis 2010"),("📍","Bassin brestois"),("✓","Devis gratuit"),("★","Avis Google 5/5")]
    inner="".join(f'<div class="item"><span class="ic">{i}</span>{t}</div>' for i,t in items)
    return f'<section class="trust"><div class="wrap">{inner}</div></section>'

def subhero(crumb_html, eyebrow, h1, lead, img, float_html, hero_alt=None):
    fl = f'<div class="float">{float_html}</div>' if float_html else ""
    return ('<section class="subhero"><div class="wrap"><div>'
            f'<div class="crumb">{crumb_html}</div>'
            f'<div class="eyebrow-blue">{eyebrow}</div>'
            f'<h1>{h1}</h1><p class="lead">{lead}</p>'
            '<div class="actions"><a class="btn solid" href="/estimation">Faire une estimation →</a>'
            f'<a class="btn line" href="tel:{PHONE_TEL}">Contacter</a></div></div>'
            f'<div class="imgcard"><img src="/assets/img/{img}" alt="{html.escape(hero_alt or "ARÉLEC, chantier en Bretagne")}" loading="eager">{fl}</div></div></section>')

def feat_section(num, eyebrow, h2, p, items, img, tag, flip=False):
    li="".join(f"<li>{x}</li>" for x in items)
    cls="feat flip" if flip else "feat"
    tg = f'<span class="tag">{tag}</span>' if tag else ""
    return (f'<section class="{cls}"><div class="wrap"><div>'
            f'<div class="num">{num}</div><div class="eyebrow-blue">{eyebrow}</div>'
            f'<h2>{h2}</h2><p>{p}</p><ul>{li}</ul></div>'
            f'<div class="imgcard"><img src="/assets/img/{img}" alt="{eyebrow}" loading="lazy">{tg}</div></div></section>')

def recap(h2, p="Estimation en ligne en quelques minutes, ou un coup de fil. Devis gratuit."):
    return (f'<section class="recap"><h2>{h2}</h2><p>{p}</p>'
            '<div class="actions"><a class="btn solid" href="/estimation">Faire une estimation →</a>'
            f'<a class="btn line" href="tel:{PHONE_TEL}">Contacter</a></div></section>')

def faq_section(qa_pairs, h2="Questions fréquentes"):
    if not qa_pairs: return ""
    items = "".join(
        f'<details class="faq-q"><summary><span class="faq-q-text">{html.escape(q)}</span><span class="faq-q-icon" aria-hidden="true">+</span></summary>'
        f'<div class="faq-a">{html.escape(a)}</div></details>'
        for q, a in qa_pairs
    )
    return (f'<section class="faq"><div class="wrap-faq">'
            f'<div class="eyebrow-blue">FAQ</div><h2>{html.escape(h2)}</h2>'
            f'<div class="faq-list">{items}</div></div></section>')

def areas_section(eyebrow, h2, paragraph_html, pills=None):
    pills_html=""
    if pills:
        pills_html='<div class="pills">'+"".join(f'<a href="{u}">{t}</a>' for u,t in pills)+'</div>'
    return (f'<section class="areas"><div class="wrap">'
            f'<div class="eyebrow-blue">{eyebrow}</div>'
            f'<h2>{h2}</h2><p>{paragraph_html}</p>{pills_html}</div></section>')

# ---------- JSON-LD + Shells ----------
# --- Données de référence pour LocalBusiness enrichi ---
PLOUZANE_GEO = {"lat": 48.3781, "lon": -4.6228}  # centre de Plouzané
SAME_AS = [
    "https://www.facebook.com/people/AR%C3%A9lec/100089481862657/",
    "https://wa.me/33678020424",
]
OPENING_HOURS = [
    {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"},
]

def _local_business(path, area, reviews=True):
    """Construit l'objet LocalBusiness (Electrician) enrichi pour le graphe."""
    if area:
        area_served = area
    else:
        area_served = ["Brest","Plouzané","Finistère"]
    lb = {
        "@context": "https://schema.org",
        "@type": "Electrician",
        "@id": f"{DOMAIN}/#business",
        "name": "ARélec",
        "alternateName": "SARL ARélec",
        "legalName": "SARL ARélec",
        "description": "Artisan électricien, chauffagiste et plombier installé à Plouzané depuis 2010. Intervention dans tout le bassin brestois (Finistère).",
        "slogan": "Une maison bien câblée, bien chauffée.",
        "image": f"{DOMAIN}/assets/img/hero.jpg",
        "logo": f"{DOMAIN}/assets/img/logo.png",
        "url": f"{DOMAIN}{path}",
        "telephone": "+33298402043",
        "email": "contact@entreprise-arelec.fr",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Plouzané",
            "postalCode": "29280",
            "addressRegion": "Finistère",
            "addressCountry": "FR",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": PLOUZANE_GEO["lat"],
            "longitude": PLOUZANE_GEO["lon"],
        },
        "areaServed": area_served,
        "serviceArea": {
            "@type": "GeoCircle",
            "geoMidpoint": {"@type": "GeoCoordinates", "latitude": PLOUZANE_GEO["lat"], "longitude": PLOUZANE_GEO["lon"]},
            "geoRadius": "30000",
        },
        "openingHoursSpecification": OPENING_HOURS,
        "priceRange": "€€",
        "paymentAccepted": "Espèces, Chèque, Virement bancaire",
        "currenciesAccepted": "EUR",
        "founder": {"@type": "Person", "name": "Arnaud Roncey"},
        "foundingDate": "2010",
        "vatID": "FR",
        "taxID": "790223036",
        "sameAs": SAME_AS,
        "knowsAbout": ["Électricité", "Chauffage", "Plomberie", "Mise aux normes NF C 15-100", "Rénovation", "Dépannage"],
    }
    if reviews:
        lb["review"] = [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": w},
                "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                "reviewBody": q.replace("&nbsp;", " "),
            }
            for q, w, _ in REVS[:3]
        ]
    return lb

def _faq_schema(qa_pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa_pairs
        ],
    }

def _service_schema(name, description, service_type, area):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "description": description,
        "serviceType": service_type,
        "provider": {"@id": f"{DOMAIN}/#business"},
        "areaServed": area or ["Brest","Plouzané","Finistère"],
    }

def _dump(obj):
    # ensure_ascii=False pour garder les accents lisibles dans le HTML
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def jsonld(path,h1_text,area,reviews=True,breadcrumb_name=None,faq=None,service=None):
    blocks = [_dump(_local_business(path, area, reviews))]
    # Breadcrumb
    if path=="/" or path=="":
        crumbs = {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{DOMAIN}/"}],
        }
    else:
        name = breadcrumb_name or h1_text.replace("<br>"," ").replace("<b>","").replace("</b>","").strip().rstrip(".")
        crumbs = {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{DOMAIN}/"},
                {"@type": "ListItem", "position": 2, "name": name, "item": f"{DOMAIN}{path}"},
            ],
        }
    blocks.append(_dump(crumbs))
    if service:
        blocks.append(_dump(_service_schema(**service, area=area)))
    if faq:
        blocks.append(_dump(_faq_schema(faq)))
    return "".join(f'<script type="application/ld+json">{b}</script>' for b in blocks)

def head_common(path,title,desc,jl):
    canon=DOMAIN+("/" if path=="" else "/"+path+"/")
    t_esc=html.escape(title); d_esc=html.escape(desc); og_img=f"{DOMAIN}/assets/img/hero.jpg"
    og=(f'<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR">'
        f'<meta property="og:site_name" content="ARélec">'
        f'<meta property="og:title" content="{t_esc}"><meta property="og:description" content="{d_esc}">'
        f'<meta property="og:url" content="{canon}"><meta property="og:image" content="{og_img}">'
        f'<meta property="og:image:width" content="1600"><meta property="og:image:height" content="900">'
        f'<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{t_esc}"><meta name="twitter:description" content="{d_esc}">'
        f'<meta name="twitter:image" content="{og_img}">')
    icons=('<link rel="icon" href="/favicon.ico" sizes="any">'
           '<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">'
           '<link rel="apple-touch-icon" sizes="180x180" href="/assets/img/apple-touch-icon.png">'
           '<meta name="theme-color" content="#0A1322">')
    return ('<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{t_esc}</title><meta name="description" content="{d_esc}">'
            f'<link rel="canonical" href="{canon}">{og}{icons}{jl}'
            '<link rel="stylesheet" href="/assets/css/styles.css?v=41"></head>')

def shell_home(path,title,desc,body,jl,dots=4):
    dotbtns="".join(f'<button{" class=\"on\"" if i==0 else ""} data-go="{i}"></button>' for i in range(dots))
    dotsdiv=f'<div class="dots">{dotbtns}</div>'
    topnav=""
    if path=="":
        nl="".join(f'<a href="{u}">{t}</a>' for u,t in NAV_LINKS)
        topnav=('<header class="topnav">'
            '<a href="/" aria-label="ARELEC accueil"><img class="logo-dark" src="/assets/img/logo-dark.png" alt="ARELEC"></a>'
            f'<nav>{nl}</nav>'
            f'<div class="ctas"><a class="tel" href="tel:{PHONE_TEL}" aria-label="Appeler {PHONE_DISP}">{SVG_PHONE} <span class="tel-label">{PHONE_DISP}</span></a>'
            '<a class="btn solid" href="/estimation">Faire une estimation</a>'
            '<button class="burger" type="button" aria-expanded="false" aria-controls="mdrawer" aria-label="Ouvrir le menu"><span></span></button></div></header>')
    return head_common(path,title,desc,jl)+f'<body>{topnav}{mobile_drawer()}{mobile_cta_bar()}{dotsdiv}<main class="snap" id="snap" role="main">{body}</main>{JS}</body></html>'
def shell_sub(path,title,desc,body,jl):
    return head_common(path,title,desc,jl)+f'<body class="sub-shell">{mobile_drawer()}{mobile_cta_bar()}<main role="main">{body}</main>{JS}</body></html>'

def write(path,h):
    d=SITE/(path.strip("/")); d.mkdir(parents=True,exist_ok=True)
    (d/"index.html").write_text(h)

# ---------- FAQ & Services (GEO) ----------
FAQ_HOME = [
    ("Qui est ARélec ?",
     "ARélec (SARL ARélec) est un artisan électricien-chauffagiste-plombier installé à Plouzané (29280) depuis 2010. Le gérant est Arnaud Roncey. La SARL intervient dans tout le bassin brestois (Finistère)."),
    ("Sur quelle zone intervient ARélec ?",
     "ARélec intervient à Plouzané (siège), Brest et dans les communes du bassin brestois — Saint-Renan, Le Conquet, Landerneau, Plouider, Guipavas, Le Relecq-Kerhuon, Guilers, Plougonvelin, Locmaria-Plouzané, Lannilis, Plabennec."),
    ("Quels métiers couvre ARélec ?",
     "Trois métiers, par la même équipe : électricité (installation, rénovation, mise aux normes NF C 15-100, dépannage, éclairage), chauffage (installation, remplacement, entretien) et plomberie (salle de bain, recherche de fuite, réseau d'eau, sanitaires). Un seul interlocuteur pour tout le chantier."),
    ("Le devis est-il payant ?",
     "Non. L'estimation en ligne est gratuite (~2 minutes). Si la fourchette correspond à votre budget, ARélec se déplace ensuite gratuitement pour établir le vrai devis sur place."),
    ("Comment contacter ARélec ?",
     "Par téléphone au 02 98 40 20 43, par WhatsApp au 06 78 02 04 24, par email à contact@entreprise-arelec.fr, ou via le formulaire de contact du site. Réponse sous 24 à 48 h."),
    ("ARélec fait-il du dépannage ?",
     "Oui : disjoncteur qui claque, prise grillée, fuite, panne d'éclairage. ARélec intervient pour les dépannages dans le bassin brestois."),
]

FAQ_ELEC = [
    ("Qu'est-ce que la norme NF C 15-100 ?",
     "NF C 15-100 est la norme française qui définit les règles d'installation électrique des logements neufs et rénovés (tableau, différentiels, prises, protection des personnes). ARélec diagnostique et met aux normes les installations existantes."),
    ("ARélec fait-il du dépannage électrique ?",
     "Oui — disjoncteur qui saute, prise grillée, panne d'éclairage, court-circuit. ARélec intervient rapidement dans le bassin brestois (Brest, Plouzané, Saint-Renan, Landerneau et alentour)."),
    ("Quand faut-il remplacer le tableau électrique ?",
     "Quand l'installation date d'avant la norme actuelle, qu'il n'y a pas de différentiels 30 mA, que le tableau est saturé, ou en cas de rénovation lourde. ARélec fait le diagnostic et remplace le tableau sans tout casser."),
    ("ARélec installe-t-il des éclairages LED ?",
     "Oui — éclairage intérieur et extérieur, conception sur mesure (escaliers LED intégrées, appliques chaudes, éclairage architectural). C'est l'une des spécialités de l'entreprise."),
    ("Faut-il un électricien certifié pour une rénovation ?",
     "Oui, pour respecter la norme NF C 15-100 et garantir la sécurité. ARélec est artisan électricien depuis 2010 et prend en charge des rénovations complètes, en coordination avec ses autres métiers (chauffage, plomberie)."),
]

FAQ_CHAUF = [
    ("Quel chauffage choisir en rénovation ?",
     "Le choix dépend de l'isolation du logement, de la surface, de l'usage et du budget. ARélec dimensionne radiateurs et distribution selon votre maison, et conseille sur les solutions les plus durables (radiateurs, pompe à chaleur, eau chaude sanitaire)."),
    ("ARélec entretient-il les chaudières ?",
     "Oui — visite annuelle, contrôle complet, réglages, petits remplacements. Un chauffage entretenu consomme moins et tombe moins souvent en panne."),
    ("Comment réduire sa facture de chauffage ?",
     "Trois leviers concrets : revoir la régulation (programmation par pièce), équilibrer le réseau (chaque radiateur à la bonne température), et améliorer l'isolation si possible. ARélec règle souvent le confort sans avoir à changer l'appareil."),
    ("ARélec installe-t-il des radiateurs neufs ?",
     "Oui — installation, remplacement, dimensionnement et raccordement. ARélec gère l'eau chaude sanitaire et la distribution dans le bassin brestois."),
    ("Quelle est la fréquence d'entretien d'un chauffage ?",
     "L'entretien annuel est recommandé (et obligatoire pour la plupart des chaudières). ARélec passe une fois par an, contrôle, règle, remplace ce qui doit l'être."),
]

FAQ_PLOMB = [
    ("ARélec rénove-t-il des salles de bain complètes ?",
     "Oui — de la dépose à la pose : douche, baignoire, WC, robinetterie, réseau d'eau, évacuations, coordination carrelage. ARélec fait toute la plomberie et l'électricité de la pièce, sans laisser de tranchée ouverte le week-end."),
    ("Comment détecter une fuite d'eau ?",
     "Compteur qui tourne sans usage, traces d'humidité, baisse de pression. ARélec localise précisément la fuite avant d'ouvrir (pas de casse inutile), répare et remet en état."),
    ("ARélec refait-il les réseaux d'eau ?",
     "Oui — dans les rénovations, ARélec reprend les canalisations, installe les évacuations et la robinetterie, et remet l'installation aux standards actuels."),
    ("Combien de temps pour rénover une salle de bain ?",
     "Cela dépend de l'ampleur du chantier (réfection totale ou rafraîchissement). ARélec établit un planning précis lors de la visite de devis pour limiter la gêne au quotidien."),
    ("ARélec installe-t-il des douches à l'italienne ?",
     "Oui — douches italiennes, finitions marbre, vasques, robinetteries soignées. Voir les exemples sur la page Réalisations."),
]

SERVICE_ELEC = {
    "name": "Travaux d'électricité — ARélec",
    "description": "Installation, rénovation, mise aux normes NF C 15-100, dépannage et éclairage par un artisan électricien installé à Plouzané depuis 2010, intervenant dans tout le bassin brestois.",
    "service_type": "Electrical installation, renovation and repair",
}
SERVICE_CHAUF = {
    "name": "Travaux de chauffage — ARélec",
    "description": "Installation, remplacement et entretien de chauffage, radiateurs et eau chaude sanitaire dans le bassin brestois. Conseil en régulation et économies d'énergie.",
    "service_type": "Heating installation, replacement and maintenance",
}
SERVICE_PLOMB = {
    "name": "Travaux de plomberie — ARélec",
    "description": "Salle de bain, sanitaires, recherche de fuite, réseau d'eau, robinetterie et évacuations dans le bassin brestois (Brest, Plouzané, et alentour).",
    "service_type": "Plumbing installation, renovation and leak detection",
}

# ---------- PAGES ----------
SECT_HOME="De la prise qui claque à la salle de bain complète : on s'occupe de toute la maison, en neuf comme en rénovation."
AVIS_HOME="Qualité, chantier propre, réactivité et bons conseils, dans tout le bassin brestois."
pages=[]

# HOME
home_body=(hero_home("Électricité · Chauffage · Plomberie — Finistère, depuis 2010","Une maison bien câblée,<br><b>bien chauffée.</b>",
  "À Plouzané et dans tout le bassin brestois depuis 2010 : électricité, chauffage et plomberie, en neuf comme en rénovation.<br><b>Faites une estimation en ligne</b> ou contactez-nous — devis gratuit.")
 +trades_panel("Trois métiers, <em>un seul interlocuteur.</em>",SECT_HOME)+avis_panel(AVIS_HOME)
 +faq_section(FAQ_HOME, h2="Vos questions, nos réponses.")+falling_panel()+FOOTER)
pages.append(("","ARélec — Électricien, chauffagiste & plombier à Plouzané (29)",
  "Électricité, chauffage et plomberie dans le bassin brestois depuis 2010. Devis gratuit, travail soigné. Estimez votre projet en ligne.",
  home_body, jsonld("/","Accueil",None,faq=FAQ_HOME), "home"))

# Helper subpage build
def gen_sub(slug,title,desc,active,crumb,eyebrow,h1,lead,hero_img,hero_float,sections,recap_h2,area,extra="",breadcrumb_name=None,hero_alt=None,faq=None,service=None):
    faq_html = faq_section(faq) if faq else ""
    body = (subnav(active) + subhero(crumb,eyebrow,h1,lead,hero_img,hero_float,hero_alt) + trust_strip()
            + "".join(feat_section(*s, flip=(i%2==1)) for i,s in enumerate(sections))
            + extra + faq_html + recap(recap_h2) + FOOTER)
    pages.append((slug,title,desc,body,jsonld("/"+slug,h1,area,breadcrumb_name=breadcrumb_name,faq=faq,service=service),"sub"))

CRUMB_M = '<a href="/">Accueil</a> › {label}'
CRUMB_L = '<a href="/">Accueil</a> › <a href="/{metier_url}">{metier}</a> › {commune}'

# ------- MÉTIERS -------
gen_sub("electricite","Électricien à Brest & Plouzané | ARélec",
 "Installation, rénovation, mise aux normes (NF C 15-100) et dépannage électrique dans le bassin brestois. Devis gratuit — ARélec.",
 "/electricite", CRUMB_M.format(label="Électricité"),
 "Électricité", "L'électricité, <b>du tableau à la dernière prise.</b>",
 'Notre cœur de métier depuis 2010. Installation, rénovation, mise aux normes et dépannage — à <a href="/electricien-brest">Brest</a>, <a href="/electricien-plouzane">Plouzané</a>, <a href="/electricien-saint-renan">Saint-Renan</a>, <a href="/electricien-landerneau">Landerneau</a> et dans une dizaine d\'autres communes du bassin brestois.',
 "escalier-led.jpg", "<span class='stars'>★★★★★</span> Avis Google",
 [("01","Installation &amp; rénovation","Du plan au dernier interrupteur",
   "Que ce soit une construction neuve ou une rénovation complète, on conçoit l'installation, on tire les gaines, on pose le tableau et les appareillages, et on remet la lumière en route. Vous repartez avec une installation propre, sûre et à jour.",
   ["Conception du plan électrique","Réseau et appareillage","Tableau et différentiels","Éclairage intérieur & extérieur"],
   "cablage.jpg","Chantier en cours"),
  ("02","Mise aux normes","NF C 15-100, sans tout casser",
   "Beaucoup de logements anciens ont une installation qui ne suit plus la norme. On vient diagnostiquer, on remplace ce qui doit l'être et on remet le tableau au propre — pièce par pièce, sans transformer votre maison en chantier.",
   ["Diagnostic complet","Mise aux normes NF C 15-100","Remplacement de tableau","Protection des personnes"],
   "reno-cablage.jpg","Rénovation"),
  ("03","Dépannage &amp; éclairage","Ça lâche ? On arrive.",
   "Un disjoncteur qui claque, une prise grillée, un éclairage qui ne marche plus : on intervient rapidement. Et pour les pièces où la lumière fait tout, on conçoit l'éclairage avec soin.",
   ["Intervention dépannage","Réparation rapide","Éclairage architectural","Pilotage simple"],
   "eclairage.jpg","Éclairage soigné")],
 "Un projet électrique ? Estimons-le ensemble.", None, breadcrumb_name="Électricité",
 faq=FAQ_ELEC, service=SERVICE_ELEC)

gen_sub("chauffage","Chauffagiste à Brest | ARélec",
 "Installation, remplacement et entretien de votre chauffage, radiateurs et eau chaude dans le bassin brestois. Devis gratuit — ARélec.",
 "/chauffage", CRUMB_M.format(label="Chauffage"),
 "Chauffage &amp; thermique", "Une maison <b>bien chauffée,</b> sans gaspiller.",
 'On installe, on remplace et on entretient votre chauffage à <a href="/chauffagiste-brest">Brest</a>, <a href="/chauffagiste-plouzane">Plouzané</a>, <a href="/chauffagiste-saint-renan">Saint-Renan</a>, <a href="/chauffagiste-landerneau">Landerneau</a> et dans une dizaine d\'autres communes du bassin brestois. L\'objectif : du confort l\'hiver, des factures sous contrôle.',
 "confort.jpg", "<span class='stars'>★★★★★</span> Avis Google",
 [("01","Installation &amp; remplacement","Un chauffage dimensionné juste",
   "On installe et on remplace votre chauffage avec un seul but : que vous soyez bien chez vous l'hiver. Radiateurs, distribution, eau chaude sanitaire — on dimensionne ce qui correspond à votre maison.",
   ["Installation neuve","Remplacement d'appareil","Radiateurs","Eau chaude sanitaire"],
   "chantier-plouider.jpg","Chantier rénovation"),
  ("02","Confort &amp; économies","Ce qui chauffe bien chauffe juste",
   "On revoit la régulation et l'équilibrage pour que chaque pièce soit à la bonne température. C'est souvent là qu'on gagne sur la facture, sans changer d'appareil.",
   ["Régulation et réglages","Équilibrage du réseau","Conseil économies","Pilotage simple"],
   "eclairage.jpg","Confort"),
  ("03","Entretien","Pour que ça dure",
   "Un chauffage entretenu consomme moins et tombe moins souvent en panne. On passe une fois par an, on contrôle, on règle, on remplace ce qui doit l'être.",
   ["Visite annuelle","Contrôle complet","Petits remplacements","Conseil de longévité"],
   "maison-bleue.jpg","Entretien à domicile")],
 "Un remplacement, une révision, une question ?", None, breadcrumb_name="Chauffage",
 faq=FAQ_CHAUF, service=SERVICE_CHAUF)

gen_sub("plomberie","Plombier à Brest | ARélec",
 "Salle de bain, sanitaires, recherche de fuite et réseau d'eau dans le bassin brestois. Rénovation soignée, devis gratuit — ARélec.",
 "/plomberie", CRUMB_M.format(label="Plomberie"),
 "Plomberie", "Sanitaire et réseau d'eau, <b>propre et durable.</b>",
 'Salle de bain, fuites, réseau d\'eau, sanitaires : on s\'occupe de toute la plomberie à <a href="/plombier-brest">Brest</a>, <a href="/plombier-plouzane">Plouzané</a>, <a href="/plombier-saint-renan">Saint-Renan</a>, <a href="/plombier-landerneau">Landerneau</a> et dans une dizaine d\'autres communes du bassin brestois.',
 "plomb.jpg", "<span class='stars'>★★★★★</span> Avis Google",
 [("01","Salle de bain","Le plus gros chantier, fait propre",
   "Refaire une salle de bain, c'est dépose, réseau d'eau, sanitaires, douche et finitions. On gère tout du début à la fin, sans laisser de tranchée ouverte le week-end.",
   ["Dépose de l'ancienne","Réseau d'eau","Douche / baignoire / WC","Coordination carrelage"],
   "sdb-bois.jpg","Salle de bain — Plouider"),
  ("02","Recherche &amp; réparation de fuites","On trouve, on répare.",
   "Une fuite, c'est rarement où on croit. On localise précisément avant d'ouvrir, on répare, et on remet en état — sans tout casser.",
   ["Localisation précise","Réparation propre","Remise en état","Conseil prévention"],
   "douche-marbre.jpg","Réno haut de gamme"),
  ("03","Réseau d'eau &amp; sanitaires","Du tuyau à la robinetterie",
   "On reprend le réseau d'eau dans les rénovations, on installe les évacuations et la robinetterie. Pas de bidouille — on remet aux standards d'aujourd'hui.",
   ["Refonte réseau eau","Évacuations","Robinetterie","Mises aux normes"],
   "sdb-marbre.jpg","Finitions soignées")],
 "Une salle de bain, une fuite, un projet ?", None, breadcrumb_name="Plomberie",
 faq=FAQ_PLOMB, service=SERVICE_PLOMB)

# ------- LOCALES -------
def gen_local(slug,title,desc,metier,metier_url,commune,commune_label,h1,lead,hero_img,sec01,sec02,sec03,recap_h2):
    crumb=CRUMB_L.format(metier_url=metier_url,metier=metier,commune=commune_label)
    gen_sub(slug,title,desc,"/"+metier_url,crumb,metier+" à "+commune,h1,lead,hero_img,
            "<span class='stars'>★★★★★</span> Avis Google",
            [sec01,sec02,sec03],recap_h2,commune,
            breadcrumb_name=commune_label,
            hero_alt=f"{metier} à {commune_label} — ARélec, chantier dans le bassin brestois")

SEC_INTERLO=("03","Un seul interlocuteur","Élec, chauffage, plomberie.",
 "On fait les trois métiers nous-mêmes. Vous n'avez pas à coordonner plusieurs entreprises : une seule personne suit le chantier, du devis à la mise en route.",
 ["Électricité","Chauffage & thermique","Plomberie","Coordination du chantier"], "maison-bleue.jpg","Vue d'ensemble")

# électricien × communes
gen_local("electricien-brest","Électricien à Brest (29) | ARélec depuis 2010",
 "Électricien à Brest : rénovation, mise aux normes, tableau et dépannage. Aussi chauffage et plomberie. Devis gratuit — ARélec.",
 "Électricité","electricite","Brest","Brest",
 "Votre <b>électricien à Brest.</b>",
 "Depuis 2010, on intervient dans tous les quartiers brestois — du centre aux Rives de la Penfeld et à Saint-Marc.",
 "cablage.jpg",
 ("01","À Brest depuis 2010","Du centre aux Rives de la Penfeld",
  "On intervient dans tous les quartiers brestois — Saint-Marc, Rives de la Penfeld, Recouvrance, l'Europe. Beaucoup de logements brestois ont une installation qui a vieilli ; on s'y connaît, on reprend ça proprement.",
  ["Brest centre & quartiers","Maisons anciennes","Appartements rénovation","Mise aux normes"], "reno-cablage.jpg","Chantier à Brest"),
 ("02","Notre savoir-faire élec","Du tableau à l'éclairage soigné",
  "Tableau électrique, mise aux normes NF C 15-100, dépannage, éclairage : c'est notre cœur de métier depuis quinze ans, et ça se voit sur les finitions.",
  ["Tableau & différentiels","Mise aux normes","Dépannage rapide","Éclairage soigné"], "escalier-led.jpg","Éclairage LED"),
 SEC_INTERLO,
 "Un projet à Brest ? Estimons-le ensemble.")

gen_local("electricien-plouzane","Électricien à Plouzané (29) | ARélec",
 "Électricien à Plouzané : ARélec est installé ici depuis 2010. Installation, rénovation, mise aux normes, dépannage. Devis gratuit.",
 "Électricité","electricite","Plouzané","Plouzané",
 "Votre <b>électricien à Plouzané.</b>",
 "Plouzané, c'est chez nous : l'entreprise est basée ici depuis 2010. On connaît le secteur, on arrive vite.",
 "maison-bleue.jpg",
 ("01","Plouzané, c'est chez nous","Basés sur la commune depuis 2010",
  "L'entreprise est à Plouzané. Concrètement : on connaît le secteur, on arrive vite, et on ne facture pas un Paris-Brest pour passer chez vous.",
  ["Intervention rapide","Sur la commune","Bassin brestois","Conseil & suivi"], "eclairage.jpg","Sur place"),
 ("02","Notre savoir-faire élec","Tableau, mise aux normes, dépannage",
  "En neuf comme en rénovation, on prend en charge le tableau, les prises, l'éclairage et la mise aux normes. Un dépannage qui ne peut pas attendre ? On est juste à côté.",
  ["Tableau & différentiels","Mise aux normes","Dépannage rapide","Éclairage soigné"], "escalier-led.jpg","Travail soigné"),
 SEC_INTERLO,
 "Un projet à Plouzané ? Estimons-le ensemble.")

gen_local("electricien-plouider","Électricien à Plouider (29) | ARélec",
 "Électricien à Plouider et alentour : installation, rénovation et dépannage électrique. ARélec, artisan depuis 2010. Devis gratuit.",
 "Électricité","electricite","Plouider","Plouider",
 "Votre <b>électricien à Plouider.</b>",
 "On a déjà nos chantiers à Plouider et on continue d'y travailler. On se déplace avec ce qu'il faut.",
 "chantier-plouider.jpg",
 ("01","À Plouider","On y a déjà nos chantiers",
  "On a réalisé une grande rénovation à Plouider et on continue d'y intervenir. L'idée : se déplacer avec le matériel qu'il faut pour repartir avec le travail terminé.",
  ["Chantiers réalisés","Déplacement préparé","Travail bouclé","Conseil sur place"], "chantier-plouider.jpg","Chantier Plouider"),
 ("02","Notre savoir-faire élec","Du tableau à l'éclairage",
  "Pour une rénovation, une remise aux normes ou un dépannage : tableau, NF C 15-100, prises, éclairage. On fait simple et propre.",
  ["Tableau & différentiels","Mise aux normes","Dépannage rapide","Éclairage soigné"], "escalier-led.jpg","Travail soigné"),
 SEC_INTERLO,
 "Un projet à Plouider ? On vient voir.")

# plombier × communes
gen_local("plombier-brest","Plombier à Brest (29) | ARélec",
 "Plombier à Brest : rénovation de salle de bain, recherche de fuite, réseau d'eau, sanitaires. Travail soigné, devis gratuit — ARélec.",
 "Plomberie","plomberie","Brest","Brest",
 "Votre <b>plombier à Brest.</b>",
 "À Brest, salle de bain et fuites en appartement : on gère tout ça dans tous les quartiers, propre et rapide.",
 "plomb.jpg",
 ("01","À Brest, salle de bain et dépannage","Du centre aux Rives de la Penfeld",
  "À Brest, deux gros sujets reviennent souvent : la salle de bain à refaire (dans les maisons anciennes du centre, à Saint-Marc, aux Rives de la Penfeld) et les fuites en appartement (centre-ville, Recouvrance). On gère les deux, proprement, sans laisser le chantier ouvert le week-end.",
  ["Maisons anciennes","Appartements centre-ville","Recherche de fuite","Salle de bain réno"], "sdb-bleue.jpg","Réno SDB à Brest"),
 ("02","Salle de bain de A à Z","Dépose, eau, douche, finitions",
  "Refaire une salle de bain, c'est dépose de l'ancienne, réseau d'eau, douche ou baignoire, sanitaires et finitions. On suit le chantier du début à la fin, sans tranchée ouverte le week-end.",
  ["Dépose de l'ancienne","Réseau d'eau","Douche / baignoire / WC","Coordination carrelage"], "sdb-bois.jpg","Salle de bain bois"),
 SEC_INTERLO,
 "Une salle de bain ou une fuite à Brest ?")

gen_local("plombier-plouzane","Plombier à Plouzané (29) | ARélec",
 "Plombier à Plouzané : ARélec, basé sur la commune. Salle de bain, fuites, réseau d'eau, sanitaires. Devis gratuit, intervention rapide.",
 "Plomberie","plomberie","Plouzané","Plouzané",
 "Votre <b>plombier à Plouzané.</b>",
 "Installés à Plouzané, on n'est jamais loin : pour une fuite ou une salle de bain, on arrive vite.",
 "plomb.jpg",
 ("01","À Plouzané, basés ici","Notre base depuis 2010",
  "Plouzané, c'est notre base depuis 2010. Pour une fuite, une salle de bain à refaire ou un réseau d'eau à reprendre, on vient vite. Et comme on est aussi électriciens et chauffagistes, on enchaîne le reste du chantier dans la foulée — un seul interlocuteur, du devis à la mise en route.",
  ["Intervention rapide","Sur la commune","Maisons individuelles","Coordination chantier"], "sdb-bleue.jpg","Réno SDB à Plouzané"),
 ("02","Salle de bain & sanitaires","Dépose, eau, finitions",
  "On reprend le réseau d'eau, on pose les sanitaires, et on laisse le chantier propre en partant. Si l'élec ou le chauffage doivent suivre, on enchaîne.",
  ["Dépose de l'ancienne","Réseau d'eau","Sanitaires & robinetterie","Finitions propres"], "sdb-bois.jpg","Finitions"),
 SEC_INTERLO,
 "Un projet de plomberie à Plouzané ?")

gen_local("plombier-plouider","Plombier à Plouider (29) | ARélec",
 "Plombier à Plouider : salle de bain, réseau d'eau et sanitaires lors de vos travaux. ARélec, artisan depuis 2010 — devis gratuit.",
 "Plomberie","plomberie","Plouider","Plouider",
 "Votre <b>plombier à Plouider.</b>",
 "À Plouider, on a fait toute la plomberie d'une grande rénovation — en même temps que l'élec et le chauffage.",
 "plomb.jpg",
 ("01","À Plouider","On y a déjà bossé",
  "On a réalisé la plomberie complète d'une grande rénovation à Plouider — salle de bain, réseau d'eau, sanitaires — en même temps que l'élec et le chauffage. Un seul interlocuteur, on suit tout du début à la fin, et le chantier reste propre.",
  ["Chantier réalisé","Plomberie complète","Salle de bain","Réseau d'eau"], "chantier-plouider.jpg","Chantier Plouider"),
 ("02","Salle de bain &amp; sanitaires","Dépose, eau, finitions",
  "On reprend le réseau d'eau, on pose la douche, le meuble et les sanitaires au propre, et on laisse le chantier net en partant. Si l'élec ou le chauffage doivent suivre, on enchaîne dans la foulée.",
  ["Dépose de l'ancienne","Réseau d'eau","Sanitaires &amp; robinetterie","Finitions propres"], "sdb-bois.jpg","Finitions soignées"),
 SEC_INTERLO,
 "Un projet de plomberie à Plouider ?")

# chauffagiste × communes
gen_local("chauffagiste-brest","Chauffagiste à Brest (29) | ARélec",
 "Chauffagiste à Brest : installation, remplacement et entretien de votre chauffage, radiateurs et eau chaude. Devis gratuit — ARélec.",
 "Chauffage","chauffage","Brest","Brest",
 "Votre <b>chauffagiste à Brest.</b>",
 "Installation, remplacement et entretien de votre chauffage à Brest. Confort, simplicité et factures sous contrôle.",
 "confort.jpg",
 ("01","À Brest","Du centre aux Rives de la Penfeld",
  "À Brest, on intervient dans toute la ville — de Saint-Marc aux Rives de la Penfeld, de Recouvrance au centre. Beaucoup d'appartements et de maisons brestoises ont une installation qui date : on remplace une chaudière fatiguée, on rééquilibre les radiateurs, on remet l'eau chaude propre.",
  ["Quartiers brestois couverts","Remplacement de chaudière","Radiateurs &amp; ECS","Mise au propre des réglages"], "eclairage.jpg","Confort à Brest"),
 ("02","Confort &amp; économies","Régulation et équilibrage",
  "On revoit la régulation et l'équilibrage du réseau : chaque pièce à la bonne température, et la facture qui baisse — sans changer d'appareil.",
  ["Régulation","Équilibrage","Conseil économies","Pilotage simple"], "maison-bleue.jpg","Ajustement fin"),
 SEC_INTERLO,
 "Un chauffage à remplacer ou à entretenir ?")

gen_local("chauffagiste-plouzane","Chauffagiste à Plouzané (29) | ARélec",
 "Chauffagiste à Plouzané : ARélec installe, remplace et entretient votre chauffage. Basé sur la commune depuis 2010. Devis gratuit.",
 "Chauffage","chauffage","Plouzané","Plouzané",
 "Votre <b>chauffagiste à Plouzané.</b>",
 "Basés à Plouzané, on s'occupe de votre chauffage de l'installation à l'entretien.",
 "confort.jpg",
 ("01","À Plouzané","Basés ici depuis 2010",
  "Plouzané, c'est chez nous. Pour les maisons néo-bretonnes du coin (et il y en a beaucoup), un chauffage bien dimensionné et bien réglé change la vie l'hiver. On installe en neuf, on remplace l'existant fatigué, on entretient — du tableau de bord aux radiateurs de l'étage.",
  ["Maisons néo-bretonnes","Installation neuve","Remplacement","Réglages &amp; entretien"], "eclairage.jpg","Sur la commune"),
 ("02","Confort &amp; économies","Le bon réglage, pas plus",
  "On revoit la régulation et l'équilibrage du réseau pour que chaque pièce soit à bonne température. Souvent, on gagne sur la facture sans changer d'appareil.",
  ["Régulation","Équilibrage","Conseil économies","Pilotage simple"], "maison-bleue.jpg","Ajustement"),
 SEC_INTERLO,
 "Un chauffage à voir à Plouzané ?")

gen_local("chauffagiste-plouider","Chauffagiste à Plouider (29) | ARélec",
 "Chauffagiste à Plouider : installation et entretien du chauffage lors de vos travaux. ARélec, artisan depuis 2010 — devis gratuit.",
 "Chauffage","chauffage","Plouider","Plouider",
 "Votre <b>chauffagiste à Plouider.</b>",
 "À Plouider, on a déjà installé le chauffage lors d'une grande rénovation — en coordination avec l'élec et la plomberie.",
 "confort.jpg",
 ("01","À Plouider","On y a déjà fait du gros chantier",
  "À Plouider, on a été missionnés pour une rénovation complète où on a installé le chauffage en plus de l'élec et de la plomberie. C'est tout l'intérêt d'ARélec : un seul interlocuteur, du tableau au radiateur du fond du couloir.",
  ["Chantier réalisé","Coordination des 3 métiers","Installation chauffage","Eau chaude sanitaire"], "chantier-plouider.jpg","Chantier Plouider"),
 ("02","Confort &amp; économies","Le bon réglage, pas plus",
  "On revoit la régulation et l'équilibrage du réseau pour que chaque pièce soit à la bonne température. Souvent, on gagne sur la facture sans changer d'appareil.",
  ["Régulation","Équilibrage","Conseil économies","Pilotage simple"], "maison-bleue.jpg","Ajustement fin"),
 SEC_INTERLO,
 "Un chauffage à voir à Plouider ?")

# ---------- PAGES LOCALES AUTO (autres communes du bassin brestois) ----------
SEC02_E=("02","Notre savoir-faire élec","Du tableau à l'éclairage soigné",
  "Tableau, mise aux normes NF C 15-100, dépannage et éclairage : c'est notre cœur de métier depuis quinze ans, et ça se voit sur les finitions.",
  ["Tableau &amp; différentiels","Mise aux normes","Dépannage rapide","Éclairage soigné"],"escalier-led.jpg","Travail soigné")
SEC02_P=("02","Salle de bain &amp; sanitaires","Dépose, eau, finitions",
  "On reprend le réseau d'eau, on pose la douche, le meuble et les sanitaires au propre, et on laisse le chantier net en partant.",
  ["Dépose de l'ancienne","Réseau d'eau","Sanitaires &amp; robinetterie","Finitions propres"],"sdb-bois.jpg","Finitions soignées")
SEC02_C=("02","Confort &amp; économies","Le bon réglage, pas plus",
  "On revoit la régulation et l'équilibrage du réseau pour que chaque pièce soit à la bonne température. Souvent, on gagne sur la facture sans changer d'appareil.",
  ["Régulation","Équilibrage","Conseil économies","Pilotage simple"],"maison-bleue.jpg","Ajustement fin")

# (metier_slug, metier_label, metier_url, hero_img, sec01_img, noun, desc_short, prest_lower, sec01_items, sec02)
METIER_DEFS=[
 ("electricien","Électricité","electricite","escalier-led.jpg","reno-cablage.jpg","Électricien",
  "installation, rénovation, mise aux normes et dépannage électrique",
  "installation, rénovation, mise aux normes (NF C 15-100), remplacement de tableau et dépannage",
  ["Installation neuve","Rénovation électrique","Mise aux normes NF C 15-100","Dépannage rapide"], SEC02_E),
 ("plombier","Plomberie","plomberie","plomb.jpg","sdb-bleue.jpg","Plombier",
  "salle de bain, recherche de fuite, réseau d'eau et sanitaires",
  "salle de bain, recherche de fuite, réseau d'eau et sanitaires",
  ["Salle de bain","Recherche de fuite","Réseau d'eau","Sanitaires"], SEC02_P),
 ("chauffagiste","Chauffage","chauffage","confort.jpg","eclairage.jpg","Chauffagiste",
  "installation, remplacement et entretien du chauffage",
  "installation, remplacement et entretien du chauffage, eau chaude sanitaire et réglages",
  ["Installation neuve","Remplacement","Eau chaude sanitaire","Réglages"], SEC02_C),
]

COMMUNE_HOOKS={
 "le-conquet":"À la pointe ouest, en bord d'iroise.",
 "saint-renan":"Au cœur du Pays d'Iroise, à 10 km de Brest.",
 "guipavas":"À l'est de Brest, secteur résidentiel dynamique.",
 "le-relecq-kerhuon":"Rive sud de l'Élorn, à 5 km de Brest.",
 "guilers":"Juste au nord de Plouzané, voisin direct.",
 "plougonvelin":"En bord de mer, vers la pointe Saint-Mathieu.",
 "locmaria-plouzane":"Juste à côté de notre atelier, on est sur place vite.",
 "lannilis":"Pays des Abers, au nord du Pays de Brest.",
 "plabennec":"Pays des Abers, à 15 km de Brest.",
 "landerneau":"Sur l'Élorn, à 20 km — on s'y déplace régulièrement.",
}

for m_slug,m_label,m_url,hero_img,sec01_img,noun,desc_short,prest_lower,sec01_items,sec02 in METIER_DEFS:
    for c_slug,c_label in EXTRA_COMMUNES:
        hook=COMMUNE_HOOKS.get(c_slug,"")
        title=f"{noun} à {c_label} (29) | ARélec"
        desc=f"{noun} à {c_label} : {desc_short}. ARélec, artisan depuis 2010 — devis gratuit."
        h1=f"Votre <b>{noun.lower()} à {c_label}.</b>"
        lead=f"ARélec intervient à {c_label} et alentour : {prest_lower}. {hook}"
        sec01=("01",f"À {c_label}", hook or "Une commune du bassin brestois",
          f"À {c_label}, on prend en charge votre projet en neuf comme en rénovation : {prest_lower}. {c_label} fait partie de notre zone d'intervention naturelle — on s'y déplace avec ce qu'il faut, sans facturer un Paris-Brest.",
          sec01_items, sec01_img, f"{noun} à {c_label}")
        gen_local(f"{m_slug}-{c_slug}", title, desc, m_label, m_url, c_label, c_label,
                  h1, lead, hero_img, sec01, sec02, SEC_INTERLO,
                  f"Un projet de {noun.lower()} à {c_label} ?")

# ---------- STUBS ----------
def stub(slug,title,desc,h1,inner,breadcrumb_name=None):
    body=('<section class="panel visible" id="hero"><div class="bg"></div>'+nav_home("/"+slug)+
      '<div class="spacer"></div><div class="content"><h1 class="reveal d2">'+h1+'</h1>'
      '<div class="hr reveal d3"></div><div class="reveal d4" style="max-width:640px;color:rgba(255,255,255,.92);line-height:1.6">'+inner+'</div></div>'
      '<div class="scrollhint">Suite<div class="arr"></div></div></section>'+FOOTER)
    pages.append((slug,title,desc,body,jsonld("/"+slug,h1,None,reviews=False,breadcrumb_name=breadcrumb_name),"home"))

# ---------- /contact : page simple (3 boutons + formulaire) ----------
PHONE_MOBILE_DISP="06 78 02 04 24"; PHONE_MOBILE_TEL="0678020424"; WHATSAPP_INT="33678020424"
contact_body=(subnav("/contact")+
 '<section class="contact-hero"><div class="wrap-c">'
 '<div class="crumb"><a href="/">Accueil</a> › Contact</div>'
 '<div class="eyebrow-blue">Contact</div>'
 '<h1>Parlons de <b>votre projet.</b></h1>'
 '<p class="lead">Trois options pour nous joindre. Le plus rapide, c\'est l\'appel ou WhatsApp.</p>'
 '</div></section>'
 '<section class="contact-methods"><div class="wrap-c">'
 f'<a class="cmethod" href="tel:{PHONE_MOBILE_TEL}"><div class="cm-icon">{SVG_PHONE}</div><div class="cm-body"><div class="cm-label">Appeler</div><div class="cm-value">{PHONE_MOBILE_DISP}</div></div></a>'
 f'<a class="cmethod cmethod-whatsapp" href="https://wa.me/{WHATSAPP_INT}" target="_blank" rel="noopener"><div class="cm-icon">{SVG_WA}</div><div class="cm-body"><div class="cm-label">WhatsApp</div><div class="cm-value">{PHONE_MOBILE_DISP}</div></div></a>'
 f'<a class="cmethod" href="mailto:{EMAIL}"><div class="cm-icon">{SVG_MAIL}</div><div class="cm-body"><div class="cm-label">Email</div><div class="cm-value">{EMAIL}</div></div></a>'
 '</div></section>'
 '<section class="contact-form-section"><div class="wrap-c">'
 '<h2>Ou laissez-nous un message.</h2>'
 '<p class="sub">On revient vers vous sous 24 à 48 h.</p>'
 '<form class="cform" id="cform" action="mailto:contact@entreprise-arelec.fr" method="POST" enctype="text/plain">'
 '<div class="cfrow">'
 '<label>Nom <input name="nom" type="text" required autocomplete="name"></label>'
 '<label>Téléphone <input name="tel" type="tel" autocomplete="tel"></label>'
 '</div>'
 '<label>Email <input name="email" type="email" required autocomplete="email"></label>'
 '<label>Votre projet <textarea name="message" rows="5" required placeholder="Type de travaux (élec, chauffage, plomberie), commune, délais..."></textarea></label>'
 '<button type="submit" class="btn solid">Envoyer →</button>'
 '<p class="cform-foot">Vos informations servent uniquement à vous répondre.</p>'
 '</form>'
 '</div></section>'+FOOTER+
 '<script>document.getElementById("cform")?.addEventListener("submit",function(e){e.preventDefault();const f=e.target;const body=`Nom: ${f.nom.value}\\nTéléphone: ${f.tel.value}\\nEmail: ${f.email.value}\\n\\nMessage:\\n${f.message.value}`;const subject=`Demande ARélec — ${f.nom.value}`;window.location.href=`mailto:contact@entreprise-arelec.fr?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;});</script>')
pages.append(("contact","Contact & devis gratuit | ARélec — Plouzané (29)",
 "Contactez ARélec : 06 78 02 04 24, WhatsApp ou contact@entreprise-arelec.fr. Devis gratuit dans tout le bassin brestois.",
 contact_body, jsonld("/contact","Contact",None), "sub"))
gen_sub("entreprise","L'entreprise | ARélec, artisan depuis 2010",
 "ARélec, artisan électricien-chauffagiste-plombier à Plouzané depuis 2010. Une équipe, un seul interlocuteur, un travail soigné dans tout le bassin brestois.",
 "/entreprise", CRUMB_M.format(label="L'entreprise"),
 "L'entreprise", "ARélec, <b>depuis 2010.</b>",
 "Artisan installé à Plouzané, on s'occupe de l'élec, du chauffage et de la plomberie dans le bassin brestois. En neuf, en rénovation, en dépannage. Un seul interlocuteur, de A à Z.",
 "hero.jpg", "<span class='stars'>★★★★★</span> Avis Google",
 [("01","Depuis 2010","Une histoire d'artisan, à Plouzané.",
   "On a démarré ARélec en 2010, ici, dans le bassin brestois. Le principe de base : qu'un même artisan puisse refaire la maison de bout en bout — élec, chauffage, plomberie — sans qu'il faille jongler avec trois entreprises. Quinze ans plus tard, on fait toujours comme ça. Le pont sur le logo, c'est le pont de l'Iroise. On est d'ici, on y reste.",
   ["Créée en 2010","Basée à Plouzané (29280)","Bassin brestois &amp; Finistère","Gérée par Arnaud Roncey"],
   "maison-bleue.jpg","Plouzané, depuis 2010"),
  ("02","Comment on bosse","Pas de magie, du travail d'artisan.",
   "On arrive, on regarde, on explique. On bosse propre, on range en partant, et on donne de vrais conseils — quitte à dire qu'un truc n'est pas utile chez vous. Si on doit revenir, on revient. C'est ce qui fait que les gens nous rappellent pour les chantiers suivants.",
   ["On bosse propre","On dit ce qu'on pense","On revient si besoin","On finit ce qu'on commence"],
   "chantier-plouider.jpg","Chantier en cours"),
  ("03","L'avantage","Trois métiers, par la même équipe.",
   'On fait les trois métiers nous-mêmes : <a href="/electricite">électricité</a>, <a href="/chauffage">chauffage</a> et <a href="/plomberie">plomberie</a>. Pour une rénovation, ça veut dire un seul devis, pas de coordination à faire entre artisans, et personne qui attend l\'autre sur le chantier. Si l\'un dépend de l\'autre, on s\'organise tout seul.',
   ["Électricité","Chauffage &amp; thermique","Plomberie","Coordination du chantier"],
   "escalier-led.jpg","Trois métiers, une équipe")],
 "Un projet ? On en parle.", None, breadcrumb_name="L'entreprise")
# ---------- /realisations : galerie des chantiers ----------
GALLERY=[
 ("hero.jpg","Rénovation","Extension bois & pierre, à l'heure bleue · Plouider"),
 ("plomb.jpg","Salle de bain","Bois & marbre — bassin brestois"),
 ("chantier-plouider.jpg","Rénovation complète","Façade & toiture en cours · Plouider"),
 ("escalier-led.jpg","Éclairage","Escalier à LED intégrées"),
 ("sdb-bois.jpg","Salle de bain","Combles & habillage bois"),
 ("eclairage.jpg","Éclairage","Pièce aménagée · appliques chaudes"),
 ("sdb-marbre.jpg","Salle de bain","Marbre noir & meuble blanc"),
 ("cablage.jpg","Électricité","Réseau électrique en cours"),
 ("confort.jpg","Rénovation","Chambre rénovée"),
 ("sdb-baignoire.jpg","Salle de bain","Combles & baignoire îlot"),
 ("douche-marbre.jpg","Plomberie","Douche italienne · marbre"),
 ("sdb-bleue.jpg","Salle de bain","Meuble bleu & finitions blanches"),
 ("reno-cablage.jpg","Électricité","Câblage & isolation phonique"),
]
gallery_items="".join(
 f'<figure class="rcard"><img src="/assets/img/{img}" alt="{cap}" loading="lazy">'
 f'<figcaption><div class="rkind">{kind}</div><div class="rloc">{cap}</div></figcaption></figure>'
 for img,kind,cap in GALLERY)
real_body=(subnav("/realisations")+
 '<section class="contact-hero"><div class="wrap-c">'
 '<div class="crumb"><a href="/">Accueil</a> › Réalisations</div>'
 '<div class="eyebrow-blue">Réalisations</div>'
 '<h1>Nos <b>chantiers.</b></h1>'
 '<p class="lead">Quelques travaux récents dans le bassin brestois — élec, chauffage, plomberie, rénovations complètes.</p>'
 '</div></section>'+trust_strip()+
 '<section class="gallery-section"><div class="wrap-g">'
 f'<div class="gallery">{gallery_items}</div>'
 '</div></section>'
 +gradual_blur(position="bottom",height="8rem",strength=1.1,divCount=6,curve="bezier",exponential=True,target="page")
 +recap("Un projet similaire ? On en parle.")+FOOTER+
 '<script>(function(){const b=document.querySelector(\'.gradual-blur[data-target="page"]\');const g=document.querySelector(".gallery-section");if(!b||!g)return;let raf=0;function u(){const r=g.getBoundingClientRect();const vh=window.innerHeight;const bh=b.offsetHeight||128;const overlap=r.top<vh && r.bottom>(vh-bh);b.classList.toggle("on",overlap);raf=0;}function onScroll(){if(!raf)raf=requestAnimationFrame(u);}window.addEventListener("scroll",onScroll,{passive:true});window.addEventListener("resize",onScroll);u();})();</script>')
pages.append(("realisations","Nos réalisations | ARélec — Brest & Finistère",
 "Galerie de nos chantiers à Brest, Plouzané et alentour : salles de bain, rénovations complètes, éclairage et installations électriques.",
 real_body, jsonld("/realisations","Réalisations",None), "sub"))
stub("estimation","Faire une estimation | ARélec",
 "Estimez vos travaux d'électricité, chauffage ou plomberie en ligne, puis ARélec vient affiner sur place. Gratuit.",
 "Estimez<br><b>vos travaux.</b>",
 "L'estimateur en ligne arrive bientôt : un aperçu de prix en quelques minutes, puis une visite sur place gratuite pour le vrai devis. En attendant, appelez-nous.",
 breadcrumb_name="Estimation")
stub("avis","Avis clients | ARélec — Brest & Plouzané",
 "Ce que nos clients disent d'ARélec : qualité, propreté, réactivité et bons conseils. Avis vérifiés Google.",
 "Ils nous<br><b>recommandent.</b>",
 "Qualité du travail, chantier propre, réactivité et bons conseils reviennent dans nos avis Google. Retrouvez-les en bas de chaque page.",
 breadcrumb_name="Avis clients")
stub("mentions-legales","Mentions légales | ARélec","Mentions légales du site ARélec (SARL ARélec, Plouzané).",
 "Mentions<br><b>légales.</b>","SARL ARélec — SIREN 790 223 036 — Plouzané (29280). Directeur de la publication : Arnaud Roncey. <em>(À compléter : hébergeur, capital, TVA.)</em>",
 breadcrumb_name="Mentions légales")
stub("politique-confidentialite","Politique de confidentialité | ARélec","Politique de confidentialité et gestion des données du site ARélec.",
 "Confidentialité.","Les données envoyées via le formulaire de contact servent uniquement à répondre à votre demande. <em>(À compléter avec Arnaud.)</em>",
 breadcrumb_name="Confidentialité")

# ---------- écriture ----------
for slug,t,d,body,jl,kind in pages:
    if kind=="sub": write(slug, shell_sub(slug,t,d,body,jl))
    else: write(slug, shell_home(slug,t,d,body,jl, dots=(4 if slug=="" else 0)))

urls=[p[0] for p in pages]
TODAY=datetime.date.today().isoformat()
def url_meta(u):
    if u=="": return ("1.0","weekly")
    if u in ("electricite","chauffage","plomberie"): return ("0.9","monthly")
    if u in ("contact","estimation"): return ("0.8","monthly")
    if u in ("realisations","entreprise","avis"): return ("0.7","monthly")
    if u in ("mentions-legales","politique-confidentialite"): return ("0.2","yearly")
    return ("0.6","monthly")  # pages locales [métier]-[commune]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    loc=DOMAIN+("/" if u=="" else "/"+u+"/")
    pr,cf=url_meta(u)
    sm+=f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n'
sm+='</urlset>\n'
(SITE/"sitemap.xml").write_text(sm)

# ---------- robots.txt avec directives IA explicites ----------
ROBOTS = f"""# robots.txt — ARélec (entreprise-arelec.fr)
User-agent: *
Allow: /

# Crawlers IA — autorisés à indexer et citer le contenu
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bingbot
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
(SITE/"robots.txt").write_text(ROBOTS)

# ---------- llms.txt — résumé pour crawlers IA ----------
LLMS_TXT = f"""# ARélec

> Artisan électricien, chauffagiste et plombier installé à Plouzané (29280) depuis 2010. Intervention dans tout le bassin brestois (Finistère).

## Identité

- **Nom légal** : SARL ARélec
- **SIREN** : 790 223 036
- **Gérant** : Arnaud Roncey
- **Adresse** : Plouzané (29280), Finistère, France
- **Téléphone** : +33 2 98 40 20 43 (fixe) · +33 6 78 02 04 24 (mobile / WhatsApp)
- **Email** : contact@entreprise-arelec.fr
- **Année de création** : 2010
- **Site web** : {DOMAIN}

## Métiers

ARélec couvre trois métiers du bâtiment, en interne, avec la même équipe :

1. **Électricité** — installation, rénovation, mise aux normes NF C 15-100, dépannage, tableau électrique, éclairage architectural.
2. **Chauffage / thermique** — installation, remplacement, dimensionnement, entretien annuel, régulation, équilibrage du réseau.
3. **Plomberie** — salle de bain complète, recherche de fuite, réseau d'eau, sanitaires, robinetterie, évacuations.

Un seul interlocuteur prend en charge le chantier de A à Z, sans coordination à faire entre plusieurs artisans.

## Zone d'intervention

Siège à Plouzané (29280). Interventions dans tout le bassin brestois :

- Brest
- Plouzané (siège)
- Saint-Renan
- Le Conquet
- Landerneau
- Plouider
- Guipavas
- Le Relecq-Kerhuon
- Guilers
- Plougonvelin
- Locmaria-Plouzané
- Lannilis
- Plabennec

Rayon d'intervention typique : environ 30 km autour de Plouzané, dans le Finistère.

## Comment travailler avec ARélec

1. **Estimation en ligne gratuite** (~2 minutes) sur {DOMAIN}/estimation
2. **Visite sur place gratuite** pour établir le vrai devis si la fourchette correspond
3. **Devis détaillé**, écrit, sans engagement
4. **Réalisation du chantier** par la même équipe, de la dépose à la mise en route

Devis toujours gratuit. Réponse sous 24 à 48 h.

## Pages clés

- [Accueil]({DOMAIN}/)
- [Électricité]({DOMAIN}/electricite/)
- [Chauffage]({DOMAIN}/chauffage/)
- [Plomberie]({DOMAIN}/plomberie/)
- [Réalisations]({DOMAIN}/realisations/)
- [L'entreprise]({DOMAIN}/entreprise/)
- [Avis clients]({DOMAIN}/avis/)
- [Estimation]({DOMAIN}/estimation/)
- [Contact]({DOMAIN}/contact/)
- [Documentation complète pour IA]({DOMAIN}/llms-full.txt)

## Pages locales par métier

ARélec a une page dédiée pour chaque combinaison métier × commune :

- Électricien : {DOMAIN}/electricien-brest/, electricien-plouzane, electricien-saint-renan, electricien-le-conquet, electricien-landerneau, electricien-plouider, electricien-guipavas, electricien-le-relecq-kerhuon, electricien-guilers, electricien-plougonvelin, electricien-locmaria-plouzane, electricien-lannilis, electricien-plabennec
- Chauffagiste : même liste de communes, préfixe `chauffagiste-`
- Plombier : même liste de communes, préfixe `plombier-`

## Contact

- Téléphone : 02 98 40 20 43
- WhatsApp : 06 78 02 04 24
- Email : contact@entreprise-arelec.fr
- Formulaire : {DOMAIN}/contact/

Dernière mise à jour : {TODAY}
"""
(SITE/"llms.txt").write_text(LLMS_TXT)

# ---------- llms-full.txt — documentation détaillée pour IA ----------
def _faq_block(title, qa_pairs):
    out = [f"### {title}", ""]
    for q, a in qa_pairs:
        out.append(f"**Q : {q}**")
        out.append("")
        out.append(f"R : {a}")
        out.append("")
    return "\n".join(out)

LLMS_FULL = f"""# ARélec — documentation complète

> Artisan électricien, chauffagiste et plombier installé à Plouzané (29280) depuis 2010. Intervention dans tout le bassin brestois (Finistère).

Ce fichier est destiné aux moteurs de recherche IA (ChatGPT, Perplexity, Claude, Google AI Overviews, Bing Copilot) pour comprendre l'activité, la zone, et les compétences d'ARélec, et pouvoir citer l'entreprise dans leurs réponses.

---

## 1. Qui est ARélec

ARélec (raison sociale : SARL ARélec, SIREN 790 223 036) est une entreprise artisanale du bâtiment fondée en 2010 et installée à Plouzané (29280), dans le Finistère, en France. Le gérant est Arnaud Roncey. L'entreprise couvre trois métiers complémentaires — électricité, chauffage, plomberie — avec une seule équipe, ce qui permet à un client de mener une rénovation complète sans coordonner plusieurs artisans.

ARélec intervient principalement dans le bassin brestois : Brest, Plouzané, Saint-Renan, Le Conquet, Landerneau, Plouider, Guipavas, Le Relecq-Kerhuon, Guilers, Plougonvelin, Locmaria-Plouzané, Lannilis, Plabennec. Le rayon d'intervention typique est d'environ 30 km autour de Plouzané.

Le devis est toujours gratuit. L'entreprise propose un outil d'estimation en ligne (~2 minutes), puis une visite sur place gratuite pour établir le vrai devis si la fourchette de prix correspond au budget du client.

---

## 2. Métiers en détail

### 2.1 Électricité

ARélec est avant tout un électricien — c'est le cœur de métier depuis 2010. Les prestations incluent :

- **Installation neuve** : conception du plan électrique, tirage des gaines, pose du tableau, des différentiels et des appareillages, éclairage intérieur et extérieur.
- **Rénovation** : reprise d'installation existante, mise au propre du tableau, remplacement d'appareillage.
- **Mise aux normes NF C 15-100** : diagnostic complet, remplacement de ce qui n'est plus conforme, sans casser inutilement les murs.
- **Dépannage** : disjoncteur qui claque, prise grillée, panne d'éclairage, court-circuit.
- **Éclairage** : conception architecturale (escaliers à LED intégrées, appliques chaudes, pilotage simple).

### 2.2 Chauffage / thermique

ARélec installe, remplace et entretient le chauffage des maisons individuelles :

- **Installation et remplacement** : radiateurs, distribution, eau chaude sanitaire, dimensionnement adapté à l'isolation et à la surface.
- **Confort et économies** : régulation par pièce, équilibrage du réseau, conseil sur les leviers d'économies sans changer l'appareil.
- **Entretien** : visite annuelle, contrôle complet, réglages, petits remplacements. Un chauffage entretenu consomme moins et tombe moins souvent en panne.

### 2.3 Plomberie

ARélec couvre toute la plomberie résidentielle :

- **Salle de bain complète** : dépose, réseau d'eau, douche / baignoire / WC, robinetterie, finitions, coordination carrelage.
- **Recherche et réparation de fuite** : localisation précise avant ouverture, réparation propre, remise en état.
- **Réseau d'eau et sanitaires** : refonte des canalisations en rénovation, évacuations, mises aux standards actuels.

---

## 3. Zone d'intervention détaillée

Siège à **Plouzané (29280)**, Finistère, Bretagne.

Communes couvertes (chacune a une page dédiée par métier) :

| Commune | Code postal |
|---|---|
| Brest | 29200 |
| Plouzané | 29280 |
| Saint-Renan | 29290 |
| Le Conquet | 29217 |
| Landerneau | 29800 |
| Plouider | 29260 |
| Guipavas | 29490 |
| Le Relecq-Kerhuon | 29480 |
| Guilers | 29820 |
| Plougonvelin | 29217 |
| Locmaria-Plouzané | 29280 |
| Lannilis | 29870 |
| Plabennec | 29860 |

---

## 4. Questions fréquentes

{_faq_block("Général", FAQ_HOME)}

{_faq_block("Électricité", FAQ_ELEC)}

{_faq_block("Chauffage", FAQ_CHAUF)}

{_faq_block("Plomberie", FAQ_PLOMB)}

---

## 5. Contact

- **Téléphone fixe** : 02 98 40 20 43
- **Téléphone mobile / WhatsApp** : 06 78 02 04 24
- **Email** : contact@entreprise-arelec.fr
- **Adresse** : Plouzané (29280), Finistère, France
- **Site** : {DOMAIN}
- **Formulaire de contact** : {DOMAIN}/contact/

Horaires habituels d'intervention : du lundi au vendredi, 8h00 – 18h00.

---

## 6. Identifiants légaux

- **Raison sociale** : SARL ARélec
- **SIREN** : 790 223 036
- **Statut** : SARL (Société à responsabilité limitée)
- **Année de création** : 2010
- **Gérant** : Arnaud Roncey

---

Dernière mise à jour : {TODAY}
"""
(SITE/"llms-full.txt").write_text(LLMS_FULL)

print("Pages :", len(pages))
for slug,*_ in pages: print("  /"+(slug or "(accueil)"))
