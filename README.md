# Widgets in Pygame

Un module Python implémentant quelques classes de widgets utilisables dans l'environnement Pygame.

## Types de widgets

- classe abstraite `Widget`
- classe abstraite `Container`
  - `Window/Frame` (`Window` a des décorations, tandis que `Frame` est juste un `Container`)
- `Label`
- classe abstraite `Button`

  - `StandardButton`
  - `CancelButton`

- `TextEntry`

## Cahier des charges

Un `Widget` doit pouvoir être affiché et réagir aux événements.

Un `Window/Frame` doit contenir des sous-Widgets (éventuellement eux-même des `Window/Frame`) et ses méthodes d'affichage et de réaction doivent non-seulement s'exécuter pour l'élément lui-même mais aussi pour ses enfants.

Chaque `Widget` doit avoir un certain nombre d'événements standards (cliquer dedans, fermeture, …) et certains événements spéciaux (Valider une entrée/bouton) auxquels il doivent réagir et il doit être facile d'ajouter la réaction spécifique souhaitée (via un callback).

Les événements vont cascader depuis le général au spécifique et il faut qu'un callback puisse arrêter la cascade, par exemple en retournant False.

Il faut que le module soit aussi facile que possible à rajouter à un programme Pygame et que la documentation indique clairement la procédure nécessaire.
