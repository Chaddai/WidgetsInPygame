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

Un programme Pygame minimal ressemble à ceci :

```python
# on importe la librairie pygame
import pygame
# pour plus de clarté, on importe les constantes dans notre espace de nom
from pygame.locals import *

# on initialise pygame (système de son, polices, graphismes...)
pygame.init()

# on crée une fenêtre (ou un plein écran avec l'option FULLSCREEN)
# pygame a des sous parties comme display qui s'occupe de l'affichage
window = pygame.display.set_mode( (800,600) )

# une variable pour indiquer si le programme est en train de tourner
running = True
# la boucle principale qui tourne en permanence pour modifier l'affichage
# et gérer les évènements
while running:
    # à chaque tour de boucle, on inspecte les événements (clavier, souris, ...)
    for event in pygame.event.get(): # get() renvoie et vide la liste des événements

        # event.type indique le type d'événement :
        # - KEYDOWN : appui sur une touche
        # - KEYUP : relache d'une touche
        # ...
        # QUIT : un événement spécial émis par l'OS lorsque l'on clique sur la croix
        # ou l'on appuie sur Alt+F4 (sous Windows)
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            # on met fin à la boucle
            running = False

    # ici on modifie l'affichage si nécessaire, par exemple en remplissant la
    # fenêtre d'une couleur unie (en rvb) :
    window.fill( (255,0,0) )

    # ATTENTION : par défaut pygame est en mode double buffer, ce qui veut dire
    # que toute vos manipulation de window sont uniquement faite en mémoire,
    # pour envoyer votre window modifiée sur l'écran il faut utiliser flip()
    pygame.display.flip()

# on arrête proprement les systèmes pygame (uniquement nécessaire si le programme
# n'est pas tout à fait fini)
pygame.quit()
```

Autrement dit :

```python
import pygame
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode( (800,600) )

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            running = False


    window.fill( (255,0,0) )
    pygame.display.flip()

pygame.quit()
```

Les `Widget` de `wipyg` héritent de [pygame.Sprite](https://www.pygame.org/docs/ref/sprite.html) donc on est censé les placer dans des [pygame.Group](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group) pour ensuite les mettre à jour et les manipuler en masse. On peut les positionner en manipulant leur attribut `rect` du type [pygame.Rect](https://www.pygame.org/docs/ref/rect.html) qui a beaucoup de propriétés pratiques pour cela.

```python
import pygame
from pygame.locals import *

from wipyg import *

pygame.init()

window = pygame.display.set_mode( (800,600) )

label = Label("hello")
entry = Entry("", length=10)
entry.rect.topright = (800,0)
widgets = Group(label, entry)

running = True
while running:
    for event in pygame.event.get():

        # Les Widgets ont une méthode react qu'on doit appeler pour qu'ils
        # réagissent correctement aux événements
        for w in widgets:
            w.react(event)

        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            running = False

    window.fill( (255,0,0) )
    widgets.update()
    widgets.draw(window)

    pygame.display.flip()

pygame.quit()
```

Noter que les widgets qui héritent de `Container` s'occupent de leurs enfants tout seul, il n'est pas nécessaire de les parcourir.
