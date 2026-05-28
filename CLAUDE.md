# ARELEC — Site vitrine

Site vitrine moderne pour **SARL ARélec** — électricité, chauffage/thermique et plomberie, à Plouzané (bassin brestois, Finistère), depuis 2010. Gérant : Arnaud Roncey. Tél : 02 98 40 20 43 · contact@entreprise-arelec.fr.

**Mission du site :** casser les codes (souvent ternes) du secteur, donner une âme forte à la marque et positionner ARélec en **leader local**.

---

## Règles non négociables

1. **100% responsive / mobile-friendly à CHAQUE modification.** Toujours penser desktop ET mobile (clamp() + media queries ≤900px et ≤560px). Vérifier le rendu petit écran systématiquement.
2. **Boutons & surfaces en liquid glass** (jamais de boutons plats opaques) : translucide, `backdrop-filter:blur(...)`, reflet spéculaire en haut, bord clair fin, ombre douce, coins très arrondis.
3. **Ton naturel d'artisan** : concret, fier du métier, rassurant. Pas de slogan tordu ni de jargon. Ex. retenu : « Une maison bien câblée, bien chauffée. »
4. **Reste un site vitrine simple.** PAS d'app de suivi de chantier, pas de SaaS.
5. **Différenciateur n°1 = l'estimateur de travaux en ligne** : aperçu de prix en ~2 min → si OK, l'électricien vient faire le vrai devis sur place (gratuit). C'est le CTA principal partout (« Estimer mes travaux »).

---

## Direction artistique (source de vérité)

**Monde retenu : « Le Réseau » — lumineux, moderne, premium.** Mot-clé visuel : **la lumière**.

### Couleurs
- Accent unique : **bleu électrique** `#1457FF` → dégradé cyan `#0BB0FF` (à doser, jamais envahissant).
- Texte : blanc pur sur photo ; bleu nuit `#0C2A5E` / `#11233F` sur fond clair.
- Fonds sombres : navy `#0A1322`, `#06101F`, dégradés `#0C2750`→`#06101F`.
- Vert « dispo / conforme / OK » : `#36E07F`.
- Verre : blanc translucide 7–22% d'opacité.

### Typographie
- **Inter** (grotesk géométrique). Titres semi-bold (600–700), interlettrage serré (`-0.03em`), grandes tailles en `clamp()`. Wordmark/labels en capitales, letter-spacing large.

### Liquid glass (recette de référence)
```css
backdrop-filter: blur(20px) saturate(160%);
background: linear-gradient(180deg, rgba(255,255,255,.22), rgba(255,255,255,.08));
border: 1px solid rgba(255,255,255,.4);
box-shadow: inset 0 1px 0 rgba(255,255,255,.6), 0 12px 30px rgba(0,0,0,.3);
/* + reflet : ::after gradient blanc sur la moitié haute */
```
Coins arrondis : pilules `999px`, cartes `18–26px`.

