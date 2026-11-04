// Formulaire de contact — fonction Vercel (POST /api/contact), utilisée par la page /contact et par l'assistant du site.
// La demande part par email à ARélec :
//   - via Resend si RESEND_API_KEY est défini (CONTACT_FROM = expéditeur sur un domaine vérifié chez Resend) ;
//   - sinon via FormSubmit (aucune clé : la toute première demande envoie un email d'activation à CONTACT_TO, à confirmer une fois).
//     FormSubmit est derrière Cloudflare, qui bloque les appels venant d'un serveur : la fonction valide la demande
//     et renvoie au navigateur de quoi l'envoyer lui-même (champ « relay »).
// CONTACT_TO (facultatif) : destinataire, contact@entreprise-arelec.fr par défaut.
// Si Upstash est branché (voir _store.js), une copie de chaque demande est gardée 90 jours.
const crypto = require("node:crypto");
const store = require("./_store.js");

const TO = process.env.CONTACT_TO || "contact@entreprise-arelec.fr";
const SITE = "https://www.entreprise-arelec.fr";
const METIERS = ["Électricité", "Chauffage", "Plomberie", "Plusieurs / je ne sais pas"];
const WINDOW_MS = 10 * 60 * 1000, MAX_HITS = 8;
const hits = new Map(); // limite par IP, au mieux (mémoire de l'instance)

function limited(ip) {
  const now = Date.now();
  const h = (hits.get(ip) || []).filter(t => now - t < WINDOW_MS);
  h.push(now);
  hits.set(ip, h);
  return h.length > MAX_HITS;
}

const clean = (v, max) => (typeof v === "string" ? v.replace(/\s+\n/g, "\n").trim().slice(0, max) : "");

function validate(b) {
  const d = {
    nom: clean(b.nom, 80),
    tel: clean(b.tel, 30),
    email: clean(b.email, 120),
    commune: clean(b.commune, 80),
    metier: METIERS.includes(b.metier) ? b.metier : "",
    message: clean(b.message, 2000),
    source: b.source === "chat" ? "Assistant du site" : "Formulaire /contact",
    page: clean(b.page, 200)
  };
  if (!d.nom) return { error: "nom" };
  if (!d.tel && !d.email) return { error: "joignable" };
  if (d.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) return { error: "email" };
  if (d.tel && d.tel.replace(/\D/g, "").length < 9) return { error: "tel" };
  if (!d.message) return { error: "message" };
  return { data: d };
}

function asText(d) {
  return [
    `Nom : ${d.nom}`,
    `Téléphone : ${d.tel || "—"}`,
    `Email : ${d.email || "—"}`,
    `Commune : ${d.commune || "—"}`,
    `Travaux : ${d.metier || "—"}`,
    "",
    d.message,
    "",
    `Envoyé depuis : ${d.source}${d.page ? " (" + d.page + ")" : ""}`
  ].join("\n");
}

