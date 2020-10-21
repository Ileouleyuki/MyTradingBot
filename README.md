<a href="http://python.org"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png" title="python" alt="python" height="100px" width="100px"></a>
<a href="https://www.xtb.com/fr"><img src="https://pbs.twimg.com/profile_images/3718376798/b718c617db10b113feb5d002ff642b6e.png" title="XTB" alt="XTB" height="100px" width="100px"></a>
<a href="#"><img src="https://jollafr.org/wp-content/uploads/2015/02/raspberry-logo.png" title="RPI" alt="RPI" height="100px" width="300px"></a>

[![Python](https://img.shields.io/badge/Python-3.7-blue)](https://img.shields.io/badge/hdfgh-dfghdfgh-blue)
[![Maitenance](https://img.shields.io/badge/Maintenance-OUI-blue)](https://img.shields.io/badge/Maintenance-OUI-blue)
[![Licence](https://img.shields.io/badge/Licence-MIT-blue)](https://img.shields.io/badge/Licence-MIT-blue)

# MyTradingBot

Il s'agit d'une tentative de créer un script de trading de marché autonome à l'aide de XTB
API REST et toute autre source de données disponible pour les prix du marché.

RobotTrader est censé être un processus «permanent» qui maintient et
analyse les marchés en prenant des mesures pour savoir si certaines conditions sont remplies.
C'est à mi-chemin d'un projet académique et un véritable morceau utile de
logiciel, je suppose que je vais voir comment ça se passe :)

L'objectif principal de ce projet est de fournir la capacité de
rédigez une stratégie de trading personnalisée avec un minimum d'effort.
RobotTrader gère toutes les choses ennuyeuses.

# Table des Matieres

- [Dependances](#Dependances)
- [Changelog](CHANGELOG.md)
- [Installation](#Installation)
- [Configuration](#Configuration)
- [Execution](#Execution)
- [Auteur](#Auteur)
- [License](#License)

# Dependances

- Python 3.7+
- Docker (optionnel)

# Installation

Installer Raspbian et demarrer

### 1 - Parametrage Raspbian 

Lancer : `sudo raspi-config`

- Changer la disposition du clavier
- Changer le mot de passe root
- Changer le hostname
- Changer la configuration reseau Pour le Wifi
- Mettre à jour

```
sudo apt-get update
sudo apt-get upgrade
```

### 2 - Mettre à jour en IP Fixe

Configurer le reseau sur Raspbian

```
sudo nano /etc/dhcpcd.conf
```

et rajouter

```
# configuration ip static pour wlan0
interface wlan0
static ip_address=192.168.1.20/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
```

### 3 - Connecter vous en ssh

Connexion en SSH au RaspBerry Pi

```
ssh pi@192.168.1.20
```

### 4 - Installation de git

Installation du client git sur la Respbian

```
sudo apt-get install git
```

### 5 - Cloner le repo

Cloner le repo en local 

```
git clone https://github.com/Ileouleyuki/RobotTrader.git
chmod +x RobotTrader/install/install.sh
```

### 6 - Executer

Lancer le script d'installation

```
./RobotTrader/install/install.sh
```

### 7 - Superviser

Superviser le fonctionnement du bot

```
tail -n 25 -f /home/pi/RobotTrader/log/activity.log
```


# Manuel

A FAIRE

# Execution

```bash
python -m RobotTrader
```

# Auteur

* **Ileouleyuki** - *Createur* - [ileouleyuki](https://github.com/Ileouleyuki)
