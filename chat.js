// Assistant du site ARélec — copié dans site/assets/js/chat.js par build_site.py.
// Mascotte qui saute en bas à droite + bulle d'accroche, panneau agrandissable, réponses en flux (/api/chat),
// mise en forme (gras, listes, liens), dictée vocale et lecture à voix haute, boutons vers les pages du site,
// relais WhatsApp ou formulaire intégré (/api/contact). La conversation suit le visiteur de page en page.
(function () {
  const launch = document.querySelector(".cb"), box = document.getElementById("chat");
  if (!launch || !box) return;
  const mascot = launch.querySelector(".cb-mascot"), tease = launch.querySelector(".cb-tease");
  const list = box.querySelector(".chat-msgs"), form = box.querySelector(".chat-form");
  const input = form.querySelector("textarea"), send = form.querySelector(".chat-send"), mic = form.querySelector(".chat-mic");
  const expand = box.querySelector(".chat-expand");
  const tpl = id => document.getElementById(id).innerHTML;
  const AVATAR = "/assets/img/mascotte-buste.png";
  const WA = box.dataset.wa, KEY = "arelec-chat-v1", MAX = 800;
  const HELLO = "Bonjour ! Je réponds aux questions sur l'**électricité**, le **chauffage** et la **plomberie** chez ARélec. Dites-moi ce qui vous amène.";
  const FALLBACK = "Je n'arrive pas à répondre pour le moment. Le plus simple : écrivez-nous sur WhatsApp, laissez vos coordonnées juste en dessous, ou appelez le **02 98 40 20 43**.";
  const SENT = "C'est envoyé. Arnaud a votre demande et vous recontacte **sous 24 à 48 h**.";
  const ERR = {
    nom: "Indiquez votre nom.", joignable: "Laissez un téléphone ou un email.", email: "L'email ne semble pas valide.",
    tel: "Le numéro ne semble pas complet.", message: "Décrivez votre projet en quelques mots.", rate: "Trop d'envois, réessayez dans quelques minutes."
  };
  const mobile = () => window.matchMedia("(max-width: 760px)").matches;

  // msgs : historique ; summary : résumé du projet ; mode : "whatsapp" | "form" ; cf : formulaire affiché ;
  // sent : demande envoyée ; nav : page ouverte depuis le chat ; draft : saisie du formulaire ; big : panneau agrandi ; seen : chat déjà ouvert
  const blank = () => ({ msgs: [], summary: "", mode: null, cf: false, sent: false, nav: false, draft: {}, big: false, seen: false });
  let st = blank(), busy = false;
  try { const d = JSON.parse(sessionStorage.getItem(KEY) || "null"); if (d) st = Object.assign(st, d); } catch (e) {}
  const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} };
  const waLink = () => "https://wa.me/" + WA + "?text=" + encodeURIComponent("Bonjour ARélec 👋 Je viens du site." + (st.summary ? "\n" + st.summary : ""));
  const scroll = () => { list.scrollTop = list.scrollHeight; };
  const el = (tag, cls, html) => { const d = document.createElement(tag); if (cls) d.className = cls; if (html != null) d.innerHTML = html; return d; };

  // ---------- mise en forme légère (le texte est échappé avant tout) ----------
  const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  function inline(s) {
    return esc(s)
      .replace(/\*\*([^*\n]+?)\*\*/g, "<b>$1</b>")
      .replace(/\*/g, "")
      .replace(/\[([^\]\n]+)\]\((\/[^\s)]*|tel:[+\d]+|mailto:[^\s)]+)\)/g, '<a href="$2">$1</a>')
      .replace(/(?<![\d+])(0[1-9](?:[ .]?\d{2}){4})(?!\d)/g, m => `<a href="tel:${m.replace(/\D/g, "")}">${m}</a>`)
      .replace(/(?<![\w./-])([\w.+-]+@[\w-]+\.[\w.]+)/g, '<a href="mailto:$1">$1</a>');
  }
  function md(text) {
    const out = []; let ul = null;
    text.replace(/\r/g, "").split("\n").forEach(line => {
      const li = line.match(/^\s*(?:[-•*]|\d+[.)])\s+(.*)/);
      if (li) { if (!ul) { ul = []; out.push(ul); } ul.push(li[1]); return; }
      ul = null;
      if (line.trim()) out.push(line.trim()); else out.push("");
    });
    let html = "", para = [];
    const flush = () => { if (para.length) { html += "<p>" + para.map(inline).join("<br>") + "</p>"; para = []; } };
    out.forEach(b => {
      if (Array.isArray(b)) { flush(); html += "<ul>" + b.map(x => "<li>" + inline(x) + "</li>").join("") + "</ul>"; }
      else if (b === "") flush();
      else para.push(b);
    });
    flush();
    return html;
  }
  // Retire les tics d'IA qui passent malgré les consignes (« Parfait ! », tirets longs…)
  const tidy = s => s
    .replace(/^\s*(?:Parfait|Super|Génial|Excellente question|Très bonne question|Absolument|Bien sûr que oui)\s*[!,.]*\s*/i, "")
    .replace(/\s*—\s*/g, ", ")
    .replace(/^./, c => c.toUpperCase());
  const visible = raw => tidy(raw.split("<<")[0].replace(/\n+$/, "")); // cache les lignes techniques pendant l'écriture

  // ---------- lecture à voix haute ----------
  const tts = "speechSynthesis" in window ? window.speechSynthesis : null;
  let speaking = null;
  function sayBtn(text) {
    if (!tts) return null;
    const b = el("button", "chat-say", tpl("chat-ic-vol") + "<span>Écouter</span>");
    b.type = "button";
    b.addEventListener("click", () => {
      const again = speaking === b;
      tts.cancel(); if (speaking) { speaking.classList.remove("on"); speaking.lastChild.textContent = "Écouter"; } speaking = null;
      if (again) return;
      const u = new SpeechSynthesisUtterance(text.replace(/\*\*/g, ""));
      u.lang = "fr-FR"; u.rate = 1.05;
      const v = tts.getVoices().find(v => v.lang && v.lang.startsWith("fr"));
      if (v) u.voice = v;
      u.onend = u.onerror = () => { b.classList.remove("on"); b.lastChild.textContent = "Écouter"; if (speaking === b) speaking = null; };
      b.classList.add("on"); b.lastChild.textContent = "Stop"; speaking = b;
      tts.speak(u);
    });
    return b;
  }

  // ---------- messages ----------
  let lastRole = null;
  function row(role) {
    const r = el("div", "chat-row " + (role === "user" ? "me" : "bot") + (lastRole === role ? " cont" : ""));
    if (role !== "user") r.appendChild(el("span", "mini", `<img src="${AVATAR}" alt="">`));
    const col = el("div", "chat-col"); r.appendChild(col);
    list.appendChild(r); lastRole = role;
    return col;
  }
  function bubble(role, text, opts = {}) {
    const col = row(role);
    const b = el("div", "chat-msg");
    if (role === "user") b.textContent = text; else b.innerHTML = md(text);
    col.appendChild(b);
    if (role !== "user" && !opts.noVoice) { const s = sayBtn(text); if (s) col.appendChild(s); }
    return { col, b };
  }
  function links(items) {
    const keep = (items || []).filter(p => p.url !== location.pathname);
    if (!keep.length) return;
    const wrap = el("div", "chat-links");
    keep.forEach(p => {
      const a = el("a", "chat-link", esc(p.title) + tpl("chat-ic-go"));
      a.href = p.url;
      a.addEventListener("click", () => { st.nav = true; save(); }); // le panneau se rouvre sur la page suivante
      wrap.appendChild(a);
    });
    list.appendChild(wrap); lastRole = null;
  }
  function hello() {
    bubble("assistant", HELLO, { noVoice: true });
    if (st.msgs.length) return;
    const h = el("div", "chat-hello");
    h.appendChild(el("p", "lead", "Choisissez un sujet ou écrivez votre question :"));
    const g = el("div", "chat-sugg", tpl("chat-sugg"));
    g.addEventListener("click", e => { const b = e.target.closest("button"); if (b) ask(b.dataset.ask); });
    h.appendChild(g); list.appendChild(h); lastRole = null;
  }

  // ---------- relais : WhatsApp ou formulaire ----------
  // Relais : carte WhatsApp + carte « Être rappelé » repliée (préremplie, elle se déroule au clic)
  function handoff() {
    list.querySelectorAll(".chat-wa,.chat-cf").forEach(n => n.remove());
    if (st.sent) return;
    if (st.summary && st.mode !== "form") {
      const a = el("a", "chat-wa", tpl("chat-wa-ic") + "<span><b>Continuer sur WhatsApp</b><small>Votre demande est déjà résumée, Arnaud prend le relais.</small></span>");
      a.href = waLink(); a.target = "_blank"; a.rel = "noopener";
      list.appendChild(a);
    }
    if (st.summary || st.cf) list.appendChild(contactForm());
    lastRole = null;
  }
  function showForm() {
    st.cf = true; st.sent = false; save(); handoff();
    const c = list.querySelector(".chat-cf");
    c?.scrollIntoView({ block: "nearest", behavior: "smooth" });
    c?.querySelector("input")?.focus({ preventScroll: true });
  }
  function contactForm() {
    const wrap = el("div", "chat-cf" + (st.cf ? " open" : "") + (st.mode === "form" ? " hl" : ""));
    const head = el("button", "chat-cf-head",
      `<span class="t"><b>${st.mode === "form" ? "Laisser mes coordonnées" : "Pas de WhatsApp ? Être rappelé"}</b><small></small></span>` + tpl("chat-ic-down"));
    head.type = "button";
    head.setAttribute("aria-expanded", st.cf ? "true" : "false");
    wrap.appendChild(head);
    const f = el("form", "chat-cf-body",
      "<small>Déjà prérempli avec votre demande. Un téléphone ou un email suffit.</small>" +
      '<input name="nom" autocomplete="name" maxlength="80" placeholder="Votre nom" aria-label="Votre nom">' +
      '<div class="two"><input name="tel" type="tel" autocomplete="tel" maxlength="30" placeholder="Téléphone" aria-label="Téléphone">' +
      '<input name="email" type="email" autocomplete="email" maxlength="120" placeholder="Email" aria-label="Email"></div>' +
      '<textarea name="message" maxlength="2000" rows="3" placeholder="Votre projet" aria-label="Votre projet"></textarea>' +
      '<input class="hp" name="site" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<p class="err" role="alert"></p><button type="submit" class="go">Envoyer ma demande</button>');
    f.noValidate = true;
    const d = st.draft || {};
    ["nom", "tel", "email"].forEach(k => { f[k].value = d[k] || ""; });
    f.message.value = d.message || (st.summary || st.msgs.filter(m => m.role === "user").map(m => m.content).join("\n")).replace(/^Mon projet\s*:\s*/i, "");
    const preview = () => { head.querySelector("small").textContent = f.message.value.trim().slice(0, 70) + (f.message.value.trim().length > 70 ? "…" : ""); };
    preview();
    head.addEventListener("click", () => {
      st.cf = !wrap.classList.contains("open"); save();
      wrap.classList.toggle("open", st.cf); head.setAttribute("aria-expanded", st.cf);
      if (st.cf) { wrap.scrollIntoView({ block: "nearest", behavior: "smooth" }); f.nom.focus({ preventScroll: true }); }
    });
    f.addEventListener("input", () => { preview(); st.draft = { nom: f.nom.value, tel: f.tel.value, email: f.email.value, message: f.message.value }; save(); });
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const err = f.querySelector(".err"), btn = f.querySelector('button[type="submit"]');
      err.textContent = "";
      if (!f.nom.value.trim()) { err.textContent = ERR.nom; f.nom.focus(); return; }
      if (!f.tel.value.trim() && !f.email.value.trim()) { err.textContent = ERR.joignable; f.tel.focus(); return; }
      btn.disabled = true; btn.textContent = "Envoi…";
      try {
        const r = await fetch("/api/contact/", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ nom: f.nom.value, tel: f.tel.value, email: f.email.value, message: f.message.value, site: f.site.value, source: "chat", page: location.pathname })
        });
        const out = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(out.error || r.status);
        st.sent = true; st.cf = false; st.draft = {};
        st.msgs.push({ role: "assistant", content: SENT });
        save(); handoff(); bubble("assistant", SENT); scroll();
      } catch (x) {
        err.textContent = ERR[x.message] || "L'envoi n'a pas fonctionné. Appelez le 02 98 40 20 43 ou écrivez à contact@entreprise-arelec.fr.";
        btn.disabled = false; btn.textContent = "Envoyer ma demande";
      }
    });
    wrap.appendChild(f);
    return wrap;
  }

  function render() {
    list.innerHTML = ""; lastRole = null;
    hello();
    st.msgs.forEach(m => { bubble(m.role, m.content); if (m.role === "assistant") links(m.links); });
    handoff();
    scroll();
  }

  // ---------- ouverture, taille ----------
  function setBig(on) {
    st.big = on; save();
    box.classList.toggle("big", on);
    expand.setAttribute("aria-label", on ? "Réduire la taille" : "Agrandir");
    expand.dataset.tip = on ? "Taille normale" : "Agrandir";
  }
  function open() {
    if (document.body.classList.contains("menu-open")) document.querySelector(".drawer-close")?.click();
    clearTimeout(teaseTimer);
    box.hidden = false;
    document.body.classList.add("chat-open");
    mascot.setAttribute("aria-expanded", "true");
    st.seen = true; save();
    setBig(st.big && !mobile());
    render();
    if (!mobile()) setTimeout(() => input.focus(), 60);
  }
  function close() {
    stopMic(); tts?.cancel();
    box.hidden = true;
    document.body.classList.remove("chat-open");
    mascot.setAttribute("aria-expanded", "false");
    mascot.focus({ preventScroll: true });
  }

  // ---------- échange avec l'assistant (réponse en flux) ----------
  async function ask(text) {
    text = (text || "").trim().slice(0, MAX);
    if (!text || busy) return;
    busy = true; send.disabled = true;
    list.querySelector(".chat-hello")?.remove();
    st.msgs.push({ role: "user", content: text }); save();
    bubble("user", text);
    input.value = ""; grow();
    const col = row("assistant");
    const typing = el("div", "chat-typing", "<i></i><i></i><i></i>");
    col.appendChild(typing); scroll();
    let raw = "", b = null, data = null;
    try {
      const r = await fetch("/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: st.msgs.slice(-16).map(m => ({ role: m.role, content: m.content })) })
      });
      if (!r.ok || !r.body) throw new Error(r.status);
      const reader = r.body.getReader(), dec = new TextDecoder();
      let buf = "";
      const paint = () => {
        const t = visible(raw);
        if (!t) return;
        if (!b) { typing.remove(); b = el("div", "chat-msg"); col.appendChild(b); }
        b.innerHTML = md(t) + '<span class="cur"></span>';
        const last = b.lastElementChild?.previousElementSibling; // curseur à la fin du dernier paragraphe
        if (last && last.tagName === "P") last.appendChild(b.querySelector(".cur"));
        scroll();
      };
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        let i;
        while ((i = buf.indexOf("\n")) >= 0) {
          const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
          if (!line) continue;
          const o = JSON.parse(line);
          if (o.d) { raw += o.d; paint(); }
          if (o.done) data = o;
          if (o.error) throw new Error(o.error);
        }
      }
      if (buf.trim()) { const o = JSON.parse(buf); if (o.done) data = o; }
      if (!data) throw new Error("incomplete");
      const reply = tidy((data.reply || "").trim()) || FALLBACK;
      const m = { role: "assistant", content: reply };
      if (Array.isArray(data.links) && data.links.length) m.links = data.links;
      st.msgs.push(m);
      if (data.handoff) { st.summary = data.handoff; st.sent = false; }
      if (data.mode === "form") st.mode = "form";
      col.parentNode.remove(); lastRole = "user";
      bubble("assistant", reply); links(m.links);
    } catch (e) {
      // Sans réponse : WhatsApp avec la demande telle quelle, et le formulaire pour ceux qui n'ont pas WhatsApp
      if (!st.summary) st.summary = "Ma demande : " + st.msgs.filter(m => m.role === "user").map(m => m.content).join(" ").slice(0, 400);
      st.msgs.push({ role: "assistant", content: FALLBACK });
      col.parentNode.remove(); lastRole = "user";
      bubble("assistant", FALLBACK);
    }
    save();
    handoff();
    scroll();
    busy = false; send.disabled = !input.value.trim();
  }

  function grow() {
    input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 140) + "px";
    send.disabled = busy || !input.value.trim();
  }

  // ---------- dictée vocale ----------
  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
  let rec = null, recBase = "";
  function stopMic() { if (rec) { try { rec.stop(); } catch (e) {} } }
  if (Rec) {
    mic.hidden = false;
    mic.addEventListener("click", () => {
      if (rec) return stopMic();
      tts?.cancel();
      rec = new Rec();
      rec.lang = "fr-FR"; rec.interimResults = true; rec.continuous = false;
      recBase = input.value ? input.value.trim() + " " : "";
      let heard = "";
      rec.onresult = e => {
        heard = Array.from(e.results).map(x => x[0].transcript).join("");
        input.value = recBase + heard; grow();
      };
      rec.onerror = e => {
        if (e.error === "not-allowed" || e.error === "service-not-allowed") input.placeholder = "Micro refusé : autorisez-le dans le navigateur";
      };
      rec.onend = () => {
        mic.classList.remove("on"); mic.setAttribute("aria-label", "Dicter un message");
        input.placeholder = "Écrivez ou dictez…";
        rec = null;
        if (heard.trim()) ask(input.value); // envoi direct après la dictée, comme un vocal
      };
      mic.classList.add("on"); mic.setAttribute("aria-label", "Arrêter la dictée");
      input.placeholder = "Je vous écoute…";
      try { rec.start(); } catch (e) { rec = null; mic.classList.remove("on"); }
    });
  }

  // ---------- mascotte : cachée en descendant, accoudée en remontant ----------
  // off → (arrivée) up → défilement vers le bas : peek (yeux + doigts) → vers le haut : up. Changements espacés pour rester calme.
  let state = "off", changedAt = 0, lastY = window.scrollY, ticking = false, teaseTimer = null;
  let teaseOff = false;
  try { teaseOff = !!sessionStorage.getItem("arelec-tease-off"); } catch (e) {}
  function setState(s) {
    if (s === state) return;
    state = s; changedAt = Date.now();
    launch.dataset.state = s;
    if (teaseOff || s === "off") return;
    tease.hidden = false;
    clearTimeout(teaseTimer);
    // Sur mobile, la bulle ne reste que quelques secondes à chaque changement
    if (mobile()) teaseTimer = setTimeout(() => { tease.hidden = true; }, s === "up" ? 6000 : 3500);
  }
  function hideTease(forever) {
    clearTimeout(teaseTimer);
    tease.hidden = true;
    if (forever) { teaseOff = true; try { sessionStorage.setItem("arelec-tease-off", "1"); } catch (e) {} }
  }
  function onScroll() {
    ticking = false;
    const y = window.scrollY, dy = y - lastY;
    if (Math.abs(dy) < 12) return;
    lastY = y;
    if (Date.now() - changedAt < 700) return;
    setState(y < 120 || dy < 0 ? "up" : "peek");
  }
  window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  setTimeout(() => setState(window.scrollY > 120 ? "peek" : "up"), 1200);
  tease.addEventListener("click", e => { if (e.target.closest(".cb-tease-x")) { e.stopPropagation(); hideTease(true); return; } open(); });

  // ---------- événements ----------
  mascot.addEventListener("click", open);
  box.querySelector(".chat-close").addEventListener("click", close);
  expand.addEventListener("click", () => { setBig(!box.classList.contains("big")); scroll(); });
  box.querySelector(".chat-reset").addEventListener("click", () => {
    tts?.cancel(); st = Object.assign(blank(), { big: st.big, seen: true }); save(); render(); input.focus();
  });
  box.addEventListener("keydown", e => { if (e.key === "Escape") close(); });
  box.querySelector(".chat-bar").addEventListener("click", e => {
    const t = e.target.closest(".chat-act");
    if (!t) return;
    if (t.hasAttribute("data-cf")) { e.preventDefault(); showForm(); }
    if (t.hasAttribute("data-nav")) { st.nav = true; save(); }
  });
  form.addEventListener("submit", e => { e.preventDefault(); ask(input.value); });
  input.addEventListener("input", grow);
  input.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); ask(input.value); } });
  // Tous les boutons « Prendre contact » ouvrent l'assistant (sans JS : lien vers /contact)
  document.addEventListener("click", e => { const t = e.target.closest("[data-chat]"); if (!t) return; e.preventDefault(); open(); });
  // Retour sur une page après un clic dans le chat : on rouvre là où on en était
  if (st.nav) { st.nav = false; save(); open(); }
})();
