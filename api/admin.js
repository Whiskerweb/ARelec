// Espace admin d'ARélec — fonction Vercel unique : /api/admin?a=<action>
// Les modifications (photos, emplacements, textes) sont enregistrées dans le dépôt GitHub
// (content/admin.json + assets/uploads/) en un seul commit ; Vercel reconstruit alors le site (~1 min).
// Variables d'environnement :
//   ADMIN_PASSWORD  mot de passe de l'espace admin (obligatoire)
//   GITHUB_TOKEN    jeton GitHub « fine-grained », droit Contents en lecture/écriture sur le dépôt (obligatoire)
//   GITHUB_REPO     facultatif, « Whiskerweb/ARelec » par défaut ; GITHUB_BRANCH facultatif, « main » par défaut
const crypto = require("node:crypto");

const REPO = process.env.GITHUB_REPO || "Whiskerweb/ARelec";
const BRANCH = process.env.GITHUB_BRANCH || "main";
const DATA_PATH = "content/admin.json";
const COOKIE = "arelec_admin", SESSION_S = 7 * 24 * 3600;
const CATEGORIES = ["Rénovation", "Salle de bain", "Électricité", "Éclairage", "Chauffage", "Plomberie", "Extérieur"];
const MAX_IMG = 4 * 1024 * 1024;
const hits = new Map(); // tentatives de connexion par IP (mémoire de l'instance)

// ---------- session : cookie signé (expiration + HMAC dérivé du mot de passe) ----------
const secret = () => crypto.createHash("sha256").update("arelec-admin:" + (process.env.ADMIN_PASSWORD || "")).digest();
const sign = v => crypto.createHmac("sha256", secret()).update(v).digest("base64url");
function session(req) {
  const c = String(req.headers.cookie || "").split(/;\s*/).find(x => x.startsWith(COOKIE + "="));
  if (!c || !process.env.ADMIN_PASSWORD) return false;
  const [exp, mac] = c.slice(COOKIE.length + 1).split(".");
  if (!exp || !mac || Number(exp) < Date.now() / 1000) return false;
  const good = Buffer.from(sign(exp)), got = Buffer.from(mac);
  return good.length === got.length && crypto.timingSafeEqual(good, got);
}
function setCookie(res, value, maxAge) {
  res.setHeader("Set-Cookie", `${COOKIE}=${value}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${maxAge}`);
}
function limited(ip) {
  const now = Date.now(), h = (hits.get(ip) || []).filter(t => now - t < 15 * 60 * 1000);
  h.push(now); hits.set(ip, h);
  return h.length > 8;
}

