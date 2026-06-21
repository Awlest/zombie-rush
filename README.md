# 🧟 Zombie Rush

Jeu mobile type *speedrun / crowd-shooter* : fais grossir ton escouade dans des portails
multiplicateurs, ramasse des armes et explose des hordes de zombies sur **25 niveaux**
(avec un boss tous les 5 niveaux).

**PWA** 100 % statique (HTML + Canvas, aucune dépendance) → installable sur Android et jouable hors-ligne.

## Jouer en local
```bash
# depuis ce dossier
python -m http.server 5599
# puis ouvrir http://localhost:5599
```
(le service worker / l'installation PWA nécessitent http(s), pas l'ouverture directe du fichier)

## Contenu
| Fichier | Rôle |
|---|---|
| `index.html` | Tout le jeu (UI + moteur Canvas) |
| `manifest.json` | Manifest PWA (nom, icônes, plein écran portrait) |
| `sw.js` | Service worker (cache hors-ligne) |
| `icon-192.png` / `icon-512.png` | Icônes (maskable) |
| `make_icons.py` | Régénère les icônes (pur Python, sans dépendance) |

## Déployer (lien partageable)
Hébergement statique gratuit, ex. **GitHub Pages** :
1. Pousser ce dossier sur un repo public.
2. Settings → Pages → Branch `main` / `/root`.
3. Le jeu est en ligne sur `https://<user>.github.io/<repo>/`.

Partage le lien : sur Android, **Chrome → menu ⋮ → « Installer l'application »** ajoute
l'icône Zombie Rush à l'écran d'accueil (plein écran, hors-ligne).

## Transformer en vrai APK (optionnel)
Via [PWABuilder](https://www.pwabuilder.com) : coller l'URL → *Android Package* → télécharge un
`.apk`/`.aab` signé (technologie TWA) à installer ou publier sur le Play Store.

## Réglage de la difficulté
Tout est centralisé dans `index.html` :
- `levelCfg(L)` — quota de zombies, cadence de spawn, taille des groupes, par-temps (étoiles)
- `WEAPONS` — armes et stats / `ZTYPES` — types de zombies / `makeBoss(L)` — vie des boss
- `GATE_OPS` — combinaisons de portails
