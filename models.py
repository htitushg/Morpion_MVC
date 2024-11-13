import datetime
import json
import os
from datetime import datetime
from logging import DEBUG
from timeit import repeat
from tkinter import *
import random
from debian.changelog import keyvalue
from numpy.ma.core import true_divide

from controller import *
from random import choice
import pandas
import time
from pickle import dump, load
from enum import Enum

class Cellule:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Categorie(Enum):
    humain = 1
    ordinateur = 2

def random_gen():
    seed = int(time.time()) ^ int(time.perf_counter() * 1_000_000)
    random.seed(seed)
    return random.randint(1, 1000)


class Joueur:
    def __init__(self, nom_joueur: str, categorie: str, motif: str, motif_texte:str):  # categorie: humain ou ordinateur
        self.nom:str = nom_joueur
        self.categorie=categorie
        self.motif:PhotoImage = PhotoImage(file = motif)  # à choisir parmi les motifs proposés
        self.motif_texte:str= motif_texte
        self.resultat = Model.Etats[0]
        self.status=""
        # Créationn de la grille du joueur
        self.grille = {}
        for ligne in range (3):
            for colonne in range (3):
                self.grille[ligne,colonne] = 0

class Model:

    modes = ['Choisir_mode', 'automatique', 'un_joueur', 'deuxjoueurs']
    categories = ["Quel_type_de_joueur", "humain", "ordinateur"]
    niveaux = ["Choisir_niveau", "Facile", "Difficile", "Expert"]
    Etats = ["En Cours", "Gagne", "Perdu", "Null"]
    # création du tableau des lignes, des colonnes et des diagonales
    alignements = [[(0, 0), (1, 0), (2, 0)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
                   [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
                   [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]

    status :str=Etats[0]

    def __init__(self, controller, mode_choisi, nom_1, nom_2, categorie_1_choisie, categorie_2_choisie, niveau_choisi, joueur_qui_commence):
        self.joueur_1 = Joueur(nom_1, categorie_1_choisie, "cercle.png", "O")
        self.joueur_2 = Joueur(nom_2, categorie_2_choisie, "croix.png", "X")
        self.controller=controller
        self.mode=mode_choisi
        self.niveau=niveau_choisi
        self.joueur_qui_commence=joueur_qui_commence
        if joueur_qui_commence == self.joueur_1.nom:
            self.joueur_en_cours = self.joueur_1
        else:
            self.joueur_en_cours = self.joueur_2

        self.gameOn = True
        self.taille_grille = 3
        self.grille = self.creer_grille()


    @staticmethod
    def new(controller, mode_choisi, nom_1, nom_2, categorie_1_choisie, categorie_2_choisie, niveau_choisi, joueur_qui_commence) -> "Model":
        print("Mode choisi:", mode_choisi)
        print("Nom joueur 1:", nom_1)
        print("Catégorie du joueur 1:", categorie_1_choisie)
        print("Nom joueur 2:", nom_2)
        print("Catégorie du joueur 2:", categorie_2_choisie)
        print("Niveau choisi:", niveau_choisi)
        print("Joueur qui commence:", joueur_qui_commence)
        #Appel du constructeur Model : "__init__"
        return Model( controller, mode_choisi, nom_1, nom_2, categorie_1_choisie, categorie_2_choisie, niveau_choisi, joueur_qui_commence)


    def creer_grille(self):
        """Crée une grille de 9 cases avec des coordonnées x et ligne."""
        grille = {}
        for ligne in range(self.taille_grille):
            for colonne in range(self.taille_grille):
                grille[colonne, ligne] = '-'
        return grille

    def mettre_a_jour_la_grille(self, ligne, colonne):
        self.grille[ligne, colonne] = self.joueur_en_cours.motif_texte
        self.joueur_en_cours.grille[ligne, colonne] = 1
        self.afficher_grille(self.grille)
        self.afficher_grille(self.joueur_en_cours.grille)

    def afficher_grille(self,grille):
        """Affiche la grille sous forme de tableau."""
        # Affichage avec formatage pour un tableau plus visuel

        print("+---+---+---+")
        for ligne in range(3): # Pour chaque ligne
            for colonne in range(3): # Pour chaque colonne
                print(f"| {grille[colonne, ligne]} ", end="")
                if colonne == 2 :
                    print("|")
                    print("+---+---+---+")

        print()

    def countAlign(self, align:int) :
        match align:
            case 1:
                return 5
            case 0:
                return 3
            case 3:
                return 1
            case _: # included 4
                return 0

    def permutter_joueurs(self):
        if self.joueur_en_cours == self.joueur_1:
            self.joueur_en_cours = self.joueur_2
        else:
            self.joueur_en_cours = self.joueur_1

    def donne_autre_joueur(self):
        if self.joueur_en_cours==self.joueur_1:
            return self.joueur_2
        return self.joueur_1

    def tableau_des_cases_vides(self) -> list[tuple[int, int]]:
        tab_coord: list[tuple[int, int]] = []  # Initialisation du tableau
        for ligne in range(self.taille_grille):
            for colonne in range(self.taille_grille):
                if self.grille[ligne,colonne] == '-':
                    tab_coord.append((ligne, colonne))
        return tab_coord

    def evaluercellule(self, ligne, colonne)->int:
        grille_J1=self.joueur_en_cours.grille
        grille_J2=self.donne_autre_joueur().grille
        line= grille_J1[ligne,0] + grille_J1[ligne,1] + grille_J1[ligne,2] + ((grille_J2[ligne,0] + grille_J2[ligne,1] + grille_J2[ligne,2]) * 3)
        column= grille_J1[0,colonne] + grille_J1[1,colonne] + grille_J1[2,colonne] + ((grille_J2[0,colonne] + grille_J2[1,colonne] + grille_J2[2,colonne]) * 3)
        isdiagonal_1 : bool = False
        isdiagonal_2 : bool = False
        match colonne:
            case 0:
                if ligne==0:
                    isdiagonal_2 = True
                if ligne==2:
                    isdiagonal_1 = True
            case 1:
                if ligne == 1:
                    isdiagonal_1 = True
                    isdiagonal_2 = True
            case 2:
                if ligne == 0:
                    isdiagonal_1 = True
                if ligne == 2:
                    isdiagonal_2 = True
        # diagonal_1 (from x=:/y:2 to x:2/y:0) count
        diagonal_1:int=0
        if isdiagonal_1 :
            diagonal_1 = grille_J1[2,0] + grille_J1[1,1] + grille_J1[0,2] + (
                        (grille_J2[2,0] + grille_J2[1,1] + grille_J2[0,2]) * 3)
        diagonal_2: int = 0
        if isdiagonal_2:
            diagonal_2 = grille_J1[0, 0] + grille_J1[1, 1] + grille_J1[2, 2] + (
                    (grille_J2[0, 0] + grille_J2[1, 1] + grille_J2[2, 2]) * 3)
        if (line == 2 or column == 2 or (isdiagonal_1==True and diagonal_1 == 2) or (
                isdiagonal_2 and diagonal_2 == 2)):
            return 70
        if (line == 6 or column == 6 or (isdiagonal_1 and diagonal_1 == 6) or (
                isdiagonal_2 and diagonal_2 == 6)):
            return 50
        count = self.countAlign(line) + self.countAlign(column)
        if isdiagonal_1:
            count += self.countAlign(diagonal_1)
        if isdiagonal_2:
            count += self.countAlign(diagonal_2)
        return count

    # --------------------------------------------------------------------------
    def checkEndGame(self, ligne, colonne):
        # check line
        if (self.joueur_en_cours.grille[ligne,0] != 0) and (self.joueur_en_cours.grille[ligne,0] == self.joueur_en_cours.grille[ligne,1]) and (self.joueur_en_cours.grille[ligne,1] == self.joueur_en_cours.grille[ligne,2]):
            self.status = self.Etats[1]
            self.maj_status()
            return True
        # check column
        if (self.joueur_en_cours.grille[0,colonne] != 0) and (self.joueur_en_cours.grille[0,colonne] == self.joueur_en_cours.grille[1,colonne]) and (self.joueur_en_cours.grille[1,colonne] == self.joueur_en_cours.grille[2,colonne]):
            self.status = self.Etats[1]
            self.maj_status()
            return True
        # check diagonals
        if (self.joueur_en_cours.grille[0,0] != 0) and (self.joueur_en_cours.grille[0,0] == self.joueur_en_cours.grille[1,1]) and (self.joueur_en_cours.grille[1,1] == self.joueur_en_cours.grille[2,2]):
            self.status = self.Etats[1]
            self.maj_status()
            return True
        if (self.joueur_en_cours.grille[2,0] != 0) and (self.joueur_en_cours.grille[2,0] == self.joueur_en_cours.grille[1,1]) and (self.joueur_en_cours.grille[1,1] == self.joueur_en_cours.grille[0,2]):
            self.status = self.Etats[1]
            self.maj_status()
            return True
        # check if match null
        tab_coord = self.tableau_des_cases_vides()
        if not tab_coord:
            self.status = self.Etats[3]
            self.maj_status()
            return True
        else:
            return False

    def maj_status(self):
        self.joueur_en_cours.status=self.status
        nom_joueur = self.donne_autre_joueur()
        if self.status == self.Etats[3]:
            nom_joueur.status=self.Etats[3]
        elif self.status == self.Etats[1]:
            nom_joueur.status = self.Etats[2]
        else:
            nom_joueur.status = self.Etats[1]

    def faire_jouer_ordinateur(self)->tuple[int, int, bool]:
        tableau = []
        cell_played: Cellule
        # Balyage des cellules vides pour les évaluer
        for ligne in range(self.taille_grille):
            for colonne in range(self.taille_grille):
                if self.grille[ligne,colonne] == '-':
                    tableau.append((ligne, colonne, self.evaluercellule(ligne, colonne)))
        # Tri du tableau par ordre décroissant selon le troisième élément du tuple
        tableau.sort(key=lambda x: x[2], reverse=True)
        print(f"ordinateur_joue : {self.joueur_en_cours.nom} tableau: {tableau}")
        # choix d'une ligne du tableau en fonction du niveau
        # for i in range(len(tableau)):
        #     print(f"ordinateur_joue: {i} : {tableau[i]}")
        #print(f"faire_jouer_ordinateur: choice(tableau) = {choice(tableau)}")
        # randomize selection
        dice = random.randint(0, 300)  # Assuming a range for randomGen
        print(f"log: autoPlay() dice: {dice}")

        # select best playingOption
        if dice > 200:
            x=tableau[0][0]
            y=tableau[0][1]
            #cell_played = {'x': tableau[0][0], 'y': tableau[0][1]}
        # select random playingOption
        else :
            index = 75 % len(tableau)
            x = tableau[index][0]
            y = tableau[index][1]
            # cell_played = {'x': tableau[index][0], 'y': tableau[index][1]}
        # # select random playingOption
        # elif dice > 50:
        #     index = dice % len(tableau)
        #     x=tableau[index][0]
        #     y=tableau[index][1]
        #     #cell_played = {'x': tableau[index][0], 'y': tableau[index][1]}
        # else:
        #     # select worst playingOption
        #     x=tableau[-1][0]
        #     y=tableau[-1][1]
            #cell_played = {'x': tableau[-1][0], 'y': tableau[-1][1]}
        self.mettre_a_jour_la_grille(x, y)
        return x, y, True
        # if len(tableau)==1:
        #     ligne, colonne, grade = tableau[0]
        #     print(f"faire_jouer_ordinateur: Dernière case ligne = {ligne}, colonne = {colonne}, grade = {grade}")
        # else:
        #     match self.niveau:
        #         case "Facile":
        #             ligne, colonne, grade = choice(tableau)
        #             print(f"faire_jouer_ordinateur: Facile ligne = {ligne}, colonne = {colonne}, grade = {grade}")
        #         case "Difficile":
        #             ligne, colonne, grade = choice(tableau[1:]) # random.randint(1, len(tableau)-1)
        #             print(f"faire_jouer_ordinateur: Difficile ligne = {ligne}, colonne = {colonne}, grade = {grade}")
        #         case "Expert":
        #             ligne, colonne, grade = tableau[0]
        #             print(f"faire_jouer_ordinateur: Expert ligne = {ligne}, colonne = {colonne}, grade = {grade}")
        # self.mettre_a_jour_la_grille(ligne, colonne)
        # return ligne, colonne, True

    # --------------------------------------------------------------------------


    def auto_play(board):
        options = []
        cell_played : Cellule
        # find all empty cells to evaluate them.
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == ' ':
                    new_option = (i, j, evaluate_cell(i, j))
                    options.append(new_option)

        # sort options
        options.sort(key=lambda x: x[2])  # Assuming the third element is the grade

        # randomize selection
        dice = random.randint(0, 300)  # Assuming a range for randomGen
        print(f"log: autoPlay() dice: {dice}")

        # select best playingOption
        if dice > 200:
            cell_played = {'x': options[0][0], 'y': options[0][1]}
        # select random playingOption
        elif dice > 50:
            index = dice % len(options)
            cell_played = {'x': options[index][0], 'y': options[index][1]}
        else:
            # select worst playingOption
            cell_played = {'x': options[-1][0], 'y': options[-1][1]}

        return cell_played





    def faire_joueur_humain(self, ligne, colonne, reponse:bool):
        # Cette fonction traite le clic gauche
        if reponse:
            print(f" joueur en cours : {self.joueur_en_cours.nom}, {self.joueur_en_cours.categorie}")
            # Est-ce que la case cochée est disponible ?
            # print(f"traite_clic_gauche: la case : ligne={ligne}:colonne={colonne}, est-elle disponible ?")
            if self.grille[ligne, colonne] == '-':
                # print(f"traite_clic_gauche: la case : ligne={ligne}:colonne={colonne}, est disponible")
                # la case est disponible
                self.mettre_a_jour_la_grille(ligne, colonne)
                # Mettre à jour le tableau de jeu avec le motif du joueur en cours
                # print(f"traite_clic_gauche: Case cliquée: ligne={ligne} , colonne={colonne}, {type(self.joueur_en_cours.motif)}")
                return ligne,colonne,True
            else:
                # La case n'est pas vide
                return ligne, colonne, False
        else:
            return ligne,colonne,False
    def traite_clic_droit(self, x, y):
        if self.mode== self.modes[1]:
            self.gameOn=False

    def lire_fichier(self, file_name):
        data=[]
        try:
            with open(file_name, 'r') as P_File:
                data = json.load(P_File)
                return data
        except IOError:
            return data

    def enregistrer_fichier(self, file_name, data):
        try:
            with open(file_name, 'wb') as f:
                dump(data, f)
        except IOError:
            with open(file_name, 'wb') as f:
                dump(data, f)

    def enregistrer_joueur(self, joueur):
        mode_encours = self.mode
        niveau_en_cours = self.niveau
        date = datetime.now()
        date_jour = "{0}/{1}/{2}".format(date.day, date.month, date.year)
        file_name = r"data_file.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as P_File:
                data_O = json.load(P_File)
        data_O.append({'Nom': joueur.nom, 'date_essai': date_jour, 'Mode': mode_encours,
                       'Niveau': niveau_en_cours, 'Resultat': joueur.status})
        with open("data_file.json", "w") as write_file:
            json.dump(data_O, write_file, indent=2)

    def enregistrer_les_donnees(self):
        if self.mode == self.modes[2]:
            if self.joueur_en_cours.categorie == self.categories[2]:
                self.enregistrer_joueur(self.donne_autre_joueur())
            else:
                self.enregistrer_joueur(self.joueur_en_cours)
        else:
            self.enregistrer_joueur(self.joueur_1)
            self.enregistrer_joueur(self.joueur_2)

    def visu_stats(self):
        file_name = r"data_file.json"
        try:
            if os.path.exists(file_name):
                with open(file_name, 'r') as P_File:
                    data_O = json.load(P_File)
                return data_O
            else:
                print(f"Le fichier {file_name} n'existe pas")
                #var = view.messagebox.showinfo(f"Le fichier {file_name} n'existe pas")
                return None
        except IOError:
            print('Pas de stats.')
            return None
