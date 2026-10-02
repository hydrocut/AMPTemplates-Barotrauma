# AMPTemplates-Barotrauma — Barotrauma (TeamKit) pour AMP

Template **AMP Generic Module** pour serveur dédié Barotrauma. Il reprend le template officiel
de CubeCoders et corrige la **graphie de quatre réglages** que Barotrauma a renommés depuis.

## Le problème qu'il règle

Sur un serveur hébergé par TeamKit, le nom saisi dans AMP n'apparaissait jamais dans le
navigateur de serveurs. En comparant les 72 réglages du template au `serversettings.xml` écrit
par le jeu lui-même, sept attributs visés par AMP n'existaient pas côté jeu.

Barotrauma a changé le nom de ces attributs. Le template officiel est resté sur l'ancienne
forme. AMP écrivait donc des attributs que le jeu ne lit pas — et le jeu, qui réécrit le
fichier quand il s'arrête, les effaçait au passage. La boucle était parfaite : le réglage
semblait enregistré dans AMP, et n'avait aucun effet.

## Ce qui est corrigé

| Réglage AMP | Le template officiel écrit | Barotrauma lit |
|---|---|---|
| Server Name | `name` | **`ServerName`** |
| Auto Restart | `autorestart` | **`AutoRestart`** |
| Server Message | `ServerMessage` | **`ServerMessageText`** |
| Level Difficulty | `LevelDifficulty` | **`SelectedLevelDifficulty`** |

Chacun de ces noms a été relevé dans un `serversettings.xml` **écrit par le jeu**, pas deviné.

Le modèle `serversettings.xml` livré par ce template porte lui aussi la bonne graphie.

## Ce qui n'est volontairement PAS corrigé

Trois réglages du template officiel n'atteignent pas non plus le jeu, mais on ne peut pas les
réparer sans risquer d'écrire n'importe quoi :

- **Allowed Mission Types** — deux candidats existent côté jeu (`MissionTypes` et
  `AllowedRandomMissionTypes`), qui n'attendent pas la même chose. Trancher au hasard ferait
  pire que le laisser inerte.
- **Allow Respawning** — remplacé par `RespawnMode`, qui n'est plus un booléen mais un mode.
  Y écrire `True` ou `False` ne produirait rien d'exploitable.
- **Allow Ragdoll Button** — ce réglage n'existe plus dans le jeu.

Ils restent donc présents dans l'interface AMP, sans effet, comme dans le template officiel.
Les corriger demande de vérifier le comportement réel du jeu réglage par réglage.

## Installation

1. Panel AMP → **ADS** → Configuration → *Configuration Repositories*, ajouter :

```
hydrocut/AMPTemplates-Barotrauma:main
```

2. Rafraîchir le catalogue des templates.
3. Créer l'instance en choisissant **Barotrauma (TeamKit)** dans la liste.

Le template porte son propre `AppConfigId` : il cohabite avec le Barotrauma officiel sans le
remplacer ni entrer en conflit avec lui.

## Ce qu'il faut savoir en l'utilisant

- **AMP écrit `serversettings.xml` au démarrage du serveur.** Un réglage modifié pendant que
  le serveur tourne ne prend effet qu'au redémarrage suivant. Ce n'est pas propre à ce
  template, mais c'est la deuxième cause de « j'ai changé et il ne se passe rien ».
- **Le jeu réécrit ce fichier quand il s'arrête**, dans son propre format. Tout attribut qu'il
  ne connaît pas disparaît alors. C'est ce qui rendait le problème d'origine si déroutant.

## Crédits

Template d'origine : **Greelan** et **ThisIslandEarth**, dans
[CubeCoders/AMPTemplates](https://github.com/CubeCoders/AMPTemplates). Ce dépôt n'en est
qu'une variante corrigée — tout le travail de fond leur revient.

Corrections et maintenance : [TeamKit](https://www.teamkit.fr).

## Admins et modérateurs depuis AMP (3 oct. 2026)

La console d'AMP n'atteint pas Barotrauma : `giverank`, `giveperm` ou `revokeperm` tapés dans AMP ne reçoivent
aucune réponse du jeu. Le jeu relit en revanche `Data/clientpermissions.xml` à chaque démarrage.

**Configuration → Barotrauma → Admins et modérateurs** : deux listes de SteamID64 (`7656…`), séparés par une
virgule ou une espace. Avant chaque démarrage, l'étape `barotraumateamkitstart.json` (script `outils/permissions_amp.py`,
passé à `python3 -c`) les écrit dans le fichier avec les rangs **Admin** et **Moderator** de `Data/permissionpresets.xml`.

- Retirer quelqu'un de la liste lui retire le rang au redémarrage suivant.
- Seuls les comptes posés par AMP sont retirés (mémo `Data/tk_amp_permissions.json`) : les droits donnés en jeu restent.
- Un SteamID `STEAM_0:Y:Z` est aussi accepté.

Le script ne doit contenir **ni guillemet double ni antislash** : il est passé tel quel dans les arguments de l'étape.
Après toute modification de `outils/permissions_amp.py`, relancer le générateur pour régénérer `barotraumateamkitstart.json`.
