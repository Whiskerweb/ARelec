// Assistant du site ARélec — copié dans site/assets/js/chat.js par build_site.py.
// Répond via /api/chat (OpenRouter) puis fait basculer le prospect sur WhatsApp,
// avec un message prérempli qui résume sa demande (repris ensuite par l'agent WhatsApp).
(function () {
  const fab = document.querySelector(".chat-fab"), box = document.getElementById("chat");
  if (!fab || !box) return;
  const list = box.querySelector(".chat-msgs"), sugg = box.querySelector(".chat-sugg");
  const form = box.querySelector(".chat-form"), input = form.querySelector("textarea"), send = form.querySelector(".chat-send");
  const WA = box.dataset.wa, KEY = "arelec-chat-v1", MAX = 800;
  const GREETING = "Bonjour 👋 Ici l'assistant d'ARélec. Électricité, chauffage ou plomberie : dites-moi ce que vous avez en tête (travaux, panne, commune) et je vous réponds.";
  const FALLBACK = "Je n'arrive pas à répondre pour le moment. Le plus simple : écrivez-nous sur WhatsApp, on vous répond directement. Ou appelez le 02 98 40 20 43.";
  let msgs = [], summary = "", busy = false;

  try { const d = JSON.parse(sessionStorage.getItem(KEY) || "null"); if (d) { msgs = d.msgs || []; summary = d.summary || ""; } } catch (e) {}
  const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify({ msgs, summary })); } catch (e) {} };
  const waLink = () => "https://wa.me/" + WA + "?text=" + encodeURIComponent("Bonjour ARélec 👋 Je viens du site." + (summary ? "\n" + summary : ""));
  const scroll = () => { list.scrollTop = list.scrollHeight; };

  function bubble(role, text) {
    const d = document.createElement("div");
    d.className = "chat-msg " + (role === "user" ? "me" : "bot");
    d.textContent = text;
    list.appendChild(d);
    return d;
  }
  function waCard() {
    list.querySelector(".chat-wa")?.remove();
    const a = document.createElement("a");
    a.className = "chat-wa"; a.href = waLink(); a.target = "_blank"; a.rel = "noopener";
    a.innerHTML = document.getElementById("chat-wa-ic").innerHTML +
      "<span><b>Continuer sur WhatsApp</b><small>Votre demande est déjà résumée, on prend le relais.</small></span>";
    list.appendChild(a);
  }
  function render() {
    list.innerHTML = "";
    bubble("assistant", GREETING);
    msgs.forEach(m => bubble(m.role, m.content));
    if (summary) waCard();
    sugg.hidden = msgs.length > 0;
    scroll();
  }

  function open() {
    if (document.body.classList.contains("menu-open")) document.querySelector(".mdrawer-close")?.click();
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
    msgs.push({ role: "user", content: text }); save();
    bubble("user", text);
    input.value = ""; grow();
    const typing = document.createElement("div");
    typing.className = "chat-typing"; typing.innerHTML = "<i></i><i></i><i></i>";
    list.appendChild(typing); scroll();
    try {
      const r = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: msgs.slice(-16) })
      });
      if (!r.ok) throw new Error(r.status);
      const data = await r.json();
      const reply = (data.reply || "").trim() || FALLBACK;
      msgs.push({ role: "assistant", content: reply });
      if (data.handoff) summary = data.handoff;
      typing.remove(); bubble("assistant", reply);
    } catch (e) {
      // Sans réponse de l'assistant, on bascule quand même sur WhatsApp avec la demande telle quelle
      if (!summary) summary = "Ma demande : " + msgs.filter(m => m.role === "user").map(m => m.content).join(" ").slice(0, 400);
      msgs.push({ role: "assistant", content: FALLBACK });
      typing.remove(); bubble("assistant", FALLBACK);
    }
    save();
    if (summary) waCard();
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
})();
