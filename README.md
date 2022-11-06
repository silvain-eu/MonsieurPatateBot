<p align="center">
  <a href="https://mpatate.silvain.eu/">
    <img alt="mpatate" src="https://mpatate.silvain.eu/favicon.png" width="128"/>
  </a>
</p>

<h1 align="center">Monsieur Patate Bot</h1>
<p align="center">
 <a href="https://drone.silvain.eu/Silvain.eu/MonsieurPatatePhp">
  <img src="https://drone.silvain.eu/api/badges/Silvain.eu/MonsieurPatatePhp/status.svg"/>
 </a>
</p>

Bot discord pour consulter l'emploi du temps de ADE ULCO (https://edt.univ-littoral.fr/).

Cette application s'inscrit dans le cadre d'un projet composé de 3 dépôts :
- [MonsieurPatatePhp](https://github.com/silvainlud/MonsieurPatatePhp/edit/main/README.md) : Site web permettant la consultation de l'emploi du temps et la gestion des devoirs. Cette application embarque également les scripts réalisant l'actualisation de l'emploi du temps et l'envoi de notifications lorsque cela est nécessaire.
- [MonsieurPatatePlanning](https://github.com/silvainlud/MonsieurPatatePlanning) : Script JS faisant des captures d'écran de l'emploi du temps fourni par ADE ULCO
- **MonsieurPatateBot** : Bot discord pour consulter l'emploi du temps

## Technologie

Ce bot est écrit avec python avec la bibliothéque [discord.py](https://pypi.org/project/discord.py/). 
L'application est déployée à travers une image docker publiée sur un dépôt privé d'images Docker.


## Fonctionnalités

- Récupérer les captures d'écran réalisé par le projet [MonsieurPatatePlanning](https://github.com/silvainlud/MonsieurPatatePlanning)
- Ajouter une commande "SLASH" à un serveur discord pour consulter ces captures

## Installation de l'environnement de développement

### Pré-requis

Pour démarrer l'environnement, vous devez avoir les outils suivants :
- [Python](https://www.python.org/)
- [Pip](https://pypi.org/project/pip/)

### Instruction

Il faut tout d'abord installer les dépendances :
```
pip install --no-cache-dir -r requirements.txt
```

Puis, pour lancer l'appplication, il suffit de saisir la commande suivante :
```
python -u ./main.py
```

**Attention :** il ne faut pas oublier de configurer l'application à l'aide du fichier `.env`:

- `token` : Jeton d'authentification au service discord
- `clientId` : Identifiant du client discord
- `voiceCategoryName`
- `db_host` : Hôte de la base de données
- `db_username` : nom d'utilisateur de la base de données
- `db_password` : mot de passe de l'utilisateur de la base de données
- `db_database` : nom de la base de données

## Déploiement

Ce projet est déployé automatiquement par un service [Drone.Io](https://www.drone.io/), qui constuit une Image Docker puis qui l'envoie dans sur un registre d'image privé.

## Licence

Ce projet est sous la licence [GNU General Public License v3.0](LICENSE) - voir le fichier  [LICENSE.md](LICENSE) pour les détails.
