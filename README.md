# Mini API de Gestion Docker

Ce projet fournit une API simple pour build et gérer des conteneurs Docker pour executer du code de manière isolé

## Technologies Utilisées

- **Python** 
- **Flask** : Api python
- **SDK Python Docker** : Utilisé pour build/run des images/container
- **Docker** : Conteneurisation

## Configuration

### Prérequis

- Bibliothèque Flask installée
- SDK Python Docker installé

### Installation

1. **Installer les dépendances :**

   ```bash
   pip install docker
   ```

   ```bash
   pip install flask
   ```

### Exécution de l'Application

1. **Démarrer l'application Flask :**

   ```bash
   python api.py
   ```

   Ceci démarrera le serveur Flask sur `http://localhost:5000`.

2. **Faire des requêtes à l'API :**

   Vous pouvez utiliser des outils comme Postman ou curl pour faire des requêtes :

   ```bash
   POST http://localhost:5000/build

   {
      "language": "java",
      "uuid": "1"
   }
   ```
