# ======================== game.py ========================
from turtle import width

import pygame
import random

from pygame.constants import K_LEFT, K_RIGHT, K_a, K_d

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_VELOCITY, SPRING_JUMP_VELOCITY,
    DOODLE_SPEED, DOODLE_WIDTH, DOODLE_HEIGHT, PLATFORM_WIDTH,
    MIN_PLATFORM_GAP, MAX_PLATFORM_GAP, CAMERA_SCROLL_THRESHOLD,
    PLATFORMS, doodle_dict, DOODLE_START_X, DOODLE_START_Y, LIVES
)
from platforms import create_platform, choose_platform_type
from doodle import doodle_left_img, doodle_right_img
from window import generate_initial_platforms


# ======================== PARTIE 3.1 ========================
def apply_gravity():
    """
    Applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y).
    Met à jour la position verticale (y) du Doodle.
    """
    # TODO : Mettez à jour la vitesse verticale puis la position verticale
    # du Doodle à partir de GRAVITY.

    # La gravité augmente la vitesse verticale vers le bas
    doodle_dict["vel_y"] += GRAVITY
    # La vitesse modifie la position verticale du Doodle
    doodle_dict["y"] += doodle_dict["vel_y"]
    return


# ======================== PARTIE 1.2 ========================
def move_doodle():
    """
    Gère le déplacement horizontal du Doodle selon les touches pressées (Flèches ou A/D).
    Implémente le passage fluide d'un côté de l'écran à l'autre (Screen Wrap).
    """
    keys = pygame.key.get_pressed()

    # TODO : Gérez les déplacements gauche/droite et mettez à jour
    # simultanément la direction et l'image du Doodle.

    # Ici je test si l'utilisateur est en train d'appuyer sur le bouton gauche ou droite
    if keys[K_LEFT] or keys[K_a]:
        doodle_dict["direction"] = "left"
        doodle_dict["image"] = doodle_left_img
        doodle_dict["x"] -= DOODLE_SPEED  # on change la position du doodle on modifie vitesse

    if keys[K_RIGHT] or keys[K_d]:
        doodle_dict["direction"] = "right"
        doodle_dict["image"] = doodle_right_img
        doodle_dict["x"] += DOODLE_SPEED

    # TODO : Implémentez le Screen Wrap pour qu'une partie du Doodle puisse
    # sortir d'un côté avant de réapparaître de l'autre.
    # N'utilisez pas de dimensions numériques écrites directement.

    # ici je teste si le doodle dpace la longueur de l'écran, alors je le remet à gauche et vice-verça
    # j'ai pris -DOODLE_WIDTH parce que la position (0,0) on voit le personnage, mais il est coller au coin
    # pour que on test si il dépasse côté gauche il faut que on fasse moins commeça son extrémité droite est juste avant le (0,0)
    if doodle_dict["x"] > SCREEN_WIDTH:
        doodle_dict["x"] = (-DOODLE_WIDTH)

    if doodle_dict["x"] < (-DOODLE_WIDTH):
        doodle_dict["x"] = SCREEN_WIDTH

    return


# ======================== PARTIE 2.3 ========================

def move_platforms():
    """
    Déplace horizontalement les plateformes mobiles ("blue").
    Fait rebondir les plateformes lorsqu'elles atteignent les bords de la fenêtre.
    """
    for i in PLATFORMS:
        # 1. Vérification que la plateforme est bleue et active
        if i["type"] == "blue" and i["active"]:
            # 2. Déplacement horizontal de la plateforme
            i["x"] += i["vx"]

            # 3. Détection de collision avec les bords de l'écran
            # - Bord gauche : i["x"] <= 0
            # - Bord droit : i["x"] + i["width"] >= SCREEN_WIDTH
            if i["x"] <= 0 or (i["x"] + i["width"]) >= SCREEN_WIDTH:
                # Inversion du sens de la vitesse
                i["vx"] = -i["vx"]

    return


def rects_collide(r1, r2):
    """Teste le chevauchement de deux rectangles (x, y, largeur, hauteur)."""
    x1, y1, w1, h1 = r1
    x2, y2, w2, h2 = r2
    return (x1 < x2 + w2) and (x1 + w1 > x2) and (y1 < y2 + h2) and (y1 + h1 > y2)

    # ===========================================================

    # ======================== PARTIE 3.2 ========================
    """
    Détecte si le Doodle atterrit sur une plateforme.
    Le rebond ne se produit QUE lorsque le Doodle descend (vel_y > 0)
    et qu'il arrive sur le dessus d'une plateforme.
    """
    # TODO : Implémentez la détection d'un atterrissage.
    # def rects_collide(r1, r2):


