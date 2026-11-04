// Agent WhatsApp ARélec — webhook WhatsApp Cloud API : GET /api/whatsapp (vérification Meta), POST (messages).
// Deux branchements possibles, même format de messages :
//   - via 360dialog (prestataire, numéro en coexistence) : D360_API_KEY + WHATSAPP_WEBHOOK_KEY
//   - via Meta en direct : WHATSAPP_TOKEN + WHATSAPP_PHONE_NUMBER_ID (+ WHATSAPP_APP_SECRET)
// Il reprend la conversation commencée sur le site, qualifie la demande, puis passe la main à Arnaud
// avec une fiche prospect. Mise en service : docs/agent-whatsapp.md.
const crypto = require("node:crypto");
const { complete, takeTag } = require("./_openrouter.js");
const store = require("./_store.js");

const D360_KEY = process.env.D360_API_KEY;
const GRAPH = `https://graph.facebook.com/${process.env.WHATSAPP_GRAPH_VERSION || "v23.0"}`;
const PHONE_ID = process.env.WHATSAPP_PHONE_NUMBER_ID;
const TOKEN = process.env.WHATSAPP_TOKEN;
const WEBHOOK_KEY = process.env.WHATSAPP_WEBHOOK_KEY;      // secret partagé avec 360dialog (en-tête X-Arelec-Key)
const NOTIFY = process.env.ARELEC_NOTIFY_WA;               // n° perso d'Arnaud (format 336…), facultatif
const NOTIFY_TEMPLATE = process.env.ARELEC_NOTIFY_TEMPLATE; // modèle Meta à 1 variable, facultatif
const CONV_TTL = 30 * 24 * 3600, PAUSE_MS = 48 * 3600 * 1000, MAX_HISTORY = 24;

const INSTRUCTIONS = `Tu es l'agent WhatsApp d'ARélec, artisan électricien, chauffagiste et plombier à Plouzané (bassin brestois, Finistère) depuis 2010. Tu écris au nom de l'entreprise (« on », « nous ») à un client qui vient souvent du site : son premier message contient alors « Mon projet : … ». Ne repose jamais une question à laquelle il a déjà répondu.

Ton objectif : préparer la visite gratuite sur place en rassemblant, une question à la fois :
1. le type de travaux et ce qu'il faut faire (description concrète) ;
2. la commune ;
3. neuf ou rénovation, et s'il y a une urgence ;
4. des photos si c'est utile (tableau électrique, chaudière, fuite, pièce à refaire…) — elles sont les bienvenues mais pas obligatoires ;
5. ses disponibilités pour une visite (jours, créneaux) ;
6. son nom.

Consignes :
- Style WhatsApp : 1 à 3 phrases courtes, chaleureuses, une seule question par message. Pas de formule de politesse à rallonge. Texte simple, sans markdown ni listes.
- Ne propose jamais de date ni d'heure précise : c'est Arnaud qui confirme le rendez-vous.
- Quand tu as au moins le besoin, la commune et ses disponibilités (le nom si possible), ou si le client demande à parler à quelqu'un, ou s'il y a une urgence : dis-lui qu'Arnaud a tout reçu et revient vers lui rapidement pour caler la visite, puis termine ton message par une fiche exactement de cette forme :
<<FICHE>>Nom : … | Travaux : … | Commune : … | Neuf/réno : … | Urgence : oui/non | Disponibilités : … | Photos : oui/non | Remarques : …<<END>>
Mets « ? » pour ce qui manque. Cette fiche est transmise à Arnaud ; ne la mentionne jamais.
- Après la fiche, si le client écrit encore, réponds simplement qu'Arnaud a sa demande et va le recontacter.
- Un message entre crochets (ex. « [photo] ») décrit un média reçu : remercie, tu ne vois pas son contenu.`;

// ---------- envoi (360dialog ou Graph API) ----------
async function graph(body) {
  const [url, auth] = D360_KEY
    ? ["https://waba-v2.360dialog.io/messages", { "D360-API-KEY": D360_KEY }]
    : [`${GRAPH}/${PHONE_ID}/messages`, { Authorization: `Bearer ${TOKEN}` }];
  const r = await fetch(url, {
    method: "POST",
    headers: { ...auth, "Content-Type": "application/json" },
    body: JSON.stringify({ messaging_product: "whatsapp", ...body }),
    signal: AbortSignal.timeout(10000)
  });
  if (!r.ok) throw new Error("Graph " + r.status + " " + (await r.text()).slice(0, 300));
  return r.json();
}
const sendText = (to, text) => graph({ to, type: "text", text: { body: text.slice(0, 4000) } });
const markRead = id => graph({ status: "read", message_id: id, typing_indicator: { type: "text" } }).catch(() => {});

async function notifyArnaud(waId, profileName, fiche) {
  if (!NOTIFY) return;
  const line = `Nouveau prospect WhatsApp — +${waId}${profileName ? " (" + profileName + ")" : ""} — ${fiche}`;
  if (NOTIFY_TEMPLATE) {
    // Un message libre n'arrive que si Arnaud a écrit au numéro pro dans les 24 h ; le modèle passe toujours.
    return graph({
      to: NOTIFY, type: "template",
      template: { name: NOTIFY_TEMPLATE, language: { code: "fr" }, components: [{ type: "body", parameters: [{ type: "text", text: line.replace(/\s*\n\s*/g, " · ").slice(0, 1000) }] }] }
    });
  }
  return sendText(NOTIFY, line);
}

