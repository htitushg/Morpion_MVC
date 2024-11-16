
from tkinter import *
# import tkinter as Tk
from tkinter import ttk

from click import command
from uaclient.api.u.pro.services.disable.v1 import disable

from models import *

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Liste des modes et catégories (à déplacer éventuellement ailleurs)
        # self.liste_modes, self.liste_categories, self.liste_niveaux = self.controller.donne_modes_categories_niveaux()
        self.liste_modes = Model.modes
        self.liste_categories = Model.categories
        self.liste_niveaux = Model.niveaux
        self.liste_joueurs = ["", ""]
        self.controller = None
        # Création des éléments graphiques
        # Création dynamique des menus déroulants, bouton, zones d'entrées...

        ################ Création frame qui va contenir les deux autres#############
        self.frame=ttk.Frame(self)
        ################ Création frame de gauche #############
        self.left_frame = ttk.Frame(self.frame)  # , bg='#4065A4')
        for i in range(10):  # Supposons 10 lignes à aligner
            self.left_frame.grid_rowconfigure(i, minsize=35, weight=0)

        self.label_message = ttk.Label(self.left_frame, text="", width=30, font=('Helvetica', 12))
        self.label_message.grid(row=0, column=0)

        self.label_mode = ttk.Label(self.left_frame, text="Choisissez le mode", width=30, font=('Helvetica', 12))
        self.label_mode.grid(row=1, column=0)
        # On crée le label nom_1
        self.label_nom_1 = ttk.Label(self.left_frame, text="Nom du Joueur 1", width=30, font=('Helvetica', 12))
        self.label_nom_1.grid(row=2, column=0)

        # On crée le label nom_2
        self.label_nom_2 = ttk.Label(self.left_frame, text="Nom du Joueur 2", width=30, font=('Helvetica', 12))
        self.label_nom_2.grid(row=3, column=0)

        self.label_categorie_1 = ttk.Label(self.left_frame, text="Catégorie 1", width=30, font=('Helvetica', 12))
        self.label_categorie_1.grid(row=4, column=0)

        self.label_categorie_2 = ttk.Label(self.left_frame, text="Catégorie 2", width=30, font=('Helvetica', 12))
        self.label_categorie_2.grid(row=5, column=0)

        self.label_niveau = ttk.Label(self.left_frame, text="Choisisez le niveau", width=30, font=('Helvetica', 12))
        self.label_niveau.grid(row=6, column=0)

        self.label_joueur_qui_commence = ttk.Label(self.left_frame, text="Qui commence ?", width=30, font=('Helvetica', 12))
        self.label_joueur_qui_commence.grid(row=7, column=0)

        self.left_frame.grid(row=0, column=0)

        ################ Création frame de droite #############
        # self.right_frame = ttk.Frame(self.frame)#, bg='#4065A4')
        # for i in range(10):  # Supposons 3 lignes à aligner
        #     self.right_frame.grid_rowconfigure(i, minsize=35, weight=0)
        # On crée une zone de texte pour des messages de recommandation
        self.msg_text = StringVar()
        self.msg = ttk.Label(self.left_frame, textvariable=self.msg_text, width=30, font=('Helvetica', 12))
        self.msg.grid(row=0, column=1)
        self.mode_var = StringVar(value=self.liste_modes[0])
        self.mode_options = OptionMenu(self.left_frame, self.mode_var, *self.liste_modes)
        self.mode_options.config(width=30, font=('Helvetica', 12))
        self.mode_options.grid(row=1, column=1)

        # On crée le controle nom_1
        self.nom_1_entry = StringVar()
        self.entry_nom_1 = ttk.Entry(self.left_frame, textvariable=self.nom_1_entry, font=('Helvetica', 12))#, command= self.mise_a_jour_nom_1)
        self.entry_nom_1.config(state=DISABLED, width=30)
        self.entry_nom_1.grid(row=2, column=1, ipadx=18, ipady=3)

        # On crée le controle nom_2
        self.nom_2_entry = StringVar()
        self.entry_nom_2 = ttk.Entry(self.left_frame, textvariable=self.nom_2_entry, font=('Helvetica', 12))#, command= self.mise_a_jour_nom_2)
        self.entry_nom_2.config(state=DISABLED, width=30)
        self.entry_nom_2.grid(row=3, column=1, ipadx=18, ipady=3)

        # On crée le controle catégorie du joueur 1.
        self.categorie_1_var = StringVar()
        self.categorie_1 = ttk.Label(self.left_frame, textvariable=self.categorie_1_var, width=30, relief='ridge',
                                  font=('Helvetica', 12))
        self.categorie_1.grid(row=4, column=1, ipadx=18, ipady=3)

        # On crée le controle catégorie du joueur 2.
        self.categorie_2_var = StringVar()
        self.categorie_2 = ttk.Label(self.left_frame, textvariable=self.categorie_2_var, width=30, relief='ridge',
                                     font=('Helvetica', 12))
        self.categorie_2.grid(row=5, column=1, ipadx=18, ipady=3)

        # On crée le controle niveau
        self.niveau_var = StringVar(value=self.liste_niveaux[0])
        self.niveau_options = OptionMenu(self.left_frame, self.niveau_var,self.liste_niveaux[1] ,*self.liste_niveaux)
        self.niveau_options.config(width=30, font=('Helvetica', 12))
        self.niveau_options.config(state=DISABLED)
        self.niveau_options.grid(row=6, column=1)

        # On crée le controle joueur qui commence
        self.joueur_qui_commence_var = StringVar()
        self.joueur_qui_commence_var.set(self.nom_1_entry.get())
        self.liste_joueurs=[self.nom_1_entry.get(),self.nom_2_entry.get()]
        self.joueur_qui_commence_options = OptionMenu(self.left_frame, self.joueur_qui_commence_var, "Qui commence ?",*self.liste_joueurs)
        self.joueur_qui_commence_options.config(width=30, font=('Helvetica', 12))
        self.joueur_qui_commence_options.config(state=DISABLED)
        self.joueur_qui_commence_options.grid(row=7, column=1)

        # Bouton pour confirmer les choix
        self.btn_confirmer = Tk.Button(self.left_frame, text="Confirmer", width=30, command=self.confirmer_choix)
        self.btn_confirmer.config(state=DISABLED)
        self.btn_confirmer.grid(row=10, column=1, ipadx=20, ipady=3)

        #self.right_frame.grid(row=0, column=1)

        self.frame.pack()


        def mettre_a_jour_mode(a, b, c):
            if self.mode_var.get()=="automatique":
                self.nom_1_entry.set("IA_1")
                self.categorie_1_var.set(self.liste_categories[2])
                self.nom_2_entry.set("IA_2")
                self.categorie_2_var.set(self.liste_categories[2])
                self.niveau_var.set(self.liste_niveaux[1])
                self.joueur_qui_commence_var.set("IA_1")
                self.btn_confirmer.config(state='normal')
            elif self.mode_var.get()=="un_joueur": # Un joueur humain
                self.entry_nom_1.config(state='normal')
                self.btn_confirmer.config(state=DISABLED)
            else: # Deux joueurs humains
                self.entry_nom_1.config(state='normal')
                self.entry_nom_2.config(state='normal')
                self.btn_confirmer.config(state=DISABLED)

        def mettre_a_jour_nom_1(a, b, c):
            if not self.entry_nom_1 =="":
                if self.mode_var.get() == self.liste_modes[2]:
                    self.categorie_1_var.set(self.liste_categories[1])
                    self.categorie_2_var.set(self.liste_categories[2])
                    self.nom_2_entry.set("IA")
                    self.niveau_options.config(state='normal')
                elif self.mode_var.get() == self.liste_modes[3]:
                    if not self.entry_nom_2 == "":
                        self.categorie_1_var.set(self.liste_categories[1])
                        self.categorie_2_var.set(self.liste_categories[1])
                        self.niveau_options.config(state='normal')

        def mettre_a_jour_nom_2(a, b, c):
            if not self.entry_nom_2 =="":
                if self.mode_var.get() == self.liste_modes[2]:
                    self.categorie_1_var.set(self.liste_categories[1])
                    self.categorie_2_var.set(self.liste_categories[2])
                    self.nom_2_entry.set("IA")
                    self.niveau_options.config(state='normal')
                elif self.mode_var.get() == self.liste_modes[3]:
                    if not self.entry_nom_1 == "":
                        self.categorie_1_var.set(self.liste_categories[1])
                        self.categorie_2_var.set(self.liste_categories[1])
                        self.niveau_options.config(state='normal')

        def mettre_a_jour_niveau(a, b, c):
            if not (self.niveau_var.get() == self.liste_niveaux[0]):
                self.liste_joueurs = [self.nom_1_entry.get(), self.nom_2_entry.get()]
                self.joueur_qui_commence_options.configure(menu=create_menu(self.liste_joueurs))
                self.joueur_qui_commence_options.config(state='normal')
            else:
                result_nom = 'Vous devez choisir le niveau de jeu'
                self.msg_text.set(result_nom)

        def mettre_a_jour_joueur_qui_commence(a, b, c):
            if self.joueur_qui_commence_var.get() not in (self.nom_1_entry.get(), self.nom_2_entry.get()):
                result_nom = 'Vous devez choisir le joueur qui commence(joueur 1/joueur 2)'
                self.msg_text.set(result_nom)
            else:
                self.joueur_qui_commence_var.get()
                self.btn_confirmer.config(state='normal')

        def create_menu(values):
            menu = Menu(self.joueur_qui_commence_options, tearoff=0)
            for value in values:
                menu.add_radiobutton(label=value, variable=self.joueur_qui_commence_var, value=value)
            return menu


        # Assurez-vous que nom_1_entry.get() et nom_2_entry.get() sont des StringVar()
        self.mode_var.trace_add("write", mettre_a_jour_mode)
        self.nom_1_entry.trace_add("write", mettre_a_jour_nom_1)
        self.nom_2_entry.trace_add("write", mettre_a_jour_nom_2)
        self.niveau_var.trace_add("write", mettre_a_jour_niveau)
        self.joueur_qui_commence_var.trace_add("write", mettre_a_jour_joueur_qui_commence)

        # Récupération des valeurs sélectionnées par l'utilisateur

    def verifier_nom(self, nom):
        pattern = r'^[A-Za-z]+[A-Z \'çéèàù¨a-z0-9]+'
        if nom == "" or not self.nom_1_entry.get() in pattern:
            result_nom = 'Vous devez entrer un nom valable (des lettres, des chiffres <60)'
            self.msg_text.set(result_nom)
            self.entry_nom_1.config(background='red')
            return True
        return False

    def confirmer_choix(self):

        nom_1 = self.nom_1_entry.get()
        nom_2 = self.nom_2_entry.get()
        mode_choisi = self.mode_var.get()
        niveau_choisi=self.niveau_var.get()
        categorie_1_choisie = self.categorie_1_var.get()
        categorie_2_choisie = self.categorie_2_var.get()
        nom_du_joueur_qui_commence = self.joueur_qui_commence_var.get()

        # Utilisation des valeurs choisies (par exemple, appel à une fonction du contrôleur)
        if self.controller:
            self.controller.traiter_choix(mode_choisi, nom_1, nom_2, categorie_1_choisie, categorie_2_choisie, niveau_choisi, nom_du_joueur_qui_commence)
            self.controller.jouer()

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

