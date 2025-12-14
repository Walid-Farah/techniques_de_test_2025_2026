# TODO

## 1. Méthodologie et Approche de Développement

### L'approche Test-First
L'adoption de l'approche **Test-First** a été un atout majeur pour ce projet. Elle m'a permis de :
- Clarifier les attentes avant même de commencer le développement.
- Avoir une idée précise du résultat attendu pour chaque fonction.
- Guider l'architecture du code en se basant sur son utilisation réelle plutôt que sur une implémentation théorique.


### Le Cycle Red-Green-Refactor
Après avoir écrit mes tests et commencé l’implémentation de l’algorithme, je suis ensuite passé au cycle **Red-Green-Refactor**:
1. **Red** : Écriture d'un test qui échoue.
2. **Green** : Implémentation du code minimal pour faire passer le test.
3. **Refactor** : Amélioration et nettoyage du code.

Cette discipline m'a permis d'avancer sereinement et d'atteindre un objectif ambitieux : **100% de couverture de code**. Toutes les fonctions sont aujourd'hui testées et validées.

## 2. Difficultés Techniques Rencontrées

### Les Mocks et l'API
L'un des principaux obstacles a été la compréhension et l'utilisation des **Mocks**, particulièrement au sein de l'API.
- J'ai eu du mal à saisir la logique d'isolation : simuler le comportement d'une dépendance sans l'exécuter réellement.
- C'était cependant nécessaire pour tester les routes de l'API indépendamment de la logique métier complexe.

### L'Algorithme de Delaunay
L'implémentation de l'algorithme de triangulation de Delaunay s'est avérée très complexe. La traduction des formules mathématiques et des concepts géométriques en un code fonctionnel et robuste a représenté un défi majeur.

### Les Tests de Performance
Afin de garantir la viabilité du projet, j'ai dû mettre en place des tests de performance stricts (visibles dans `test_perf_triangulate.py`). Cela a impliqué :
- **Montée en charge** : Validation de l'algorithme sur des sets de 10, 100 et 1000 points.
- **Contraintes de temps** : Respect de seuils critiques (ex: < 1.0s pour 100 points, < 30.0s pour 1000 points).
- **Sérialisation** : Optimisation des entrées/sorties avec des tests sur 10 000 points pour s'assurer que la conversion des données ne ralentisse pas le processus global.

## 3. Découverte d'Outils

Ce projet a été l'occasion de découvrir des outils puissants qui ont amélioré ma productivité :

- **Ruff** : Un linter et formateur incroyablement rapide qui m'a aidé à maintenir un code propre.
- **Coverage** : Indispensable pour visualiser les zones non testées et atteindre les 100% de couverture.