def check_platform_collisions():
    # Le Doodle ne peut atterrir que s'il est en phase de descente
    if doodle_dict["vel_y"] <= 0:
        return

    # Rectangle actuel du Doodle (utilisation des variables globales DOODLE_WIDTH et DOODLE_HEIGHT)
    doodle_rect = (
        doodle_dict["x"],
        doodle_dict["y"],
        DOODLE_WIDTH,
        DOODLE_HEIGHT
    )

    # Position des pieds actuelle et précédente
    doodle_feet_current = doodle_dict["y"] + DOODLE_HEIGHT
    doodle_feet_previous = doodle_feet_current - doodle_dict["vel_y"]

    for plat in PLATFORMS:
        # Ignorer les plateformes inactives
        if not plat.get("active", True):
            continue

        plat_rect = (plat["x"], plat["y"], plat["width"], plat["height"])

        # Vérifier le chevauchement des rectangles
        if rects_collide(doodle_rect, plat_rect):
            plat_top = plat["y"]

            # Vérifier l'atterrissage par le dessus avec la tolérance de 14 pixels
            is_landing = (
                    doodle_feet_previous <= plat_top + 14 and
                    doodle_feet_current >= plat_top
            )

            if is_landing:
                plat_type = plat.get("type", "green")

                # Appliquer le rebond selon le type de plateforme
                if plat_type == "spring":
                    doodle_dict["vel_y"] = SPRING_JUMP_VELOCITY
                elif plat_type == "brown":
                    doodle_dict["vel_y"] = JUMP_VELOCITY
                    plat["active"] = False  # La plateforme marron disparaît/devient inactive
                else:
                    doodle_dict["vel_y"] = JUMP_VELOCITY

                # Un seul rebond traité par appel
                break

    return
    # Contraintes :
    # - aucun rebond pendant la montée ;
    # - ignorer les plateformes inactives ;
    # - utiliser rects_collide(...) pour le chevauchement des rectangles ;
    # - un simple chevauchement ne suffit pas : le Doodle doit arriver par
    #   le dessus de la plateforme. Pour le vérifier, comparez la position
    #   actuelle de ses pieds à leur position approximative à l'image
    #   précédente à l'aide de vel_y. Une tolérance de 14 pixels est permise ;
    # - spring : SPRING_JUMP_VELOCITY ;
    # - brown : JUMP_VELOCITY puis désactivation de la plateforme ;
    # - green/blue : JUMP_VELOCITY.

    return


# ======================== PARTIE 3.3 ========================
def scroll_camera():
    """
    Fait défiler le monde lorsque le Doodle dépasse CAMERA_SCROLL_THRESHOLD.
    Met à jour le score et maintient les plateformes visibles.
    """
    # TODO : Lorsque le Doodle dépasse le seuil de caméra, il doit rester
    # visuellement au seuil pendant que les plateformes sont déplacées vers
    # le bas de la même distance.
    #
    # Le score doit représenter la distance verticale ainsi parcourue et le
    # meilleur score doit être mis à jour. Les plateformes sorties sous
    # l'écran doivent être retirées, puis de nouvelles plateformes générées.

    if doodle_dict["y"] < CAMERA_SCROLL_THRESHOLD:

        # c'est la distance dotn tout le monde doit descendre pour que le jeux redevienne à jour
        distance = CAMERA_SCROLL_THRESHOLD - doodle_dict["y"]

        doodle_dict["y"] = CAMERA_SCROLL_THRESHOLD
        # gérer le score
        doodle_dict["score"] += int(distance)

        # gérer le high score
        if doodle_dict["score"] > doodle_dict["high_score"]:
            doodle_dict["high_score"] = doodle_dict["score"]

        for platform in PLATFORMS[:]:
            platform["y"] += distance  # on décale la position des plateforms vers le bas

            # supression des platforms hors de l'écran
            if platform["y"] > SCREEN_HEIGHT:
                PLATFORMS.remove(platform)
        generate_new_platforms()

    return


# ===========================================================


# ======================== PARTIE 3.4 ========================
def generate_new_platforms():
    """
    Génère de nouvelles plateformes au-dessus du haut de l'écran pour maintenir
    un flux continu lorsque la caméra défile.
    """
    # TODO : Complétez cette fonction en vous inspirant de la logique de
    # génération initiale, sans la recopier inutilement.
    #
    # Vous devrez partir de la plateforme actuellement la plus haute et
    # continuer à ajouter des plateformes tant que nécessaire. Utilisez
    # choose_platform_type(...) avec les probabilités indiquées dans le README.

    # on vérifie d'abord si la liste PLATFORM contient quelque chose
    if len(PLATFORMS) > 0:
        # la plateform la plus haute aura le plus petit y
        maxHauteur = min(p["y"] for p in PLATFORMS)  # retourne la platfrom la plus haute
        current_y = maxHauteur - random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)

    else:
        # on choisi une hauteur par defaut pour le prochain current_y
        current_y = SCREEN_HEIGHT

    while (current_y > -MAX_PLATFORM_GAP):# pour éviter d'avoir un trou
        platform_cree = create_platform(
            random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH),
            current_y,
            choose_platform_type(0.55, 0.20, 0.13)
        )

        # il faut modifier la position du current_y sinon on aura une boucle infinie
        current_y -= random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)

        PLATFORMS.append(platform_cree)

    return


# ===========================================================


def check_game_over():
    """
    Vérifie si le Doodle tombe sous le bas de l'écran.
    Si oui, réduit les vies.
    Retourne True si la partie est terminée.
    """
    if doodle_dict["y"] > SCREEN_HEIGHT:
        doodle_dict["lives"] -= 1
        return True
    return False


def restart_game():
    """
    Réinitialise la partie : position du Doodle, vitesse, score et plateformes.
    """
    doodle_dict["x"] = DOODLE_START_X
    doodle_dict["y"] = DOODLE_START_Y
    doodle_dict["vel_y"] = 0.0
    doodle_dict["direction"] = "right"
    doodle_dict["image"] = doodle_right_img
    doodle_dict["score"] = 0
    doodle_dict["lives"] = LIVES

    generate_initial_platforms()


def rects_collide(r1, r2):
    """
    Vérifie si deux rectangles (x, y, largeur, hauteur) se chevauchent.
    Cette fonction est fournie et ne doit pas être modifiée.
    """
    return not (
            r1[0] + r1[2] <= r2[0] or r1[0] >= r2[0] + r2[2] or
            r1[1] + r1[3] <= r2[1] or r1[1] >= r2[1] + r2[3]
    )