class TableauDeJeu(ttk.Frame):
    def __init__(self, parent, controller, taille_grille=3):
        super().__init__(parent)
        self.controller = controller

        self.taille_grille = taille_grille
        self.game = Canvas(self, width=405, height=405, bg="lightgrey")
        self.game['highlightbackground'] = 'black'
        self.game['highlightthickness'] = 2  # change the highlight thickness!
        self.game.place(x=0, y=0, width=405, height=405)
        self.config(width=405, height=405)  # self.frameTableauJeu.pack()
        self.grille = [[' ' for _ in range(taille_grille)] for _ in range(taille_grille)]
        self.taille_case = 405 // self.taille_grille
        # Dessiner les lignes de la grille (code simplifié)
        for i in range(1, self.taille_grille):
            self.game.create_line(i * self.taille_case, 0, i * self.taille_case, 405)
            self.game.create_line(0, i * self.taille_case, 405, i * self.taille_case)
        # Liaison de l'événement clic gauche au canvas
        self.game.bind("<Button-1>", self.gestion_clic_gauche)
        self.game.bind("<Button-3>", self.gestion_clic_droit)
        # Création d'une frame à droite du tableau de jeu
        self.frame_right = ttk.Frame(self, width=265, height= 425)
        # Création à l'intérieur de la frame_right
        # de deux frames pour séparer les libellés et le contenu
        self.frame_data_left = ttk.Frame(self.frame_right)
        self.frame_data_right = ttk.Frame(self.frame_right)
        # self.frame_data_left.grid_rowconfigure(1, weight=1)
        # self.frame_data_left.grid_columnconfigure(0, weight=1)
        # Déterminer la taille minimum des champs
        for i in range(10):  # Supposons 10 lignes à aligner
            # print(f"i= {i}")
            self.frame_data_left.grid_rowconfigure(i, minsize=35, weight=1)

        self.label_mode = ttk.Label(self.frame_data_left, text="Mode choisi", width=17, font=('Helvetica', 12))
        self.label_mode.grid(row=0, column=0)

        self.label_nom_1 = ttk.Label(self.frame_data_left, text="Nom joueur 1", width=17, font=('Helvetica', 12))
        self.label_nom_1.grid(row=1, column=0)

        self.label_categorie_1 = ttk.Label(self.frame_data_left, text="Catégorie 1", width=17, font=('Helvetica', 12))
        self.label_categorie_1.grid(row=2, column=0)

        self.label_nom_2 = ttk.Label(self.frame_data_left, text="Nom joueur 2", width=17, font=('Helvetica', 12))
        self.label_nom_2.grid(row=3, column=0)

        self.label_categorie_2 = ttk.Label(self.frame_data_left, text="Catégorie 2", width=17, font=('Helvetica', 12))
        self.label_categorie_2.grid(row=4, column=0)

        self.label_niveau = ttk.Label(self.frame_data_left, text="Niveau choisi", width=17, font=('Helvetica', 12))
        self.label_niveau.grid(row=5, column=0)

        self.label_qui_commence = ttk.Label(self.frame_data_left, text="Celui qui commence", width=17, font=('Helvetica', 12))
        self.label_qui_commence.grid(row=6, column=0)

        self.label_qui_joue = ttk.Label(self.frame_data_left, text="A qui de jouer ?", width=17, font=('Helvetica', 12))
        self.label_qui_joue.grid(row=8, column=0, sticky = W)

        #self.frame_data_left.grid(row=0, column=0)


        # self.frame_data_right = Frame(self.frame_right)
        # # Déterminer la taille minimum des champs
        for i in range(10):  # Supposons 3 lignes à aligner
            self.frame_data_right.grid_rowconfigure(i, minsize=35, weight=1)

        self.mode_jeu_text = StringVar()
        self.mode_jeu = ttk.Label(self.frame_data_right, textvariable=self.mode_jeu_text, width=10, relief='ridge',
                                  font=('Helvetica', 12))
        self.mode_jeu.grid(row=0, column=1, ipadx=12, ipady=1, sticky = E)

        self.nom_j_1_text = StringVar()
        self.nom_j_1 = ttk.Label(self.frame_data_right, textvariable=self.nom_j_1_text, width=10, relief='ridge',
                                 font=('Helvetica', 12))
        self.nom_j_1.grid(row=1, column=1, ipadx=12, ipady=1, sticky = E)

        self.categorie_j_1_text = StringVar()
        self.categorie_j_1 = ttk.Label(self.frame_data_right, textvariable=self.categorie_j_1_text, width=10, relief='ridge',
                                 font=('Helvetica', 12))
        self.categorie_j_1.grid(row=2, column=1, ipadx=12, ipady=1, sticky = E)

        self.nom_j_2_text = StringVar()
        self.nom_j_2 = ttk.Label(self.frame_data_right, textvariable=self.nom_j_2_text, width=10, relief='ridge',
                                 font=('Helvetica', 12))
        self.nom_j_2.grid(row=3, column=1, ipadx=12, ipady=1, sticky = E)

        self.categorie_j_2_text = StringVar()
        self.categorie_j_2 = ttk.Label(self.frame_data_right, textvariable=self.categorie_j_2_text, width=10,
                                       relief='ridge',
                                       font=('Helvetica', 12))
        self.categorie_j_2.grid(row=4, column=1, ipadx=12, ipady=1, sticky = E)

        self.niveau_text = StringVar()
        self.niveau_jeu = ttk.Label(self.frame_data_right, textvariable=self.niveau_text, width=10, relief='ridge',
                                    borderwidth=2, font=('Helvetica', 12))
        self.niveau_jeu.grid(row=5, column=1, ipadx=12, ipady=1, sticky = E)

        self.qui_commence_text = StringVar()
        self.qui_commence = ttk.Label(self.frame_data_right, textvariable=self.qui_commence_text, width=10, relief='ridge',
                                      borderwidth=2,
                                      font=('Helvetica', 12))
        self.qui_commence.grid(row=6, column=1, ipadx=12, ipady=1, sticky = E)

        self.qui_joue_text = StringVar()
        self.qui_joue = ttk.Label(self.frame_data_right, textvariable=self.qui_joue_text, width=10, relief='ridge',
                                  borderwidth=2, font=('Helvetica', 12))
        self.qui_joue.grid(row=8, column=1, ipadx=12, ipady=1, sticky = E)

        self.frame_data_left.grid(row=0, column=0)
        self.frame_data_right.grid(row=0, column=1)
        self.frame_right.place(x=420, y=0)

        self.resultat_jeu_text = StringVar()
        self.resultat_jeu = ttk.Label(self, textvariable=self.resultat_jeu_text, justify=CENTER,
                                      relief='ridge', borderwidth=2, font=('Helvetica', 12))
        self.resultat_jeu.place(x=350, y=420, anchor='center')

        self.btn_rejouer = Tk.Button(self, text="Rejouer", width=50, font=('Helvetica', 12, 'bold'), command=self.controller.rejouer)
        self.btn_rejouer.place(x= 350, y=440, anchor='center')

        self.btn_stats = Tk.Button(self, text="Statistiques", width=50, font=('Helvetica', 12, 'bold'),
                                     command=self.controller.voir_stats)
        self.btn_stats.place(x=350, y=460, anchor='center')

        self.btn_quitter = Tk.Button(self, text="Quitter", width=50, font=('Helvetica', 12, 'bold'),
                                     command=self.controller.quitter)
        self.btn_quitter.place(x=350, y=480, anchor='center')

        self.grid(row=0, column=0, padx=10, pady=10)

    def cacher(self):
        self.place_forget()

    def mettre_a_jour_case(self, x, y, motif):
        self.game.create_image( x , y , anchor = 'center', image = motif)

    def joueur_qui_doit_jouer_var(self, joueur_qui_doit_jouer):
        # pass
        self.qui_joue_text.set(joueur_qui_doit_jouer)
        # self.update()

    def mettre_a_jour_donnees(self, mode, nom_joueur_1, categorie_joueur_1, nom_joueur_2, categorie_joueur_2, niveau_jeu, nom_joueur, disable_rejouer):
        # print("Mode choisi:", mode)
        # print("Nom joueur 1:", nom_joueur_1)
        # print("Catégorie du joueur 1:", categorie_joueur_1)
        # print("Nom joueur 2:", nom_joueur_2)
        # print("Catégorie du joueur 2:", categorie_joueur_2)
        # print("Niveau choisi:", niveau_jeu)
        # print("Joueur qui commence:", nom_joueur)

        self.mode_jeu_text.set(f"{mode}")
        self.nom_j_1_text.set(f"{nom_joueur_1}")
        self.categorie_j_1_text.set(f"{categorie_joueur_1}")
        self.nom_j_2_text.set(f"{nom_joueur_2}")
        self.categorie_j_2_text.set(f"{categorie_joueur_2}")
        self.niveau_text.set(f"{niveau_jeu}")
        self.qui_commence_text.set(f"{nom_joueur}")
        if disable_rejouer:
            self.btn_rejouer.config(state=DISABLED )
            self.resultat_jeu.place_forget()
        else:
            self.btn_rejouer.config(state=NORMAL )
        self.update()


    def ecrire_resultat(self, resultat_jeu, disable_rejouer):
        if disable_rejouer:
            self.btn_rejouer.config(state=DISABLED)
        else:
            self.btn_rejouer.config(state=NORMAL)
            self.resultat_jeu_text.set(resultat_jeu)
            self.resultat_jeu.place(x= 350, y=420, anchor='center')

    def gestion_clic_gauche(self,event):
        # L'opérateur // donne la division entière x//135
        x, y = event.x // 135, event.y // 135  # Acquisition clic joueur
        # self.msg_text = StringVar()
        # self.msg_text.set(" X = "+str(x)+" Y = "+str(y))
        # self.msg = Tk.Label(self, textvariable=self.msg_text, font=('Helvetica', 12), fg='red')
        # self.msg.pack()
        self.controller.valid_click_gauche(x, y)

    def gestion_clic_droit(self, event):
        x, y = event.x // 135, event.y // 135  # Acquisition clic joueur
        self.controller.valid_click_droit(x, y)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

