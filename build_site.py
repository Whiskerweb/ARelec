#!/usr/bin/env python3
# Generateur du site statique ARELEC — DA inspirée de voltora.framer.website (Geist, crème, accent #E3FF4A).
# HOME = scroll-snap (hero photo + metiers + avis + footer).
# SUBPAGES (metier + locales) = layout inspire de traaaction.com/portal :
#   subnav claire sticky, hero 2 colonnes, trust strip, 3 sections numerotees, recap CTA, footer.
import os, re, html, pathlib, datetime, json
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT/"site"; IMG = SITE/"assets/img"; CSS = SITE/"assets/css"
DOMAIN = "https://www.entreprise-arelec.fr"
PHONE_DISP = "02 98 40 20 43"; PHONE_TEL = "0298402043"; EMAIL = "contact@entreprise-arelec.fr"
PHONE_MOBILE_DISP="06 78 02 04 24"; PHONE_MOBILE_TEL="0678020424"; WHATSAPP_INT="33678020424"
# Note publique relevée sur avis-electricien.fr (reprise de la fiche Google) le 03/11/2026
RATING="4,6"; RATING_COUNT=9
ADDRESS="Rue du Cloître, 29280 Plouzané"
SVG_PHONE='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
SVG_MAIL='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'
SVG_WA='<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2zm.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23-1.48 0-2.93-.39-4.19-1.15l-.3-.17-3.12.82.83-3.04-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24zM8.53 7.33c-.16 0-.43.06-.66.31-.22.25-.87.86-.87 2.07 0 1.22.89 2.39 1 2.56.14.17 1.76 2.67 4.25 3.73.59.27 1.05.42 1.41.53.59.19 1.13.16 1.56.1.48-.07 1.46-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.07-.1-.23-.16-.48-.27-.25-.14-1.47-.74-1.69-.82-.23-.08-.4-.12-.56.12-.17.25-.64.81-.78.97-.15.17-.29.19-.53.07-.26-.13-1.06-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.12-.24-.01-.39.11-.5.11-.11.27-.29.37-.44.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.11-.56-1.35-.77-1.84-.2-.48-.4-.42-.56-.43-.14 0-.3-.01-.47-.01z"/></svg>'
SVG_FB='<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12.07C22 6.51 17.52 2 12 2S2 6.51 2 12.07c0 5.02 3.66 9.18 8.44 9.93v-7.02H7.9v-2.91h2.54V9.84c0-2.51 1.49-3.89 3.78-3.89 1.09 0 2.24.19 2.24.19v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.88h2.77l-.44 2.91h-2.33V22c4.78-.75 8.43-4.91 8.43-9.93z"/></svg>'
JS_DIR = SITE/"assets/js"; API = ROOT/"api"
for p in (IMG,CSS,JS_DIR,API): p.mkdir(parents=True, exist_ok=True)

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
                   (22,"reno-cablage.jpg",1100),(9,"chantier-toiture.jpg",1100)]:
    save(f"photo-{n:02d}.jpg", name, wpx)
# Logos : blanc (nav photo sombre) + sombre (subnav claire)
wl = Image.open(ROOT/"assets/logo-arelec-white.png").convert("RGBA"); wl.thumbnail((640,640), Image.LANCZOS); wl.save(IMG/"logo.png")
alpha = wl.split()[3]; dark = Image.new("RGBA", wl.size, (18,18,17,255)); dark.putalpha(alpha); dark.save(IMG/"logo-dark.png")