// ---------- messages entrants ----------
function describe(msg) {
  switch (msg.type) {
    case "text": return msg.text?.body || "";
    case "image": return "[photo]" + (msg.image?.caption ? " " + msg.image.caption : "");
    case "video": return "[vidéo]" + (msg.video?.caption ? " " + msg.video.caption : "");
    case "document": return "[document]" + (msg.document?.caption ? " " + msg.document.caption : "");
    case "audio": return "[message vocal, non écouté — demande gentiment de l'écrire si c'est important, Arnaud l'écoutera]";
    case "location": return `[localisation : ${msg.location?.name || ""} ${msg.location?.address || ""}]`.trim();
    case "button": return msg.button?.text || "";
    case "interactive": return msg.interactive?.button_reply?.title || msg.interactive?.list_reply?.title || "";
    default: return "";
  }
}

async function handleMessage(msg, contact) {
  if (!(await store.once("wa:seen:" + msg.id, 3 * 24 * 3600))) return; // Meta renvoie parfois le même événement
  const waId = msg.from;
  const key = "wa:conv:" + waId;
  const conv = (await store.get(key)) || { msgs: [], status: "bot", since: Date.now() };
  const text = describe(msg).slice(0, 1500);
  if (!text) return;
  conv.msgs.push({ role: "user", content: text });
  conv.msgs = conv.msgs.slice(-MAX_HISTORY);

  // Arnaud a pris la main depuis l'app (écho de son message) : l'agent se tait pendant la pause.
  if (conv.status === "human" && Date.now() < (conv.until || 0)) { await store.set(key, conv, CONV_TTL); return; }
  if (conv.status === "human") conv.status = "bot";

  markRead(msg.id);
  let reply;
  try {
    const out = takeTag(await complete(INSTRUCTIONS, conv.msgs, 400), "FICHE");
    reply = out.text;
    if (out.value && !conv.fiche) {
      conv.fiche = out.value;
      conv.status = "handed";
      await notifyArnaud(waId, contact?.profile?.name, out.value).catch(e => console.error("notify", e.message));
    }
  } catch (e) {
    console.error("agent", e.message);
    reply = "Merci pour votre message ! Arnaud vous répond dès que possible. En cas d'urgence : 02 98 40 20 43.";
  }
  if (reply) {
    await sendText(waId, reply);
    conv.msgs.push({ role: "assistant", content: reply });
  }
  await store.set(key, conv, CONV_TTL);
}

// Message envoyé par Arnaud depuis l'app WhatsApp Business (mode coexistence) → pause de l'agent.
async function handleEcho(echo) {
  const key = "wa:conv:" + echo.to;
  const conv = (await store.get(key)) || { msgs: [], since: Date.now() };
  conv.status = "human";
  conv.until = Date.now() + PAUSE_MS;
  const text = echo.type === "text" ? echo.text?.body : `[${echo.type}]`;
  if (text) conv.msgs = [...conv.msgs, { role: "assistant", content: "(Arnaud) " + text }].slice(-MAX_HISTORY);
  await store.set(key, conv, CONV_TTL);
}

// ---------- handler ----------
// Ne jamais lire req.body ici : sur Vercel il est parsé à la demande et le texte brut (signé) serait perdu.
async function rawBody(req) {
  if (typeof req.rawBody === "string") return req.rawBody; // dev-server.mjs
  let raw = "";
  for await (const c of req) raw += c;
  return raw;
}

const same = (x, y) => { const a = Buffer.from(String(x || "")), b = Buffer.from(String(y)); return a.length === b.length && crypto.timingSafeEqual(a, b); };

function signed(req, raw) {
  // 360dialog ne signe pas les webhooks : il renvoie l'en-tête secret qu'on lui a donné (scripts/setup-360dialog.mjs).
  if (D360_KEY) return !!WEBHOOK_KEY && same(req.headers["x-arelec-key"], WEBHOOK_KEY);
  const secret = process.env.WHATSAPP_APP_SECRET;
  if (!secret) return true; // conseillé en production : voir docs/agent-whatsapp.md
  return same(req.headers["x-hub-signature-256"], "sha256=" + crypto.createHmac("sha256", secret).update(raw, "utf8").digest("hex"));
}

module.exports = async (req, res) => {
  if (req.method === "GET") {
    const q = new URL(req.url, "http://x").searchParams;
    if (q.get("hub.mode") === "subscribe" && process.env.WHATSAPP_VERIFY_TOKEN && q.get("hub.verify_token") === process.env.WHATSAPP_VERIFY_TOKEN) {
      res.statusCode = 200; return res.end(q.get("hub.challenge") || "");
    }
    res.statusCode = 403; return res.end();
  }
  if (req.method !== "POST") { res.statusCode = 405; return res.end(); }

  const raw = await rawBody(req);
  if (!signed(req, raw)) { res.statusCode = 401; return res.end(); }
  if (!D360_KEY && (!PHONE_ID || !TOKEN)) { res.statusCode = 503; return res.end(); }

  let payload;
  try { payload = JSON.parse(raw); } catch (e) { res.statusCode = 400; return res.end(); }

  // On traite avant de répondre 200 : sur Vercel, la fonction s'arrête dès la réponse envoyée.
  for (const entry of payload.entry || []) {
    for (const change of entry.changes || []) {
      const v = change.value || {};
      try {
        if (change.field === "messages" && (!PHONE_ID || v.metadata?.phone_number_id === PHONE_ID)) {
          for (const msg of v.messages || []) {
            await handleMessage(msg, (v.contacts || []).find(c => c.wa_id === msg.from));
          }
        } else if (change.field === "smb_message_echoes") {
          for (const echo of v.message_echoes || []) await handleEcho(echo);
        }
      } catch (e) {
        console.error("webhook", e.message);
      }
    }
  }
  res.statusCode = 200;
  res.end("ok");
};