// ---------- GitHub ----------
async function gh(path, opts = {}) {
  const r = await fetch(`https://api.github.com/repos/${REPO}${path}`, {
    ...opts,
    headers: {
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`, Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "arelec-admin", "Content-Type": "application/json"
    },
    signal: AbortSignal.timeout(20000)
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) { const e = new Error(`GitHub ${r.status} ${body.message || ""}`); e.status = r.status; throw e; }
  return body;
}
async function readData() {
  const f = await gh(`/contents/${DATA_PATH}?ref=${BRANCH}`);
  return { data: JSON.parse(Buffer.from(f.content, "base64").toString("utf8")), sha: f.sha };
}

// ---------- validation de content/admin.json ----------
const ID = /^[a-z0-9][a-z0-9-]{5,39}$/;
const str = (v, max) => (typeof v === "string" ? v.trim().slice(0, max) : "");
function validate(d) {
  if (!d || typeof d !== "object") throw new Error("data");
  const media = (Array.isArray(d.media) ? d.media : []).slice(0, 500).filter(m => m && ID.test(m.id)).map(m => ({
    id: m.id, name: str(m.name, 80), alt: str(m.alt, 160),
    category: CATEGORIES.includes(m.category) ? m.category : "",
    added: /^\d{4}-\d{2}-\d{2}$/.test(m.added) ? m.added : new Date().toISOString().slice(0, 10)
  }));
  const ids = new Set(media.map(m => m.id));
  const images = {}, texts = {};
  for (const [k, v] of Object.entries(d.images || {})) {
    if (!/^(\*|\/[a-z0-9/-]*)\|[a-z0-9._-]+\.(jpe?g|png|webp)(#\d+)?$/.test(k)) continue;
    if (typeof v === "string" && (ids.has(v) || /^site:[a-z0-9._-]+\.(jpe?g|png|webp)$/.test(v))) images[k] = v;
  }
  for (const [k, v] of Object.entries(d.texts || {})) {
    if (/^(\*|\/[a-z0-9/-]*)\|[0-9a-f]{10}$/.test(k) && typeof v === "string" && v.trim()) texts[k] = v.slice(0, 3000);
  }
  return { version: 1, media, images, texts };
}

// ---------- actions ----------
async function publish(body) {
  const { data: current, sha } = await readData();
  if (body.base && body.base !== sha) { const e = new Error("conflict"); e.status = 409; throw e; }
  const next = validate(body.data);
  const files = (Array.isArray(body.files) ? body.files : []).filter(f => ID.test(f.id) && /^[0-9a-f]{40}$/.test(f.sha));
  // Photos retirées de la médiathèque : on supprime aussi le fichier du dépôt
  const removed = current.media.map(m => m.id).filter(id => !next.media.some(m => m.id === id));
  const ref = await gh(`/git/ref/heads/${BRANCH}`);
  const head = await gh(`/git/commits/${ref.object.sha}`);
  const tree = await gh("/git/trees", {
    method: "POST",
    body: JSON.stringify({
      base_tree: head.tree.sha,
      tree: [
        { path: DATA_PATH, mode: "100644", type: "blob", content: JSON.stringify(next, null, 1) + "\n" },
        ...files.map(f => ({ path: `assets/uploads/${f.id}.jpg`, mode: "100644", type: "blob", sha: f.sha })),
        ...removed.map(id => ({ path: `assets/uploads/${id}.jpg`, mode: "100644", type: "blob", sha: null }))
      ]
    })
  });
  const commit = await gh("/git/commits", {
    method: "POST",
    body: JSON.stringify({
      message: "Admin : " + (str(body.message, 120) || "mise à jour du site"),
      tree: tree.sha, parents: [ref.object.sha],
      author: { name: "Espace admin ARélec", email: "site@entreprise-arelec.fr", date: new Date().toISOString() }
    })
  });
  await gh(`/git/refs/heads/${BRANCH}`, { method: "PATCH", body: JSON.stringify({ sha: commit.sha, force: false }) });
  return { commit: commit.sha };
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Robots-Tag", "noindex, nofollow");
  const a = String(req.query?.a || new URL(req.url, "http://x").searchParams.get("a") || "");
  if (!process.env.ADMIN_PASSWORD || !process.env.GITHUB_TOKEN) return res.status(503).json({ error: "unconfigured" });

  if (req.method === "POST") {
    const origin = req.headers.origin;
    let same = false;
    try { same = !origin || new URL(origin).host === req.headers.host; } catch (e) {}
    if (!same) return res.status(403).json({ error: "origin" });
  }
  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  body = body || {};

  try {
    if (a === "login" && req.method === "POST") {
      const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "local";
      if (limited(ip)) return res.status(429).json({ error: "rate" });
      const good = crypto.createHash("sha256").update(process.env.ADMIN_PASSWORD).digest();
      const got = crypto.createHash("sha256").update(String(body.password || "")).digest();
      if (!crypto.timingSafeEqual(good, got)) return res.status(401).json({ error: "password" });
      const exp = String(Math.floor(Date.now() / 1000) + SESSION_S);
      setCookie(res, `${exp}.${sign(exp)}`, SESSION_S);
      return res.status(200).json({ ok: true });
    }
    if (a === "logout") { setCookie(res, "", 0); return res.status(200).json({ ok: true }); }
    if (!session(req)) return res.status(401).json({ error: "auth" });

    if (a === "me") return res.status(200).json({ ok: true });
    if (a === "data" && req.method === "GET") {
      const { data, sha } = await readData();
      return res.status(200).json({ data, sha });
    }
    if (a === "blob" && req.method === "POST") {
      // Photo déjà redimensionnée par le navigateur (JPEG) : stockée tout de suite, publiée au prochain « Publier »
      const b64 = String(body.data || "").replace(/^data:image\/jpeg;base64,/, "");
      const buf = Buffer.from(b64, "base64");
      if (!buf.length || buf.length > MAX_IMG || buf[0] !== 0xff || buf[1] !== 0xd8) return res.status(400).json({ error: "image" });
      const blob = await gh("/git/blobs", { method: "POST", body: JSON.stringify({ content: b64, encoding: "base64" }) });
      return res.status(200).json({ sha: blob.sha });
    }
    if (a === "publish" && req.method === "POST") return res.status(200).json(await publish(body));
    return res.status(404).json({ error: "action" });
  } catch (e) {
    console.error("admin:", a, e.message);
    return res.status(e.status === 409 ? 409 : 502).json({ error: e.status === 409 ? "conflict" : "github" });
  }
};
