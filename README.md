# Veille-Informatique
Bot discord pour centraliser les FluxRSS

## Sommaire

* #### [Intro](https://github.com/AetherBlack/Veille-Informatique#user-content-intro-1)
* #### [Téléchargement](https://github.com/AetherBlack/Veille-Informatique#user-content-téléchargement-1)
* #### [Installation des libs](https://github.com/AetherBlack/Veille-Informatique#user-content-installation-des-libs-1)
* #### [Création du bot](https://github.com/AetherBlack/Veille-Informatique#user-content-création-du-bot-1)
* #### [Lancement du bot](https://github.com/AetherBlack/Veille-Informatique#user-content-lancement-du-bot-1)
* #### [Flux RSS](https://github.com/AetherBlack/Veille-Informatique#user-content-flux-rss-1)
* #### [Finalisation](https://github.com/AetherBlack/Veille-Informatique#user-content-finalisation-1)
* #### [Bonus - Changement du temps entre deux vérification](https://github.com/AetherBlack/Veille-Informatique#user-content-bonus---changement-du-temps-entre-deux-vérification-1)

## Intro

Ce bot a pour but de vous aider dans la centralisation des informations contenues dans les fluxrss que vous auriez potentiellement utilisé.

J'ai personnellement utilisé ce bot pour ma Veille Informatique de BTS SIO.

## Téléchargement

* Linux

```
git clone https://github.com/AetherBlack/Veille-Informatique
```

* Windows

