Ce document présente le plan de tests pour le micro-service Triangulator. L'objectif est de garantir la fiabilité, la justesse, la performance et la qualité de l'implémentation.
## Strategie
- Écrire les tests avant l'implémentation
- Viser 100% pour la couverture du code
- priviliger les tests de qualité 
- faire differents type de test pour chacun (test unitaire, integration(pour la réponse API), performance)

Dans ce cas on peut utiliser l'algorithme de Triangulation de Delaunay:
Nombre de triangles = 2n - 2 - h où h est le nombre de points sur l'enveloppe convexe et n le nombre de sommets.

exemple: avec 5 points
Tous les 5 points sur l'enveloppe convexe (pentagone convexe)

Triangles = 2(5) - 2 - 5 = 3 triangles

4 points sur l'enveloppe convexe, 1 point à l'intérieur

Triangles = 2(5) - 2 - 4 = 4 triangles

3 points sur l'enveloppe convexe, 2 points à l'intérieur
Triangles = 2(5) - 2 - 3 = 5 triangles

## Tests
- test sur un PointSetId qui n'existe pas
- test de faire une triangulation avec pointsetID qui n'existe pas 
- test sur des points qui se retrouve dans la meme ligne = 0 triangle
- test sur un point qui a les meme coordonées donc une duplication de point 
- test de faire triangulation avec 0 point => c'est impossible 
- test de faire triangulation avec 1 point => c'est impossible 
- test de faire triangulation avec 2 point => c'est impossible 
- test conversion vers/depuis le format binaire => peuvent être des opérations gourmandes (données tronquées ou trop longues)
- test triangulation avec 10, 15 points 
- test transformer depuis binaire point
- test transformer vers binaire point
- test transformer depuis binaire triangle pour 1 ou plusieurs triangle
- test transformer vers binaire triangle pour 1 ou plusierus triangles
- test transformer vers/depuis binaire pour un/ plusieurs points 
- test pour des valeurs trop grandes 
- test 1 triangle rend 3 points (on peut faire pour plusieurs point mais ça sera compliqué) vers/depuis binaire  


### integration
- test api triangulation vrai
- test api point n'existe pas retourne une Bad request  
- test api triangulation temps de reponse  
- test plusieurs requete en meme temps
- test si un point est invalide (n'existe pas ou duplication ...etc)

### Tests de performance

- perf test triangulation 10 points : Temps pour 10 points
- perf test triangulation 100 points : Temps pour 100 points
- perf test triangulation 1000 points : Temps pour 1000 points
- perf test triangulation 10000 points : Temps pour 10000 point   

- perf test transformer vers binaire pointset large :  10000 points
- perf test transformer depuis binaire pointset large : 10000 points
- perf test pour les triangles exemple 500 ou 1000 triangle

## Risques et limitations identifiés
- Algorithme compliqué pour calculer un point il est sur l'enveloppe convexe
- eviter aussi pour l'utilisateur de mettre des valeurs compliqué comme pi
- eviter des valeurs trop grandes aussi ou l'inverse 