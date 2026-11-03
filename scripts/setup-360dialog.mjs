// Branche le numéro 360dialog sur l'agent : 360dialog enverra les messages WhatsApp à /api/whatsapp
// avec l'en-tête secret X-Arelec-Key (la même valeur que WHATSAPP_WEBHOOK_KEY dans Vercel).
//   D360_API_KEY=… WHATSAPP_WEBHOOK_KEY=… node scripts/setup-360dialog.mjs [url]
const key = process.env.D360_API_KEY, secret = process.env.WHATSAPP_WEBHOOK_KEY;
const url = process.argv[2] || "https://www.entreprise-arelec.fr/api/whatsapp";
if (!key || !secret) {
  console.error("Il faut D360_API_KEY et WHATSAPP_WEBHOOK_KEY dans l'environnement.");
  process.exit(1);
}
const r = await fetch("https://waba-v2.360dialog.io/v1/configs/webhook", {
  method: "POST",
  headers: { "D360-API-KEY": key, "Content-Type": "application/json" },
  body: JSON.stringify({ url, headers: { "X-Arelec-Key": secret } })
});
console.log(r.status, await r.text());
process.exit(r.ok ? 0 : 1);
