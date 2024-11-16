import tkinter as Tk
from doctest import master

from models import *
from views import *


class Controller:
    def __init__(self, window: Tk, view: View):
        self.model: Model = None
        self.tableaudejeu: TableauDeJeu = None
        self.window = window
        self.view = view

#----------------------------------------------------------------------
    def donne_modes_categories_niveaux(self):
        return self.model.modes, self.model.categories, self.model.niveaux

    def traiter_choix(self, mode_choisi, nom_1, nom_2, categorie_1_choisie, categorie_2_choisie, niveau_choisi, joueur_qui_commence):
        # Appel de la fonction statique "@staticmethod" "new" du modèle "Model"
        self.model = Model.new(self,mode_choisi, nom_1, nom_2, categorie_1_choisie, categorie_2_choisie, niveau_choisi, joueur_qui_commence)

        self.view.grid_remove()

        self.tableaumorpion()
        self.tableaudejeu.mettre_a_jour_donnees(mode_choisi, nom_1, categorie_1_choisie, nom_2, categorie_2_choisie, niveau_choisi, joueur_qui_commence,True)
        self.tableaudejeu.joueur_qui_doit_jouer_var(self.model.joueur_en_cours.nom)

        self.model.gameOn=True

    def jouer(self, ligne: int=10, colonne:int = 10, reponse=False):
        if self.model.mode == "automatique":
            while self.model.gameOn:
                ligne, colonne, reponse = self.model.faire_jouer_ordinateur()
                print(f"jouer: Case cliquée: ligne={ligne} , colonne={colonne}, {type(self.model.joueur_en_cours.motif)}")
                self.ecrire_dans_tabeau_de_jeu( ligne, colonne, self.model.joueur_en_cours)
                # introduire une temporisation de deux secondes
                time.sleep(2)
                if self.model.checkEndGame(ligne,colonne):
                    self.model.gameOn= False
                    print(f"le joueur {self.model.joueur_en_cours.nom} a {self.model.status} !")
                    self.tableaudejeu.ecrire_resultat( f"le joueur {self.model.joueur_en_cours.nom} a {self.model.status} !", False)
                self.model.permutter_joueurs()
                self.window.update()
        else:
            if self.model.gameOn:
                if self.model.joueur_en_cours.categorie=="ordinateur":
                    ligne, colonne, reponse = self.model.faire_jouer_ordinateur()
                    print(f"jouer: Case cliquée: ligne={ligne} , colonne={colonne}, {type(self.model.joueur_en_cours.motif)}")
                    self.ecrire_dans_tabeau_de_jeu(ligne, colonne, self.model.joueur_en_cours)
                    if self.model.checkEndGame(ligne, colonne):
                        self.model.gameOn = False
                        print(f"le joueur {self.model.joueur_en_cours.nom} a {self.model.status} !")
                        self.tableaudejeu.ecrire_resultat(f"le joueur {self.model.joueur_en_cours.nom} a {self.model.status} !", False)
                        self.model.enregistrer_les_donnees()
                    self.model.permutter_joueurs()
                else:
                    # traiter les cas où le joueur est humain
                    # Traitement du clic
                    ligne, colonne, ok = self.model.faire_joueur_humain(ligne, colonne, reponse)
                    if ok:
                        self.ecrire_dans_tabeau_de_jeu(ligne,colonne, self.model.joueur_en_cours)
                        if self.model.checkEndGame(ligne, colonne):
                            self.model.gameOn = False
                            print(f"le joueur {self.model.joueur_en_cours.nom} a {self.model.status} !")
                            self.tableaudejeu.ecrire_resultat(f"le joueur {self.model.joueur_en_cours.nom} a {self.model.status} !", False)
                            self.model.enregistrer_les_donnees()
                        # Permuttation des deux joueurs
                        self.model.permutter_joueurs()
                        if self.model.joueur_en_cours.categorie=="ordinateur":
                            self.jouer()
                self.window.update()

    def tableaumorpion(self):
        self.tableaudejeu = TableauDeJeu(self.window, self, self.model.taille_grille)
        self.tableaudejeu.config(height= 500, width=700)

    def rejouer(self):
        print("Appui sur le bouton Rejouer")
        if self.model.joueur_qui_commence == self.model.joueur_1.nom:
            self.model.joueur_qui_commence = self.model.joueur_2.nom
        else:
            self.model.joueur_qui_commence = self.model.joueur_1.nom
        self.model = Model.new(self, self.model.mode, self.model.joueur_1.nom, self.model.joueur_2.nom, self.model.joueur_1.categorie, self.model.joueur_2.categorie, self.model.niveau,
                               self.model.joueur_qui_commence)
        self.tableaumorpion()
        self.tableaudejeu.mettre_a_jour_donnees(self.model.mode, self.model.joueur_1.nom, self.model.joueur_1.categorie, self.model.joueur_2.nom, self.model.joueur_2.categorie, self.model.niveau, self.model.joueur_qui_commence, True)
        self.jouer()

    def voir_stats(self):
        print("Appui sur le bouton Stats")
        data =self.model.visu_stats()
        # print(f"Data= {data}")
        if self.model.joueur_1.categorie==self.model.categories[2]:
            joueur=self.model.joueur_2.nom
        else:
            joueur = self.model.joueur_1.nom
            # Création des colonnes
        entete = ["Nom", "Date de l'essai", "Mode", "Niveau", "Résultat"]
        if data:
            stat = StatsWindow(data, entete)
        else:
            return False

    def quitterstats(self):
        print("Appui sur le bouton Quitter")
        self.window.destroy()

    def quitter(self):
        print("Appui sur le bouton Quitter")
        self.window.destroy()


    def valid_click_gauche(self, ligne, colonne):
        # Traitement du clic
        if ligne in [0,1,2] and colonne in [0,1,2] and self.model.joueur_en_cours.categorie == self.model.categories[1]:
            #[x,y,reponse]= self.model.faire_joueur_humain(x, y, True)
            self.jouer(ligne, colonne, True)
        else:
            self.jouer(ligne, colonne, False)

    def valid_click_droit(self, ligne, colonne):
        self.model.traite_clic_droit(ligne, colonne)

    def ecrire_dans_tabeau_de_jeu(self, ligne, colonne, joueur_en_cours):
        self.tableaudejeu.mettre_a_jour_case(68 + ligne * 135, 68 + colonne * 135, joueur_en_cours.motif)

    def mise_a_jour_joueur_qui_doit_jouer(self, maj_joueur_qui_doit_jouer):
        self.tableaudejeu.joueur_qui_doit_jouer_var(maj_joueur_qui_doit_jouer)