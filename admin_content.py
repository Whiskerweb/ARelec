# Contenu modifié depuis l'espace admin (/admin) — utilisé par build_site.py.
# content/admin.json est écrit par l'admin (commit GitHub via /api/admin) puis Vercel reconstruit le site :
#   media  : photos envoyées par Arnaud (assets/uploads/<id>.jpg), avec nom, texte alternatif et catégorie
#   images : emplacement -> photo   « /page/|fichier.jpg#n » (cet endroit) ou « *|fichier.jpg » (partout)
#   texts  : texte -> nouveau texte « /page/|empreinte » (cet endroit) ou « *|empreinte » (partout)
import re, json, hashlib, html as _html
from html.parser import HTMLParser
from PIL import Image, ImageOps

CATEGORIES = ["Rénovation", "Salle de bain", "Électricité", "Éclairage", "Chauffage", "Plomberie", "Extérieur"]
SKIP_IMG = ("logo", "mascotte", "partenaires/", "favicon", "apple-touch", "u/")
MAX_W, THUMB_W = 1600, 480


def load(root):
    try:
        data = json.loads((root / "content/admin.json").read_text())
    except Exception:
        data = {}
    for k, v in (("media", []), ("images", {}), ("texts", {})):
        data.setdefault(k, v)
    return data


def build_media(root, img_dir, data):
    """Met chaque photo envoyée au bon format : orientation corrigée, 1600 px max, vignette 480 px."""
    out = img_dir / "u"
    out.mkdir(exist_ok=True)
    for m in data["media"]:
        src = root / "assets/uploads" / f"{m['id']}.jpg"
        if not src.exists():
            continue
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        for name, w in ((f"{m['id']}.jpg", MAX_W), (f"{m['id']}-t.jpg", THUMB_W)):
            v = im.copy()
            if v.width > w:
                v = v.resize((w, round(v.height * w / v.width)), Image.LANCZOS)
            v.save(out / name, "JPEG", quality=80, optimize=True, progressive=True)


def media_src(data, mid):
    """Adresse publique d'une photo : envoyée (« <id> ») ou d'origine du site (« site:fichier.jpg »)."""
    if mid.startswith("site:"):
        return "/assets/img/" + mid[5:]
    if any(m["id"] == mid for m in data["media"]):
        return f"/assets/img/u/{mid}.jpg"
    return None


def media_alt(data, mid):
    m = next((m for m in data["media"] if m["id"] == mid), None)
    return (m.get("alt") or m.get("name") or "") if m else None


# ---------- texte autorisé dans un texte modifié (gras, italique, retour à la ligne, lien) ----------
class _Clean(HTMLParser):
    OK = {"b", "strong", "i", "em", "br", "a"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def handle_starttag(self, t, attrs):
        if t not in self.OK:
            return
        if t == "a":
            href = dict(attrs).get("href") or ""
            if re.match(r"^(/|tel:|mailto:|https://)", href):
                self.out.append(f'<a href="{_html.escape(href)}">')
            else:
                self.out.append("<a>")
        else:
            self.out.append(f"<{t}>")

    def handle_endtag(self, t):
        if t in self.OK and t != "br":
            self.out.append(f"</{t}>")

    def handle_data(self, d):
        self.out.append(_html.escape(d, quote=False))


def clean_html(s):
    p = _Clean()
    p.feed(s or "")
    p.close()
    return "".join(p.out).strip()


def text_key(inner):
    norm = " ".join(re.sub(r"<[^>]+>", " ", inner).split())
    return hashlib.sha1(norm.encode()).hexdigest()[:10]


_IMG = re.compile(r'<img\b([^>]*?)\bsrc="/assets/img/([^"]+)"([^>]*)>')
_TXT = re.compile(r"<(h1|h2|h3|h4|p|li)\b([^>]*)>(.*?)</\1>", re.S)
_BLOCKY = re.compile(r"<(div|p|ul|ol|li|svg|img|button|section|figure|table|form|input|textarea|select|picture)\b")


def apply(url, page, data):
    """Repère et modifie images et textes du <main> d'une page (data-slot / data-edit pour l'admin)."""
    a, b = page.find("<main"), page.rfind("</main>")
    if a < 0 or b < 0:
        return page
    main = page[a:b]
    seen = {}

    def img(m):
        pre, file, post = m.group(1), m.group(2), m.group(3)
        if any(x in file for x in SKIP_IMG):
            return m.group(0)
        n = seen.get(file, 0)
        seen[file] = n + 1
        slot = f"{file}#{n}"
        mid = data["images"].get(f"{url}|{slot}") or data["images"].get(f"*|{file}")
        src = media_src(data, mid) if mid else None
        tag = f'<img{pre} src="{src or "/assets/img/" + file}"{post}>'
        if src:
            alt = media_alt(data, mid)
            if alt:
                tag = re.sub(r'\balt="[^"]*"', f'alt="{_html.escape(alt)}"', tag, count=1)
            tag = re.sub(r'\s(?:srcset|sizes)="[^"]*"', "", tag)
        return tag.replace("<img", f'<img data-slot="{slot}"', 1)

    def txt(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if "data-edit" in attrs or _BLOCKY.search(inner) or len(re.sub(r"<[^>]+>|\s", "", inner)) < 2:
            return m.group(0)
        k = text_key(inner)
        new = data["texts"].get(f"{url}|{k}") or data["texts"].get(f"*|{k}")
        return f'<{tag}{attrs} data-edit="{k}">{clean_html(new) if new else inner}</{tag}>'

    main = _IMG.sub(img, main)
    main = _TXT.sub(txt, main)
    return page[:a] + main + page[b:]


def gallery_items(data):
    """Photos classées par Arnaud, à ajouter en tête de la galerie Réalisations (les plus récentes d'abord)."""
    return [(f"/assets/img/u/{m['id']}.jpg", m["category"], m.get("name") or m["category"], m.get("alt") or m.get("name") or "")
            for m in reversed(data["media"]) if m.get("category") in CATEGORIES]
