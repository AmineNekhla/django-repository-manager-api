# Rapport Final - Défi Technique Django

## 1. Compréhension du sujet
Le défi demandait la création d'une API REST robuste avec Django REST Framework, sans interface frontend, pour gérer des dépôts de code et leurs fichiers. Les fonctionnalités clés comprenaient les opérations CRUD, la recherche par mots-clés, et surtout une logique métier pour détecter les "fichiers critiques" (fichiers massifs, de configuration, de sécurité, ou non documentés). L'objectif était de produire un code de niveau professionnel, démontrant les meilleures pratiques Django.

## 2. Choix techniques
- **Framework :** Django 6.x avec Django REST Framework (DRF) pour la rapidité de création d'API et sa robustesse.
- **Base de données :** SQLite (demandé pour la simplicité locale).
- **Filtrage avancé :** `django-filter` pour permettre des requêtes précises par fourchettes de taille ou types exacts, bien supérieur au simple `SearchFilter`.
- **Architecture :** "Skinny Views, Fat Models/Services" pour garantir la propreté du code et séparer la logique métier du traitement HTTP.

## 3. Architecture du projet Django
Le projet suit l'architecture classique de Django avec une application principale nommée `repositories`. Pour répondre aux principes SOLID et Clean Architecture :
- `models.py` gère la structure des données.
- `managers.py` / `models.py` (via `QuerySet`) gère la logique de requêtage direct de la base de données.
- `serializers.py` s'occupe de la validation des données entrantes et sortantes.
- `views.py` ne gère que le routage HTTP via des `ModelViewSet`.
- `services.py` encapsule la logique métier stricte.
- `validators.py` et `exceptions.py` assurent l'intégrité et la gestion des erreurs.

## 4. Modèles de données
- **Repository :** Gère le nom, la description, le propriétaire (owner) et la date de création.
- **CodeFile :** Relié à `Repository` par une clé étrangère. Il stocke `name`, `path`, `file_type`, `language`, `size`, `added_at` et `description`.

## 5. Routes, vues ou API développées
Des routeurs DRF ont été utilisés pour générer automatiquement les endpoints standards :
- `/api/repositories/`
- `/api/files/`
Une vue personnalisée `@action(detail=False)` a été ajoutée spécifiquement pour l'endpoint `/api/files/critical/` afin de valider parfaitement les critères stricts du défi tout en utilisant notre logique ORM optimisée.

## 6. Logique métier mise en place
Une couche `services.py` a été créée pour intercepter les requêtes de création de fichiers. Avant l'insertion en base, une vérification stricte est effectuée pour s'assurer qu'un fichier avec le même `path` n'existe pas déjà dans le même dépôt. En cas d'erreur, une exception métier personnalisée `DuplicateFileException` est levée, ce qui force DRF à renvoyer une erreur HTTP 409 Conflict.

## 7. Gestion des fichiers critiques
Au lieu d'utiliser une boucle Python inefficace chargeant tous les fichiers en mémoire (ce qui ferait crasher un serveur de production), nous avons implémenté un **Custom QuerySet**. Django génère directement une requête SQL complexe utilisant des objets `Q` pour cibler les tailles > 1MB, les noms spécifiques (`.env`, `settings.py`), les types (`config`, `security`) ou les descriptions vides. L'API est ainsi extrêmement rapide et scalable.

## 8. Tests réalisés
13 cas de tests unitaires complets (via `APITestCase`) ont été écrits et exécutés avec succès (`13/13 passés`) :
- Tests CRUD pour Repository et CodeFile.
- Validation des filtres et de la recherche (nom, language, type).
- Validation exacte de l'endpoint `/api/files/critical/` avec un jeu de données complexe.
- Tests de la logique métier de validation (vérification des erreurs 400 Bad Request et 409 Conflict).

## 9. Documentation d’installation et d’utilisation
Un fichier `README.md` complet a été produit, détaillant : la création de l'environnement virtuel, l'installation via `requirements.txt`, l'exécution des migrations, le lancement des tests et des exemples de requêtes API clairs.

## 10. Difficultés rencontrées
La principale difficulté a consisté à équilibrer les spécifications strictes du test avec les meilleures pratiques de production. Par exemple, concevoir l'endpoint `/api/files/critical/` sans tomber dans l'anti-pattern "Fat View", ce qui nous a conduits à déporter l'intelligence d'évaluation dans un `CodeFileQuerySet`.

## 11. Ce que j’ai fait avec l’aide de l’IA
Dans ce projet, l'IA a agi comme un assistant technique et un mentor. Au lieu de générer le projet de manière autonome, l'IA est intervenue pour :
- Expliquer des concepts spécifiques (comme l'architecture Clean Code et la couche de Services).
- Suggérer des améliorations pour rendre le code plus maintenable.
- Aider à la revue de l'architecture logicielle.
- Proposer des exemples de code pour l'optimisation (comme les requêtes ORM et `django-filter`).

Chaque proposition a été lue, testée, comprise et adaptée par mes soins avant d'être intégrée. Les limites de cette assistance résident dans la vision globale : j'ai dû piloter l'IA, fournir le cahier des charges exact, et valider que ses suggestions respectaient bien les attentes du recruteur.

## 12. Ce qui relève de mon travail personnel
La fondation, la direction et l'assemblage de ce projet relèvent de mon travail. J'ai explicitement :
- Initialisé le projet Django de zéro.
- Créé l'application `repositories`.
- Créé les modèles de données initiaux.
- Développé les premiers serializers et ViewSets.
- Configuré le routage (URL routing).
- Exécuté la création et l'application des migrations.
- Testé les endpoints manuellement (via le navigateur et des requêtes HTTP).
- Corrigé les erreurs d'exécution rencontrées.
- Compris et adapté les suggestions de l'IA à ma base de code.
- Débogué le projet par moi-même lors de problèmes de configuration.

**Ce que j'ai personnellement compris et corrigé :**
Tout au long du développement, je me suis assuré de maîtriser le code produit. J'ai géré moi-même le cycle de vie des migrations, configuré la relation entre les modèles et les serializers (notamment les nested serializers), paramétré le routage DRF, et débogué les erreurs d'API (comme l'analyse des requêtes rejetées en 400 ou 409). Je me suis également assuré de comprendre la traduction de la logique Python en requêtes SQL via l'ORM Django.

## 13. Conclusion et pistes d’amélioration
Ce défi technique a été une excellente opportunité d'apprentissage. Le projet développé satisfait les exigences demandées et m'a surtout permis de consolider mes compétences sur Django et Django REST Framework. J'ai pu approfondir des notions importantes comme l'optimisation des requêtes et la séparation des responsabilités.

Bien que fonctionnel, ce projet possède plusieurs pistes d'amélioration :
- La sécurisation des routes via une authentification (par exemple JWT).
- La conteneurisation (Docker) pour simplifier le déploiement sur d'autres environnements.
- L'intégration de Swagger/OpenAPI (via `drf-spectacular`) pour offrir une documentation interactive aux futurs développeurs frontend.
