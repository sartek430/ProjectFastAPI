# Application FastAPI

Cette application FastAPI est un exemple de base pour une application Web utilisant le framework FastAPI, SQLAlchemy et SQLite. Elle présente une architecture simple avec des modèles de données, des routes API et une intégration avec une base de données SQLite.

## Contenu de l'application

L'application comprend les éléments suivants :

- **Modèles de données** : Les modèles de données définissent la structure des tables de la base de données. Les modèles inclus dans cette application sont :

  - `User` : Représente un utilisateur avec des attributs tels que `firstName`, `lastName`, `email`, `password` et `role`.

    |   firstName  |  lastName   |     email       |    password    |    role    |
    |--------------|-------------|-----------------|----------------|------------|
    |    John      |    Doe      | john@example.com |   password123  |   user     |

  - `Company` : Représente une entreprise liée à un utilisateur avec des attributs tels que `name`, `address` et une clé étrangère `fk_user` pour référencer l'utilisateur propriétaire.

    |     name      |    address   |    fk_user    |
    |---------------|--------------|---------------|
    |   Company A   | 123 Main St  |      1        |
    |   Company B   | 456 Oak St   |      1        |

  - `Planning` : Représente un planning avec des attributs tels que `day`, `start_time` et `end_time`.

    |      day      | start_time  |  end_time   |
    |---------------|-------------|-------------|
    |    2023-05-17 |  09:00 AM   |   10:00 AM  |
    |    2023-05-18 |  02:00 PM   |   04:00 PM  |

  - `Activity` : Représente une activité liée à un planning avec des attributs tels que `name` et une clé étrangère `fk_planning` pour référencer le planning.

    |     name      |  fk_planning |
    |---------------|--------------|
    |   Activity A  |      1       |
    |   Activity B  |      2       |

- **Routes API** : L'application expose plusieurs routes API pour effectuer des opérations CRUD (Create, Read, Update, Delete) sur les modèles de données. Les principales routes API incluses sont :

  - `/users` : Gère les opérations sur les utilisateurs.
  - `/companies` : Gère les opérations sur les entreprises.
  - `/plannings` : Gère les opérations sur les plannings.
  - `/activities` : Gère les opérations sur les activités.

- **Base de données** : L'application utilise SQLite comme base de données pour stocker les données. La configuration de la base de données se trouve dans le fichier `database.py`.

## Prérequis

Avant de lancer l'application, assurez-vous d'avoir les éléments suivants installés sur votre système :

- Python 3.x
- Pip (le gestionnaire de paquets Python)

## Installation

1. Clonez ce dépôt sur votre machine locale :

   ```bash
   git clone https://github.com/sartek430/ProjectFastAPI.git
   ```

2. Accédez au répertoire du projet :

   ```bash
   cd app
   ```

3. Installez les dépendances nécessaires en exécutant la commande suivante :

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Avant de lancer l'application, vous pouvez modifier certains paramètres de configuration si nécessaire :

- Dans le fichier `database.py`, vous pouvez modifier les détails de connexion à la base de données, tels que le nom du fichier de la base de données.

## Lancement de l'application

Une fois les étapes d'installation et de configuration terminées, vous pouvez lancer l'application en exécutant la commande suivante :

```bash
uvicorn main:app --reload
```

L'application sera alors accessible à l'adresse [http://localhost:8000/docs](http://localhost:8000/docs).

---

Pour vous connecter à l'application, utilisez les informations d'identification suivantes :

- Email : `string`
- Mot de passe : `string`

Cet utilisateur a le rôle de `user`.