# ---------- CSS partage (DA inspirée de Voltora : Geist, crème #F3F2EE, encre #121211, accent #E3FF4A) ----------
CSS_TXT = r""":root{--ink:#121211;--ink2:#191917;--mist:#F3F2EE;--line:#E4E2DC;--muted:#6F6D66;--lime:#E3FF4A;--white:#fff;
--font:'Geist',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;--mono:'Geist Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
--ease:cubic-bezier(.2,.7,.2,1);--max:1248px}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:#fff;color:var(--ink);font-family:var(--font);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-x:hidden}
img{display:block;max-width:100%}
a{color:inherit}
p{margin:0}
ul{margin:0;padding:0;list-style:none}
:focus-visible{outline:2px solid var(--ink);outline-offset:3px;border-radius:8px}
.dk :focus-visible,.hero :focus-visible,.cta-card :focus-visible,.footer :focus-visible,.drawer :focus-visible{outline-color:var(--lime)}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}
.sec{padding:120px 0}
.sec.tight{padding:72px 0}
.ic{width:20px;height:20px;flex:none;display:inline-block}
.tbd{overflow-wrap:anywhere}
.stat-n .tbd,.score .tbd{white-space:nowrap}
/* les enfants de grille peuvent rétrécir sous leur contenu (évite tout débordement sur mobile) */
.story-card>*,.split-head>*,.why-body>*,.rating-card>*,.dark-card>*,.areas-card>*,.faq-grid>*,.phero-card>*,.feat-row>*,.two-col>*,.contact-grid>*,.post-feat>*,.f-top>*{min-width:0}
/* --- typo --- */
.h1{font-size:clamp(40px,5vw,68px);line-height:1.02;font-weight:300;letter-spacing:-.035em;margin:0}
.h2{font-size:clamp(32px,3.4vw,48px);line-height:1.08;font-weight:300;letter-spacing:-.03em;margin:0}
.h1 b,.h2 b{font-weight:300;color:var(--muted)}
.dk .h1 b,.dk .h2 b,.hero .h1 b,.cta-card .h2 b{color:rgba(255,255,255,.55)}
.h3{font-size:22px;line-height:1.25;font-weight:400;letter-spacing:-.015em;margin:0}
.lead{font-size:18px;line-height:1.55;color:var(--muted);letter-spacing:-.005em}
.lead a,.prose a,.feat-txt p a{color:var(--ink);text-decoration-thickness:1px;text-underline-offset:3px}
.small{font-size:15px;line-height:1.6;color:var(--muted)}
.label{display:inline-flex;align-items:center;gap:8px;padding:7px 14px 7px 12px;border-radius:100px;background:#fff;border:1px solid var(--line);font-family:var(--mono);font-size:12px;font-weight:500;line-height:1.2;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.label::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--ink);flex:none}
.label.dark{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.18);color:#fff;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.label.dark::before{background:var(--lime)}
.label.on-mist{border-color:transparent}
.mono{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:.06em;text-transform:uppercase}
.head{display:flex;flex-direction:column;align-items:flex-start;gap:20px}
.head.center{align-items:center;text-align:center;margin:0 auto;max-width:820px}
.split-head{display:grid;grid-template-columns:1.25fr 1fr;gap:40px;align-items:end}
.split-head .side{display:flex;flex-direction:column;align-items:flex-start;gap:20px;max-width:420px;justify-self:end}
/* --- boutons --- */
.btn{position:relative;display:inline-flex;align-items:center;gap:12px;min-height:48px;padding:6px 22px 6px 6px;border-radius:100px;font:500 15px/1 var(--font);letter-spacing:-.01em;text-decoration:none;white-space:nowrap;cursor:pointer;border:0;transition:transform .35s var(--ease),background .3s,box-shadow .3s}
.btn:hover{transform:translateY(-1px)}
.btn .chip{width:36px;height:36px;border-radius:100px;display:grid;place-items:center;flex:none;transition:transform .45s var(--ease)}
.btn .chip .ic{width:17px;height:17px}
.btn:hover .chip{transform:rotate(45deg)}
.btn.no-rot:hover .chip{transform:scale(1.06)}
.btn.plain{padding:12px 22px}
.btn-dark{background:var(--ink);color:#fff}.btn-dark .chip{background:var(--lime);color:var(--ink)}
.btn-glass{background:rgba(255,255,255,.14);color:#fff;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.14)}.btn-glass .chip{background:#fff;color:var(--ink)}
.btn-light{background:#fff;color:var(--ink);box-shadow:inset 0 0 0 1px var(--line)}.btn-light .chip{background:var(--ink);color:var(--lime)}
.btn-lime{background:var(--lime);color:var(--ink)}.btn-lime .chip{background:var(--ink);color:var(--lime)}
.actions{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
/* --- nav --- */
.nav{position:fixed;top:12px;left:0;right:0;z-index:50;padding:0 16px;pointer-events:none}
.nav-in{pointer-events:auto;max-width:1200px;margin:0 auto;height:64px;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:0 8px 0 18px;border-radius:20px;background:rgba(255,255,255,.9);-webkit-backdrop-filter:blur(18px) saturate(160%);backdrop-filter:blur(18px) saturate(160%);box-shadow:0 0 0 1px rgba(18,18,17,.05),0 8px 24px rgba(18,18,17,.06);transition:box-shadow .4s var(--ease),background .4s}
.nav.scrolled .nav-in{background:rgba(255,255,255,.96);box-shadow:0 0 0 1px rgba(18,18,17,.06),0 14px 40px rgba(18,18,17,.12)}
.brand{display:flex;align-items:center;min-height:44px}
.brand img{height:34px;width:auto}
.nav-links{display:flex;gap:2px}
.nav-links a{padding:10px 14px;border-radius:100px;font-size:14px;color:var(--muted);text-decoration:none;transition:color .2s,background .2s}
.nav-links a:hover{color:var(--ink);background:var(--mist)}
.nav-links a[aria-current]{color:var(--ink);font-weight:500}
.nav-right{display:flex;align-items:center;gap:8px}
.nav-tel{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 12px;font-size:14px;color:var(--ink);text-decoration:none;border-radius:100px}
.nav-tel:hover{background:var(--mist)}
.nav-tel .ic{width:16px;height:16px}
.burger{display:none;width:48px;height:48px;border-radius:100px;border:0;background:var(--mist);cursor:pointer;place-items:center;padding:0;color:var(--ink)}
.burger span,.burger span::before{display:block;width:18px;height:1.5px;background:currentColor;border-radius:2px;position:relative}
.burger span::before{content:"";position:absolute;top:6px;left:0}
.burger span{transform:translateY(-3px)}
/* --- tiroir mobile --- */
.drawer{position:fixed;inset:0;z-index:70;background:var(--ink);color:#fff;display:flex;flex-direction:column;gap:28px;padding:calc(20px + env(safe-area-inset-top)) 20px calc(24px + env(safe-area-inset-bottom));overflow-y:auto;opacity:0;transform:translateY(-12px);transition:opacity .35s var(--ease),transform .35s var(--ease)}
.drawer.open{opacity:1;transform:none}
.drawer[hidden]{display:none}
.drawer-head{display:flex;align-items:center;justify-content:space-between}
.drawer-head img{height:34px;width:auto}
.drawer-close{width:48px;height:48px;border-radius:100px;border:0;background:rgba(255,255,255,.1);color:#fff;font-size:26px;line-height:1;cursor:pointer}
.drawer nav{display:flex;flex-direction:column}
.drawer nav a{display:flex;justify-content:space-between;align-items:center;padding:16px 4px;font-size:30px;font-weight:300;letter-spacing:-.03em;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.1)}
.drawer nav a .ic{color:var(--lime)}
.drawer-foot{margin-top:auto;display:flex;flex-direction:column;gap:12px}
.drawer-foot .btn{justify-content:space-between}
.drawer-tel{display:flex;align-items:center;gap:12px;color:rgba(255,255,255,.75);text-decoration:none;font-size:15px;min-height:44px}
body.menu-open{overflow:hidden}
/* --- apparitions au scroll --- */
.js .r{opacity:0;transform:translateY(28px);filter:blur(8px);transition:opacity 1s var(--ease),transform 1s var(--ease),filter 1s var(--ease);transition-delay:var(--d,0s)}
.js .r.in{opacity:1;transform:none;filter:none}
/* --- hero accueil --- */
.hero{padding:12px 12px 0}
.hero-card{position:relative;isolation:isolate;overflow:hidden;border-radius:32px;min-height:max(720px,calc(100svh - 24px));display:flex;align-items:flex-end;padding:170px 56px 56px;color:#fff}
.hero-bg{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover;transform:scale(1.08);animation:heroZoom 2.6s var(--ease) .1s forwards}
@keyframes heroZoom{to{transform:scale(1)}}
.hero-card::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(18,18,17,.78) 0%,rgba(18,18,17,.35) 50%,rgba(18,18,17,.05) 100%),linear-gradient(0deg,rgba(18,18,17,.6) 0%,rgba(18,18,17,0) 50%)}
.hero-grid{width:100%;display:flex;align-items:flex-end;justify-content:space-between;gap:40px}
.hero-content{max-width:760px;display:flex;flex-direction:column;align-items:flex-start;gap:24px}
.hero-content .lead{color:rgba(255,255,255,.8);max-width:540px}
.trust-line{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:4px}
.trust-line span{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:rgba(255,255,255,.82)}
.trust-line .ic{width:18px;height:18px;padding:3px;border-radius:50%;background:var(--lime);color:var(--ink)}
.avail{width:300px;flex:none;padding:10px 10px 18px;border-radius:24px;background:rgba(255,255,255,.12);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.14)}
.avail img{width:100%;height:150px;object-fit:cover;border-radius:16px}
.avail .status{display:flex;align-items:center;gap:8px;margin:14px 8px 6px;font-size:15px;font-weight:500}
.pulse{width:9px;height:9px;border-radius:50%;background:var(--lime);box-shadow:0 0 0 0 rgba(227,255,74,.6);animation:pulse 2s infinite}
@keyframes pulse{70%{box-shadow:0 0 0 10px rgba(227,255,74,0)}100%{box-shadow:0 0 0 0 rgba(227,255,74,0)}}
.avail p{margin:0 8px;font-size:13px;line-height:1.5;color:rgba(255,255,255,.72)}
.avail p a{color:#fff}
/* --- bandeau logos --- */
.logos{padding:44px 0 8px}
.logos .wrap{display:flex;align-items:center;gap:48px}
.logos-intro{flex:none;width:250px;display:flex;flex-direction:column;gap:6px}
.logos-intro .small{font-size:13px;line-height:1.5}
.ticker{flex:1;min-width:0;overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.ticker-track{display:flex;gap:56px;width:max-content;animation:marquee 32s linear infinite}
.ticker-item{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:500;letter-spacing:-.02em;color:#9a978e;white-space:nowrap}
.ticker-item .ic{width:22px;height:22px}
@keyframes marquee{to{transform:translateX(-50%)}}
/* --- chiffres --- */
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:64px}
.stat{border-top:1px solid var(--line);padding-top:22px}
.stat-n{font-size:56px;line-height:1;font-weight:300;letter-spacing:-.04em}
.stat-l{font-size:13px;color:var(--muted);margin-top:14px}
/* --- pourquoi nous --- */
.why{padding:0 12px}
.why-card{position:relative;isolation:isolate;overflow:hidden;border-radius:32px;padding:80px 40px}
.why-card>img{position:absolute;inset:0;z-index:-1;width:100%;height:100%;object-fit:cover}
.why-card::after{content:"";position:absolute;inset:0;z-index:-1;background:rgba(18,18,17,.18)}
.why-inner{max-width:1120px;margin:0 auto;background:#fff;border-radius:28px;box-shadow:0 30px 60px rgba(18,18,17,.12);padding:56px 48px 48px}
.why-body{display:grid;grid-template-columns:1fr 1.15fr;gap:16px;margin-top:48px}
.why-body>img{width:100%;height:100%;min-height:420px;object-fit:cover;border-radius:20px}
.feat-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.mist-card{background:var(--mist);border-radius:20px;padding:28px;display:flex;flex-direction:column;gap:24px}
.mist-card .txt{display:flex;flex-direction:column;gap:10px;margin-top:auto}
.icon-chip{width:48px;height:48px;border-radius:100px;background:#fff;display:grid;place-items:center;color:var(--ink);flex:none}
.on-white .icon-chip{background:var(--mist)}
/* --- services --- */
.svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:56px}
.svc{position:relative;isolation:isolate;overflow:hidden;border-radius:24px;min-height:460px;display:flex;align-items:flex-end;padding:12px;color:#fff;text-decoration:none}
.svc>img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover;transition:transform 1.1s var(--ease)}
.svc:hover>img{transform:scale(1.06)}
.svc::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(18,18,17,.55),rgba(18,18,17,0) 60%)}
.svc .num{position:absolute;top:14px;left:14px;padding:8px 12px;border-radius:100px;background:rgba(255,255,255,.16);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.svc-body{width:100%;padding:20px;border-radius:18px;background:rgba(18,18,17,.32);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.1);display:flex;flex-direction:column;gap:8px}
.svc-body p{font-size:14px;line-height:1.55;color:rgba(255,255,255,.75)}
.svc-more{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:500;color:var(--lime);margin-top:4px}
.svc-more .ic{width:15px;height:15px}
/* --- réalisation à la une --- */
.story-card{background:var(--mist);border-radius:32px;padding:16px;display:grid;grid-template-columns:1fr 1fr;gap:48px}
.story-img{position:relative;min-height:560px}
.story-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:24px}
.tag{position:absolute;top:16px;left:16px;display:inline-flex;align-items:center;gap:6px;padding:8px 12px;border-radius:100px;color:#fff;background:rgba(18,18,17,.35);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.tag .ic{width:14px;height:14px}
.story-txt{padding:40px 24px 8px 0;display:flex;flex-direction:column;align-items:flex-start;gap:20px}
.quote-card{width:100%;margin-top:auto;background:#fff;border-radius:20px;padding:24px;display:flex;flex-direction:column;gap:18px}
.quote-card .q{font-size:18px;line-height:1.55;letter-spacing:-.005em}
.author{display:flex;align-items:center;gap:12px}
.avatar{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;flex:none;background:var(--ink);color:var(--lime);font:500 13px var(--mono)}
.author>div>b{display:block;font-size:15px;font-weight:500}
.author>div>span{display:block;font-size:13px;color:var(--muted)}
.quote-foot{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px}
/* --- note --- */
.rating-card{border:1px solid var(--line);border-radius:32px;padding:16px 16px 16px 56px;display:grid;grid-template-columns:1fr 440px;gap:48px;align-items:center}
.rating-panel{background:var(--ink);color:#fff;border-radius:24px;padding:36px}
.score{display:flex;align-items:baseline;gap:6px}
.score b{font-size:68px;line-height:1;font-weight:300;letter-spacing:-.035em}
.score>span{font-size:20px;color:rgba(255,255,255,.55)}
.stars{display:flex;gap:4px;color:var(--lime);margin:18px 0}
.stars .ic{width:18px;height:18px}
.stars.ink{color:var(--ink)}
.rating-panel hr{border:0;border-top:1px solid rgba(255,255,255,.12);margin:22px 0}
.rating-panel p{font-size:15px;color:rgba(255,255,255,.72)}
/* --- carte sombre (sécurité) --- */
.dark-wrap{padding:0 12px}
.dark-card{background:var(--ink2);color:#fff;border-radius:32px;padding:16px 16px 16px 56px;display:grid;grid-template-columns:1fr 1fr;gap:56px}
.dark-txt{padding:48px 0;display:flex;flex-direction:column;align-items:flex-start;gap:22px}
.dark-txt .lead{color:rgba(255,255,255,.7)}
.points{display:flex;flex-direction:column;gap:12px;width:100%}
.points li{display:flex;align-items:center;gap:14px;font-size:16px}
.points .icon-chip{width:40px;height:40px;background:rgba(255,255,255,.1);color:var(--lime)}
.points .icon-chip .ic{width:18px;height:18px}
.note{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.5;color:rgba(255,255,255,.55)}
.note .ic{width:16px;height:16px;color:var(--lime);margin-top:1px}
.dark-img{position:relative;min-height:600px}
.dark-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:24px}
.badge{position:absolute;left:16px;bottom:16px;right:16px;max-width:340px;padding:16px 18px;border-radius:18px;background:rgba(18,18,17,.45);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);font-size:14px;line-height:1.45;color:rgba(255,255,255,.88);box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.badge b{display:block;color:#fff;font-weight:500;margin-bottom:2px}
/* --- étapes --- */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:64px}
.step-top{display:flex;align-items:center;gap:12px}
.step-n{padding:8px 12px;border-radius:100px;background:var(--ink);color:#fff}
.step-line{flex:1;height:1px;background:var(--line);transform-origin:left;transform:scaleX(0);transition:transform 1.2s var(--ease) calc(var(--d,0s) + .3s)}
.r.in .step-line,.no-js .step-line{transform:scaleX(1)}
.step h3{margin:28px 0 10px}
/* --- témoignages --- */
.rate-chip{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:100px;background:var(--mist);font-size:13px}
.rate-chip .ic{width:15px;height:15px}
.testi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:56px}
.carousel{margin-top:56px}
.c-track{display:flex;gap:16px;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-behavior:smooth;scrollbar-width:none;-webkit-overflow-scrolling:touch;cursor:grab}
.c-track::-webkit-scrollbar{display:none}
.c-track.drag{scroll-snap-type:none;scroll-behavior:auto;cursor:grabbing;user-select:none}
.c-track>*{flex:0 0 calc((100% - 32px)/3);scroll-snap-align:start}
.c-foot{display:flex;align-items:center;gap:24px;margin-top:28px}
.c-bar{flex:1;height:2px;background:var(--line);border-radius:2px;overflow:hidden}
.c-fill{height:100%;background:var(--ink);transform-origin:left;transform:scaleX(.33);transition:transform .45s var(--ease)}
.c-count{min-width:52px;color:var(--muted)}
.c-nav{display:flex;gap:8px}
.c-btn{width:48px;height:48px;border-radius:100px;border:0;background:var(--mist);color:var(--ink);display:grid;place-items:center;cursor:pointer;transition:background .25s,color .25s,opacity .25s}
.c-btn:hover:not(:disabled){background:var(--ink);color:var(--lime)}
.c-btn:disabled{opacity:.35;cursor:default}
.c-btn .ic{width:18px;height:18px}
.c-btn.prev .ic{transform:scaleX(-1)}
.testi{background:var(--mist);border-radius:24px;padding:28px;display:flex;flex-direction:column;gap:22px}
.testi .stars{margin:0}
.testi .q{font-size:17px;line-height:1.55;letter-spacing:-.005em}
.testi .author{margin-top:auto}
/* --- zones --- */
.areas-card{background:var(--mist);border-radius:32px;padding:56px;display:grid;grid-template-columns:1.2fr 1fr;gap:56px;align-items:start}
.areas-txt{display:flex;flex-direction:column;align-items:flex-start;gap:22px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.area-chip{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:10px 16px 10px 12px;border-radius:100px;background:#fff;font-size:14px;text-decoration:none;transition:background .2s,color .2s}
.area-chip .ic{width:16px;height:16px}
a.area-chip:hover{background:var(--ink);color:#fff}
.coverage{display:flex;flex-direction:column;gap:12px}
.cov{background:#fff;border-radius:20px;padding:22px;display:flex;gap:16px;align-items:flex-start}
.cov .icon-chip{background:var(--mist)}
.cov b{display:block;font-size:18px;font-weight:400;letter-spacing:-.01em;margin-bottom:4px}
.cov p{font-size:14px;color:var(--muted);line-height:1.55}
/* --- FAQ --- */
.faq-grid{display:grid;grid-template-columns:400px 1fr;gap:72px;align-items:start}
.faq-intro{position:sticky;top:120px;display:flex;flex-direction:column;align-items:flex-start;gap:20px}
.faq-list{display:flex;flex-direction:column;gap:10px}
.faq-q{background:var(--mist);border-radius:18px;padding:0 24px}
.faq-q summary{list-style:none;cursor:pointer;min-height:72px;display:flex;align-items:center;justify-content:space-between;gap:16px;font-size:17px;letter-spacing:-.01em}
.faq-q summary::-webkit-details-marker{display:none}
.toggle{width:34px;height:34px;border-radius:100px;background:#fff;display:grid;place-items:center;flex:none;transition:transform .35s var(--ease),background .3s}
.toggle .ic{width:16px;height:16px}
.faq-q[open] .toggle{transform:rotate(45deg);background:var(--lime)}
.faq-a{padding:0 48px 24px 0;font-size:15px;line-height:1.65;color:var(--muted)}
.faq-q[open] .faq-a{animation:fadeUp .45s var(--ease)}
@keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
/* --- CTA image --- */
.cta{padding:0 12px}
.cta-card{position:relative;isolation:isolate;overflow:hidden;border-radius:32px;min-height:560px;display:grid;place-items:center;text-align:center;color:#fff;padding:96px 24px}
.cta-card>img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover}
.cta-card::after{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(70% 80% at 50% 50%,rgba(18,18,17,.55),rgba(18,18,17,.78))}
.cta-in{max-width:760px;display:flex;flex-direction:column;align-items:center;gap:24px}
.cta-in .mark{height:58px;width:auto;margin-bottom:8px}
.cta-in .lead{color:rgba(255,255,255,.78);max-width:560px}
/* --- footer (carte crème, logo-texte pixel) --- */
.footer{padding:120px 12px 12px}
.footer-card{background:var(--mist);color:var(--ink);border-radius:32px;padding:72px 56px 28px;overflow:hidden}
.f-top{display:grid;grid-template-columns:1.25fr 1fr 1fr 1fr;gap:40px}
.f-brand{display:flex;flex-direction:column;gap:18px;align-items:flex-start;max-width:400px}
.f-brand img{height:40px;width:auto}
.f-brand .tagline{font-size:22px;line-height:1.3;font-weight:400;letter-spacing:-.015em}
.f-contact{display:flex;flex-direction:column;gap:12px;font-size:14px;margin-top:4px}
.f-contact a,.f-contact>span{display:inline-flex;align-items:center;gap:12px;color:var(--ink);text-decoration:none}
.f-contact a:hover{text-decoration:underline;text-underline-offset:3px}
.f-ic{width:32px;height:32px;border-radius:100px;background:#fff;display:grid;place-items:center;flex:none}
.f-ic .ic{width:15px;height:15px}
.f-col h4{margin:6px 0 18px;color:var(--muted)}
.f-col li{margin:0 0 12px}
.f-col a,.f-col span{font-size:14px;color:var(--ink);text-decoration:none}
.f-col a:hover{color:var(--muted)}
.f-seo{display:grid;grid-template-columns:repeat(3,1fr);gap:24px 40px;margin-top:56px;padding-top:32px;border-top:1px solid var(--line)}
.f-seo h4{margin:0 0 10px;color:var(--muted)}
.f-seo ul{display:flex;flex-wrap:wrap;gap:4px 0}
.f-seo li{font-size:13px;color:var(--muted)}
.f-seo li:not(:last-child)::after{content:"·";margin:0 8px;color:#b9b6ad}
.f-seo a{color:var(--muted);text-decoration:none}
.f-seo a:hover{color:var(--ink)}
.f-mark{margin:64px 0 32px;font-family:'Doto',var(--mono);font-weight:900;font-size:clamp(64px,17.5vw,268px);line-height:.8;letter-spacing:.02em;color:var(--line);text-align:center;white-space:nowrap;user-select:none}
.f-legal{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;padding-top:24px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
.f-legal nav{display:flex;gap:20px}
.f-legal a{color:var(--muted);text-decoration:none}
.f-legal a:hover{color:var(--ink)}
.f-social{display:flex;gap:8px;justify-content:flex-end}
.f-social a{width:36px;height:36px;border-radius:100px;background:#fff;display:grid;place-items:center;color:var(--ink)}
.f-social a:hover{background:var(--ink);color:var(--lime)}
.f-social .ic{width:16px;height:16px}
/* --- hero des pages intérieures --- */
.phero{padding:12px 12px 0}
.phero-card{background:var(--mist);border-radius:32px;padding:150px 56px 56px;display:grid;grid-template-columns:1.05fr 1fr;gap:56px;align-items:center}
.phero-card.solo{grid-template-columns:1fr;padding-bottom:72px}
.phero-txt{display:flex;flex-direction:column;align-items:flex-start;gap:22px}
.phero-card.solo .phero-txt{max-width:820px}
.crumb{font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--muted)}
.crumb a{color:var(--muted);text-decoration:none}
.crumb a:hover{color:var(--ink)}
.phero-img{position:relative}
.phero-img img{width:100%;aspect-ratio:4/3.6;object-fit:cover;border-radius:24px}
.float{position:absolute;left:16px;bottom:16px;padding:12px 16px;border-radius:16px;background:rgba(255,255,255,.88);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);font-size:13px;font-weight:500;display:flex;align-items:center;gap:8px}
.float .stars{margin:0;color:var(--ink)}
.float .stars .ic{width:14px;height:14px}
/* --- bandeau de confiance --- */
.trust{padding:28px 0;border-bottom:1px solid var(--line)}
.trust .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px 32px}
.trust span{display:inline-flex;align-items:center;gap:10px;font-size:15px}
.trust .ic{width:20px;height:20px;padding:4px;border-radius:50%;background:var(--ink);color:var(--lime)}
/* --- sections métier (alternées) --- */
.feat-rows{display:flex;flex-direction:column;gap:16px}
.feat-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:stretch}
.feat-row.flip .feat-img{order:2}
.feat-img{position:relative;min-height:480px}
.feat-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:24px}
.feat-txt{background:var(--mist);border-radius:24px;padding:48px;display:flex;flex-direction:column;align-items:flex-start;gap:18px}
.feat-txt .kicker{display:flex;align-items:center;gap:12px;color:var(--muted)}
.feat-txt p{font-size:16px;line-height:1.65;color:var(--muted)}
.checks{display:grid;grid-template-columns:1fr 1fr;gap:12px 20px;margin-top:6px;width:100%}
.checks li{display:flex;align-items:flex-start;gap:10px;font-size:15px;line-height:1.4}
.checks .ic{width:18px;height:18px;padding:3px;border-radius:50%;background:var(--ink);color:var(--lime);margin-top:1px}
/* --- cartes génériques --- */
.cards-4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:56px}
.cards-3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:56px}
.cards-2{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:56px}
.img-card{position:relative;isolation:isolate;overflow:hidden;border-radius:24px;min-height:520px;display:flex;align-items:flex-end;padding:12px;color:#fff}
.img-card>img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover}
.img-card::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(18,18,17,.6),rgba(18,18,17,0) 55%)}
.img-card .svc-body{gap:12px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.two-col>img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:24px}
.steps-v{display:flex;flex-direction:column;gap:12px;margin-top:8px;width:100%}
.steps-v li{display:flex;gap:16px;align-items:flex-start;padding:20px;border-radius:18px;background:var(--mist)}
.steps-v .step-n{flex:none}
.steps-v b{display:block;font-size:17px;font-weight:400;margin-bottom:4px}
.steps-v p{font-size:14px;color:var(--muted);line-height:1.55}
.team-card{background:var(--mist);border-radius:24px;padding:12px 12px 24px;display:flex;flex-direction:column;gap:16px}
.ph{aspect-ratio:4/4.4;border-radius:18px;background:repeating-linear-gradient(135deg,#e9e7e1 0 12px,#e4e2dc 12px 24px);display:grid;place-items:center;color:var(--muted);text-align:center;padding:16px}
.team-card .who{padding:0 12px}
.team-card .who b{display:block;font-size:20px;font-weight:400;letter-spacing:-.015em}
.team-card .who span{font-size:14px;color:var(--muted)}
/* --- blog --- */
.post-feat{display:grid;grid-template-columns:1.2fr 1fr;gap:16px;background:var(--mist);border-radius:32px;padding:16px}
.post-feat .img{position:relative;min-height:460px}
.post-feat .img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:24px}
.post-feat .txt{padding:40px 32px;display:flex;flex-direction:column;align-items:flex-start;gap:18px;justify-content:center}
.posts{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:48px}
.post{display:flex;flex-direction:column;gap:16px}
.post .img{position:relative}
.post .img img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:20px}
.post .meta{display:flex;gap:10px;align-items:center;color:var(--muted)}
.post h3{font-size:20px}
.pill{display:inline-flex;align-items:center;padding:6px 10px;border-radius:100px;background:var(--mist);color:var(--ink)}
.pill.lime{background:var(--lime)}
/* --- contact --- */
.contact-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:16px;align-items:start}
.panel{border-radius:24px;padding:40px;display:flex;flex-direction:column;gap:20px}
.panel.mist{background:var(--mist)}
.panel.ink{background:var(--ink);color:#fff}
.method{display:flex;align-items:center;gap:16px;padding:16px;border-radius:18px;background:#fff;text-decoration:none;color:var(--ink);transition:transform .3s var(--ease);border:0;font:inherit;text-align:left;cursor:pointer;width:100%}
.method:hover{transform:translateX(4px)}
.method .icon-chip{background:var(--mist)}
.method.wa .icon-chip{background:#25D366;color:#fff}
.method.ai .icon-chip{background:var(--ink);color:var(--lime)}
.method>div>b{display:block;font-size:16px;font-weight:500}
.method>div>span{font-size:14px;color:var(--muted)}
.method .go{margin-left:auto;color:var(--muted)}
.cform{display:flex;flex-direction:column;gap:14px}
.cform .row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.cform label{display:flex;flex-direction:column;gap:8px;font-size:13px;color:rgba(255,255,255,.7)}
.cform input,.cform textarea,.cform select{font:inherit;font-size:16px;color:#fff;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:13px 14px;min-height:48px}
.cform select option{color:var(--ink)}
.cform input:focus,.cform textarea:focus,.cform select:focus{outline:none;border-color:var(--lime)}
.cform .btn{align-self:flex-start;margin-top:6px}
.cform-foot{font-size:12px;color:rgba(255,255,255,.5)}
/* --- galerie --- */
.gallery{columns:3;column-gap:16px}
.gcard{position:relative;break-inside:avoid;margin:0 0 16px;border-radius:20px;overflow:hidden}
.gcard img{width:100%;height:auto;transition:transform 1s var(--ease)}
.gcard:hover img{transform:scale(1.04)}
.gcard figcaption{position:absolute;left:10px;right:10px;bottom:10px;padding:12px 14px;border-radius:14px;color:#fff;background:rgba(18,18,17,.4);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.gcard figcaption .mono{color:var(--lime);font-size:11px}
.gcard figcaption span{display:block;font-size:14px;margin-top:3px}
/* --- texte long --- */
.prose{max-width:760px;font-size:16px;line-height:1.75;color:var(--muted)}
.prose h2{font-size:24px;font-weight:400;letter-spacing:-.02em;color:var(--ink);margin:40px 0 12px}
.prose p{margin:0 0 14px}
/* --- assistant : bulle discrète + panneau --- */
.chat-fab{position:fixed;right:calc(18px + env(safe-area-inset-right));bottom:calc(18px + env(safe-area-inset-bottom));z-index:1200;width:58px;height:58px;padding:0;border-radius:999px;display:grid;place-items:center;cursor:pointer;color:var(--lime);font:inherit;background:var(--ink);border:0;box-shadow:0 0 0 1px rgba(255,255,255,.08),0 14px 34px rgba(18,18,17,.35);transition:transform .3s var(--ease),opacity .2s}
.chat-fab:hover{transform:translateY(-2px)}
.chat-fab:focus-visible,.chat button:focus-visible,.chat a:focus-visible,.chat textarea:focus-visible{outline:2px solid var(--lime);outline-offset:2px}
.chat-fab .ic{width:24px;height:24px}
.chat-fab .live{position:absolute;top:6px;right:7px;width:11px;height:11px;border-radius:50%;background:var(--lime);border:2px solid var(--ink)}
body.chat-open .chat-fab,body.menu-open .chat-fab{opacity:0;pointer-events:none;transform:scale(.8)}
.chat{position:fixed;right:calc(18px + env(safe-area-inset-right));bottom:calc(18px + env(safe-area-inset-bottom));z-index:1201;width:min(390px,calc(100vw - 36px));height:min(600px,calc(100vh - 36px));height:min(600px,calc(100dvh - 36px));display:flex;flex-direction:column;border-radius:24px;overflow:hidden;color:var(--ink);background:#fff;box-shadow:0 0 0 1px rgba(18,18,17,.06),0 30px 70px rgba(18,18,17,.28);transform-origin:bottom right;animation:chatIn .25s var(--ease)}
.chat[hidden]{display:none}
@keyframes chatIn{from{opacity:0;transform:translateY(12px) scale(.97)}to{opacity:1;transform:none}}
.chat-head{display:flex;align-items:center;gap:10px;padding:14px 14px 14px 18px;color:#fff;background:var(--ink)}
.chat-id{flex:1;min-width:0;line-height:1.25}
.chat-id b{display:block;font-size:15px;font-weight:500}
.chat-id span{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,.6)}
.chat-id span::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--lime)}
.chat-hbtn{width:44px;height:44px;flex:none;border-radius:100px;display:grid;place-items:center;color:#fff;text-decoration:none;cursor:pointer;padding:0;font:inherit;font-size:24px;line-height:1;background:rgba(255,255,255,.1);border:0}
.chat-hbtn:hover{background:rgba(255,255,255,.18)}
.chat-hbtn .ic{width:18px;height:18px}
.chat-msgs{flex:1;overflow-y:auto;overscroll-behavior:contain;padding:16px;display:flex;flex-direction:column;gap:10px}
.chat-msg{max-width:86%;padding:10px 14px;border-radius:18px;font-size:14.5px;line-height:1.5;white-space:pre-wrap;overflow-wrap:anywhere}
.chat-msg.bot{align-self:flex-start;background:var(--mist);border-bottom-left-radius:6px}
.chat-msg.me{align-self:flex-end;color:#fff;background:var(--ink);border-bottom-right-radius:6px}
.chat-typing{align-self:flex-start;display:flex;gap:4px;padding:14px 16px;border-radius:18px;background:var(--mist)}
.chat-typing i{width:7px;height:7px;border-radius:50%;background:#a5a29a;animation:chatDot 1s infinite ease-in-out}
.chat-typing i:nth-child(2){animation-delay:.15s}.chat-typing i:nth-child(3){animation-delay:.3s}
@keyframes chatDot{0%,80%,100%{opacity:.3;transform:translateY(0)}40%{opacity:1;transform:translateY(-3px)}}
.chat-wa{align-self:stretch;display:flex;align-items:center;gap:12px;padding:12px 14px;min-height:56px;border-radius:16px;text-decoration:none;color:#fff;background:#1fa952}
.chat-wa .ic{width:24px;height:24px;flex:none}
.chat-wa b{display:block;font-size:15px;font-weight:500}
.chat-wa small{display:block;font-size:12px;opacity:.9;line-height:1.3}
.chat-sugg{display:flex;flex-wrap:wrap;gap:8px;padding:0 16px 10px}
.chat-sugg[hidden]{display:none}
.chat-sugg button{min-height:44px;padding:8px 14px;border-radius:100px;cursor:pointer;font:inherit;font-size:13.5px;color:var(--ink);background:#fff;border:1px solid var(--line)}
.chat-sugg button:hover{background:var(--mist)}
.chat-form{display:flex;align-items:flex-end;gap:8px;padding:10px 12px;border-top:1px solid var(--line)}
.chat-form textarea{flex:1;resize:none;min-height:44px;max-height:120px;padding:11px 14px;border-radius:16px;font:inherit;font-size:16px;line-height:1.35;color:var(--ink);background:var(--mist);border:1px solid transparent}
.chat-form textarea:focus{outline:none;border-color:var(--ink)}
.chat-send{width:44px;height:44px;flex:none;border-radius:100px;display:grid;place-items:center;cursor:pointer;padding:0;color:var(--lime);background:var(--ink);border:0}
.chat-send:disabled{opacity:.5;cursor:default}
.chat-send .ic{width:18px;height:18px}
.chat-note{margin:0;padding:0 14px 10px;font-size:11px;color:var(--muted);text-align:center}
.chat-note a{color:inherit}
/* --- responsive --- */
@media (max-width:1100px){
  .svc-grid,.cards-3,.testi-grid,.posts{grid-template-columns:repeat(2,1fr)}
  .c-track>*{flex-basis:calc((100% - 16px)/2)}
  .steps,.cards-4{grid-template-columns:repeat(2,1fr);row-gap:40px}
  .f-top{grid-template-columns:1fr 1fr 1fr}
  .f-brand{grid-column:1/-1}
  .rating-card{grid-template-columns:1fr 380px;padding-left:40px}
}
@media (max-width:960px){
  .nav-links,.nav-tel{display:none}
  .burger{display:grid}
  .nav-cta{padding-right:16px}
  .sec{padding:88px 0}
  .hero-card{padding:140px 28px 28px}
  .hero-grid{flex-direction:column;align-items:flex-start}
  .avail{width:100%;max-width:420px;display:flex;gap:14px;align-items:center;padding:10px}
  .avail img{width:110px;height:84px;flex:none}
  .avail .status{margin:0 0 4px}
  .avail p{margin:0}
  .split-head,.why-body,.story-card,.rating-card,.dark-card,.areas-card,.faq-grid,.phero-card,.feat-row,.two-col,.contact-grid,.post-feat{grid-template-columns:1fr}
  .split-head .side{justify-self:start}
  .faq-intro{position:static}
  .faq-grid{gap:40px}
  .story-img,.dark-img{min-height:380px}
  .story-card{gap:8px}
  .story-txt{padding:20px 8px 8px}
  .rating-card{padding:16px}
  .rating-card>div:first-child{padding:24px 16px 8px}
  .dark-card{padding:16px;gap:16px}
  .dark-txt{padding:24px 8px 8px}
  .dark-img{order:-1}
  .feat-row.flip .feat-img{order:0}
  .feat-img{min-height:340px}
  .phero-card{padding:120px 28px 28px;gap:32px}
  .logos .wrap{flex-direction:column;align-items:flex-start;gap:20px}
  .logos-intro{width:auto}
  .ticker{width:100%}
  .gallery{columns:2}
}
@media (max-width:560px){
  .wrap{padding:0 16px}
  .sec{padding:72px 0}
  .hero,.phero,.why,.dark-wrap,.cta{padding-left:8px;padding-right:8px}
  .hero{padding-top:8px}
  .nav{top:8px;padding:0 8px}
  .nav-in{height:60px;padding:0 6px 0 14px;border-radius:18px}
  .brand img{height:30px}
  .nav-cta{display:none}
  .hero-card{border-radius:24px;min-height:max(640px,calc(100svh - 16px));padding:112px 18px 18px}
  .hero-content .actions{width:100%}
  .hero .h1 br{display:none}
  .quote-foot .btn{width:100%}
  .hero-content .actions .btn{flex:1 1 auto}
  .avail img{width:84px;height:72px}
  .stats-grid{grid-template-columns:1fr 1fr;row-gap:32px;margin-top:44px}
  .stat-n{font-size:44px}
  .why-card{padding:8px;border-radius:24px}
  .why-inner{padding:32px 18px 18px;border-radius:20px}
  .why-body>img{min-height:260px}
  .feat-grid,.svc-grid,.cards-3,.cards-2,.cards-4,.testi-grid,.steps,.posts,.checks,.cform .row{grid-template-columns:1fr}
  .svc{min-height:400px}
  .c-track>*{flex-basis:86%}
  .c-foot{gap:16px}
  .story-card,.areas-card{border-radius:24px}
  .areas-card{padding:28px 18px}
  .feat-txt{padding:28px 20px}
  .phero-card{border-radius:24px;padding:104px 18px 18px}
  .cta-card{border-radius:24px;min-height:480px;padding:72px 18px}
  .footer{padding:72px 8px 8px}
  .footer-card{border-radius:24px;padding:48px 20px 24px}
  .f-mark{margin:48px 0 24px}
  .f-top{grid-template-columns:1fr 1fr}
  .f-seo{grid-template-columns:1fr}
  .f-legal{grid-template-columns:1fr;justify-items:start}
  .f-social{justify-content:flex-start}
  .panel{padding:24px 18px}
  .gallery{columns:1}
  .chat-fab{width:52px;height:52px;right:calc(14px + env(safe-area-inset-right));bottom:calc(14px + env(safe-area-inset-bottom))}
  .chat-fab .ic{width:22px;height:22px}
  .chat{left:8px;right:8px;width:auto;bottom:calc(8px + env(safe-area-inset-bottom));height:min(640px,calc(100vh - 70px));height:min(640px,calc(100dvh - 70px));border-radius:22px}
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .js .r{opacity:1;transform:none;filter:none;transition:none}
  .hero-bg{animation:none;transform:none}
  .ticker-track,.pulse,.chat,.chat-typing i{animation:none}
  .c-track{scroll-behavior:auto}
  .step-line{transform:none;transition:none}
  .btn,.svc>img,.gcard img,.method{transition:none}
}
"""
(CSS/"styles.css").write_text(CSS_TXT)

