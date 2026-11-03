# ARELEC — Site vitrine

Site vitrine moderne pour **SARL ARélec** — électricité, chauffage/thermique et plomberie, à Plouzané (bassin brestois, Finistère), depuis 2010. Gérant : Arnaud Roncey. Tél : 02 98 40 20 43 · contact@entreprise-arelec.fr.

**Mission du site :** casser les codes (souvent ternes) du secteur, donner une âme forte à la marque et positionner ARélec en **leader local**.

---

## Règles non négociables

1. **100% responsive / mobile-friendly à CHAQUE modification.** Toujours penser desktop ET mobile (clamp() + media queries ≤900px et ≤560px). Vérifier le rendu petit écran systématiquement.
2. **DA « Voltora »** (refonte nov. 2026, inspirée de voltora.framer.website) : voir la section Direction artistique. Boutons pilule avec pastille ronde, cartes très arrondies.
3. **Ton naturel d'artisan** : concret, fier du métier, rassurant. Pas de slogan tordu ni de jargon. Ex. retenu : « Une maison bien câblée, bien chauffée. »
4. **Reste un site vitrine simple.** PAS d'app de suivi de chantier, pas de SaaS.
5. **CTA principal = « Prendre contact »** (attribut `data-chat`) : ouvre l'assistant du site, qui répond aux questions puis fait basculer le prospect sur **WhatsApp** (message prérempli avec le résumé de sa demande ; un agent WhatsApp prendra le relais). L'estimateur en ligne est abandonné (`/estimation` redirige vers `/contact/`). Jamais de prix donné par l'assistant.

---

## Direction artistique (source de vérité) — refonte « Voltora » (nov. 2026)
Inspirée de https://voltora.framer.website (mise en page, typo, effets), avec le contenu, les photos et le logo d'ARélec.
- **Polices** : Geist 300 pour les titres (H1 68px, H2 48px, interlettrage -0.035em), Geist 400 pour le texte, **Geist Mono 500** en capitales pour les étiquettes, **Doto 900** (police pixel) pour le grand « ARÉLEC » du footer.
- **Couleurs** : encre `#121211` / `#191917`, crème `#F3F2EE`, filet `#E4E2DC`, texte secondaire `#6F6D66`, **accent jaune-vert `#E3FF4A`** (pastilles des boutons, étoiles, puces). Fond de page blanc.
- **Composants** : étiquette pilule « ● TEXTE » en mono ; bouton pilule sombre avec pastille ronde jaune-vert (flèche qui pivote au survol) ; cartes de 32px de rayon posées à 12px des bords (hero, CTA, footer) ; cartes crème de 20 à 24px ; panneaux en verre flouté sur les photos.
- **Effets** : apparition au scroll en fondu + flou + montée (`.r` → `.in`, `--d` = délai) ; compteurs animés ; défilant de logos ; zoom lent de la photo du hero ; trait des étapes qui se dessine. Tout est coupé avec `prefers-reduced-motion`.
- **Informations inconnues** : affichées entre astérisques avec `tbd()` (ex. « *1 200+* », « *Partenaire 1* ») = à compléter avec ARélec, ne jamais inventer.
- **Avis** : note 4,6/5 sur 9 avis (relevée sur avis-electricien.fr, reprise de la fiche Google, le 03/11/2026), adresse Rue du Cloître, 29280 Plouzané. `AggregateRating` toujours absent du JSON-LD : à ajouter seulement avec la fiche Google officielle.
- **Pages** : Accueil, Services (`/services`), À propos (`/entreprise`), Réalisations, Blog (`/blog`, maquette en noindex tant que les articles ne sont pas rédigés), Contact, Avis, pages métier et 39 pages locales SEO (même gabarit `gen_sub`, contenu inchangé).