#-----------------------------------------------------------------
class StatsWindow(Tk.Toplevel):
    def __init__(self, data, entete):
        super().__init__()
        # calcul des dimensions et choix de la fonte
        width_column, total_width, total_height = self.calcul_des_dimensions(data, entete)
        taille_fonte = 14
        data = sorted(data, key=lambda joueur: joueur['Nom'])
        # data.sort(key=['Nom'])
        self.title("Résultats des joueurs")
        btn_quitter = Button(self, text="Quitter", font=('Helvetica', 12, 'bold'),
                             command=self.destroy)
        btn_quitter.pack(fill="both", expand=True)
        # Création d'un frame pour contenir le canvas et la scrollbar
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True)
        # Création du canvas pour l'en-tête
        self.header_canvas = Canvas(frame, width=500, height=30)
        self.header_canvas.pack(fill="x")

        # Création de la scrollbar
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Création du canvas lié à la scrollbar
        self.canvas_body = Canvas(frame, width=500, yscrollcommand=scrollbar.set)
        # Création du canvas d'entete
        self.canvas_body.pack(side="left", fill="both", expand=True)

        # Configuration de la scrollbar pour qu'elle suive le canvas
        scrollbar.config(command=self.canvas_body.yview)


        self.canvas_body.config(width=total_width*taille_fonte, height=total_height, bg='gray')
        self.header_canvas.config(width=total_width*taille_fonte, height=30, bg='lightgray')
        coulcar = "#000000"

        font=("Helvetica", taille_fonte)
        y = 20
        x = 50
        for i in range(len(entete)):
            largeur_texte = width_column[i]*taille_fonte
            self.header_canvas.create_text(x, y, text=f"{entete[i]:^{width_column[i]}}", fill=coulcar, font=font) # width=(width_column[i]), font=("Helvetica", 12))
            print(f"entete[{i}]={entete[i]}, x= {x}, width_column[i]={width_column[i]}")
            x += largeur_texte

        coulcar = "#071468"
        coulfond = "#680735"

        # Création des lignes pour les joueurs
        j = 0
        for joueur in data:
            x = 50
            if (j % 2 == 0):
                coulcar = "#680735"
                coulfond = "#729fcf"
            else:
                coulcar = "#071468"
                coulfond = "#babdb6"

            for i, (cle, valeur) in enumerate(joueur.items()):

                self.canvas_body.create_text(x, taille_fonte + y, text=f"{valeur:^{width_column[i]}}", fill=coulcar, font=font)
                x += width_column[i]*taille_fonte
            y += 20
            j+=1

        # Met à jour les dimensions de la zone scrollable du canvas
        self.canvas_body.configure(scrollregion=self.canvas_body.bbox("all"))

    def calcul_des_dimensions(self, data, entete):
        # Calcul de la hauteur
        total_rows = len(data)
        row_height = 20
        total_height = total_rows * row_height + 50  # +50 pour les marges
        if total_height > 300:
            total_height = 300

        # calcul de la largeur de chaque colonne dans les donnees et dans l'entete
        width_column = [0] * len(data[0])
        for joueur in data:
            for i, (cle, valeur) in enumerate(joueur.items()):
                if len(str(valeur)) > width_column[i]:
                    width_column[i] = len(str(valeur))
        for valeur in entete:
            for i, (valeur) in enumerate(entete):
                if len(str(valeur)) > width_column[i]:
                    width_column[i] = len(str(valeur))
        total_width = 0
        for i in range(len(width_column)):
            total_width = total_width + width_column[i]
        print(f"width_column = {width_column}")

        taille_fonte = 14
        print(f"total_width = {total_width}")
        print(f"total_height = {total_height}")
        return width_column, total_width, total_height

