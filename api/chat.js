// Assistant du site ARélec — fonction Vercel (POST /api/chat).
// Variables d'environnement (Vercel > Settings > Environment Variables) :
//   OPENROUTER_API_KEY  (obligatoire)   OPENROUTER_MODEL  (facultatif)
const { complete, takeTag } = require("./_openrouter.js");

const MAX_MSGS = 16, MAX_LEN = 800;
const WINDOW_MS = 10 * 60 * 1000, MAX_HITS = 30;
const hits = new Map(); // limite par IP, au mieux (mémoire de l'instance)

const INSTRUCTIONS = `Tu es l'assistant du site d'ARélec, artisan électricien, chauffagiste et plombier à Plouzané (bassin brestois, Finistère) depuis 2010. Tu réponds aux visiteurs du site en français, au nom de l'entreprise (« on », « nous »).

Ton objectif : répondre clairement aux questions, comprendre le besoin, puis amener le visiteur à continuer la conversation sur WhatsApp, où ARélec prend le relais pour préparer la visite et le devis gratuit.

Consignes :
- Réponses courtes : 2 à 4 phrases.
- Si tu ne sais pas, propose WhatsApp ou le téléphone.
- Pose une seule question à la fois pour comprendre le besoin : type de travaux, commune, urgence ou non, neuf ou rénovation.
- Dès que tu connais le besoin et la commune, ou au plus tard à ta troisième réponse, ou dès que le visiteur parle de devis, prix, rendez-vous ou contact : invite-le à continuer sur WhatsApp, puis termine ton message par une ligne exactement de cette forme :
<<WHATSAPP>>Mon projet : <résumé en une ou deux phrases à la première personne : type de travaux, commune, détails utiles><<END>>
Cette ligne sert à préremplir son message WhatsApp ; ne la mentionne jamais.
- Ne demande pas l'adresse exacte.`;

function limited(ip) {
  const now = Date.now();
  const h = (hits.get(ip) || []).filter(t => now - t < WINDOW_MS);
  h.push(now);
  hits.set(ip, h);
  return h.length > MAX_HITS;
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

  if (!process.env.OPENROUTER_API_KEY) return res.status(503).json({ error: "unconfigured" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = null; } }
  const messages = (Array.isArray(body?.messages) ? body.messages : [])
    .filter(m => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content.trim())
    .slice(-MAX_MSGS)
    .map(m => ({ role: m.role, content: m.content.slice(0, MAX_LEN) }));
  if (!messages.length || messages[messages.length - 1].role !== "user") return res.status(400).json({ error: "messages" });

  try {
    const { text, value } = takeTag(await complete(INSTRUCTIONS, messages), "WHATSAPP");
    return res.status(200).json({ reply: text, handoff: value ? value.slice(0, 500) : null });
  } catch (e) {
    return res.status(502).json({ error: "upstream" });
  }
};