# ---------- icônes ----------
_IC = {
 "arrow":'<path d="M7 17 17 7M8 7h9v9"/>',
 "right":'<path d="M5 12h14M13 6l6 6-6 6"/>',
 "check":'<path d="M20 6 9 17l-5-5"/>',
 "plus":'<path d="M12 5v14M5 12h14"/>',
 "pin":'<path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "bolt":'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "flame":'<path d="M12 22c4 0 7-3 7-7 0-5-4-7-5-12-2 3-3 5-3 7-1-1-2-2-2-4-2 2-4 5-4 9 0 4 3 7 7 7z"/>',
 "drop":'<path d="M12 2.7s-6 6.3-6 11.3a6 6 0 0 0 12 0c0-5-6-11.3-6-11.3z"/>',
 "shield":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "user":'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
 "users":'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.5 3-5.5 6.5-5.5s6.5 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18.5 14.8c2 .7 3 2.4 3 5.2"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "cal":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "home":'<path d="M3 11 12 4l9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 "alert":'<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/>',
 "spark":'<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
 "broom":'<path d="M14 4 8.5 13.5M5 14h8l1 7H4z"/><path d="M8 17v4M11 17v4"/>',
 "chat":'<path d="M21 11.5a8.4 8.4 0 0 1-9 8.5 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7A8.4 8.4 0 0 1 12 3a8.5 8.5 0 0 1 9 8.5z"/>',
 "doc":'<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
 "eye":'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "tool":'<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
 "logo":'<rect x="3" y="3" width="18" height="18" rx="5"/><path d="M8 15l4-8 4 8M9.5 12.5h5"/>',
}
def ic(name, extra=""):
    fill = ' fill="currentColor" stroke="none"' if name == "star" else ' fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
    path = '<path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/>' if name == "star" else _IC[name]
    return f'<svg class="ic{(" "+extra) if extra else ""}" viewBox="0 0 24 24"{fill} aria-hidden="true">{path}</svg>'
