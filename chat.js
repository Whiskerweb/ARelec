// Assistant du site ARélec — copié dans site/assets/js/chat.js par build_site.py.
// Répond via /api/chat (OpenRouter), propose des pages du site en boutons, puis fait basculer le prospect
// sur WhatsApp (message prérempli qui résume sa demande) ou, sans WhatsApp, sur un formulaire intégré (/api/contact).
// La conversation (et l'ouverture du panneau) suit le visiteur d'une page à l'autre pendant la session.
(function () {
  const fab = document.querySelector(".chat-fab"), box = document.getElementById("chat");
  if (!fab || !box) return;
  const list = box.querySelector(".chat-msgs"), sugg = box.querySelector(".chat-sugg");
  const form = box.querySelector(".chat-form"), input = form.querySelector("textarea"), send = form.querySelector(".chat-send");
  const WA = box.dataset.wa, KEY = "arelec-chat-v1", MAX = 800;
  const GREETING = "Bonjour 👋 Ici l'assistant d'ARélec. Électricité, chauffage ou plomberie : dites-moi ce que vous avez en tête (travaux, panne, commune) et je vous réponds.";
  const FALLBACK = "Je n'arrive pas à répondre pour le moment. Le plus simple : écrivez-nous sur WhatsApp, ou laissez vos coordonnées dans le formulaire ci-dessous. Vous pouvez aussi appeler le 02 98 40 20 43.";
  const SENT = "C'est envoyé ✅ Arnaud a votre demande et revient vers vous sous 24 à 48 h.";
  const ERR = {
    nom: "Indiquez votre nom.", joignable: "Laissez un téléphone ou un email.", email: "L'email ne semble pas valide.",
    tel: "Le numéro ne semble pas complet.", message: "Décrivez votre projet en quelques mots.", rate: "Trop d'envois, réessayez dans quelques minutes."
  };
  // msgs : historique ; summary : résumé du projet ; mode : "whatsapp" | "form" ; cf : formulaire affiché ; draft : saisie en cours ; nav : page ouverte depuis le chat
  let st = { msgs: [], summary: "", mode: null, cf: false, sent: false, nav: false, draft: {} }, busy = false;

  try { const d = JSON.parse(sessionStorage.getItem(KEY) || "null"); if (d) st = Object.assign(st, d); } catch (e) {}
  const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} };
  const waLink = () => "https://wa.me/" + WA + "?text=" + encodeURIComponent("Bonjour ARélec 👋 Je viens du site." + (st.summary ? "\n" + st.summary : ""));
  const scroll = () => { list.scrollTop = list.scrollHeight; };
  const el = (tag, cls, text) => { const d = document.createElement(tag); if (cls) d.className = cls; if (text != null) d.textContent = text; return d; };

  function bubble(role, text) {
    const d = el("div", "chat-msg " + (role === "user" ? "me" : "bot"), text);
    list.appendChild(d);
    return d;
  }
  function links(items) {
    if (!items?.length) return;
    const wrap = el("div", "chat-links");
    items.forEach(p => {
      if (p.url === location.pathname) return;
      const a = el("a", "chat-link", p.title + " →");
      a.href = p.url;
      // Le panneau reste ouvert sur la page suivante, avec la conversation
      a.addEventListener("click", () => { st.nav = true; save(); });
      wrap.appendChild(a);
    });
    if (wrap.children.length) list.appendChild(wrap);
  }

  function handoff() {
    list.querySelectorAll(".chat-wa,.chat-alt,.chat-cf").forEach(n => n.remove());
    if (st.sent) return;
    if (st.summary && st.mode !== "form") {
      const a = el("a", "chat-wa");
      a.href = waLink(); a.target = "_blank"; a.rel = "noopener";
      a.innerHTML = document.getElementById("chat-wa-ic").innerHTML +
        "<span><b>Continuer sur WhatsApp</b><small>Votre demande est déjà résumée, on prend le relais.</small></span>";
      list.appendChild(a);
    }
    if (st.cf || st.mode === "form") list.appendChild(contactForm());
    else if (st.summary) {
      const b = el("button", "chat-alt", "Pas de WhatsApp ? Laisser mes coordonnées");
      b.type = "button";
      b.addEventListener("click", () => { st.cf = true; save(); handoff(); scroll(); list.querySelector(".chat-cf input")?.focus(); });
      list.appendChild(b);
    }
  }

  function contactForm() {
    const f = el("form", "chat-cf");
    f.noValidate = true;
    f.innerHTML = "<b>On vous recontacte</b><small>Un téléphone ou un email suffit.</small>" +
      '<input name="nom" autocomplete="name" maxlength="80" placeholder="Votre nom" aria-label="Votre nom">' +
      '<input name="tel" type="tel" autocomplete="tel" maxlength="30" placeholder="Téléphone" aria-label="Téléphone">' +
      '<input name="email" type="email" autocomplete="email" maxlength="120" placeholder="Email" aria-label="Email">' +
      '<textarea name="message" maxlength="2000" rows="3" placeholder="Votre projet" aria-label="Votre projet"></textarea>' +
      '<input class="hp" name="site" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<p class="err" role="alert"></p><button type="submit">Envoyer ma demande</button>';
    const d = st.draft || {};
    ["nom", "tel", "email"].forEach(k => { f[k].value = d[k] || ""; });
    f.message.value = d.message || (st.summary || st.msgs.filter(m => m.role === "user").map(m => m.content).join("\n")).replace(/^Mon projet\s*:\s*/i, "");
    f.addEventListener("input", () => { st.draft = { nom: f.nom.value, tel: f.tel.value, email: f.email.value, message: f.message.value }; save(); });
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const err = f.querySelector(".err"), btn = f.querySelector("button");
      err.textContent = "";
      if (!f.nom.value.trim()) { err.textContent = ERR.nom; f.nom.focus(); return; }
      if (!f.tel.value.trim() && !f.email.value.trim()) { err.textContent = ERR.joignable; f.tel.focus(); return; }
      btn.disabled = true; btn.textContent = "Envoi…";
      try {
        const r = await fetch("/api/contact", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ nom: f.nom.value, tel: f.tel.value, email: f.email.value, message: f.message.value, site: f.site.value, source: "chat", page: location.pathname })
        });
        const out = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(out.error || r.status);
        st.sent = true; st.cf = false; st.draft = {};
        st.msgs.push({ role: "assistant", content: SENT });
        save(); f.remove(); list.querySelectorAll(".chat-wa,.chat-alt").forEach(n => n.remove());
        bubble("assistant", SENT); scroll();
      } catch (x) {
        err.textContent = ERR[x.message] || "L'envoi n'a pas fonctionné. Appelez le 02 98 40 20 43 ou écrivez à contact@entreprise-arelec.fr.";
        btn.disabled = false; btn.textContent = "Envoyer ma demande";
      }
    });
    return f;
  }

  function render() {
    list.innerHTML = "";
    bubble("assistant", GREETING);
    st.msgs.forEach(m => { bubble(m.role, m.content); if (m.role === "assistant") links(m.links); });
    handoff();
    sugg.hidden = st.msgs.length > 0;
    scroll();
  }

  function open() {
    if (document.body.classList.contains("menu-open")) document.querySelector(".drawer-close")?.click();
    box.hidden = false;
    document.body.classList.add("chat-open");
    fab.setAttribute("aria-expanded", "true");
    render();
    if (window.matchMedia("(hover: hover)").matches) setTimeout(() => input.focus(), 60);
  }
  function close() {
    box.hidden = true;
    document.body.classList.remove("chat-open");
    fab.setAttribute("aria-expanded", "false");
    fab.focus();
  }

  async function ask(text) {
    text = text.trim().slice(0, MAX);
    if (!text || busy) return;
    busy = true; send.disabled = true; sugg.hidden = true;
    st.msgs.push({ role: "user", content: text }); save();
    bubble("user", text);
    input.value = ""; grow();
    const typing = el("div", "chat-typing");
    typing.innerHTML = "<i></i><i></i><i></i>";
    list.appendChild(typing); scroll();
    try {
      const r = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: st.msgs.slice(-16).map(m => ({ role: m.role, content: m.content })) })
      });
      if (!r.ok) throw new Error(r.status);
      const data = await r.json();
      const reply = (data.reply || "").trim() || FALLBACK;
      const m = { role: "assistant", content: reply };
      if (Array.isArray(data.links) && data.links.length) m.links = data.links;
      st.msgs.push(m);
      if (data.handoff) { st.summary = data.handoff; st.sent = false; }
      if (data.mode === "form") st.mode = "form";
      typing.remove(); bubble("assistant", reply); links(m.links);
    } catch (e) {
      // Sans réponse de l'assistant : WhatsApp avec la demande telle quelle, et le formulaire pour ceux qui n'ont pas WhatsApp
      if (!st.summary) st.summary = "Ma demande : " + st.msgs.filter(m => m.role === "user").map(m => m.content).join(" ").slice(0, 400);
      st.msgs.push({ role: "assistant", content: FALLBACK });
      typing.remove(); bubble("assistant", FALLBACK);
    }
    save();
    handoff();
    scroll();
    busy = false; send.disabled = false;
  }

  function grow() { input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 120) + "px"; }

  fab.addEventListener("click", open);
  box.querySelector(".chat-close").addEventListener("click", close);
  box.addEventListener("keydown", e => { if (e.key === "Escape") close(); });
  sugg.addEventListener("click", e => { const b = e.target.closest("button"); if (b) ask(b.textContent); });
  form.addEventListener("submit", e => { e.preventDefault(); ask(input.value); });
  input.addEventListener("input", grow);
  input.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); ask(input.value); } });
  // Tous les boutons « Prendre contact » ouvrent l'assistant (sans JS : lien vers /contact)
  document.addEventListener("click", e => { const t = e.target.closest("[data-chat]"); if (!t) return; e.preventDefault(); open(); });
  // Retour sur une page après un clic dans le chat : on rouvre là où on en était
  if (st.nav) { st.nav = false; save(); open(); }
})();
