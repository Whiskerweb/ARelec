# Agent WhatsApp ARélec — mise en service

## Ce que fait l'agent
1. Le prospect discute avec l'assistant du site, puis clique « Continuer sur WhatsApp ». Son message est prérempli : « Bonjour ARélec 👋 Je viens du site. Mon projet : … ».
2. Le message arrive sur le numéro WhatsApp d'ARélec. Meta l'envoie au webhook `https://www.entreprise-arelec.fr/api/whatsapp` (`api/whatsapp.js`).
3. L'agent reprend la conversation **sans reposer ce qui est déjà dit**. Il pose une question à la fois : travaux, commune, neuf ou rénovation, urgence, photos (facultatives), disponibilités pour la visite, nom. Il ne donne jamais de prix ni de date.
4. Quand il en sait assez, il dit au client qu'Arnaud revient vers lui. Il envoie alors à Arnaud une **fiche prospect** : nom, travaux, commune, urgence, disponibilités, photos, numéro du client.
5. Si Arnaud répond lui-même depuis l'app WhatsApp Business (mode coexistence), l'agent **se tait pendant 48 h** dans cette conversation.

Les photos et les vocaux sont signalés à l'agent (« [photo] »), mais il ne les voit pas et n'écoute pas les vocaux. Arnaud les retrouve dans WhatsApp.

## 1. Choisir le numéro (décision à prendre)
- **Option A, recommandée : garder le 06 78 02 04 24 en « coexistence ».** Arnaud continue d'utiliser l'app **WhatsApp Business** sur son téléphone, et l'API (donc l'agent) fonctionne sur le même numéro. Il voit toutes les conversations de l'agent et peut reprendre la main à tout moment.
  - Si le numéro est aujourd'hui sur WhatsApp « classique », il faut d'abord passer à l'app WhatsApp Business. Les discussions sont conservées.
  - L'inscription passe par le parcours Meta « connecter un compte WhatsApp Business existant ». Meta change souvent ce parcours : vérifier les conditions au moment de l'inscription (pays, ancienneté du compte).
- **Option B : un numéro dédié à l'agent** (nouvelle ligne). C'est plus simple côté Meta, mais il faut changer le numéro sur le site (`WHATSAPP_INT` dans `build_site.py`) et Arnaud ne voit les échanges que par la fiche.

## 2. Côté Meta (developers.facebook.com)
1. Créer un **portefeuille Meta Business** (business.facebook.com), au nom de SARL ARélec.
2. Créer une **app** de type « Business » et lui ajouter le produit **WhatsApp**. Y rattacher le numéro choisi à l'étape 1.
3. **Jeton permanent** : Paramètres de l'entreprise › Utilisateurs système › créer un utilisateur système « admin ». Générer un jeton avec les permissions `whatsapp_business_messaging` et `whatsapp_business_management`, puis le copier dans `WHATSAPP_TOKEN`.
4. Noter le **Phone number ID** (WhatsApp › Configuration de l'API) dans `WHATSAPP_PHONE_NUMBER_ID`, et le **secret de l'app** (Paramètres › Général) dans `WHATSAPP_APP_SECRET`.
5. **Webhook** (WhatsApp › Configuration) :
   - URL de rappel : `https://www.entreprise-arelec.fr/api/whatsapp`
   - Jeton de vérification : une phrase au choix, identique à `WHATSAPP_VERIFY_TOKEN`
   - Champs abonnés : `messages`, et `smb_message_echoes` en coexistence (c'est ce qui permet la pause quand Arnaud répond).
6. Passer l'app en mode **Live**.

## 3. Côté Vercel (Settings › Environment Variables)
| Variable | Obligatoire | Rôle |
|---|---|---|
| `OPENROUTER_API_KEY` | oui | IA du site et de WhatsApp |
| `OPENROUTER_MODEL` | non | modèle, `anthropic/claude-haiku-4.5` par défaut |
| `WHATSAPP_TOKEN` | oui | jeton permanent de l'utilisateur système |
| `WHATSAPP_PHONE_NUMBER_ID` | oui | identifiant du numéro |
| `WHATSAPP_VERIFY_TOKEN` | oui | phrase de vérification du webhook |
| `WHATSAPP_APP_SECRET` | fortement conseillé | vérifie que les appels viennent bien de Meta |
| `ARELEC_NOTIFY_WA` | non | n° perso d'Arnaud pour la fiche, format `336XXXXXXXX` |
| `ARELEC_NOTIFY_TEMPLATE` | non | nom d'un modèle Meta pour la fiche (voir § 5) |
| `WHATSAPP_GRAPH_VERSION` | non | version de l'API Graph, `v23.0` par défaut |

**Mémoire des conversations** : dans Vercel › Storage, ajouter **Upstash (Redis)** au projet. Les variables `KV_REST_API_URL` et `KV_REST_API_TOKEN` sont créées automatiquement. Sans Redis, l'agent oublie la conversation à chaque redémarrage de la fonction : ce n'est pas utilisable en production.

Redéployer après avoir ajouté les variables.

## 4. Tester
1. Depuis un autre téléphone, écrire au numéro ARélec : l'agent doit répondre en quelques secondes.
2. Faire le parcours complet depuis le site : assistant › « Continuer sur WhatsApp » › questions › fiche reçue par Arnaud.
3. Répondre une fois depuis l'app d'Arnaud : l'agent ne doit plus intervenir dans cette conversation.
4. Erreurs : Vercel › Logs, fonction `/api/whatsapp`.

## 5. Fiche envoyée à Arnaud
WhatsApp n'accepte un message libre vers Arnaud que s'il a écrit au numéro pro dans les dernières 24 h. Pour que la fiche arrive toujours, créer dans WhatsApp Manager un modèle de catégorie **Utilitaire**, en français, avec une seule variable :

> Nouvelle demande client : {{1}}

Une fois le modèle approuvé, mettre son nom dans `ARELEC_NOTIFY_TEMPLATE`. Les modèles sont facturés par Meta (voir leurs tarifs en vigueur). Les réponses aux clients qui écrivent en premier ne sont pas concernées.

En coexistence (option A), Arnaud voit déjà toutes les conversations dans son app : la fiche reste un résumé pratique, mais elle n'est pas indispensable.

## Essai local (sans Meta)
```bash
OPENROUTER_API_KEY=… WHATSAPP_TOKEN=x WHATSAPP_PHONE_NUMBER_ID=x WHATSAPP_VERIFY_TOKEN=x node dev-server.mjs
```
Sans vrai numéro, les réponses ne partent pas. Pour tester avec Meta avant la mise en ligne, exposer le port 4400 avec un tunnel (par exemple cloudflared) et mettre cette adresse comme webhook.
