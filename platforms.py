# ======================== platforms.py ========================

import os
import random
import pygame
from config import ASSETS_DIR, PLATFORM_SIZE, MOVING_PLATFORM_SPEED

# Chargement des différentes images de plateformes
platform_green_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_green.png"))
platform_green_img = pygame.transform.scale(platform_green_img, PLATFORM_SIZE)

platform_blue_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_blue.png"))
platform_blue_img = pygame.transform.scale(platform_blue_img, PLATFORM_SIZE)

platform_brown_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_brown.png"))
platform_brown_img = pygame.transform.scale(platform_brown_img, PLATFORM_SIZE)

platform_spring_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_spring.png"))
platform_spring_img = pygame.transform.scale(platform_spring_img, (PLATFORM_SIZE[0], PLATFORM_SIZE[1] + 10))

# Dictionnaire d'accès aux images selon le type de plateforme
platform_images = {
    "green": platform_green_img,
    "blue": platform_blue_img,
    "brown": platform_brown_img,
    "spring": platform_spring_img
}


# ======================== PARTIE 2.1 ========================
def create_platform(x, y, platform_type="green"):
    """
    Crée et retourne un dictionnaire représentant une plateforme.

    Le dictionnaire ci-dessous représente pour l'instant correctement une
    plateforme verte. Votre travail consiste à le généraliser afin qu'il
    représente aussi correctement les plateformes bleues, marron et à ressort.
    """

    platform = {
        "x": float(x),
        "y": float(y),
        "type": platform_type,  # TODO
        "image": platform_images[platform_type],  # TODO
        "vx": MOVING_PLATFORM_SPEED if platform_type == "blue" else 0.00,  # TODO
        "active": True,
        "width": PLATFORM_SIZE[0],
        "height": (PLATFORM_SIZE[1] + 10) if platform_type == "spring" else PLATFORM_SIZE[1]  # TODO
    }

    # TODO : Modifiez le dictionnaire ci-dessus pour qu'il dépende réellement
    # de l'argument platform_type.

    #
    # Contraintes :
    # - l'image doit être obtenue à partir de platform_images ;
    # - une plateforme bleue se déplace à MOVING_PLATFORM_SPEED ;
    # - une plateforme à ressort est 10 pixels plus haute ;
    # - les autres plateformes sont immobiles et gardent la hauteur normale.

    return platform


# ===========================================================


# ======================== PARTIE 2.2 ========================
def choose_platform_type(green_probability, blue_probability, spring_probability):
    """
    Choisit aléatoirement un type de plateforme.

    Les trois paramètres donnent les probabilités respectives des plateformes
    verte, bleue et à ressort. La probabilité restante correspond à une
    plateforme marron.
    """

    # TODO : Utilisez random.random() et les probabilités reçues en paramètres
    # pour retourner l'une des chaînes suivantes :
    # "green", "blue", "spring" ou "brown".

    # on veut déterminer ce sera quelle platefrome
    # les arguments sont les extrémités pour avoir chaque plateforme

    random_number = random.random()

    if random_number < green_probability:
        return "green"

    elif random_number < blue_probability + green_probability:
        return "blue"

    elif random_number < spring_probability + blue_probability + green_probability:
        return "spring"

    else:
        return "brown"

    # Attention : les seuils utilisés avec random.random() doivent être
    # cumulatifs.


# ===========================================================

# Questions
# ecq il faut enlever le =green a l'argument de platform_type dans la focntion crete platfrom


'''
Explication de choose_platform_type

On reçoit en paramètre (3) nomrbes entre 0 et 1 représentant des probabilités 
on créer un nombre random de 0 à 1 nommé random_number

exemple:
green_probability=0.3
blue_probability=0.2

on test:
si le random_number est entre 0 et green_probability --> ça va retourner la couleur verte

si le random_number est entre green_probability et (green_probability + blue probability) --> return bleu  
   ==> if random_number < (green_probability:0.3 +blue_probability: 0.2)
    Donc si random_number est entre 0.3 et 0.5 --> l'écart est de 0,2 donc notre condition marche , car blue_probability=0.2

'''
