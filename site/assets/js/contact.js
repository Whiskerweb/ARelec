// Formulaire de la page /contact — copié dans site/assets/js/contact.js par build_site.py.
// Envoie la demande à /api/contact ; en cas d'échec, propose l'email et le téléphone.
// Si le visiteur a déjà décrit son projet à l'assistant, le message est prérempli avec son résumé.
(function () {
  const f = document.getElementById("cform");
  if (!f) return;
  const btn = f.querySelector('button[type="submit"]'), status = f.querySelector(".cform-status");
  const label = btn.lastChild, LABEL = label.textContent;
  const MAIL = f.dataset.mail, PHONE = f.dataset.phone;
  const ERR = {
    nom: "Indiquez votre nom.",
    joignable: "Laissez un téléphone ou un email pour qu'on puisse vous répondre.",
    email: "L'adresse email ne semble pas valide.",
    tel: "Le numéro de téléphone ne semble pas complet.",
    message: "Décrivez votre demande en quelques mots.",
    rate: "Trop d'envois d'affilée. Réessayez dans quelques minutes."
  };

  try {
    const d = JSON.parse(sessionStorage.getItem("arelec-chat-v1") || "null");
    if (d?.summary && !f.message.value) f.message.value = d.summary.replace(/^Mon projet\s*:\s*/i, "");
  } catch (e) {}

  function say(text, ok) {
    status.hidden = !text;
    status.className = "cform-status" + (ok ? " ok" : "");
    status.innerHTML = text;
  }

  // Sans Resend, le serveur valide puis c'est le navigateur qui transmet à FormSubmit (bloqué depuis un serveur)
  async function relay(out) {
    if (!out.relay) return;
    const r = await fetch(out.relay.url, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(out.relay.body), signal: AbortSignal.timeout(12000) });
    const o = await r.json().catch(() => ({}));
    if (!r.ok || String(o.success) !== "true") throw new Error("relay");
  }

  f.addEventListener("submit", async e => {
    e.preventDefault();
    if (!f.tel.value.trim() && !f.email.value.trim()) { say(ERR.joignable); f.tel.focus(); return; }
    btn.disabled = true; say(""); label.textContent = "Envoi en cours…";
    const data = Object.fromEntries(new FormData(f));
    data.page = location.pathname;
    try {
      const r = await fetch("/api/contact/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data), signal: AbortSignal.timeout(12000) });
      const out = await r.json().catch(() => ({}));
      if (r.ok) {
        await relay(out);
        f.classList.add("sent");
        f.innerHTML = '<div class="cform-done"><b>Merci, c\'est envoyé.</b><p>On revient vers vous sous 24 à 48 h pour préciser le besoin et caler la visite gratuite.</p></div>';
        try { sessionStorage.removeItem("arelec-chat-v1"); } catch (e) {}
        return;
      }
      if (ERR[out.error]) { say(ERR[out.error]); btn.disabled = false; label.textContent = LABEL; return; }
      throw new Error(out.error || r.status);
    } catch (err) {
      say(`L'envoi n'a pas fonctionné. Écrivez-nous à <a href="mailto:${MAIL}">${MAIL}</a> ou appelez le <a href="tel:${PHONE.replace(/\s/g, "")}">${PHONE}</a>.`);
      btn.disabled = false; label.textContent = LABEL;
    }
  });
})();