## Expérience de défilement
**Scroll par panneaux façon Apple** (pas un scroll continu) : chaque section = plein écran, **`scroll-snap-type:y proximity`** + `scroll-snap-stop:always` (⚠️ **proximity, PAS mandatory** : avec `mandatory`, le bandeau/footer de bas de page — qui n'est pas un panneau plein écran — devient inatteignable, le scroll « repince » vers le dernier panneau). Le fond se remplace et le contenu apparaît en fondu/translation (IntersectionObserver ajoute `.visible`). Bandeau contact + footer = blocs en flux normal (`scroll-snap-align:none`, sauf le bandeau en `start`). Points de navigation latéraux. Sur mobile (≤760px), idem proximity.

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
4. **Pages locales SEO** — motif `[métier]-[commune]` (électricien-brest, plombier-brest, électricien-plouzane…), même mockup, mots adaptés. CTA = **Prendre contact** (assistant) ou **Contacter** (téléphone). Aucun prix inventé. Démo : `page-electricien-brest`.
5. À venir : mise en service Meta de l'agent WhatsApp, réalisations, l'entreprise, contact/footer, pages légales (mentions, RGPD).

---

## Assistant (chat) & WhatsApp
- Bulle discrète en bas à droite (tous écrans, remplace l'ancienne barre mobile Appeler/Estimer) + panneau : `chat_widget()` dans `build_site.py`, logique dans `chat.js` (copié vers `site/assets/js/chat.js` au build).
- Fonction Vercel `api/chat.js` → OpenRouter. Variables Vercel : `OPENROUTER_API_KEY` (obligatoire), `OPENROUTER_MODEL` (facultatif, défaut `anthropic/claude-haiku-4.5`). Le contexte (`api/_context.js`) est **généré** depuis `llms-full.txt` : modifier le contenu dans `build_site.py`, pas à la main.
- Bascule WhatsApp : le modèle termine par `<<WHATSAPP>>résumé<<END>>`, l'API le retire et le client ouvre `wa.me/33678020424` avec le résumé prérempli.
- Aperçu local avec l'API : `OPENROUTER_API_KEY=… node dev-server.mjs` → http://127.0.0.1:4400.
- **Agent WhatsApp** (06 78 02 04 24 en coexistence via **360dialog** ; Meta direct reste possible) : webhook Cloud API `api/whatsapp.js`, branchement `scripts/setup-360dialog.mjs`, (même socle `api/_openrouter.js`, mémoire `api/_store.js` sur Upstash Redis). Il reprend le « Mon projet : … » du site, qualifie (travaux, commune, urgence, photos, dispos, nom), envoie une fiche à Arnaud puis se tait 48 h si Arnaud répond depuis l'app (coexistence). Mise en service et variables : `docs/agent-whatsapp.md`.

## Maquettes & outils
- Maquettes de brainstorming (compagnon visuel) : `.superpowers/brainstorm/.../content/*.html` (HTML autonomes, logo embarqué en data-URI). Servir le fichier le plus récent.
- **Site réel généré** dans `site/` par `build_site.py` (`python build_site.py`, nécessite Pillow ; chemins relatifs au script). 18 pages, CSS unique (`site/assets/css/styles.css`) + images mutualisées (`site/assets/img/`), ~950 Ko au total. Pour modifier le contenu/design d'une page : éditer `build_site.py` (données des pages + composants partagés) puis relancer le script. Aperçu local : `python -m http.server` dans `site/`.
- Chaque page : `<title>`/meta/H1 uniques, `canonical`, Open Graph, **JSON-LD** (Electrician + Review réels + BreadcrumbList), contenu **unique humanisé** (anti-duplicate), footer groupé métier/territoire. `sitemap.xml` + `robots.txt` générés.
- ⚠️ Communes limitées aux confirmées (Brest, Plouzané, Plouider). **`AggregateRating` volontairement omis** tant que la note/nombre d'avis Google officiels ne sont pas fournis (ne pas inventer). Stubs à compléter : contact (formulaire), entreprise, réalisations, légal.
- Mémoire projet : `~/.claude/projects/.../memory/` (DA + règle responsive).
