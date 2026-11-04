// Formulaire de contact — fonction Vercel (POST /api/contact), utilisée par la page /contact et par l'assistant du site.
// La demande part par email à ARélec :
//   - via Resend si RESEND_API_KEY est défini (CONTACT_FROM = expéditeur sur un domaine vérifié chez Resend) ;
//   - sinon via FormSubmit (aucune clé : la toute première demande envoie un email d'activation à CONTACT_TO, à confirmer une fois).
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

async function viaResend(d, subject) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: process.env.CONTACT_FROM || "Site ARélec <site@entreprise-arelec.fr>",
      to: [TO], subject, text: asText(d), ...(d.email ? { reply_to: d.email } : {})
    }),
    signal: AbortSignal.timeout(10000)
  });
  if (!r.ok) throw new Error("Resend " + r.status);
}

async function viaFormSubmit(d, subject) {
  const r = await fetch(`https://formsubmit.co/ajax/${encodeURIComponent(TO)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json", Origin: SITE, Referer: SITE + "/contact/" },
    body: JSON.stringify({
      _subject: subject, _template: "table", _captcha: "false",
      Nom: d.nom, "Téléphone": d.tel || "—", Commune: d.commune || "—", Travaux: d.metier || "—",
      Message: d.message, Source: d.source + (d.page ? " (" + d.page + ")" : ""),
      ...(d.email ? { email: d.email, _replyto: d.email } : {})
    }),
    signal: AbortSignal.timeout(10000)
  });
  const raw = await r.text();
  let out = {};
  try { out = JSON.parse(raw); } catch (e) {}
  // Tant que le lien d'activation reçu par email n'a pas été cliqué, FormSubmit refuse l'envoi (message « needs Activation »)
  if (!r.ok || String(out.success) !== "true") throw new Error("FormSubmit " + r.status + " " + (out.message || raw.slice(0, 200)));
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
  try {
    await (process.env.RESEND_API_KEY ? viaResend : viaFormSubmit)(data, subject);
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error("contact:", e.message);
    return res.status(502).json({ error: "send" });
  }
};
