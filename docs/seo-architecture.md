# Architecture SEO & SEA — Site ARELEC

> Objectif : devenir la référence locale (électricité / chauffage / plomberie) sur **Brest + bassin brestois**.
> **Règles de contenu (imposées) :** ne rien inventer · rester simple · **aucun prix affiché** · CTA = **« Contacter »** ou **« Faire une estimation »** (renvoie vers le futur logiciel d'estimation). Même mockup, mots adaptés par page.
> NAP unique partout : **ARélec — Plouzané 29280 — 02 98 40 20 43** — gérant **Arnaud Roncey**.

---

## 1. Arborescence (sitemap)

```
/                              Accueil (marque + 3 métiers + estimation + réalisations + avis + contact)
/electricite                   Métier — Électricité
/chauffage                     Métier — Chauffage & thermique
/plomberie                     Métier — Plomberie
/realisations                  Portfolio (vraies photos chantiers)
/entreprise                    À propos (depuis 2010, équipe, valeurs, certifs)
/avis                          Témoignages (avis Google réels)
/contact                       Coordonnées + formulaire + carte
/estimation                    Page passerelle → logiciel d'estimation (à venir)
/mentions-legales              Légal
/politique-confidentialite     RGPD

— Pages locales (SEO de proximité), motif [métier]-[commune] —
/electricien-brest    /electricien-plouzane    /electricien-…
/plombier-brest       /plombier-plouzane       /plombier-…
/chauffagiste-brest   /chauffagiste-plouzane   /chauffagiste-…
```

**Pages locales = même mockup, mots adaptés.** Une page = un métier × une commune (intention de recherche réelle).

## 2. Communes cibles — ⚠️ À VALIDER avec Arnaud (zone exacte = Q17-19, non confirmée)
- **Preuves existantes :** Plouzané (siège), **Brest** (chantiers + avis), **Plouider** (chantier).
- **Proposées (à confirmer) :** Le Relecq-Kerhuon, Guipavas, Bohars, Guilers, Saint-Renan, Locmaria-Plouzané, Plougonvelin, Le Conquet, Milizac-Guipronvel, Plouzévédé/Lesneven (selon rayon).
> Ne créer une page locale **que** pour une commune réellement desservie. Sinon risque de contenu trompeur + dilution SEO.

## 3. Plan des pages : intention, mots-clés, metadata

| Page | Intention | Mots-clés cibles | Title (≤60c) | Meta description (≤155c) | H1 (unique) |
|---|---|---|---|---|---|
| `/` | Marque + global | ARélec, électricien chauffagiste plombier Plouzané | `ARélec — Électricien, chauffagiste & plombier (29)` | `Électricité, chauffage et plomberie dans le bassin brestois depuis 2010. Devis gratuit, travail soigné. Estimez votre projet en ligne.` | `Une maison bien câblée, bien chauffée.` |
| `/electricite` | Service | installation électrique, mise aux normes, rénovation élec Brest | `Électricien à Brest & Plouzané | ARélec` | `Installation, rénovation, mise aux normes (NF C 15-100) et dépannage électrique dans le bassin brestois. Devis gratuit — ARélec.` | `Électricité — installation, rénovation, dépannage` |
| `/chauffage` | Service | chauffagiste Brest, pompe à chaleur, plancher chauffant | `Chauffagiste à Brest | Pompe à chaleur — ARélec` | `Pompe à chaleur, plancher chauffant, radiateurs et entretien dans le bassin brestois. Confort et économies. Devis gratuit — ARélec.` | `Chauffage & thermique — confort toute l'année` |
| `/plomberie` | Service | plombier Brest, rénovation salle de bain, fuite | `Plombier à Brest | Salle de bain — ARélec` | `Salle de bain, sanitaires, recherche de fuite et réseau d'eau dans le bassin brestois. Rénovation soignée. Devis gratuit — ARélec.` | `Plomberie — sanitaire, salle de bain, dépannage` |
| `/realisations` | Preuve | rénovation maison Brest, chantiers électricien Finistère | `Nos réalisations | ARélec — Brest & Finistère` | `Découvrez nos chantiers d'électricité, chauffage et plomberie à Brest, Plouzané et alentour. Rénovations et installations soignées.` | `Nos réalisations` |
| `/entreprise` | Marque/confiance | ARélec Arnaud Roncey, artisan Plouzané depuis 2010 | `L'entreprise | ARélec, artisan depuis 2010` | `ARélec, artisan électricien-chauffagiste-plombier à Plouzané depuis 2010. Une équipe, un seul interlocuteur, un travail soigné.` | `ARélec, votre artisan depuis 2010` |
| `/avis` | Confiance | avis ARélec, électricien Brest avis | `Avis clients | ARélec — Brest & Plouzané` | `Ce que nos clients disent d'ARélec : qualité, propreté, réactivité et bons conseils. Avis vérifiés.` | `Ils nous recommandent` |
| `/contact` | Conversion | contact électricien Brest, devis | `Contact & devis gratuit | ARélec — Plouzané` | `Contactez ARélec à Plouzané : 02 98 40 20 43. Devis gratuit pour vos travaux d'électricité, chauffage et plomberie dans le bassin brestois.` | `Parlons de votre projet` |

### Templates pages locales (variables `{Commune}`)
- **Électricien** — Title : `Électricien à {Commune} (29) | ARélec depuis 2010` · Desc : `Électricien à {Commune} : installation, rénovation, mise aux normes et dépannage. + chauffage & plomberie. Devis gratuit — ARélec.` · H1 : `Votre électricien à {Commune}`
- **Plombier** — Title : `Plombier à {Commune} (29) | ARélec` · Desc : `Plombier à {Commune} : salle de bain, recherche de fuite, réseau d'eau, sanitaires. Rénovation soignée. Devis gratuit — ARélec.` · H1 : `Votre plombier à {Commune}`
- **Chauffagiste** — Title : `Chauffagiste à {Commune} (29) | ARélec` · Desc : `Chauffagiste à {Commune} : pompe à chaleur, plancher chauffant, radiateurs, entretien. Confort & économies. Devis gratuit — ARélec.` · H1 : `Votre chauffagiste à {Commune}`

> ⚠️ **Anti-duplicate :** chaque page locale doit avoir ≥ 1 bloc de texte unique (quartiers/repères de la commune, 1-2 chantiers réalisés sur place, mention transport/délai local). Sinon Google les traite comme du contenu dupliqué.

## 4. Données structurées (JSON-LD) — à poser sur chaque page
- **`Electrician` / `LocalBusiness`** (Accueil + pages locales) : `name`, `address` (Plouzané 29280), `telephone`, `url`, `image` (logo/photo), `areaServed` (liste des communes desservies), `openingHours` (⚠️ à confirmer), `geo` si dispo. *Pas de `priceRange` inventé.*
- **`AggregateRating` + `Review`** : utiliser les **avis Google réels** (voir `avis.md`). ⚠️ Remplir `ratingValue` + `reviewCount` avec les **vrais chiffres Google** (à récupérer) — ne pas inventer.
- **`Service`** (pages métiers) : un par prestation (électricité, chauffage, plomberie) avec `areaServed`.
- **`BreadcrumbList`** sur toutes les pages internes.

## 5. Maillage interne
- Accueil → 3 pages métiers → pages locales correspondantes.
- Chaque page locale → la page métier mère + `/realisations` (filtrées commune si possible) + `/contact` + `/estimation`.
- `/realisations` → pages métiers (cross-link par type de chantier).
- Fil d'Ariane partout. 1 H1 unique/page. URLs courtes en minuscules, sans accent (`/electricien-plouzane`).

## 6. SEO technique
- `sitemap.xml` (toutes les pages) + `robots.txt` (autorise tout + lien sitemap).
- `canonical` auto sur chaque page. `lang="fr"` (pas de hreflang, site FR uniquement).
- **Mobile-first + Core Web Vitals** : images optimisées (les photos chantiers en WebP/AVIF, `loading="lazy"`, dimensions explicites), CSS léger, pas de blocage de rendu. (cf. règle responsive de `CLAUDE.md`).
- **NAP cohérent** site / Google Business Profile / annuaires (PagesJaunes, etc.).
- **Google Business Profile** : poste régulier des chantiers (les vraies photos), catégories Électricien + Plombier + Chauffagiste, zone de service = communes.
- Open Graph / Twitter Card par page (titre + photo chantier).

## 7. SEA — Google Ads (Search local)
- **Structure :** 1 campagne par métier (Électricité / Chauffage / Plomberie), ciblage géo = communes desservies (rayon autour de Plouzané/Brest).
- **Groupes d'annonces :** {métier} × {commune} → ex. « Électricien Brest », « Plombier Brest », « Chauffagiste Brest », « Électricien Plouzané »…
- **Mots-clés** (expression/exact) : `électricien brest`, `dépannage électrique brest`, `mise aux normes électrique brest`, `plombier brest`, `rénovation salle de bain brest`, `recherche de fuite brest`, `chauffagiste brest`, `installation pompe à chaleur brest`, + variantes « plouzané ».
- **Mots-clés négatifs :** `emploi`, `recrutement`, `formation`, `salaire`, `cours`, `pdf`, `leroy merlin`, `castorama`, noms de concurrents.
- **RSA (annonces) — titres (sans prix) :** « Électricien à {Commune} », « ARélec — depuis 2010 », « Devis gratuit », « Travail soigné & rapide », « Électricité · Chauffage · Plomberie », « Intervention dans le bassin brestois ». **Descriptions :** « Installation, rénovation, mise aux normes et dépannage. Devis gratuit, chantier propre. », « Un seul interlocuteur pour l'élec, le chauffage et la plomberie. Estimez en ligne. »
- **Extensions :** appel (02 98 40 20 43), lieu, liens annexes (Réalisations / Contact / Estimation), accroches (Depuis 2010 · Devis gratuit · Bassin brestois · Chantier propre).
- **Landing :** chaque groupe d'annonces pointe vers **sa page locale** (message match). CTA = Contacter / Faire une estimation.
- **Conversions :** appels téléphoniques, envoi du formulaire, démarrage d'une estimation.

## 8. CTA (règle unique sur tout le site)
- **Primaire : « Faire une estimation »** → `/estimation` (logiciel à venir).
- **Secondaire : « Contacter »** → `/contact` ou `tel:0298402043`.
- Aucun prix affiché tant que l'estimateur n'est pas en ligne.

## 9. Statut
- ✅ Acquis : marque, métiers, NAP, gérant, **vraies photos** (`assets/realisations/`), **avis réels** (`avis.md`).
- ⛔ À obtenir : zone exacte (communes), **note + nb d'avis Google** (AggregateRating), certifications/assurances, horaires, prestations détaillées (cf. `questionnaire-fondateur.md`).
