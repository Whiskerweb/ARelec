// Assistant du site ARélec — fonction Vercel (POST /api/chat).
// Variables d'environnement (Vercel > Settings > Environment Variables) :
//   OPENROUTER_API_KEY  (obligatoire)   OPENROUTER_MODEL  (facultatif)
// Réponse en flux NDJSON : des lignes {"d":"<morceau de texte>"} pendant l'écriture,
// puis une dernière ligne {"done":true, reply, links, handoff, mode}.
const { stream, takeTag } = require("./_openrouter.js");
const { PAGES } = require("./_pages.js");
const { SOURCES } = require("./_sources.js");
const KNOWN = new Map(PAGES.map(p => [p.url, p.title]));
const SRC = new Map(SOURCES.map(x => [x.id, x]));

const MAX_MSGS = 16, MAX_LEN = 800;
const WINDOW_MS = 10 * 60 * 1000, MAX_HITS = 30;
const hits = new Map(); // limite par IP, au mieux (mémoire de l'instance)

const INSTRUCTIONS = `Tu es l'assistant du site d'ARélec, artisan électricien, chauffagiste et plombier à Plouzané (bassin brestois, Finistère) depuis 2010. Tu réponds dans une petite fenêtre de chat, en français, au nom de l'équipe (« on », « nous »), en vouvoyant le visiteur.

Ton objectif : répondre à la question, guider vers la bonne page du site, comprendre le besoin, puis faire transmettre la demande : sur WhatsApp, où Arnaud prend le relais pour la visite et le devis gratuit, ou par le formulaire de contact pour ceux qui n'ont pas WhatsApp.

Comment tu écris (c'est le plus important) :
- Très court. 1 ou 2 phrases, 35 mots maximum en tout. Une seule question à la fois, à la fin.
- Tu parles comme un artisan au téléphone : simple, direct, chaleureux. Des mots de tous les jours. Tu peux commencer par « Oui », « Ah », « D'accord », « Bien sûr » ou entrer directement dans le sujet.
- Mets en gras avec **deux astérisques** l'information clé de ta réponse (un mot ou trois, pas plus, et pas à chaque message). Jamais d'astérisque seul, jamais de titre.
- Une liste à tirets seulement si le visiteur demande de comparer des options, 3 lignes maximum.
- Interdit : « Parfait ! », « Excellente question », « Super ! », « N'hésitez pas », « Je comprends tout à fait », « Absolument », « En effet », « Il est important de noter », « Que ce soit… ou… », les tirets longs (—), les points d'exclamation en rafale, les émojis, les formules de fin du type « Je reste à votre disposition ». Pas de compliments sur la question. Ne répète pas ce que le visiteur vient de dire.
- Varie tes tournures d'un message à l'autre. Pas de structure en trois éléments.

Déroulé :
- Pour comprendre le besoin : type de travaux, commune, urgence ou non, neuf ou rénovation. Une question par message, et jamais une question à laquelle il a déjà répondu.
- Dès que tu connais le besoin et la commune, ou au plus tard à ta troisième réponse, ou dès qu'il parle de devis, prix, rendez-vous ou contact : propose-lui de continuer sur WhatsApp (ou le formulaire juste en dessous s'il n'a pas WhatsApp), puis termine par une ligne exactement de cette forme :
<<WHATSAPP>>Mon projet : <résumé en une ou deux phrases à la première personne : type de travaux, commune, détails utiles><<END>>
- S'il dit qu'il n'a pas WhatsApp, préfère l'email, le formulaire ou être rappelé : dis-lui que le formulaire est juste en dessous (son nom, un téléphone ou un email suffit), puis termine par la même ligne avec <<FORMULAIRE>> à la place de <<WHATSAPP>>.
Ces lignes servent à préremplir sa demande ; ne les mentionne jamais.
- Navigation : quand une page du site répond à sa question (un métier, sa commune, les réalisations, les avis, l'entreprise, le contact), dis-le en quelques mots (« je vous mets la page juste en dessous ») et ajoute sur la toute dernière ligne au plus 2 adresses de la liste ci-dessous, exactement sous cette forme :
<<PAGES>>/chauffage/ /chauffagiste-brest/<<END>>
Le site les affiche en boutons ; n'écris jamais d'adresse dans ta phrase. Pour une commune, préfère la page « métier à commune » si elle existe.
- Ne demande pas l'adresse exacte.
- Source (obligatoire) : dès que ta réponse affirme un fait sur ARélec (ce qu'on fait ou ne fait pas, la zone, les délais, les garanties, la façon de travailler…), cherche dans les « Extraits du site » ci-dessous celui qui le dit et ajoute sur la toute dernière ligne son identifiant, exactement sous cette forme (un seul, le plus précis) :
<<SOURCE>>S12<<END>>
Le site affiche alors un petit lien « Source » qui emmène le visiteur à ce passage. Pas de source seulement si aucun extrait ne dit ce que tu affirmes, ou si ta réponse n'est qu'une question.
- N'ajoute aucun argument qui n'est pas écrit dans les informations (pas de « c'est moins cher », « plus écologique », « plus rapide »…).

Exemples du ton attendu :
Visiteur : vous faites les pompes à chaleur ?
Toi : Oui, on pose des **PAC air/eau et air/air** dans tout le bassin brestois. C'est pour remplacer un chauffage existant ou pour du neuf ?
Visiteur : vous pouvez remplacer ma chaudière fioul par une neuve ?
Toi : Non, on n'installe **ni gaz ni fioul**. On travaille sur l'électricité et la pompe à chaleur. Vous voulez qu'on regarde une PAC à la place ?
<<SOURCE>>(identifiant de l'extrait qui dit qu'ARélec n'installe pas de gaz ni de fioul)<<END>>
Visiteur : mon disjoncteur saute tout le temps
Toi : Ça arrive souvent avec un appareil en défaut ou un circuit surchargé. Ça saute quand vous allumez quelque chose en particulier ?

Pages du site (adresse · titre) :
${PAGES.map(p => p.url + " · " + p.title).join("\n")}

Extraits du site (identifiant · page · texte) :
${SOURCES.map(x => x.id + " · " + x.page + " · " + x.text).join("\n")}`;

