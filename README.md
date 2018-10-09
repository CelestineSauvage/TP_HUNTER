# Shark vs Fish

## Objectif
L'objectif du Tp est de similué un environement proi prédateur, pour ce faire nous avons 2 agents.
Les poissons, ils pouvent se déplacer et se reproduire dans l'environement et les requins, qui 
peuvent se déplacer, se reproduire et manger les poissons dans l'environement.

## Implémentation

## Question
1. Est-il préférable d'initialiser les agents avec les mêmes valeurs pour les 3 différents compteurs
ou initialiser ces compteurs aléatoirement?
Il n'est pas préférable d'initialisé les même valeurs, en effet selon la taille de la grille et la disposition, les requins 
vont disparaitre, ou les poisson.
Il est plus préférable d'adapter les valeur au environement.

2. Testez différents variantes comportementales. Quels sont les comportements qui donnent les 
meilleures dynamique?
    * Une action à chaque tick : soit manger, soit se reproduire, soit bouger
    * Se reproduire en bougeant
    * Se reproduire en mangeant
Vous fournirez notamment la Courbe d'évolution du nombre de Fishes et de Sharks et de la courbe
d'évolution du nombre de Fishes sur le nombre de Sharks pour chacun de ces cas.