STARS = '<div class="stars" aria-label="5 étoiles sur 5">' + ic("star")*5 + '</div>'
def tbd(s):
    # Information inconnue : laissée visible, entre astérisques, à compléter avec ARélec
    return f'<span class="tbd" title="Information à compléter">*{s}*</span>'
def label(t, cls=""): return f'<span class="label{(" "+cls) if cls else ""}">{t}</span>'
def btn(t, href, kind="dark", icon="arrow", attrs=""):
    return f'<a class="btn btn-{kind}" href="{href}"{attrs}><span class="chip">{ic(icon)}</span>{t}</a>'
def btn_contact(kind="dark", t="Prendre contact"): return btn(t, "/contact", kind, "arrow", " data-chat")
def btn_call(kind="light"): return btn(PHONE_DISP, f"tel:{PHONE_TEL}", kind, "bolt", ' aria-label="Appeler le '+PHONE_DISP+'"').replace('class="btn ', 'class="btn no-rot ')
def R(d=0, cls=""):
    # élément révélé au scroll (fondu + flou), d = délai en secondes
    return f' class="r{(" "+cls) if cls else ""}"' + (f' style="--d:{d}s"' if d else "")

YEARS = datetime.date.today().year - 2010

# ---------- navigation ----------
NAV_LINKS=[("/","Accueil"),("/services","Services"),("/entreprise","À propos"),
           ("/realisations","Réalisations"),("/blog","Blog"),("/contact","Contact")]
def nav(active):
    links="".join(f'<a href="{u}"{" aria-current=\"page\"" if u==active else ""}>{t}</a>' for u,t in NAV_LINKS)
    return ('<header class="nav"><div class="nav-in">'
            '<a class="brand" href="/" aria-label="ARélec, accueil"><img src="/assets/img/logo-dark.png" alt="ARélec" width="120" height="34"></a>'
            f'<nav class="nav-links" aria-label="Navigation principale">{links}</nav>'
            '<div class="nav-right">'
            f'<a class="nav-tel" href="tel:{PHONE_TEL}">{ic("bolt")}{PHONE_DISP}</a>'
            + btn("Prendre contact","/contact","dark","arrow"," data-chat").replace('class="btn ','class="btn nav-cta ') +
            '<button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Ouvrir le menu"><span></span></button>'
            '</div></div></header>')

def mobile_drawer():
    links="".join(f'<a href="{u}">{t}{ic("arrow")}</a>' for u,t in NAV_LINKS)
    return ('<div class="drawer" id="drawer" hidden role="dialog" aria-label="Menu">'
            '<div class="drawer-head"><img src="/assets/img/logo.png" alt="ARélec" width="120" height="34">'
            '<button class="drawer-close" type="button" aria-label="Fermer le menu">×</button></div>'
            f'<nav aria-label="Menu mobile">{links}</nav>'
            '<div class="drawer-foot">'
            + btn("Prendre contact","/contact","lime","arrow"," data-chat") +
            f'<a class="drawer-tel" href="tel:{PHONE_TEL}">{ic("bolt")} {PHONE_DISP} · Lun–Ven 8h–18h</a>'
            f'<a class="drawer-tel" href="https://wa.me/{WHATSAPP_INT}" target="_blank" rel="noopener">{SVG_WA} WhatsApp · {PHONE_MOBILE_DISP}</a>'
            '</div></div>')

# ---------- sections de l'accueil ----------
def hero_home():
    return ('<section class="hero"><div class="hero-card">'
            '<img class="hero-bg" src="/assets/img/hero.jpg" alt="Maison rénovée à l\'heure bleue, chantier ARélec" fetchpriority="high">'
            '<div class="hero-grid"><div class="hero-content">'
            f'<span{R(.05)}>{label("Électricité · Chauffage · Plomberie — depuis 2010","dark")}</span>'
            f'<h1{R(.12,"h1")}>Une maison bien câblée,<br>bien chauffée.</h1>'
            f'<p{R(.2,"lead")}>À Plouzané et dans tout le bassin brestois, on s\'occupe de l\'électricité, du chauffage et de la plomberie, en neuf comme en rénovation. Un seul artisan, du devis à la mise en route.</p>'
            f'<div{R(.28,"actions")}>{btn_contact("dark")}{btn("Nos services","/services","glass","right")}</div>'
            f'<div{R(.36,"trust-line")}><span>{ic("check")}Artisan depuis 2010</span><span>{ic("check")}Devis gratuit, sur place</span><span>{ic("check")}Un seul interlocuteur</span></div>'
            '</div>'
            f'<aside{R(.45,"avail")}><img src="/assets/img/escalier-led.jpg" alt="Escalier à LED intégrées, réalisation ARélec" loading="lazy">'
            '<div><div class="status"><span class="pulse" aria-hidden="true"></span>On vous répond</div>'
            f'<p>Dépannage, rénovation, salle de bain. Appelez le <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a> ou écrivez-nous.</p></div></aside>'
            '</div></div></section>')

