# API EDC (execution de code)

Ce projet a pour but d'exécuter du code de manière isolé et sécurisé dans des containers docker.

## Technologies Utilisées

- **Python**
- **Flask** : Api python
- **SDK Python Docker** : Piloter l'exécution des dockers
- **Docker** : Conteneurisation
- **Socket IO** : Transmission des résultats

## Fonctionnalités
Nous pouvons pour l'instant exécuter du code en :
- java 11, 17, 21
- javascript


## Configuration

### Prérequis

- Avoir à sa disposition un docker host en local

### Installation

1. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

2. Configurer le .env (voir `.env.example`)


### Exécution de l'Application

Il nous faut démarrer 5 services.
- Rabbitmq
- Redis Server
- Worker (tâches celery)
- Serveur Socket IO
- API Flask


1. **Rabbit MQ :**
   Si vous ne disposez pas d'un service rabbitmq, vous pouvez l'installer avec un container docker :
    ```bash
       docker run -p 15672:15672 -p 5672:5672 rabbitmq:3-management
    ```

   URL: http://127.0.0.1:15672/#/

2. **Redis :**

   Si vous ne disposez pas d'un serveur redis, vous pouvez l'installer avec un container docker :
     ```bash
     docker run -p 6379:6379 -e ALLOW_EMPTY_PASSWORD=yes redis:latest
    ```

3. **Worker**
   Executer du code peut parfois être très long. Pour ne pas bloquer le threaad principal nous avons implémenté des workers
   celery qui se chargeront d'exécuter le code

     ```bash
     celery -A tasks worker --concurrency=2 -n worker@%h --loglevel=info
    ```

   **Monitor**
   Nous pouvons monitorer le tout via flower.
     ```bash
     celery flower --broker=amqp://guest:guest@127.0.0.1:5672//  --broker-api=http://127.0.0.1:15672/api/ --result-backend=redis://127.0.0.1:6379/0 --port=5555
    ```
   URL: http://127.0.0.1:5555/tasks

4. **Serveur Socket IO**
   Une fois qu'un worker a finit sa tâche, il transmet le résultat au serveur socket io. A son tour, ce serveur émettra
   à l'aide de l'identifiant de la tâche le résultat correspondant. Bien sur, pour réceptionner le résultat, il faut un client
   qui écoute l'évènement.

    ```bash
      python socketServer.py
    ```
5. **API Flask**
   L'api flask permet de recevoir le code ainsi que d'autres données pour pouvoir exécuter du code. Elle fait
   donc appel ainsi à un worker pour faire le travail en la mettant dans une queue (rabbit mq)
    ```bash
      python flaskApi.py
    ```

   Vous pouvez utiliser des outils comme Postman ou curl pour faire des requêtes :

   ```bash
   POST http://localhost:5000/execute-code

   {
       "code": "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello, World!\"); } }",
       "language": "java",
       "version": "17",
       "uuid": "1"
   }
   ```