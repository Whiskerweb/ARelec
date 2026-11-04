// Assistant du site ARélec — fonction Vercel (POST /api/chat).
// Variables d'environnement (Vercel > Settings > Environment Variables) :
//   OPENROUTER_API_KEY  (obligatoire)   OPENROUTER_MODEL  (facultatif)
const { complete, takeTag } = require("./_openrouter.js");
const { PAGES } = require("./_pages.js");
const KNOWN = new Map(PAGES.map(p => [p.url, p.title]));

const MAX_MSGS = 16, MAX_LEN = 800;
const WINDOW_MS = 10 * 60 * 1000, MAX_HITS = 30;
const hits = new Map(); // limite par IP, au mieux (mémoire de l'instance)

const INSTRUCTIONS = `Tu es l'assistant du site d'ARélec, artisan électricien, chauffagiste et plombier à Plouzané (bassin brestois, Finistère) depuis 2010. Tu réponds aux visiteurs du site en français, au nom de l'entreprise (« on », « nous »).

Ton objectif : répondre clairement aux questions, guider le visiteur vers les bonnes pages du site, comprendre son besoin, puis l'amener à transmettre sa demande : sur WhatsApp, où ARélec prend le relais pour préparer la visite et le devis gratuit, ou par le formulaire de contact s'il n'a pas WhatsApp.

Consignes :
- Réponses courtes : 2 à 4 phrases.
- Si tu ne sais pas, propose WhatsApp ou le téléphone.
- Pose une seule question à la fois pour comprendre le besoin : type de travaux, commune, urgence ou non, neuf ou rénovation.
- Dès que tu connais le besoin et la commune, ou au plus tard à ta troisième réponse, ou dès que le visiteur parle de devis, prix, rendez-vous ou contact : invite-le à continuer sur WhatsApp (ou par le formulaire, juste en dessous, s'il n'a pas WhatsApp), puis termine ton message par une ligne exactement de cette forme :
<<WHATSAPP>>Mon projet : <résumé en une ou deux phrases à la première personne : type de travaux, commune, détails utiles><<END>>
- Si le visiteur dit qu'il n'a pas WhatsApp, préfère l'email, le formulaire ou être rappelé : dis-lui que le formulaire s'affiche juste en dessous (nom, téléphone ou email), puis termine par la même ligne résumé mais avec <<FORMULAIRE>> à la place de <<WHATSAPP>>.
Ces lignes servent à préremplir sa demande ; ne les mentionne jamais.
- Navigation : quand une page du site répond à sa question (un métier, sa commune, les réalisations, les avis, l'entreprise, le contact), propose-la. Ajoute alors, sur la toute dernière ligne, au plus 2 adresses de la liste ci-dessous, exactement sous cette forme :
<<PAGES>>/chauffage/ /chauffagiste-brest/<<END>>
Le site les affiche en boutons cliquables ; n'écris jamais d'adresse dans ta phrase. Pour une commune, préfère la page « métier à commune » si elle existe.
- Ne demande pas l'adresse exacte.

Pages du site (adresse · titre) :
${PAGES.map(p => p.url + " · " + p.title).join("\n")}`;

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
    const raw = await complete(INSTRUCTIONS, messages);
    const pages = takeTag(raw, "PAGES");
    const wa = takeTag(pages.text, "WHATSAPP");
    const form = takeTag(wa.text, "FORMULAIRE");
    const summary = form.value || wa.value;
    // On ne garde que des pages qui existent vraiment sur le site
    const links = [...new Set(String(pages.value || "").match(/\/[a-z0-9-]*\/?/g) || [])]
      .map(u => (u.endsWith("/") ? u : u + "/")).filter(u => KNOWN.has(u)).slice(0, 2)
      .map(u => ({ url: u, title: KNOWN.get(u) }));
    return res.status(200).json({
      reply: form.text, links,
      handoff: summary ? summary.slice(0, 500) : null,
      mode: form.value ? "form" : summary ? "whatsapp" : null
    });
  } catch (e) {
    return res.status(502).json({ error: "upstream" });
  }
};
