# Widgets in Pygame

Un module Python implémentant quelques classes de widgets utilisables dans l'environnement Pygame.

## Types de widgets

- classe abstraite `Widget`
- classe abstraite `Container`
  - `Window` avec une barre de titre (qu'on peut déplacer, réduire et fermer depuis la barre)
  - classe abstraite `GridContainer` gérant le placement des widgets contenus sur une grille.
    - `Frame`
- `Label`
- classe abstraite `Button`

  - `PlainButton` : classe parente pour les boutons basiques avec des variantes
    - `CancelButton`
    - `SubmitButton`
  - `IconButton`

- `Entry`

## Cahier des charges

- Un `Widget` doit pouvoir être affiché et réagir aux événements (et on doit pouvoir désactiver ces réactions à la demande).

- Un `Window/Frame` doit contenir des sous-Widgets (éventuellement eux-même des `Window/Frame`) et ses méthodes d'affichage, de réaction et de mises à jour doivent non-seulement s'exécuter pour l'élément lui-même mais aussi pour ses enfants.

- Chaque `Widget` doit avoir un certain nombre d'événements standards (cliquer dedans, fermeture, …) et certains événements spéciaux (Valider une entrée/bouton) auxquels il doivent réagir et il doit être facile d'ajouter la réaction spécifique souhaitée (via un callback).

- Les événements vont cascader du Widget au Container et il faut qu'un callback puisse arrêter la cascade, par exemple en retournant True.

- Il faut que le module soit aussi facile que possible à rajouter à un programme Pygame et que la documentation indique clairement la procédure nécessaire.

- L'`Entry` doit réagir au clavier et à la souris de façon propre.

## Installation

En se plaçant dans le répertoire de ce README, on peut utiliser les commandes suivantes sous Linux :

    > python3 -m venv venv
    > source venv/bin/activate
    > pip3 install .

ou sous Windows :

    > python -m venv venv
    > venv\Scripts\activate
    > pip install .

Et il devient alors possible d'exécuter les scripts dans le répertoire `demo`.

## Documentation

L'API est documentée en deux emplacements :

- Doxygen produit une documentation sèche ne comprenant pas bien les spécificités des docstrings Python mais génère un [schéma de la hiérarchie](doc/html/classwipyg_1_1abstracts_1_1_widget.html) des classes très clair et utile.
- D'un autre côté pour une documentation un peu plus abordable, on peut se reporter à la [production de pdoc3](html/wipyg/index.html).

### Tutorial minimal