// ---------- email HTML aux couleurs du site (encre, crème, jaune-vert) ----------
// Tableaux et styles en ligne : c'est ce que Gmail, Outlook et Apple Mail affichent de façon fiable.
const C = { ink: "#121211", cream: "#F3F2EE", lime: "#E3FF4A", line: "#E4E2DC", muted: "#6F6D66", wa: "#1FA952" };
const FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif";
const escH = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
function phone(t) {
  const n = String(t || "").replace(/\D/g, "");
  if (/^0\d{9}$/.test(n)) return { tel: "+33" + n.slice(1), wa: /^0[67]/.test(n) ? "33" + n.slice(1) : null };
  if (/^33\d{9}$/.test(n)) return { tel: "+" + n, wa: /^33[67]/.test(n) ? n : null };
  return n.length >= 9 ? { tel: "+" + n, wa: null } : null;
}
function button(href, label, bg, fg) {
  return `<td style="padding:0 8px 8px 0"><a href="${escH(href)}" style="display:inline-block;padding:13px 20px;border-radius:100px;background:${bg};color:${fg};font:600 14px/1 ${FONT};text-decoration:none;white-space:nowrap">${label}</a></td>`;
}
function asHtml(d, subject) {
  const ph = phone(d.tel);
  const rows = [["Nom", d.nom], ["Téléphone", d.tel], ["Email", d.email], ["Commune", d.commune], ["Travaux", d.metier]]
    .filter(([, v]) => v)
    .map(([k, v], i) => `<tr><td style="padding:12px 16px;${i ? `border-top:1px solid ${C.line};` : ""}font:13px/1.4 ${FONT};color:${C.muted};width:110px;vertical-align:top">${k}</td>` +
      `<td style="padding:12px 16px;${i ? `border-top:1px solid ${C.line};` : ""}font:500 15px/1.4 ${FONT};color:${C.ink}">${escH(v)}</td></tr>`).join("");
  const btns = [
    ph && button("tel:" + ph.tel, "Appeler " + escH(d.tel), C.lime, C.ink),
    ph && ph.wa && button("https://wa.me/" + ph.wa, "WhatsApp", C.wa, "#ffffff"),
    d.email && button("mailto:" + d.email + "?subject=" + encodeURIComponent("Votre demande à ARélec"), "Répondre par email", C.ink, "#ffffff")
  ].filter(Boolean).join("");
  const page = d.page ? `<a href="${SITE}${escH(d.page)}" style="color:${C.muted}">${escH(d.page)}</a>` : "";
  return `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light only"><title>${escH(subject)}</title></head>
<body style="margin:0;padding:0;background:${C.cream}">
<div style="display:none;max-height:0;overflow:hidden">${escH((d.metier ? d.metier + " · " : "") + (d.commune ? d.commune + " · " : "") + d.message.slice(0, 90))}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.cream}"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px">
<tr><td style="background:${C.ink};border-radius:24px 24px 0 0;padding:22px 28px">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
  <td><img src="${SITE}/assets/img/logo.png" width="96" alt="ARélec" style="display:block;border:0;width:96px;height:auto"></td>
  <td align="right"><span style="display:inline-block;padding:7px 12px;border-radius:100px;background:${C.lime};color:${C.ink};font:600 12px/1 ${FONT};letter-spacing:.02em">NOUVELLE DEMANDE</span></td>
  </tr></table></td></tr>
<tr><td style="background:#ffffff;padding:30px 28px 8px">
  <h1 style="margin:0 0 6px;font:500 26px/1.2 ${FONT};color:${C.ink};letter-spacing:-.02em">${escH(d.nom)}</h1>
  <p style="margin:0 0 22px;font:14px/1.5 ${FONT};color:${C.muted}">Demande reçue via ${escH(d.source.toLowerCase())}${d.commune ? " · " + escH(d.commune) : ""}</p>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.cream};border-radius:16px">${rows}</table>
  <p style="margin:24px 0 8px;font:600 12px/1 ${FONT};color:${C.muted};letter-spacing:.06em">SON PROJET</p>
  <div style="padding:16px 18px;border-left:3px solid ${C.lime};background:${C.cream};border-radius:0 12px 12px 0;font:15px/1.6 ${FONT};color:${C.ink};white-space:pre-wrap">${escH(d.message)}</div>
  <table role="presentation" cellpadding="0" cellspacing="0" style="margin:24px 0 14px"><tr>${btns}</tr></table>
</td></tr>
<tr><td style="background:${C.ink};border-radius:0 0 24px 24px;padding:18px 28px;font:12px/1.6 ${FONT};color:rgba(255,255,255,.6)">
  Envoyé depuis <a href="${SITE}" style="color:${C.lime};text-decoration:none">entreprise-arelec.fr</a>${page ? " · page " + page.replace(`color:${C.muted}`, "color:rgba(255,255,255,.75)") : ""}<br>Rappeler sous 24 à 48 h, comme annoncé sur le site.
</td></tr>
</table></td></tr></table></body></html>`;
}

async function viaResend(d, subject) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: process.env.CONTACT_FROM || "Site ARélec <site@entreprise-arelec.fr>",
      to: [TO], subject, html: asHtml(d, subject), text: asText(d), ...(d.email ? { reply_to: d.email } : {})
    }),
    signal: AbortSignal.timeout(10000)
  });
  if (!r.ok) throw new Error("Resend " + r.status);
}

// Demande prête à être envoyée à FormSubmit par le navigateur du visiteur
function formSubmitRelay(d, subject) {
  return {
    url: `https://formsubmit.co/ajax/${encodeURIComponent(TO)}`,
    body: {
      _subject: subject, _template: "table", _captcha: "false",
      Nom: d.nom, "Téléphone": d.tel || "—", Commune: d.commune || "—", Travaux: d.metier || "—",
      Message: d.message, Source: d.source + (d.page ? " (" + d.page + ")" : ""),
      ...(d.email ? { email: d.email, _replyto: d.email } : {})
    }
  };
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return res.status(405).json({ error: "method" }); }

  const origin = req.headers.origin;
  if (origin) {
    let same = false;
    try { same = new URL(origin).host === req.headers.host; } catch (e) {}
    if (!same) return res.status(403).json({ error: "origin" });
  }
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "local";
  if (limited(ip)) return res.status(429).json({ error: "rate" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = null; } }
  if (!body || typeof body !== "object") return res.status(400).json({ error: "body" });
  // Champ piège invisible : rempli = robot. On répond « ok » sans rien envoyer.
  if (clean(body.site, 200)) return res.status(200).json({ ok: true });

  const { data, error } = validate(body);
  if (error) return res.status(400).json({ error });

  const subject = `Demande site ARélec — ${data.nom}${data.commune ? " (" + data.commune + ")" : ""}`;
  if (store.persistent) {
    const id = new Date().toISOString().slice(0, 19) + "-" + crypto.randomBytes(3).toString("hex");
    await store.set("contact:" + id, { ...data, at: Date.now() }, 90 * 24 * 3600).catch(() => {});
  }
  if (!process.env.RESEND_API_KEY) return res.status(200).json({ ok: true, relay: formSubmitRelay(data, subject) });
  try {
    await viaResend(data, subject);
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error("contact:", e.message);
    return res.status(502).json({ error: "send" });
  }
};

// Pour l'aperçu et l'email de test (scripts locaux)
module.exports.asHtml = asHtml;
module.exports.asText = asText;