def logos_band():
    items="".join(f'<span class="ticker-item">{ic("logo")}{tbd("Partenaire "+str(i))}</span>' for i in range(1,7))
    return ('<section class="logos"><div class="wrap">'
            f'<div{R(0,"logos-intro")}><span class="mono">Ils nous font confiance</span>'
            '<span class="small">Fournisseurs, partenaires et clients pros du bassin brestois.</span></div>'
            f'<div class="ticker" aria-label="Logos partenaires (à compléter)"><div class="ticker-track">{items}{items}</div></div>'
            '</div></section>')

def stats_section(title='Un savoir-faire qui se voit.<br><b>Un travail qui dure.</b>',
                  side="Chaque chantier est mené avec soin, des explications claires et le souci de laisser une installation sûre et propre."):
    stats=[(tbd("1 200+"),"Chantiers réalisés",None),
           (f"{YEARS} ans","D'expérience, depuis 2010",(YEARS," ans")),
           ("3","Métiers, une seule équipe",(3,"")),
           (str(len(ALL_COMMUNES)),"Communes du bassin brestois",(len(ALL_COMMUNES),""))]
    cells=""
    for i,(n,l,c) in enumerate(stats):
        cnt=f' data-count="{c[0]}" data-suffix="{c[1]}"' if c else ""
        cells+=f'<div{R(.08*i,"stat")}><div class="stat-n"{cnt}>{n}</div><div class="stat-l">{l}</div></div>'
    return ('<section class="sec"><div class="wrap">'
            f'<div class="split-head"><div class="head"><span{R()}>{label("Notre parcours")}</span><h2{R(.08,"h2")}>{title}</h2></div>'
            f'<div class="side"><p{R(.16,"lead")}>{side}</p></div></div>'
            f'<div class="stats-grid">{cells}</div></div></section>')

WHY=[("users","Un seul interlocuteur","Élec, chauffage et plomberie par la même équipe : pas de coordination à gérer entre artisans."),
     ("doc","Un devis clair, gratuit","On se déplace, on regarde, on explique. Le devis détaillé arrive avant le moindre travaux."),
     ("broom","Un chantier propre","On protège, on range en partant. Pas de tranchée ouverte le week-end."),
     ("shield","Des conseils honnêtes","On dit ce qui est utile chez vous, et ce qui ne l'est pas. Même si ça réduit le devis.")]
def why_section():
    cards="".join(f'<div{R(.08*i,"mist-card")}><span class="icon-chip">{ic(icn)}</span><div class="txt"><h3 class="h3">{t}</h3><p class="small">{p}</p></div></div>'
                  for i,(icn,t,p) in enumerate(WHY))
    return ('<section class="why"><div class="why-card"><img src="/assets/img/sdb-marbre.jpg" alt="" loading="lazy">'
            '<div class="why-inner">'
            f'<div class="head center"><span{R()}>{label("La différence ARélec")}</span>'
            f'<h2{R(.08,"h2")}>Un travail d\'artisan,<br><b>sans mauvaise surprise.</b></h2>'
            f'<p{R(.16,"lead")}>Des travaux qui se passent simplement, du premier appel à la mise en route : on explique les options, on respecte votre maison, on s\'engage sur un résultat durable.</p></div>'
            f'<div class="why-body"><img{R(.1)} src="/assets/img/chantier-plouider.jpg" alt="Chantier de rénovation ARélec à Plouider" loading="lazy"><div class="feat-grid">{cards}</div></div>'
            '</div></div></section>')

SERVICES6=[("/electricite","cablage.jpg","Installation &amp; rénovation électrique","Du plan électrique au dernier interrupteur, en neuf comme en rénovation complète."),
           ("/electricite","reno-cablage.jpg","Mise aux normes NF C 15-100","Diagnostic, remplacement du tableau, protection des personnes — pièce par pièce."),
           ("/electricite","escalier-led.jpg","Dépannage &amp; éclairage","Disjoncteur qui saute, prise grillée, éclairage soigné : on intervient vite."),
           ("/chauffage","confort.jpg","Chauffage &amp; eau chaude","Installation, remplacement, réglages et entretien pour un confort juste."),
           ("/plomberie","sdb-baignoire.jpg","Salle de bain clé en main","Dépose, réseau d'eau, sanitaires, douche et finitions, coordonnés de A à Z."),
           ("/plomberie","douche-marbre.jpg","Fuites &amp; réseau d'eau","On localise précisément avant d'ouvrir, on répare et on remet en état.")]
def svc_cards():
    return "".join(
        f'<a{R(.06*(i%3),"svc")} href="{u}"><img src="/assets/img/{img}" alt="" loading="lazy">'
        f'<span class="num mono">{i+1:02d}</span>'
        f'<span class="svc-body"><h3 class="h3">{t}</h3><p>{p}</p><span class="svc-more">En savoir plus {ic("arrow")}</span></span></a>'
        for i,(u,img,t,p) in enumerate(SERVICES6))
def services_section():
    return ('<section class="sec"><div class="wrap">'
            f'<div class="split-head"><div class="head"><span{R()}>{label("Ce qu\'on fait")}</span>'
            f'<h2{R(.08,"h2")}>Des solutions pour<br><b>toute la maison.</b></h2></div>'
            f'<div class="side"><p{R(.12,"lead")}>De la prise qui claque à la salle de bain complète : électricité, chauffage et plomberie, en neuf comme en rénovation.</p>'
            f'<span{R(.18)}>{btn("Tous nos services","/services","light","arrow")}</span></div></div>'
            f'<div class="svc-grid">{svc_cards()}</div></div></section>')

def story_section():
    q,w,c=REVS[1]
    init="".join(x[0] for x in w.split()[:2]).upper()
    return ('<section class="sec" style="padding-top:0"><div class="wrap"><div class="story-card">'
            f'<div{R(0,"story-img")}><img src="/assets/img/maison-bleue.jpg" alt="Extension bois et pierre à Plouider, à l\'heure bleue" loading="lazy">'
            f'<span class="tag mono">{ic("pin")}Plouider · 29</span></div>'
            '<div class="story-txt">'
            f'<span{R(.05)}>{label("Une réalisation ARélec","on-mist")}</span>'
            f'<h2{R(.1,"h2")}>Extension bois &amp; pierre,<br><b>à l\'heure bleue.</b></h2>'
            f'<p{R(.15,"lead")}>Une extension contemporaine à Plouider, bardage bois et pierre, avec un éclairage extérieur chaleureux. {tbd("Détail du chantier à compléter : travaux réalisés par ARélec, durée, contraintes")}</p>'
            f'<div{R(.2,"quote-card")}><span aria-hidden="true">{ic("chat")}</span><p class="q">« {q} »</p>'
            f'<div class="quote-foot"><div class="author"><span class="avatar">{init}</span><div><b>{w}</b><span>Avis Google · {c}</span></div></div>'
            f'{btn("Parler de votre projet","/contact","dark","arrow"," data-chat")}</div></div>'
            '</div></div></div></section>')

def rating_section():
    return ('<section class="sec" style="padding-top:0"><div class="wrap"><div class="rating-card">'
            f'<div class="head"><span{R()}>{label("Avis &amp; notes")}</span>'
            f'<h2{R(.08,"h2")}>Du bon travail.<br><b>Des retours honnêtes.</b></h2>'
            f'<p{R(.14,"lead")}>La confiance se gagne chantier après chantier : qualité du travail, chantier propre, réactivité et bons conseils reviennent dans nos avis.</p>'
            f'<span{R(.2)}>{btn("Lire les avis","/avis","light","arrow")}</span></div>'
            f'<div{R(.1,"rating-panel")}><div class="score"><b>{RATING}</b><span>/5</span></div>{STARS}'
            f'<p>Note moyenne sur Google</p><hr><p>Basé sur {RATING_COUNT} avis clients Google</p></div>'
            '</div></div></section>')

def safety_section():
    pts=[("eye","Repérer les signaux d'alerte"),("tool","Faire entretenir ses installations"),("shield","Confier les travaux à un professionnel")]
    li="".join(f'<li><span class="icon-chip">{ic(i)}</span>{t}</li>' for i,t in pts)
    return ('<section class="dark-wrap dk"><div class="dark-card">'
            '<div class="dark-txt">'
            f'<span{R()}>{label("La sécurité d\'abord","dark")}</span>'
            f'<h2{R(.08,"h2")}>Les petits signes<br><b>méritent qu\'on s\'y arrête.</b></h2>'
            f'<p{R(.14,"lead")}>Un disjoncteur qui saute souvent, une prise qui chauffe, une odeur de brûlé, une tache d\'humidité qui s\'étend, un radiateur qui reste froid : ce sont des signaux à ne pas laisser traîner. Coupez l\'appareil concerné et faites vérifier.</p>'
            f'<ul{R(.2,"points")}>{li}</ul>'
            f'<span{R(.26)}>{btn("Faire vérifier mon installation","/contact","lime","arrow"," data-chat")}</span>'
            f'<p{R(.3,"note")}>{ic("alert")}<span>Odeur de gaz, fumée, étincelles ou danger immédiat ? Éloignez-vous, coupez si possible le gaz ou le courant et appelez les secours (18 ou 112).</span></p>'
            '</div>'
            f'<div{R(.1,"dark-img")}><img src="/assets/img/reno-cablage.jpg" alt="Câblage électrique en cours de rénovation" loading="lazy">'
            f'<div class="badge"><b>Dépannage</b>Disjoncteur, prise, fuite, panne d\'éclairage : on intervient dans le bassin brestois.</div></div>'
            '</div></section>')

PROCESS=[("Parlez-nous du projet","Par l'assistant du site, sur WhatsApp ou au téléphone : le besoin, la commune, vos disponibilités."),
         ("Visite gratuite sur place","On vient voir, on écoute et on vous explique les options possibles chez vous."),
         ("Devis détaillé","Un devis écrit, clair et sans engagement. Les travaux démarrent seulement après votre accord."),
         ("Réalisation &amp; mise en route","La même équipe, de la dépose à la mise en route. On vous explique tout avant de partir.")]
def process_section(h2='Un déroulé clair,<br><b>de l\'appel à la mise en route.</b>'):
    steps="".join(f'<div{R(.1*i,"step")}><div class="step-top"><span class="step-n mono">{i+1:02d}</span><span class="step-line"></span></div>'
                  f'<h3 class="h3">{t}</h3><p class="small">{p}</p></div>' for i,(t,p) in enumerate(PROCESS))
    return ('<section class="sec"><div class="wrap">'
            f'<div class="head center"><span{R()}>{label("Comment ça se passe")}</span><h2{R(.08,"h2")}>{h2}</h2></div>'
            f'<div class="steps">{steps}</div></div></section>')

def testi_cards(revs):
    out=""
    for i,(q,w,c) in enumerate(revs):
        init="".join(x[0] for x in w.split()[:2]).upper()
        out+=(f'<article class="testi"><div class="stars ink" aria-label="5 étoiles sur 5">{ic("star")*5}</div>'
              f'<p class="q">« {q} »</p><div class="author"><span class="avatar">{init}</span><div><b>{w}</b><span>Avis Google · {c}</span></div></div></article>')
    return out
def testimonials_section(revs=None):
    return ('<section class="sec" style="padding-top:0"><div class="wrap">'
            f'<div class="split-head"><div class="head"><span{R()}>{label("Ils nous recommandent")}</span>'
            f'<h2{R(.08,"h2")}>Un service<br><b>qui fait la différence.</b></h2></div>'
            f'<div class="side"><span{R(.12,"rate-chip")}>{ic("star")} {RATING}/5 · {RATING_COUNT} avis Google</span></div></div>'
            + carousel(testi_cards(revs or REVS), "Avis clients") + '</div></section>')
def carousel(items_html, name):
    # Carrousel : défilement aimanté natif (doigt, trackpad, souris) + flèches, barre de progression, défilement auto (site.js)
    return (f'<div class="carousel" role="region" aria-roledescription="carrousel" aria-label="{name}">'
            f'<div class="c-track" tabindex="0">{items_html}</div>'
            '<div class="c-foot"><div class="c-bar" aria-hidden="true"><div class="c-fill"></div></div>'
            '<span class="c-count mono" aria-live="polite"></span>'
            f'<div class="c-nav"><button class="c-btn prev" type="button" aria-label="Avis précédent">{ic("right")}</button>'
            f'<button class="c-btn next" type="button" aria-label="Avis suivant">{ic("right")}</button></div></div></div>')

