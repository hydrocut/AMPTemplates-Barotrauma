import sys, os, re, json
import xml.etree.ElementTree as ET
# Admins et modérateurs réglés dans AMP (Configuration > Barotrauma > Admins et modérateurs), appliqués avant chaque
# démarrage dans Data/clientpermissions.xml : la console d'AMP n'atteint pas Barotrauma (aucune réponse à giveperm),
# le fichier, lui, est relu au démarrage. Rangs copiés depuis Data/permissionpresets.xml (Admin, Moderator).
# Seuls les comptes posés par AMP sont retirés quand on les enlève de la liste : ceux donnés en jeu restent.
# Écrit en apostrophes seulement et sans antislash : ce texte est passé tel quel à python3 -c par AMP.
NL = chr(10)
def ids(texte):
    out = []
    for brut in re.split('[,; ]+', (texte or '').strip()):
        b = brut.strip().upper()
        if not b:
            continue
        if b.isdigit() and len(b) == 17 and b.startswith('7656'):
            n = int(b) - 76561197960265728
            b = 'STEAM_1:' + str(n % 2) + ':' + str(n // 2)
        if re.fullmatch('STEAM_[01]:[01]:[0-9]+', b):
            out.append('STEAM_1' + b[7:])
        else:
            print('Ignoré (pas un SteamID) : ' + brut)
    return out
admins, modos, dossier = ids(sys.argv[1]), ids(sys.argv[2]), sys.argv[3]
modos = [m for m in modos if m not in admins]
fichier = os.path.join(dossier, 'clientpermissions.xml')
memo = os.path.join(dossier, 'tk_amp_permissions.json')
presets = {}
try:
    for p in ET.parse(os.path.join(dossier, 'permissionpresets.xml')).getroot().iter('Preset'):
        presets[p.get('name')] = (p.get('permissions') or 'None', [c.get('name') for c in p.iter('Command')])
except Exception as e:
    print('permissionpresets.xml illisible : ' + str(e))
rangs = {'Admin': presets.get('Admin', ('All', [])), 'Moderator': presets.get('Moderator', ('ManageRound,Kick,SelectSub,SelectMode,ManageCampaign,ConsoleCommands,ServerLog,ManageSettings,ManageMoney,ManageBotTalents,SpamImmunity', []))}
try:
    racine = ET.parse(fichier).getroot()
except Exception:
    racine = ET.Element('ClientPermissions')
try:
    avant = set(json.load(open(memo, encoding='utf-8')))
except Exception:
    avant = set()
voulus = {i: 'Admin' for i in admins}
voulus.update({i: 'Moderator' for i in modos})
vus = set()
for c in list(racine.findall('Client')):
    aid = (c.get('accountid') or c.get('steamid') or '').upper()
    if aid in voulus:
        rang = voulus[aid]
        c.set('permissions', rangs[rang][0])
        for x in list(c.findall('command')) + list(c.findall('Command')):
            c.remove(x)
        for nom in rangs[rang][1]:
            ET.SubElement(c, 'command', {'name': nom})
        vus.add(aid)
    elif aid in avant:
        racine.remove(c)
        print('Retiré : ' + (c.get('name') or aid))
for aid, rang in voulus.items():
    if aid in vus:
        continue
    c = ET.SubElement(racine, 'Client', {'name': rang + ' (AMP)', 'accountid': aid, 'permissions': rangs[rang][0]})
    for nom in rangs[rang][1]:
        ET.SubElement(c, 'command', {'name': nom})
ET.indent(racine, space='  ')
with open(fichier, 'w', encoding='utf-8') as f:
    f.write('<?xml version=' + chr(34) + '1.0' + chr(34) + ' encoding=' + chr(34) + 'utf-8' + chr(34) + '?>' + NL + ET.tostring(racine, encoding='unicode') + NL)
json.dump(sorted(voulus), open(memo, 'w', encoding='utf-8'))
print('Admins AMP : ' + str(len(admins)) + ', modérateurs AMP : ' + str(len(modos)))