Vous pouvez télécharger le fichier zip sur [ce lien](https://github.com/AetherBlack/Veille-Informatique/archive/master.zip).

## Installation des libs

* Linux

```
pip3 install -r requirements.txt
```

* Windows

```
pip3 install -r requirements.txt
```

OU

```
LECTEUR:\PATH\TO\Python3\Scripts\pip3.exe install -r LECTEUR:\PATH\TO\PROJECT\requirements.txt
```

## Création du bot

Rendez-vous sur le site web developer de discord : https://discordapp.com/developers/applications

Connectez-vous avec votre compte ou créez en un.

Créer ensuite une application. 

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/1.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/2.PNG">

Puis rendez-vous dans la section "SETTINGS>BOT" sur le panneau de gauche.

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/3.PNG">

Cliquez ensuite sur "Add Bot" > "Yes, do it!". Votre bot est créé.

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/4.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/5.PNG">

Il faut maintenant créer le serveur. Depuis l'application discord sur le panneau de gauche : "Add a server" > "Create a server" > "Nom de votre serveur" > "Create". Au passage créer un channel spécifique si vous avez besoin.

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/6.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/7.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/8.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/9.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/10.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/11.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/12.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/13.PNG">

Lancez ensuite le lien suivant en remplacement YOUR_CLIENT_ID_HERE dans votre URL par votre CLIENT ID qui se situe sur la page developer de discord toujours sur la partie gauche "SETTINGS>General Information" : https://discordapp.com/oauth2/authorize?client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=536083519

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/14.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/15.PNG">

Le site va alors vous demander de vous authentifiez. Si vous êtes déjà authentifié avec votre compte alors sélectionné votre serveur dans la liste déroulante "ADD BOT TO:" puis "Continue". Laissez lui tous les droits et enfin faite "Authorize". Validez le captcha et votre bot sera sur votre serveur.

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/16.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/17.PNG">
<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/18.PNG">

## Lancement du bot

Pour que le bot fonctionne il va falloir modifier deux valeurs.

Premièrement depuis la section "SETTINGS>BOT" sur le portail developers de discord récupéré le TOKEN de votre bot.

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/19.PNG">

Une fois celui-ci copié, collé-le dans le fichier ```const/__init__.py``` à la place de "YOUR_BOT_TOKEN".

```python
#Token
TOKEN = "YOUR_BOT_TOKEN" #<= ICI
#TOKEN = "Njk4ODg2OTI2NjUyMDE0NjIz.XpMXYA.zR_25AujmbkulKsIOBc-04ca9zg"
```

Ensuite, il va falloir récupérer l'ID du channel pour que le bot envoie les notifications sur celui-ci.

Récupérer le code ci-dessous et collé le dans un fichier python. Remplacé à nouveau "YOUR_TOKEN_BOT" par votre TOKEN dans le script et exécuter le.

```python
#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from discord.ext import commands, tasks

import sys

TOKEN = "YOUR_BOT_TOKEN"
#TOKEN = "Njk4ODg2OTI2NjUyMDE0NjIz.XpMXYA.zR_25AujmbkulKsIOBc-04ca9zg"

# Prefix du bot
bot = commands.Bot(command_prefix='!')

# Au lancement
@bot.event
async def on_ready():
    print("Logged in as {0}\n{1}".format(bot.user.name, bot.user.id))
    print("------------------")
    # Recuperation de l'id des channels
    global channel
    channel = list()
    for guild in bot.guilds:
        #print(guild.channels)
        channel.append(guild.channels)
    await bot.close()

if __name__ == "__main__":
    bot.run(TOKEN)
    
    for index in range(len(channel[0])):
        print(channel[0][index].name, channel[0][index].id)
```

Dans mon cas j'ai une catégorie nommé "FluxRSS" et un channel nommé "notifications". Je vais donc récupérer l'ID du channel "notifications".

Après l'exécution du script. Vous devriez avoir une liste de channel ainsi que leur id correspondant.

*Les ID si dessous sont à titre d'exemple*
```
Logged in as Veille Informatique
111111111111111111
------------------
Flux RSS 222222222222222222
notifications 333333333333333333
```

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/20.PNG">

Récupérer l'id de votre channel et collé le à nouveau dans le fichier ```const/__init__.py``` à la variable "CHANNEL_RSS" :

```python
#CHANNEL FLUX RSS -> NOTIF ID
CHANNEL_RSS = INT_CHANNEL # <= ICI
#CHANNEL_RSS = 698887787075862559
```

## Flux RSS

Maintenant que votre bot est quasi fonctionnement il ne vous reste plus qu'à mettre vos lien de fluxrss dans la variable FLUX_RSS toujours dans le fichier ```const/__init__.py``` :

*Les liens ci-dessous sont des fluxrss de Google Alertes pour le WPA-3 à titre d'exemple*
```python
#Flux RSS
FLUX_RSS = ["https://www.google.com/alerts/feeds/10044275366631447452/1055738863244347746",
            "https://www.google.com/alerts/feeds/10044275366631447452/5208661666063475899",
            "https://www.google.fr/alerts/feeds/10044275366631447452/3528165564465536219",
            "https://www.google.fr/alerts/feeds/10044275366631447452/9042324707641309434"]
```

Remplacer donc les valeurs actuellements définis par les votres

```python
FLUX_RSS = ["REPLACE_WITH_RSS_LINK",
            "https://www.google.com/alerts/feeds/10044275366631447452/5208661666063475899"]#<= Exemple de FluxRSS avec Google Alertes
```

## Finalisation

Une fois cela fait il reste plus qu'à lancer votre bot discord.

```
$ python3 main.py

Logged in as Veille Informatique
686300298574168078
------------------
```

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/21.PNG">

Vous pouvez le laisser tourné h24 sur un raspberry ou alors le lancer quand cela vous chantes. Libre à vous.

Sous Linux vous pouvez mettre l'éxécution du script en tâche de fond en ajout le caractère "&" à la fin de votre commande :

```
$ python3 main.py &

Logged in as Veille Informatique
686300298574168078
------------------
```

<img src="https://github.com/AetherBlack/Veille-Informatique/blob/master/image/22.PNG">

## Bonus - Changement du temps entre deux vérification

Le bot vérifie par défaut toute les heures s'il y a des nouvelles news.

Pour changer cette valeur, modifier la variable "WAIT_NEW_NEWS" dans le fichier ```const/__init__.py```

```python
WAIT_NEW_NEWS = 60 * 60#Each hours
```

Si vous avez des questions ou que vous rencontrez des problèmes, contactez moi à : yohan.fevre@protonmail.com
