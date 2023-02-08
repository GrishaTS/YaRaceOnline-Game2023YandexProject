# YaRaceOnline

![flake8 test](https://github.com/GrishaTS/YaRaceOnline-Game2023YandexProject/actions/workflows/python-package.yml/badge.svg)

## Contents
* [About](#about)

* [Deployment instructions](#deployment-instructions)
  * [Cloning project](#1-cloning-project-from-github)
  * [Activation venv](#2-creation-and-activation-venv)
  * [Requirements](#3-installation-all-requirements)
  * [.Env](#4-generate-file-with-virtual-environment-variables-env)
  * [Running](#5-running-project)
* [Database](#database)
  * [ER-diagram](#er-diagram)


## About

This project is the second credit project at the Yandex Academy Lyceum. This is a racing game that can be played alone or together online over a local network.

![Image of the race between two users](https://github.com/GrishaTS/YaRaceOnline-Game2023YandexProject/raw/main/media_for_README/two-cars.png)
![Image of the victory](https://github.com/GrishaTS/YaRaceOnline-Game2023YandexProject/raw/main/media_for_README/victory.png)
![Image of the garage](https://github.com/GrishaTS/YaRaceOnline-Game2023YandexProject/raw/main/media_for_README/garage.png)
***

## Deployment instructions


### 1. Cloning project from GitHub

1.1 Run this command
```commandline
git clone https://github.com/GrishaTS/YaRaceOnline-Game2023YandexProject
```

### 2. Creation and activation venv

2.1 First of all, from root directory run this command
```commandline
python -m venv venv
```
2.2 Then run this command to activate venv
#### Mac OS / Linux
```commandline
source venv/bin/activate
```
#### Windows
```commandline
.\venv\Scripts\activate
```

### 3. Installation all requirements

3.3 Run this command 
```commandline
pip install -r requirements.txt
```
### 4. Generate file with virtual environment variables (.env)

4.1 Generate file '.env' in root directory with such structure
```text
IPv4=YOUR-IPv4-address
DATABASE=YOUR-DATABASE-FILE
```

### 5. Running project

5.1 Run this command
```commandline
python main.py
```

***

## ER-diagram
![Image of the ER-diagram](https://github.com/GrishaTS/YaRaceOnline-Game2023YandexProject/raw/main/media_for_README/ER-diagram.png)

***