### Photographie
Cinématique, jamais cliché « ouvrier en gilet ». Heure bleue/dorée, lumière chaude, zone sombre pour poser le texte blanc.
- Hero maquette (provisoire) : **côte bretonne à l'heure dorée** (identité Finistère, écho au pont du logo).
- **Objectif version finale : vraies photos des chantiers ARélec** (maison bretonne pierre/ardoise à l'heure bleue) — le plus crédible et le plus local.

### Logo
- `assets/logo-arelec-white.png` — monoline blanc transparent : signature « Arélec » + **pont à haubans (Pont de l'Iroise, Brest)** = ancrage local fort + wordmark ARELEC. Se pose sur fond sombre / dans une pilule de verre. Prévoir version lisible sans contenant.

### Mise en page hero (validée)
Inspirée de la réf. « abysse » : titre en bas à gauche, CTA primaire (verre clair) à droite, ligne de séparation fine, puis puces de confiance (📞 / 📍 Plouzané / ✓ devis gratuit) à gauche et descriptif à droite. Nav = pilule de verre (logo gauche · liens centre · CTA « Estimer mes travaux » droite ; burger en verre ≤900px).

---

## Expérience de défilement
**Scroll par panneaux façon Apple** (pas un scroll continu) : chaque section = plein écran, **`scroll-snap-type:y proximity`** + `scroll-snap-stop:always` (⚠️ **proximity, PAS mandatory** : avec `mandatory`, le bandeau/footer de bas de page — qui n'est pas un panneau plein écran — devient inatteignable, le scroll « repince » vers le dernier panneau). Le fond se remplace et le contenu apparaît en fondu/translation (IntersectionObserver ajoute `.visible`). Bandeau estimation + footer = blocs en flux normal (`scroll-snap-align:none`, sauf le bandeau en `start`). Points de navigation latéraux. Sur mobile (≤760px), idem proximity.

## Conformité Apple HIG (Human Interface Guidelines)
Principes : **Clarté, Déférence, Profondeur** (le contenu prime, les ornements restent subtils, les couches/mouvements donnent la hiérarchie). Règles concrètes à respecter partout :
- **Cibles tactiles ≥ 44×44 pt** (liens nav, boutons, burger, pagination).
- **`prefers-reduced-motion: reduce`** : couper reveals/parallaxe/scroll-smooth.
- **Focus clavier visible** (`:focus-visible`, anneau contrasté ; blanc sur le hero sombre).
- **Safe-area insets** (`env(safe-area-inset-*)`) pour encoche / barre d'accueil.
- Centrage vertical des sections via **`margin:auto`** (pas `justify-content:center`, qui clippe le haut dans un conteneur scrollable) + padding haut/bas garanti → le titre a toujours de l'air au-dessus.
- Liquid glass = « materials/vibrancy » Apple : garder des contrastes de texte lisibles (WCAG AA).
- Espacement sur une trame régulière (~4/8px), généreux et cohérent.

## Sections du site (plan)
Architecture SEO/SEA complète : `docs/seo-architecture.md` · avis réels : `docs/avis.md` · questionnaire fondateur : `docs/questionnaire-fondateur.md` · contenu extrait : `docs/contenu-extrait.md`.
1. **Hero** — vraie maison bretonne à l'heure bleue (`assets/realisations/photo-10.jpg`) — fait.
2. **Nos corps de métier** — Électricité / Chauffage / Plomberie, cartes liquid glass clair + vraies photos — fait.
3. **Avis** — avis Google réels, cartes verre — fait (maquette).
4. **Pages locales SEO** — motif `[métier]-[commune]` (électricien-brest, plombier-brest, électricien-plouzane…), même mockup, mots adaptés. CTA = **Faire une estimation** (`/estimation`, logiciel à venir) ou **Contacter**. Aucun prix inventé. Démo : `page-electricien-brest`.
5. À venir : estimateur (logiciel), réalisations, l'entreprise, contact/footer, pages légales (mentions, RGPD).

---

## Maquettes & outils
- Maquettes de brainstorming (compagnon visuel) : `.superpowers/brainstorm/.../content/*.html` (HTML autonomes, logo embarqué en data-URI). Servir le fichier le plus récent.
- **Site réel généré** dans `site/` par `build_site.py` (`/tmp/arelec_venv/bin/python build_site.py`). 18 pages, CSS unique (`site/assets/css/styles.css`) + images mutualisées (`site/assets/img/`), ~950 Ko au total. Pour modifier le contenu/design d'une page : éditer `build_site.py` (données des pages + composants partagés) puis relancer le script. Aperçu local : `python -m http.server` dans `site/`.
- Chaque page : `<title>`/meta/H1 uniques, `canonical`, Open Graph, **JSON-LD** (Electrician + Review réels + BreadcrumbList), contenu **unique humanisé** (anti-duplicate), footer groupé métier/territoire. `sitemap.xml` + `robots.txt` générés.
- ⚠️ Communes limitées aux confirmées (Brest, Plouzané, Plouider). **`AggregateRating` volontairement omis** tant que la note/nombre d'avis Google officiels ne sont pas fournis (ne pas inventer). Stubs à compléter : contact (formulaire), entreprise, réalisations, estimation, légal.
- Mémoire projet : `~/.claude/projects/.../memory/` (DA + règle responsive).