def areas_block(metier_slug="electricien", h2='Un artisan du coin,<br><b>près de chez vous.</b>', lab="Zone d'intervention"):
    chips="".join(f'<a class="area-chip" href="/{metier_slug}-{s}">{ic("pin")}{l}</a>' for s,l in ALL_COMMUNES)
    cov=[("pin",f"{len(ALL_COMMUNES)} communes","Plouzané, Brest et tout le bassin brestois, dans un rayon d'environ 30 km."),
         ("cal","Visite gratuite sur place","Un rendez-vous pour voir le chantier et établir un devis juste."),
         ("home","Neuf &amp; rénovation","Maisons, appartements, extensions : de la construction à la rénovation complète.")]
    covh="".join(f'<div{R(.08*i,"cov")}><span class="icon-chip">{ic(a)}</span><div><b>{b}</b><p>{c}</p></div></div>' for i,(a,b,c) in enumerate(cov))
    return ('<section class="sec" style="padding-top:0"><div class="wrap"><div class="areas-card">'
            '<div class="areas-txt">'
            f'<span{R()}>{label(lab,"on-mist")}</span><h2{R(.08,"h2")}>{h2}</h2>'
            f'<p{R(.14,"lead")}>Installés à Plouzané depuis 2010, on intervient dans tout le bassin brestois. Dites-nous votre commune et le type de travaux : on vous confirme vite.</p>'
            f'<div{R(.2,"chips")}>{chips}</div>'
            f'<span{R(.26)}>{btn_contact("dark","Vérifier ma commune")}</span></div>'
            f'<div class="coverage">{covh}</div></div></div></section>')

def faq_section(qa_pairs, h2="Questions fréquentes"):
    if not qa_pairs: return ""
    items="".join(
        f'<details class="faq-q"><summary><span>{html.escape(q)}</span><span class="toggle">{ic("plus")}</span></summary>'
        f'<div class="faq-a">{html.escape(a)}</div></details>' for q,a in qa_pairs)
    return ('<section class="sec"><div class="wrap"><div class="faq-grid">'
            f'<div class="faq-intro"><span{R()}>{label("FAQ")}</span><h2{R(.08,"h2")}>{html.escape(h2)}</h2>'
            f'<p{R(.14,"lead")}>Vous ne trouvez pas votre réponse ? Parlez-nous de votre projet, on vous aide pour la suite.</p>'
            f'<span{R(.2)}>{btn_contact("light","Poser ma question")}</span></div>'
            f'<div{R(.1,"faq-list")}>{items}</div></div></div></section>')

def cta_section(h2='Votre projet mérite<br><b>un artisan sérieux.</b>', p="Une rénovation, une panne, une salle de bain ? Dites-nous ce dont vous avez besoin : on vous répond et on prépare la visite gratuite.", img="hero.jpg"):
    return ('<section class="cta"><div class="cta-card">'
            f'<img src="/assets/img/{img}" alt="" loading="lazy">'
            '<div class="cta-in">'
            f'<img{R(0,"mark")} src="/assets/img/logo.png" alt="ARélec" width="160" height="58">'
            f'<h2{R(.08,"h2")}>{h2}</h2><p{R(.14,"lead")}>{p}</p>'
            f'<div{R(.2,"actions")} style="justify-content:center">{btn_contact("lime")}{btn("Appeler le "+PHONE_DISP,"tel:"+PHONE_TEL,"glass","bolt")}</div>'
            '</div></div></section>')
recap = lambda h2, p=None: cta_section(h2, p) if p else cta_section(h2)

# ---------- pages intérieures ----------
def phero(crumb_html, lab, h1, lead, img=None, float_html=None, hero_alt=None, actions=None):
    acts = actions if actions is not None else btn_contact("dark") + btn_call("light")
    txt=(f'<div class="phero-txt"><div{R(0,"crumb")}>{crumb_html}</div>'
         f'<span{R(.04)}>{label(lab,"on-mist")}</span>'
         f'<h1{R(.1,"h1")}>{h1}</h1><p{R(.16,"lead")}>{lead}</p>'
         + (f'<div{R(.22,"actions")}>{acts}</div>' if acts else "") + '</div>')
    if not img:
        return f'<section class="phero"><div class="phero-card solo">{txt}</div></section>'
    fl=f'<div class="float">{float_html}</div>' if float_html else ""
    return (f'<section class="phero"><div class="phero-card">{txt}'
            f'<div{R(.12,"phero-img")}><img src="/assets/img/{img}" alt="{html.escape(hero_alt or "Chantier ARélec dans le bassin brestois")}" fetchpriority="high">{fl}</div>'
            '</div></section>')
FLOAT_AVIS = f'<div class="stars">{ic("star")*5}</div> Avis Google'

def trust_strip():
    items=[("Artisan depuis 2010"),("Bassin brestois"),("Devis gratuit, sur place"),("Un seul interlocuteur")]
    return '<section class="trust"><div class="wrap">'+"".join(f'<span>{ic("check")}{t}</span>' for t in items)+'</div></section>'

def feat_section(num, eyebrow, h2, p, items, img, tag, flip=False):
    li="".join(f"<li>{ic('check')}<span>{x}</span></li>" for x in items)
    tg=f'<span class="tag mono">{tag}</span>' if tag else ""
    return (f'<div class="feat-row{" flip" if flip else ""}">'
            f'<div{R(0,"feat-img")}><img src="/assets/img/{img}" alt="{html.escape(re.sub("<[^>]+>","",eyebrow).replace("&amp;","&"))}" loading="lazy">{tg}</div>'
            f'<div{R(.08,"feat-txt")}><div class="kicker"><span class="step-n mono">{num}</span><span class="mono">{eyebrow}</span></div>'
            f'<h2 class="h2">{h2}</h2><p>{p}</p><ul class="checks">{li}</ul></div></div>')

# ---------- footer ----------
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
def _seo_list(metier_slug): return "".join(f'<li><a href="/{metier_slug}-{c}">{l}</a></li>' for c,l in ALL_COMMUNES)
FOOTER=('<footer class="footer"><div class="footer-card">'
 '<div class="f-top"><div class="f-brand">'
 '<a href="/" aria-label="ARélec, accueil"><img src="/assets/img/logo-dark.png" alt="ARélec" width="140" height="40"></a>'
 '<p class="tagline">Une maison bien câblée, bien chauffée.</p>'
 '<p class="small">Électricité, chauffage et plomberie pour les maisons du bassin brestois. Un seul interlocuteur, depuis 2010.</p>'
 '<div class="f-contact">'
 f'<a href="tel:{PHONE_TEL}"><span class="f-ic">{ic("bolt")}</span>{PHONE_DISP}</a>'
 f'<a href="https://wa.me/{WHATSAPP_INT}" target="_blank" rel="noopener"><span class="f-ic">{SVG_WA}</span>WhatsApp · {PHONE_MOBILE_DISP}</a>'
 f'<a href="mailto:{EMAIL}"><span class="f-ic">{SVG_MAIL}</span>{EMAIL}</a>'
 f'<span><span class="f-ic">{ic("pin")}</span>{ADDRESS}</span>'
 '</div></div>'
 '<div class="f-col"><h4 class="mono">Navigation</h4><ul>'+"".join(f'<li><a href="{u}">{t}</a></li>' for u,t in NAV_LINKS)+'</ul></div>'
 '<div class="f-col"><h4 class="mono">Services</h4><ul><li><a href="/electricite">Électricité</a></li><li><a href="/chauffage">Chauffage</a></li><li><a href="/plomberie">Plomberie</a></li><li><a href="/realisations">Réalisations</a></li><li><a href="/avis">Avis clients</a></li></ul></div>'
 '<div class="f-col"><h4 class="mono">Horaires</h4><ul><li><span>Lun–Ven : 8h–18h</span></li><li><span>Sam : '+tbd("à compléter")+'</span></li><li><span>Dim : fermé '+tbd("à confirmer")+'</span></li></ul></div>'
 '</div>'
 '<div class="f-seo">'
 f'<div><h4 class="mono">Électricien à…</h4><ul>{_seo_list("electricien")}</ul></div>'
 f'<div><h4 class="mono">Plombier à…</h4><ul>{_seo_list("plombier")}</ul></div>'
 f'<div><h4 class="mono">Chauffagiste à…</h4><ul>{_seo_list("chauffagiste")}</ul></div>'
 '</div>'
 '<div class="f-mark" aria-hidden="true">ARÉLEC</div>'
 '<div class="f-legal"><span>© '+str(datetime.date.today().year)+' SARL ARélec — SIREN 790 223 036</span>'
 '<nav aria-label="Liens légaux"><a href="/mentions-legales">Mentions légales</a><a href="/politique-confidentialite">Confidentialité</a></nav>'
 '<div class="f-social">'
 '<a href="https://www.facebook.com/people/AR%C3%A9lec/100089481862657/" target="_blank" rel="noopener" aria-label="Facebook">'+SVG_FB+'</a>'
 f'<a href="https://wa.me/{WHATSAPP_INT}" target="_blank" rel="noopener" aria-label="WhatsApp">{SVG_WA}</a>'
 f'<a href="mailto:{EMAIL}" aria-label="Email">{SVG_MAIL}</a>'
 '</div></div>'
 '</div></footer>')

SITE_JS = r'''(function(){
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
'''

# ---------- assistant (bulle + panneau) ----------
SVG_CHAT='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
SVG_SEND='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
def chat_widget():
    # Bulle discrète en bas à droite + panneau de l'assistant (logique : /assets/js/chat.js, API : /api/chat)
    sugg="".join(f'<button type="button">{t}</button>' for t in
                 ("Rénover mon électricité","Changer mon chauffage","Une fuite, une panne","Vous venez chez moi ?"))
    return (f'<button class="chat-fab" type="button" aria-label="Poser une question à ARélec" aria-controls="chat" aria-expanded="false"><span class="live" aria-hidden="true"></span>{SVG_CHAT}</button>'
            f'<section class="chat" id="chat" hidden role="dialog" aria-label="Assistant ARélec" data-wa="{WHATSAPP_INT}">'
            '<div class="chat-head"><div class="chat-id"><b>ARélec</b><span>On vous répond tout de suite</span></div>'
            f'<a class="chat-hbtn" href="tel:{PHONE_TEL}" aria-label="Appeler le {PHONE_DISP}">{SVG_PHONE}</a>'
            '<button class="chat-hbtn chat-close" type="button" aria-label="Fermer">×</button></div>'
            '<div class="chat-msgs" aria-live="polite"></div>'
            f'<div class="chat-sugg">{sugg}</div>'
            '<form class="chat-form"><textarea rows="1" maxlength="800" placeholder="Votre question, votre projet…" aria-label="Votre message"></textarea>'
            f'<button class="chat-send" type="submit" aria-label="Envoyer">{SVG_SEND}</button></form>'
            '<p class="chat-note">Assistant automatique · <a href="/politique-confidentialite">confidentialité</a></p></section>'
            f'<template id="chat-wa-ic">{SVG_WA}</template>'
            '<script src="/assets/js/chat.js?v=1" defer></script>')

# ---------- avis Google réels ----------
REVS=[("Redistribution des prises et des points lumineux dans le cadre du réagencement de notre rez-de-chaussée (maison années 30). Intervention de très bonne qualité, chantier propre et rapide. Je recommande ARÉLEC.","Philippe C.","Rénovation électrique"),
 ("Super entreprise, travail de qualité et toujours dans la bonne humeur. De bons conseils et toujours à l'écoute. Un grand merci pour la rénovation de notre maison&nbsp;!","Mélanie Hautecoeur","Rénovation complète"),
 ("Très pro, Arnaud et son collègue font du bon travail, propre, de plus ils sont sympas.","Yvon Riou","Installation électrique"),
 ("Super dépannage… rapide, efficace, au top — avec de l'humour en prime&nbsp;;)","Carole Yven","Dépannage"),
 ("Sympa et efficace, je recommande sans problème.","Ronan Madec","Client ARÉLEC"),
 ("J'ai fait refaire ma salle de bain et l'électricité avec eux. Je conseille.","JL le grand","Salle de bain + élec")]

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

def head_common(path,title,desc,jl,noindex=False):
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
           '<meta name="theme-color" content="#121211">')
    robots='<meta name="robots" content="noindex, follow">' if noindex else ""
    fonts=('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Doto:wght@900&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@500&display=swap">')
    return ('<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{t_esc}</title><meta name="description" content="{d_esc}">{robots}'
            f'<link rel="canonical" href="{canon}">{og}{icons}{jl}{fonts}'
            '<link rel="stylesheet" href="/assets/css/styles.css?v=54">'
            '<script>document.documentElement.classList.add("js")</script></head>')

