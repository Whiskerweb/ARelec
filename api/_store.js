// Petit stockage clé/valeur JSON : Upstash Redis (REST) si configuré, sinon mémoire de l'instance.
// Vercel > Storage > Upstash (Redis) crée KV_REST_API_URL / KV_REST_API_TOKEN ;
// les noms UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN sont aussi acceptés.
const URL_ = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
const mem = new Map();

async function redis(cmd) {
  const r = await fetch(URL_, {
    method: "POST",
    headers: { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify(cmd),
    signal: AbortSignal.timeout(5000)
  });
  if (!r.ok) throw new Error("Redis " + r.status);
  return (await r.json()).result;
}

function memGet(key) {
  const e = mem.get(key);
  if (!e) return null;
  if (e.exp && e.exp < Date.now()) { mem.delete(key); return null; }
  return e.val;
}

async function get(key) {
  if (!URL_) return memGet(key);
  const v = await redis(["GET", key]);
  return v == null ? null : JSON.parse(v);
}

async function set(key, val, ttlSec) {
  if (!URL_) { mem.set(key, { val, exp: ttlSec ? Date.now() + ttlSec * 1000 : 0 }); return; }
  await redis(ttlSec ? ["SET", key, JSON.stringify(val), "EX", ttlSec] : ["SET", key, JSON.stringify(val)]);
}

// true si la clé vient d'être posée (première fois), false si elle existait déjà.
async function once(key, ttlSec) {
  if (!URL_) {
    if (memGet(key) != null) return false;
    mem.set(key, { val: 1, exp: Date.now() + ttlSec * 1000 });
    return true;
  }
  return (await redis(["SET", key, "1", "NX", "EX", ttlSec])) === "OK";
}

module.exports = { get, set, once, persistent: !!URL_ };
