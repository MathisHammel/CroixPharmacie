# CroixPharmacie

Ce projet permet de contrôler à distance l'affichage d'une croix de pharmacie. Si vous n'avez pas la chance de posséder une croix de pharmacie chez vous, le code vous permet également de simuler l'affichage localement.

![Chute de sable sur une croix de pharmacie](Sandfall.gif)

## Comment contribuer ?

Si vous souhaitez proposer un module (animation, jeu, etc.) pour la croix de pharmacie, c'est très simple : n'hésitez pas à vous inspirer du fichier [example.py](example.py) ou des autres modules.

Tout le contrôle de la croix de pharmacie (réelle ou simulée) passe par l'objet `pharmacontroller.PharmaScreen`. Pour afficher une image sur l'écran, utilisez sa méthode `set_image(img)`, où `img` est un tableau de 48x48 pixels sous formes de nombres flottants, compris entre 0.0 (noir) et 1.0 (vert).

Certaines zones de `img` sont inutilisées, car on affiche les pixels sur une croix et non un carré : vous pouvez y mettre n'importe quelle valeur. Pour vérifier si une coordonnée de pixel est sur la croix, utilisez la méthode `is_drawable` sur l'objet `PharmaScreen`

Pour des raisons matérielles, la croix gère deux modes de couleur :
- `PharmaScreen(color_scale=True)` peut afficher jusqu'à 8 nuances de vert, avec un taux de rafraîchissement de 20 FPS. C'est l'option par défaut.
- `PharmaScreen(color_scale=False)` ne gère que 2 couleurs (noir/vert), mais peut afficher jusqu'à 60 FPS.

## Liste des modules

- Exemple - [example.py](src/croix_pharmacie/mains/example.py)
- Affichage d'une vidéo avec le son - [videoplayer.py](videoplayer.py)
- Jeu pong imaginé par [le_egar](https://twitter.com/le_egar/status/1517539004627001346), avec 4 joueurs - [pong.py](src/croix_pharmacie/mains/pong.py)
- Doom (voir instructions ci-dessous) - [doom.py](src/croix_pharmacie/mains/doom.py)
- Simulation de chute de sable - [falling_sand_simulation.py](src/croix_pharmacie/mains/falling_sand_simulation.py)
- Simon says - [simon.py](src/croix_pharmacie/mains/simon.py)
- Snake - [snake.py](src/croix_pharmacie/mains/snake.py)
- Animation d'un cube rotatif - [cube.py](src/croix_pharmacie/mains/cube.py)
- Affichage de texte - [textwriter.py](src/croix_pharmacie/mains/textwriter.py)
- Effets visuels - [visual_effects.py](src/croix_pharmacie/mains/visual_effects.py)
- Spirale hypnotique - [youreundercontrol.py](src/croix_pharmacie/mains/youreundercontrol.py)
- Plasma - [plasma.py](src/croix_pharmacie/mains/plasma.py)
- Rotozoom - [rotozoom.py](src/croix_pharmacie/mains/rotozoom.py)

## Installation
Pour juste l'installer : `pip install git+https://github.com/MathisHammel/CroixPharmacie`
Si vous voulez faire des modifications `pip install --editable git+https://github.com/MathisHammel/CroixPharmacie`

Pour ajouter des features vous pouvez aussi installer [rye](https://rye.astral.sh/) puis faire:
* `rye sync`
* `rye run pong` (si vous voulez lancer le pong par example)

## Une idée à ajouter ?

Les pull requests sont les bienvenues sur ce dépôt ! Et si vous envoyez votre code d'ici la fin du mois (juin 2024), vous aurez potentiellement la chance de le voir être exécuté sur une vraie croix de pharmacie 😉

Pour soumettre une idée si vous n'êtes pas en mesure de coder, n'hésitez pas à créer [une issue GitHub](https://github.com/MathisHammel/CroixPharmacie/issues), ou m'envoyer des propositions en [DM sur Twitter](https://twitter.com/MathisHammel).

## Comment jouer à Doom ?
Utilisez les flèches pour vous déplacer, Ctrl gauche pour tirer, et la barre espace pour ouvrir les portes.
