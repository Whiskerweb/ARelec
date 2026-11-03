// Aperçu local : sert site/ comme Vercel (cleanUrls) + la fonction /api/chat.
//   OPENROUTER_API_KEY=... node dev-server.mjs   →  http://127.0.0.1:4400
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const ROOT = path.dirname(new URL(import.meta.url).pathname);
const SITE = path.join(ROOT, "site");
const PORT = Number(process.env.PORT || 4400);
const chat = require("./api/chat.js");
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".png": "image/png", ".jpg": "image/jpeg", ".ico": "image/x-icon", ".txt": "text/plain; charset=utf-8", ".xml": "application/xml" };

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  if (url.pathname === "/api/chat") {
    res.status = c => { res.statusCode = c; return res; };
    res.json = o => { res.setHeader("Content-Type", "application/json"); res.end(JSON.stringify(o)); };
    let raw = ""; for await (const c of req) raw += c;
    req.body = raw;
    return chat(req, res);
  }
  let p = path.normalize(path.join(SITE, decodeURIComponent(url.pathname)));
  if (!p.startsWith(SITE)) { res.statusCode = 403; return res.end(); }
  if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, "index.html");
  else if (!fs.existsSync(p) && fs.existsSync(p + ".html")) p += ".html";
  if (!fs.existsSync(p)) { res.statusCode = 404; return res.end("404"); }
  res.setHeader("Content-Type", TYPES[path.extname(p)] || "application/octet-stream");
  fs.createReadStream(p).pipe(res);
}).listen(PORT, "127.0.0.1", () => console.log(`ARélec : http://127.0.0.1:${PORT}`));