function limited(ip) {
  const now = Date.now();
  const h = (hits.get(ip) || []).filter(t => now - t < WINDOW_MS);
  h.push(now);
  hits.set(ip, h);
  return h.length > MAX_HITS;
}

// Sépare la réponse visible des lignes techniques (<<PAGES>>, <<WHATSAPP>>, <<FORMULAIRE>>)
function finish(raw) {
  const src = takeTag(raw, "SOURCE");
  const pages = takeTag(src.text, "PAGES");
  const wa = takeTag(pages.text, "WHATSAPP");
  const form = takeTag(wa.text, "FORMULAIRE");
  const summary = form.value || wa.value;
  // On ne garde que des pages qui existent vraiment sur le site
  const links = [...new Set(String(pages.value || "").match(/\/[a-z0-9-]*\/?/g) || [])]
    .map(u => (u.endsWith("/") ? u : u + "/")).filter(u => KNOWN.has(u)).slice(0, 2)
    .map(u => ({ url: u, title: KNOWN.get(u) }));
  // Source : l'extrait cité, avec le début de son texte pour retrouver l'endroit exact sur la page
  const hit = SRC.get(String(src.value || "").match(/S\d+/)?.[0]);
  const words = hit ? hit.text.split(" ") : [];
  const source = hit ? { url: hit.url, page: hit.page, quote: words.slice(0, 9).join(" ") } : null;
  return {
    done: true, reply: form.text, links, source,
    handoff: summary ? summary.slice(0, 500) : null,
    mode: form.value ? "form" : summary ? "whatsapp" : null
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

  if (!process.env.OPENROUTER_API_KEY) return res.status(503).json({ error: "unconfigured" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = null; } }
  const messages = (Array.isArray(body?.messages) ? body.messages : [])
    .filter(m => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content.trim())
    .slice(-MAX_MSGS)
    .map(m => ({ role: m.role, content: m.content.slice(0, MAX_LEN) }));
  if (!messages.length || messages[messages.length - 1].role !== "user") return res.status(400).json({ error: "messages" });

  let started = false;
  try {
    const raw = await stream(INSTRUCTIONS, messages, d => {
      if (!started) {
        started = true;
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/x-ndjson; charset=utf-8");
      }
      res.write(JSON.stringify({ d }) + "\n");
    }, 260);
    if (!started) { res.statusCode = 200; res.setHeader("Content-Type", "application/x-ndjson; charset=utf-8"); }
    res.end(JSON.stringify(finish(raw)) + "\n");
  } catch (e) {
    if (started) return res.end(JSON.stringify({ error: "upstream" }) + "\n");
    return res.status(502).json({ error: "upstream" });
  }
};
