# Agent WhatsApp ARélec — mise en service

## Ce que fait l'agent
1. Le prospect discute avec l'assistant du site, puis clique « Continuer sur WhatsApp ». Son message est prérempli : « Bonjour ARélec 👋 Je viens du site. Mon projet : … ».
2. Le message arrive sur le **06 78 02 04 24**. 360dialog le transmet au webhook `https://www.entreprise-arelec.fr/api/whatsapp` (`api/whatsapp.js`).
3. L'agent reprend la conversation **sans reposer ce qui est déjà dit**. Il pose une question à la fois : travaux, commune, neuf ou rénovation, urgence, photos (facultatives), disponibilités pour la visite, nom. Il ne donne jamais de prix ni de date.
4. Quand il en sait assez, il dit au client qu'Arnaud revient vers lui. Il peut aussi envoyer à Arnaud une **fiche prospect** (facultatif, voir § 5).
5. Arnaud garde son app **WhatsApp Business** et voit toutes les conversations. S'il répond lui-même, l'agent **se tait pendant 48 h** dans cette conversation.

Les photos et les vocaux sont signalés à l'agent (« [photo] »), mais il ne les voit pas et n'écoute pas les vocaux. Arnaud les retrouve dans son app.

## Choix retenu
Le numéro **06 78 02 04 24** reste sur l'app WhatsApp Business d'Arnaud. Il est branché à l'API en **coexistence** par l'intermédiaire de **360dialog**, un prestataire agréé par Meta.

## 1. Avant de commencer (Arnaud)
- Le 06 78 02 04 24 doit être sur l'app **WhatsApp Business**, et non sur WhatsApp classique. Pour passer de l'une à l'autre, installer WhatsApp Business et suivre la migration : les discussions sont conservées.
- Mettre l'app à jour. Le téléphone doit avoir un appareil photo, car il faudra scanner un QR code.
- Avoir un compte Facebook pour créer ou relier le **portefeuille Meta Business** de SARL ARélec.
- À la fin du branchement, WhatsApp Web et les autres appareils liés sont déconnectés. Il suffit de les reconnecter ensuite.

## 2. Chez 360dialog
1. Créer un compte sur hub.360dialog.com et choisir l'offre qui inclut la **coexistence** (« WhatsApp Business App » / « Coexistence »). Vérifier le tarif mensuel au moment de l'inscription.
2. Lancer l'inscription : connexion Facebook, choix du portefeuille Meta Business, puis l'option **« connecter un numéro déjà utilisé sur l'app WhatsApp Business »**.
3. Sur le téléphone d'Arnaud : scanner le QR code et confirmer dans l'app. Il peut choisir de partager l'historique, ce n'est pas nécessaire pour l'agent.
4. Dans le hub 360dialog, générer la **clé API** du numéro (`D360-API-KEY`). Attention : générer une nouvelle clé invalide l'ancienne.

## 3. Dans Vercel (Settings › Environment Variables)
| Variable | Obligatoire | Rôle |
|---|---|---|
| `OPENROUTER_API_KEY` | oui | IA du site et de WhatsApp |
| `OPENROUTER_MODEL` | non | modèle, `anthropic/claude-haiku-4.5` par défaut |
| `D360_API_KEY` | oui | clé API 360dialog du numéro |
| `WHATSAPP_WEBHOOK_KEY` | oui | longue phrase secrète au choix (ex. 40 caractères aléatoires) ; 360dialog la renvoie à chaque message pour prouver que c'est lui |
| `ARELEC_NOTIFY_WA` | non | n° perso d'Arnaud pour la fiche, format `336XXXXXXXX` |
| `ARELEC_NOTIFY_TEMPLATE` | non | nom du modèle de message pour la fiche (voir § 5) |

**Mémoire des conversations** : dans Vercel › Storage, ajouter **Upstash (Redis)** au projet. Les variables `KV_REST_API_URL` et `KV_REST_API_TOKEN` sont créées automatiquement. Sans Redis, l'agent oublie la conversation à chaque redémarrage de la fonction : ce n'est pas utilisable en production.

Redéployer après avoir ajouté les variables.

## 4. Brancher le webhook
Une fois le site redéployé, depuis le dossier du projet :
```bash
D360_API_KEY=… WHATSAPP_WEBHOOK_KEY=… node scripts/setup-360dialog.mjs
```
Le script indique à 360dialog d'envoyer les messages à `https://www.entreprise-arelec.fr/api/whatsapp`, avec l'en-tête secret. Il doit afficher un code `200`. Les deux valeurs doivent être **exactement** celles de Vercel.

## 5. Tester
1. Depuis un autre téléphone, écrire au 06 78 02 04 24 : l'agent doit répondre en quelques secondes. Arnaud doit voir l'échange dans son app.
2. Faire le parcours complet depuis le site : assistant › « Continuer sur WhatsApp » › questions › fin de qualification.
3. Répondre une fois depuis l'app d'Arnaud : l'agent ne doit plus intervenir dans cette conversation pendant 48 h.
4. En cas d'erreur, ouvrir Vercel › Logs, fonction `/api/whatsapp`. Un code `401` signifie que la phrase secrète diffère entre Vercel et le script.

## 6. Fiche envoyée à Arnaud (facultatif)
Arnaud voit déjà toutes les conversations dans son app : la fiche n'est qu'un résumé pratique sur un autre numéro (`ARELEC_NOTIFY_WA`). WhatsApp n'accepte un message libre vers ce numéro que s'il a écrit au numéro pro dans les dernières 24 h. Pour qu'elle arrive toujours, créer un modèle de catégorie **Utilitaire**, en français, avec une seule variable :

> Nouvelle demande client : {{1}}

Une fois le modèle approuvé, mettre son nom dans `ARELEC_NOTIFY_TEMPLATE`. Les modèles sont facturés par Meta (voir leurs tarifs en vigueur). Les réponses aux clients qui écrivent en premier ne sont pas concernées.

## Variante : Meta en direct (sans prestataire)
`api/whatsapp.js` sait aussi parler directement à Meta. Il faut alors ne pas définir `D360_API_KEY`, et renseigner `WHATSAPP_TOKEN` (jeton permanent d'un utilisateur système), `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_VERIFY_TOKEN` et `WHATSAPP_APP_SECRET`. Le webhook se configure alors dans l'app Meta avec les champs `messages` et `smb_message_echoes`. La coexistence n'est pas accessible par ce chemin sans implémenter le parcours d'inscription Meta (« Embedded Signup »).

## Essai local
```bash
OPENROUTER_API_KEY=… D360_API_KEY=… WHATSAPP_WEBHOOK_KEY=… node dev-server.mjs
```
Pour que 360dialog atteigne la machine locale, exposer le port 4400 avec un tunnel (par exemple cloudflared). Lancer ensuite `scripts/setup-360dialog.mjs` avec l'adresse du tunnel suivie de `/api/whatsapp`, puis remettre l'adresse du site après le test.