#-----------------------------------------------------------------
# class Identification(Tk.Toplevel):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         #Tk.Frame.__init__(self, parent)
#         self.userid = ""
#         self.nom = ""
#         self.prenom = ""
#         self.ddn = '01/01/1900'
#         self.date_valide = False
#         self.data_p = []
#         self.userid_valide = False
#         self.prenom_valide = False
#         self.nom_valide = False
#         self.couleurFondMenu = 'lightyellow'
#         self.couleurFondExo = 'lightgreen'
#         # Tester l'existence du fichier
#         file_name = r"personnes.json"
#         if os.path.exists(file_name):
#             with open(file_name, 'r') as P_File:
#                 self.data_p = json.load(P_File)
#         self.identite = Tk.StringVar()
#         if len(self.data_p) + 1 > 5:
#             hauteur = 5
#         else:
#             hauteur = len(self.data_p) + 1
#         self.liste_P = Tk.Listbox(self, height=hauteur + 1, width=50, state='normal')
#         self.liste_P.title = "Choisissez votre nom dans la liste ou ajoutez le en cliquant sur le bouton 'Ajouter un " \
#                              "utilisateur' "
#         self.liste_P.pack()
#         for x in range(len(self.data_p)):
#             self.liste_P.insert(END, "{0}-{1}-{2}".format(self.data_p[x]["Userid"], self.data_p[x]["firstName"],
#                                                           self.data_p[x]["lastName"]))
#         self.liste_P.focus_set()
#         self.liste_P.index(2)
#         self.liste_P.activate (2)
#         self.liste_P.bind('<Return>', self.focusliste_p)
#
#     def focusliste_p(self, event=None):
#         self.liste_P.focus_set()