NOINDEX = {"blog"}  # pages encore en maquette (contenu à rédiger)
def shell(path,title,desc,body,jl,active):
    return (head_common(path,title,desc,jl,noindex=path in NOINDEX)
            + f'<body>{nav(active)}{mobile_drawer()}{chat_widget()}<main id="main">{body}</main>{FOOTER}'
            + '<script src="/assets/js/site.js?v=2" defer></script></body></html>')

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
     "Non. Le devis est gratuit : on échange d'abord sur votre projet (assistant du site, WhatsApp ou téléphone), puis ARélec se déplace gratuitement pour établir le vrai devis sur place."),
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
pages=[]  # (slug, title, desc, body, jsonld, nav actif)

# HOME
home_body=(hero_home()+logos_band()+stats_section()+why_section()+services_section()+story_section()
 +rating_section()+safety_section()+process_section()+testimonials_section()+areas_block()
 +faq_section(FAQ_HOME, h2="Vos questions, nos réponses.")+cta_section())
pages.append(("","ARélec — Électricien, chauffagiste & plombier à Plouzané (29)",
  "Électricité, chauffage et plomberie dans le bassin brestois depuis 2010. Devis gratuit, travail soigné. Parlez-nous de votre projet.",
  home_body, jsonld("/","Accueil",None,faq=FAQ_HOME), "/"))

# Gabarit des pages métier et des pages locales SEO (contenu inchangé, nouvelle DA)
METIER_OF = {"/electricite":"electricien","/chauffage":"chauffagiste","/plomberie":"plombier"}
def gen_sub(slug,title,desc,active,crumb,eyebrow,h1,lead,hero_img,hero_float,sections,recap_h2,area,extra="",breadcrumb_name=None,hero_alt=None,faq=None,service=None):
    rows="".join(feat_section(*s, flip=(i%2==1)) for i,s in enumerate(sections))
    metier=METIER_OF.get(active,"electricien")
    area_h2=(f'On intervient à {area}<br><b>et dans tout le bassin brestois.</b>' if area else None)
    body=(phero(crumb,eyebrow,h1,lead,hero_img,FLOAT_AVIS,hero_alt)+trust_strip()
          +f'<section class="sec"><div class="wrap"><div class="feat-rows">{rows}</div></div></section>'
          +extra+(areas_block(metier,area_h2) if area_h2 else areas_block(metier))
          +(faq_section(faq) if faq else "")+cta_section(recap_h2))
    pages.append((slug,title,desc,body,jsonld("/"+slug,h1,area,breadcrumb_name=breadcrumb_name,faq=faq,service=service),"/services"))

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

# ---------- /services ----------
services_body=(phero(CRUMB_M.format(label="Services"),"Nos services",
  "Électricité, chauffage, plomberie.<br><b>Une seule équipe.</b>", SECT_HOME+" Un seul devis, un seul interlocuteur, du début à la fin.",
  "plomb.jpg",FLOAT_AVIS,"Salle de bain bois et marbre rénovée par ARélec")
 +trust_strip()
 +('<section class="sec"><div class="wrap">'
   f'<div class="split-head"><div class="head"><span{R()}>{label("Ce qu\'on fait")}</span>'
   f'<h2{R(.08,"h2")}>Six façons de garder<br><b>votre maison au top.</b></h2></div>'
   f'<div class="side"><p{R(.12,"lead")}>Choisissez le service qui correspond à votre besoin, ou décrivez-nous la situation : on vous oriente.</p></div></div>'
   f'<div class="svc-grid">{svc_cards()}</div></div></section>')
 +('<section class="sec" style="padding-top:0"><div class="wrap"><div class="two-col">'
   f'<img{R()} src="/assets/img/reno-cablage.jpg" alt="Câblage et isolation en cours de rénovation" loading="lazy">'
   f'<div class="head"><span{R(.05)}>{label("Notre méthode")}</span><h2{R(.1,"h2")}>Un travail soigné.<br><b>Des conseils clairs.</b></h2>'
   f'<p{R(.15,"lead")}>On ne se lance jamais sans avoir compris. On arrive, on regarde, on explique — quitte à dire qu\'un truc n\'est pas utile chez vous.</p>'
   f'<ul{R(.2,"steps-v")}>'
   '<li><span class="step-n mono">01</span><div><b>Comprendre le besoin</b><p>Ce qui ne va pas, ce que vous voulez, vos contraintes et votre budget.</p></div></li>'
   '<li><span class="step-n mono">02</span><div><b>Étudier les options</b><p>On vérifie l\'existant sur place et on vous présente les solutions possibles.</p></div></li>'
   '<li><span class="step-n mono">03</span><div><b>Expliquer avant d\'agir</b><p>Un devis détaillé, écrit, sans engagement. Rien ne démarre sans votre accord.</p></div></li>'
   '</ul></div></div></div></section>')
 +('<section class="sec" style="padding-top:0"><div class="wrap">'
   f'<div class="head"><span{R()}>{label("Neuf &amp; rénovation")}</span><h2{R(.08,"h2")}>De la construction<br><b>à la rénovation complète.</b></h2></div>'
   '<div class="cards-2">'
   f'<div{R(0,"img-card")}><img src="/assets/img/cablage.jpg" alt="" loading="lazy"><div class="svc-body"><h3 class="h3">Construction neuve</h3>'
   '<p>On conçoit l\'installation, on tire les gaines, on pose le tableau, le chauffage et les sanitaires, et on met tout en route.</p></div></div>'
   f'<div{R(.08,"img-card")}><img src="/assets/img/sdb-bois.jpg" alt="" loading="lazy"><div class="svc-body"><h3 class="h3">Rénovation</h3>'
   '<p>Mise aux normes, remplacement du chauffage, salle de bain refaite : pièce par pièce, sans tout casser.</p></div></div>'
   '</div></div></section>')
 +process_section()+faq_section(FAQ_HOME[2:6], h2="Des questions sur votre projet ?")+cta_section('Besoin d\'un artisan ?<br><b>Commencez ici.</b>'))
pages.append(("services","Nos services : électricité, chauffage, plomberie | ARélec",
  "Installation et rénovation électrique, mise aux normes, dépannage, chauffage, salle de bain et plomberie dans le bassin brestois. Devis gratuit — ARélec.",
  services_body, jsonld("/services","Services",None,faq=FAQ_HOME[2:6],breadcrumb_name="Services"), "/services"))

# ---------- /entreprise (À propos) ----------
VALUES=[("broom","On bosse propre","On protège, on range en partant. Votre maison reste votre maison pendant le chantier."),
        ("chat","On dit ce qu'on pense","Des conseils francs, quitte à dire qu'un équipement n'est pas utile chez vous."),
        ("tool","On revient si besoin","Un souci après le chantier ? On revient, c'est la base du métier."),
        ("check","On finit ce qu'on commence","Un chantier se termine proprement, mis en route et expliqué.")]
about_body=(phero(CRUMB_M.format(label="L'entreprise"),"À propos d'ARélec",
  "Un artisan d'ici,<br><b>depuis 2010.</b>",
  "Installés à Plouzané, on s'occupe de l'élec, du chauffage et de la plomberie dans le bassin brestois. En neuf, en rénovation, en dépannage. Un seul interlocuteur, de A à Z.",
  "maison-bleue.jpg",FLOAT_AVIS,"Maison rénovée à l'heure bleue, chantier ARélec")
 +('<section class="sec"><div class="wrap"><div class="two-col">'
   f'<div class="head"><span{R()}>{label("Notre histoire")}</span><h2{R(.08,"h2")}>Une histoire d\'artisan,<br><b>à Plouzané.</b></h2>'
   f'<p{R(.14,"lead")}>On a démarré ARélec en 2010, ici, dans le bassin brestois. Le principe de base : qu\'un même artisan puisse refaire la maison de bout en bout — élec, chauffage, plomberie — sans qu\'il faille jongler avec trois entreprises. Quinze ans plus tard, on fait toujours comme ça.</p>'
   f'<p{R(.18,"lead")}>Le pont sur le logo, c\'est le pont de l\'Iroise. On est d\'ici, on y reste.</p></div>'
   f'<img{R(.1)} src="/assets/img/chantier-plouider.jpg" alt="Chantier ARélec à Plouider" loading="lazy">'
   '</div></div></section>')
 +stats_section('Quelques repères<br><b>sur ARélec.</b>',"SARL ARélec, gérée par Arnaud Roncey, basée à Plouzané (29280) et immatriculée sous le SIREN 790 223 036.")
 +('<section class="sec" style="padding-top:0"><div class="wrap">'
   f'<div class="head center"><span{R()}>{label("Nos valeurs")}</span><h2{R(.08,"h2")}>Ce qui guide<br><b>chaque intervention.</b></h2></div>'
   '<div class="cards-4">'+"".join(f'<div{R(.08*i,"mist-card")}><span class="icon-chip">{ic(a)}</span><div class="txt"><h3 class="h3">{b}</h3><p class="small">{c}</p></div></div>' for i,(a,b,c) in enumerate(VALUES))+
   '</div></div></section>')
 +('<section class="sec" style="padding-top:0"><div class="wrap">'
   f'<div class="split-head"><div class="head"><span{R()}>{label("L\'équipe")}</span><h2{R(.08,"h2")}>Les gens derrière<br><b>ARélec.</b></h2></div>'
   f'<div class="side"><p{R(.12,"lead")}>Une petite équipe d\'artisans qui fait les trois métiers elle-même.</p></div></div>'
   '<div class="cards-3">'
   f'<div{R(0,"team-card")}><div class="ph mono">{tbd("Photo à ajouter")}</div><div class="who"><b>Arnaud Roncey</b><span>Gérant · électricité, chauffage, plomberie</span></div></div>'
   f'<div{R(.08,"team-card")}><div class="ph mono">{tbd("Photo à ajouter")}</div><div class="who"><b>{tbd("Prénom Nom")}</b><span>{tbd("Rôle à compléter")}</span></div></div>'
   f'<div{R(.16,"team-card")}><div class="ph mono">{tbd("Photo à ajouter")}</div><div class="who"><b>{tbd("Prénom Nom")}</b><span>{tbd("Rôle à compléter")}</span></div></div>'
   '</div></div></section>')
 +('<section class="sec" style="padding-top:0"><div class="wrap">'
   f'<div class="head"><span{R()}>{label("Garanties")}</span><h2{R(.08,"h2")}>Des engagements<br><b>clairement expliqués.</b></h2></div>'
   '<div class="cards-3">'
   f'<div{R(0,"mist-card")}><span class="icon-chip">{ic("doc")}</span><div class="txt"><h3 class="h3">Entreprise immatriculée</h3><p class="small">SARL ARélec, SIREN 790 223 036, Plouzané (29280).</p></div></div>'
   f'<div{R(.08,"mist-card")}><span class="icon-chip">{ic("shield")}</span><div class="txt"><h3 class="h3">Assurances</h3><p class="small">{tbd("Assurance décennale et RC pro : assureur et n° de contrat à compléter")}</p></div></div>'
   f'<div{R(.16,"mist-card")}><span class="icon-chip">{ic("check")}</span><div class="txt"><h3 class="h3">Qualifications</h3><p class="small">{tbd("Labels et qualifications à compléter")}</p></div></div>'
   '</div></div></section>')
 +cta_section('Et si on parlait<br><b>de votre projet ?</b>'))
pages.append(("entreprise","L'entreprise | ARélec, artisan depuis 2010",
  "ARélec, artisan électricien-chauffagiste-plombier à Plouzané depuis 2010. Une équipe, un seul interlocuteur, un travail soigné dans tout le bassin brestois.",
  about_body, jsonld("/entreprise","L'entreprise",None,breadcrumb_name="L'entreprise"), "/entreprise"))

# ---------- /blog (maquette : articles à rédiger, page en noindex) ----------
POSTS=[("chauffage","confort.jpg","Chauffage : les réglages qui font baisser la facture"),
       ("plomberie","sdb-bleue.jpg","Rénover sa salle de bain : par où commencer ?"),
       ("électricité","reno-cablage.jpg","Mise aux normes NF C 15-100 : ce qu'il faut savoir"),
       ("plomberie","douche-marbre.jpg","Une fuite invisible ? Les signes qui ne trompent pas"),
       ("électricité","eclairage.jpg","Bien éclairer une pièce : nos conseils d'artisan"),
       ("chauffage","maison-bleue.jpg","Entretien annuel du chauffage : pourquoi c'est utile")]
posts="".join(f'<article{R(.06*(i%3),"post")}><div class="img"><img src="/assets/img/{img}" alt="" loading="lazy"><span class="tag mono">{cat}</span></div>'
              f'<div class="meta mono"><span class="pill lime">À rédiger</span>{tbd("date")}</div><h3 class="h3">{t}</h3>'
              f'<p class="small">{tbd("Résumé de l\'article à rédiger")}</p></article>' for i,(cat,img,t) in enumerate(POSTS))
blog_body=(phero(CRUMB_M.format(label="Blog"),"Le journal ARélec",
  "Des conseils pratiques<br><b>pour une maison sûre et confortable.</b>",
  "Électricité, chauffage, plomberie : les bons réflexes et les questions qu'on nous pose le plus, expliqués simplement.",actions="")
 +('<section class="sec"><div class="wrap">'
   f'<article{R(0,"post-feat")}><div class="img"><img src="/assets/img/cablage.jpg" alt="" loading="lazy"><span class="tag mono">À la une</span></div>'
   f'<div class="txt"><div class="meta mono"><span class="pill lime">À rédiger</span></div>'
   '<h2 class="h2">Disjoncteur qui saute :<br><b>les bons réflexes.</b></h2>'
   f'<p class="lead">{tbd("Introduction de l\'article à rédiger")}</p></div></article>'
   f'<div class="head" style="margin-top:96px"><span{R()}>{label("Derniers articles")}</span></div>'
   f'<div class="posts">{posts}</div></div></section>')
 +cta_section('Une question précise ?<br><b>Posez-la directement.</b>',"Notre assistant vous répond tout de suite, puis l'équipe prend le relais sur WhatsApp."))
pages.append(("blog","Blog — conseils électricité, chauffage, plomberie | ARélec",
  "Conseils d'artisan sur l'électricité, le chauffage et la plomberie : bons réflexes, entretien et rénovation, par ARélec.",
  blog_body, jsonld("/blog","Blog",None,reviews=False,breadcrumb_name="Blog"), "/blog"))

# ---------- /contact ----------
contact_body=(phero(CRUMB_M.format(label="Contact"),"Contact",
  "Dites-nous ce dont vous avez besoin.<br><b>On s'occupe de la suite.</b>",
  "Le plus rapide : notre assistant, WhatsApp ou un coup de fil. Réponse sous 24 à 48 h, devis gratuit sur place.",actions="")
 +('<section class="sec"><div class="wrap"><div class="contact-grid">'
   f'<div{R(0,"panel mist")}><span class="mono">Parler à l\'équipe</span>'
   f'<button class="method ai" type="button" data-chat><span class="icon-chip">{ic("chat")}</span><div><b>Assistant du site</b><span>Réponse immédiate, puis relais WhatsApp</span></div><span class="go">{ic("arrow")}</span></button>'
   f'<a class="method wa" href="https://wa.me/{WHATSAPP_INT}" target="_blank" rel="noopener"><span class="icon-chip">{SVG_WA}</span><div><b>WhatsApp</b><span>{PHONE_MOBILE_DISP}</span></div><span class="go">{ic("arrow")}</span></a>'
   f'<a class="method" href="tel:{PHONE_TEL}"><span class="icon-chip">{ic("bolt")}</span><div><b>Téléphone</b><span>{PHONE_DISP} · mobile {PHONE_MOBILE_DISP}</span></div><span class="go">{ic("arrow")}</span></a>'
   f'<a class="method" href="mailto:{EMAIL}"><span class="icon-chip">{SVG_MAIL}</span><div><b>Email</b><span>{EMAIL}</span></div><span class="go">{ic("arrow")}</span></a>'
   f'<div class="method" style="cursor:default"><span class="icon-chip">{ic("clock")}</span><div><b>Horaires</b><span>Lun–Ven · 8h–18h · {ADDRESS}</span></div></div>'
   '</div>'
   f'<div{R(.08,"panel ink dk")}><span class="mono" style="color:rgba(255,255,255,.55)">Demander une intervention</span>'
   '<h2 class="h2" style="font-size:32px">Laissez-nous un message.</h2>'
   '<form class="cform" id="cform">'
   '<div class="row"><label>Nom <input name="nom" type="text" required autocomplete="name"></label>'
   '<label>Téléphone <input name="tel" type="tel" autocomplete="tel"></label></div>'
   '<div class="row"><label>Email <input name="email" type="email" required autocomplete="email"></label>'
   '<label>Commune <input name="commune" type="text" autocomplete="address-level2"></label></div>'
   '<label>Type de travaux <select name="metier"><option>Électricité</option><option>Chauffage</option><option>Plomberie</option><option>Plusieurs / je ne sais pas</option></select></label>'
   '<label>Votre projet <textarea name="message" rows="5" required placeholder="Ce qu\'il faut faire, neuf ou rénovation, urgence, délais…"></textarea></label>'
   f'<button type="submit" class="btn btn-lime"><span class="chip">{ic("arrow")}</span>Envoyer ma demande</button>'
   '<p class="cform-foot">Vos informations servent uniquement à vous répondre.</p>'
   '</form></div>'
   '</div></div></section>')
 +('<section class="sec" style="padding-top:0"><div class="wrap">'
   f'<div class="head center"><span{R()}>{label("Après votre demande")}</span><h2{R(.08,"h2")}>Un chemin simple,<br><b>de la demande à la visite.</b></h2></div>'
   '<div class="cards-3">'
   + "".join(f'<div{R(.08*i,"mist-card")}><span class="step-n mono" style="align-self:flex-start">{i+1:02d}</span><div class="txt"><h3 class="h3">{a}</h3><p class="small">{b}</p></div></div>'
             for i,(a,b) in enumerate([("On lit votre demande","Type de travaux, commune, urgence : on regarde ce qu'il vous faut."),
                                       ("On vous recontacte","Sous 24 à 48 h, par téléphone ou WhatsApp, pour préciser le besoin."),
                                       ("On cale la visite","Visite gratuite sur place, puis devis détaillé et sans engagement.")]))
   + '</div></div></section>')
 +faq_section([("Sous combien de temps répondez-vous ?","Sous 24 à 48 h en général. L'assistant du site, lui, répond tout de suite et transmet votre demande sur WhatsApp."),
               ("Faut-il savoir quel métier choisir ?","Non. Décrivez simplement la situation : on fait l'électricité, le chauffage et la plomberie, on saura vous orienter."),
               FAQ_HOME[3], FAQ_HOME[1]], h2="Avant de nous écrire"))
pages.append(("contact","Contact & devis gratuit | ARélec — Plouzané (29)",
  "Contactez ARélec : assistant en ligne, WhatsApp 06 78 02 04 24, téléphone 02 98 40 20 43 ou contact@entreprise-arelec.fr. Devis gratuit dans tout le bassin brestois.",
  contact_body+'<script>document.getElementById("cform")?.addEventListener("submit",function(e){e.preventDefault();const f=e.target;const body=`Nom: ${f.nom.value}\\nTéléphone: ${f.tel.value}\\nEmail: ${f.email.value}\\nCommune: ${f.commune.value}\\nTravaux: ${f.metier.value}\\n\\nMessage:\\n${f.message.value}`;window.location.href=`mailto:'+EMAIL+'?subject=${encodeURIComponent("Demande ARélec — "+f.nom.value)}&body=${encodeURIComponent(body)}`;});</script>',
  jsonld("/contact","Contact",None,breadcrumb_name="Contact"), "/contact"))

# ---------- /realisations ----------
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
 ("chantier-toiture.jpg","Rénovation","Chantier en bord de mer"),
]
gallery_items="".join(f'<figure{R(.05*(i%3),"gcard")}><img src="/assets/img/{img}" alt="{html.escape(cap)}" loading="lazy">'
                      f'<figcaption><div class="mono">{kind}</div><span>{cap}</span></figcaption></figure>' for i,(img,kind,cap) in enumerate(GALLERY))
real_body=(phero(CRUMB_M.format(label="Réalisations"),"Réalisations",
  "Le travail bien fait,<br><b>en vrai.</b>",
  "Quelques chantiers récents dans le bassin brestois : rénovations complètes, salles de bain, tableaux électriques, éclairage soigné.",actions="")
 +f'<section class="sec"><div class="wrap"><div class="gallery">{gallery_items}</div></div></section>'
 +cta_section('Un projet similaire ?<br><b>On en parle.</b>',img="sdb-baignoire.jpg"))
pages.append(("realisations","Nos réalisations | ARélec — Brest & Finistère",
  "Galerie de nos chantiers à Brest, Plouzané et alentour : salles de bain, rénovations complètes, éclairage et installations électriques.",
  real_body, jsonld("/realisations","Réalisations",None,breadcrumb_name="Réalisations"), "/realisations"))

# ---------- /avis ----------
avis_body=(phero(CRUMB_M.format(label="Avis clients"),"Avis clients",
  "Ils nous<br><b>recommandent.</b>",
  "Qualité du travail, chantier propre, réactivité et bons conseils : voici ce que nos clients disent d'ARélec sur Google.",actions="")
 +rating_section().replace(btn("Lire les avis","/avis","light","arrow"),btn_contact("dark"))
 +testimonials_section()+cta_section())
pages.append(("avis","Avis clients | ARélec — Brest & Plouzané",
  "Ce que nos clients disent d'ARélec : qualité, propreté, réactivité et bons conseils. Avis vérifiés Google.",
  avis_body, jsonld("/avis","Avis clients",None,breadcrumb_name="Avis clients"), "/"))

# ---------- pages légales ----------
def legal(slug,title,desc,h1,inner,breadcrumb_name):
    body=(phero(CRUMB_M.format(label=breadcrumb_name),breadcrumb_name,h1,"Informations légales du site entreprise-arelec.fr.",actions="")
          +f'<section class="sec"><div class="wrap"><div class="prose">{inner}</div></div></section>')
    pages.append((slug,title,desc,body,jsonld("/"+slug,breadcrumb_name,None,reviews=False,breadcrumb_name=breadcrumb_name),"/"))
legal("mentions-legales","Mentions légales | ARélec","Mentions légales du site ARélec (SARL ARélec, Plouzané).",
  "Mentions<br><b>légales.</b>",
  "<h2>Éditeur</h2><p>SARL ARélec — SIREN 790 223 036 — Plouzané (29280).<br>Directeur de la publication : Arnaud Roncey.<br>"
  f"Contact : {EMAIL} · {PHONE_DISP}</p>"
  f"<h2>Informations à compléter</h2><p>{tbd('Capital social')} · {tbd('N° de TVA intracommunautaire')} · {tbd('Adresse du siège')}</p>"
  "<h2>Hébergement</h2><p>Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, États-Unis.</p>",
  "Mentions légales")
legal("politique-confidentialite","Politique de confidentialité | ARélec","Politique de confidentialité et gestion des données du site ARélec.",
  "Confidentialité.",
  "<h2>Formulaire de contact</h2><p>Les données envoyées via le formulaire de contact servent uniquement à répondre à votre demande.</p>"
  "<h2>Assistant du site</h2><p>Les messages écrits à l'assistant du site sont transmis à un service d'IA (via OpenRouter) uniquement pour générer la réponse ; le site ne les enregistre pas. Si vous poursuivez sur WhatsApp, la conversation est traitée par ARélec et son agent WhatsApp pour préparer votre demande.</p>"
  f"<h2>Vos droits</h2><p>Pour toute question ou demande de suppression : {EMAIL}. {tbd('Durées de conservation et détails RGPD à compléter avec Arnaud')}</p>",
  "Confidentialité")

# ---------- écriture ----------
(JS_DIR/"site.js").write_text(SITE_JS)
for slug,t,d,body,jl,active in pages:
    write(slug, shell(slug,t,d,body,jl,active))

urls=[p[0] for p in pages if p[0] not in NOINDEX]
TODAY=datetime.date.today().isoformat()
def url_meta(u):
    if u=="": return ("1.0","weekly")
    if u in ("electricite","chauffage","plomberie"): return ("0.9","monthly")
    if u == "contact": return ("0.8","monthly")
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

1. **Premier échange** : assistant du site, puis WhatsApp (06 78 02 04 24), ou téléphone
2. **Visite sur place gratuite** pour établir le vrai devis
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

Le devis est toujours gratuit. Le premier échange se fait via l'assistant du site puis sur WhatsApp (ou par téléphone), puis ARélec se déplace gratuitement pour établir le vrai devis sur place.

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
# Contexte de l'assistant (/api/chat) = la documentation complète du site
(API/"_context.js").write_text("// Généré par build_site.py — ne pas éditer.\nmodule.exports = { CONTEXT: " + json.dumps(LLMS_FULL, ensure_ascii=False) + " };\n")
(JS_DIR/"chat.js").write_text((ROOT/"chat.js").read_text())

print("Pages :", len(pages))
for slug,*_ in pages: print("  /"+(slug or "(accueil)"))
