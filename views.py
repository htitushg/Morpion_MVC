
from tkinter import *
import tkinter as Tk
from tkinter import ttk

from models import *

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Liste des modes et catégories (à déplacer éventuellement ailleurs)
        self.liste_modes = Model.modes
        self.liste_categories = Model.categories
        self.liste_niveaux = Model.niveaux
        self.liste_joueurs = ["", ""]
        # Création des éléments graphiques

        # Bouton pour déclencher la demande de mode, de nom, de niveau ... et de catégorie
        self.btn_demander = ttk.Button(self,
                                      text="Choisir mode de jeu, catégorie de joueur et niveau de jeu", width=50,
                                      command=self.demander_options)
        self.btn_demander.pack()
        # set the controller
        self.controller = None


    def demander_options(self):
        self.btn_demander.pack_forget()
        # Création dynamique des menus déroulants, bouton, zones d'entrées...
        #On crée une zone de texte pour des messages de recommandation
        self.msg_text = StringVar()
        self.msg = ttk.Label(self, textvariable=self.msg_text, font=('Helvetica', 12))
        self.msg.pack()
        self.mode_var = StringVar(value=self.liste_modes[0])
        self.mode_options = OptionMenu(self, self.mode_var, *self.liste_modes)
        self.mode_options.config(width=15, font=('Helvetica', 12))
        self.mode_options.pack()
        # On crée le controle nom_1)
        self.label_nom_1 = ttk.Label(self, text="Nom du Joueur", font=('Helvetica', 12))
        #self.label_nom_1.pack()
        self.nom_1_entry = StringVar()
        self.entry_nom_1 = ttk.Entry(self, textvariable=self.nom_1_entry)
        #self.entry_nom_1.pack()
        # On crée le controle nom_2)
        self.label_nom_2 = ttk.Label(self, text="Nom du Joueur", font=('Helvetica', 12))
        #self.label_nom_2.pack()
        self.nom_2_entry = StringVar()
        self.entry_nom_2 = ttk.Entry(self, textvariable=self.nom_2_entry)
        #self.entry_nom_2.pack()
        # On crée le controle catégorie du joueur 1
        self.categorie_1_var = StringVar(value=self.liste_categories[0])
        self.categorie_1_options = OptionMenu(self, self.categorie_1_var, *self.liste_categories)
        self.categorie_1_options.config(width=15, font=('Helvetica', 12))
        #self.categorie_1_options.pack()
        # On crée le controle catégorie du joueur 2
        self.categorie_2_var = StringVar(value=self.liste_categories[0])
        self.categorie_2_options = OptionMenu(self, self.categorie_2_var, *self.liste_categories)
        self.categorie_2_options.config(width=15, font=('Helvetica', 12))
        #self.categorie_2_options.pack()
        # On crée le controle niveau
        self.niveau_var = StringVar(value=self.liste_niveaux[0])
        self.niveau_options = OptionMenu(self, self.niveau_var,self.liste_niveaux[1] ,*self.liste_niveaux)
        self.niveau_options.config(width=15, font=('Helvetica', 12))
        #self.niveau_options.pack()
        # On crée le controle joueur qui commence
        self.joueur_qui_commence_var = StringVar()
        self.joueur_qui_commence_var.set(self.nom_1_entry.get())
        self.liste_joueurs=[self.nom_1_entry.get(),self.nom_2_entry.get()]
        self.joueur_qui_commence_options = OptionMenu(self, self.joueur_qui_commence_var, *self.liste_joueurs)
        self.joueur_qui_commence_options.config(width=15, font=('Helvetica', 12))
        #self.joueur_qui_commence_options.pack()
        # Bouton pour confirmer les choix
        self.btn_confirmer = Tk.Button(self, text="Confirmer", command=self.confirmer_choix)
        self.btn_confirmer.pack_forget()




        def mettre_a_jour_affichage(a, b, c):
            # ... (placement et configuration de l'OptionMenu)
            if self.mode_var.get()=="Choisir_mode":
                self.label_nom_1.pack_forget()
                self.entry_nom_1.pack_forget()
                self.label_nom_2.pack_forget()
                self.entry_nom_2.pack_forget()
                self.categorie_1_options.pack_forget()
                self.categorie_2_options.pack_forget()
                self.niveau_options.pack_forget()
                self.joueur_qui_commence_options.pack_forget()
                self.btn_confirmer.pack_forget()
            elif self.mode_var.get()=="automatique":
                #self.mode_options.pack_forget()
                self.nom_1_entry.set("IA_1")
                self.categorie_1_var.set(self.liste_categories[2])
                self.nom_2_entry.set("IA_2")
                self.categorie_2_var.set(self.liste_categories[2])
                self.niveau_var.set(self.liste_niveaux[1])
                self.joueur_qui_commence_var.set("IA_1")
                self.btn_confirmer.pack()
            elif self.mode_var.get()=="un_joueur": # Un joueur humain
                self.btn_confirmer.pack_forget()
                self.label_nom_1.pack()
                self.entry_nom_1.pack()
                if self.verifier_nom(self.nom_1_entry.get()):
                    self.nom_2_entry.set("IA_2")
                    self.categorie_1_var.set(self.liste_categories[1])
                    self.categorie_2_var.set(self.liste_categories[2])
                    self.niveau_options.pack()
                    print(f"Niveau choisi: {self.niveau_var.get()}")
                    #if not (self.niveau_var.get()== liste_niveaux[0]):
                    self.joueur_qui_commence_options.pack()
                    if self.joueur_qui_commence_var.get() not in (self.nom_1_entry.get(),self.nom_2_entry.get()) :
                        result_nom = 'Vous devez choisir le joueur qui commence(joueur 1/joueur 2)'
                        self.msg_text.set(result_nom)
                    else:
                        self.joueur_qui_commence_var.get()
                        self.btn_confirmer.pack()
                    # else:
                    #     result_nom = 'Vous devez choisir le niveau de jeu'
                    #     self.msg_text.set(result_nom)

            else: # deux joueurs humains
                self.btn_confirmer.pack_forget()
                self.label_nom_1.pack()
                self.entry_nom_1.pack()
                self.label_nom_2.pack()
                self.entry_nom_2.pack()
                if self.verifier_nom(self.nom_1_entry.get()) and self.verifier_nom(self.nom_2_entry.get()):
                    self.categorie_1_var.set(self.liste_categories[1])
                    self.categorie_2_var.set(self.liste_categories[1])
                    #self.niveau_options.pack()
                    self.joueur_qui_commence_options.pack()
                    if self.verifier_nom(self.nom_1_entry.get() and self.verifier_nom(self.nom_2_entry.get())):
                        self.categorie_1_var.set(self.liste_categories[1])
                        self.categorie_2_var.set(self.liste_categories[1])
                        self.niveau_options.pack()
                        #if not self.niveau_var.get() == liste_niveaux[0]:
                        self.joueur_qui_commence_options.pack()
                        if self.joueur_qui_commence_var.get() not in (self.nom_1_entry.get(),self.nom_2_entry.get()) :
                            result_nom = 'Vous devez choisir le joueur qui commence(joueur/ordinateur)'
                            self.msg_text.set(result_nom)
                        else:
                            self.joueur_qui_commence_var.get()
                            self.btn_confirmer.pack()
                        # else:
                        #     result_nom = 'Vous devez choisir le niveau du jeu'
                        #     self.msg_text.set(result_nom)
                # else:
                #     result_nom = 'Vous devez entrer le nom des deux joueurs'
                #     self.msg_text.set(result_nom)

        def mettre_a_jour_liste_joueurs(a,b,c):
            self.liste_joueurs = [self.nom_1_entry.get(), self.nom_2_entry.get()]
            self.joueur_qui_commence_options.configure(menu=create_menu(self.liste_joueurs))

        def create_menu(values):
            menu = Menu(self.joueur_qui_commence_options)
            for value in values:
                menu.add_radiobutton(label=value, variable=self.joueur_qui_commence_var, value=value)
            return menu



        # Assurez-vous que nom_1_entry.get() et nom_2_entry.get() sont des StringVar()
        self.nom_1_entry.trace("w", mettre_a_jour_liste_joueurs)
        self.nom_2_entry.trace("w", mettre_a_jour_liste_joueurs)
        self.mode_var.trace("w", mettre_a_jour_liste_joueurs)
        self.mode_var.trace("w", mettre_a_jour_affichage)
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
        joueur_qui_commence = self.joueur_qui_commence_var.get()
        # Utilisation des valeurs choisies (par exemple, appel à une fonction du contrôleur)
        if self.controller:
            self.controller.traiter_choix(mode_choisi, nom_1, nom_2, categorie_1_choisie, categorie_2_choisie, niveau_choisi, joueur_qui_commence)
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

        self.mode_jeu_text = StringVar()
        self.mode_jeu = ttk.Label(self, textvariable=self.mode_jeu_text, width=50, relief='ridge', font=('Helvetica', 12))
        self.mode_jeu.place(x=450, y=10)

        self.nom_j_1_text = StringVar()
        self.nom_j_1 = ttk.Label(self, textvariable=self.nom_j_1_text, width=50, relief='ridge',  font=('Helvetica', 12))
        self.nom_j_1.place(x= 450, y=40 )

        self.nom_j_2_text = StringVar()
        self.nom_j_2 = ttk.Label(self, textvariable=self.nom_j_2_text,  width=50, relief='ridge', font=('Helvetica', 12))
        self.nom_j_2.place(x=450, y=70)

        self.niveau_text = StringVar()
        self.niveau_jeu = ttk.Label(self, textvariable=self.niveau_text,  width=50, relief='ridge', borderwidth=2, font=('Helvetica', 12))
        self.niveau_jeu.place(x= 450, y=100)

        self.qui_commence_text = StringVar()
        self.qui_commence = ttk.Label(self, textvariable=self.qui_commence_text, width=50, relief='ridge', borderwidth=2,
                                    font=('Helvetica', 12))
        self.qui_commence.place(x=450, y=130)

        self.resultat_jeu_text = StringVar()
        self.resultat_jeu = ttk.Label(self, textvariable=self.resultat_jeu_text, justify=CENTER, relief='ridge', borderwidth=2,font=('Helvetica', 12))
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

    def mettre_a_jour_donnees(self, mode, nom_joueur_1, nom_joueur_2, niveau_jeu, nom_joueur, disable_rejouer):
        self.mode_jeu_text.set(f"Mode de jeu       : {mode}")
        self.nom_j_1_text.set(f"Nom du joueur 1 : {nom_joueur_1}")
        self.nom_j_2_text.set(f"Nom du joueur 2 : {nom_joueur_2}")
        self.niveau_text.set(f"Niveau de jeu : {niveau_jeu}")
        self.qui_commence_text.set(f"Joueur qui commence : {nom_joueur}")
        if disable_rejouer:
            self.btn_rejouer.config(state=DISABLED )
            self.resultat_jeu.place_forget()
        else:
            self.btn_rejouer.config(state=NORMAL )


    def ecrire_resultat(self, resultat_jeu, disable_rejouer):
        if disable_rejouer:
            self.btn_rejouer.config(state=DISABLED)
        else:
            self.btn_rejouer.config(state=NORMAL)
            self.resultat_jeu_text.set(resultat_jeu)
            self.resultat_jeu.place(x= 350, y=420, anchor='center')

    def gestion_clic_gauche(self,event):
        # Récupération des coordonnées du clic
        # x, y = event.x, event.y
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
class Identification(Tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        #Tk.Frame.__init__(self, parent)
        self.userid = ""
        self.nom = ""
        self.prenom = ""
        self.ddn = '01/01/1900'
        self.date_valide = False
        self.data_p = []
        self.userid_valide = False
        self.prenom_valide = False
        self.nom_valide = False
        self.couleurFondMenu = 'lightyellow'
        self.couleurFondExo = 'lightgreen'
        # Tester l'existence du fichier
        file_name = r"personnes.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as P_File:
                self.data_p = json.load(P_File)
        self.identite = Tk.StringVar()
        if len(self.data_p) + 1 > 5:
            hauteur = 5
        else:
            hauteur = len(self.data_p) + 1
        self.liste_P = Tk.Listbox(self, height=hauteur + 1, width=50, state='normal')
        self.liste_P.title = "Choisissez votre nom dans la liste ou ajoutez le en cliquant sur le bouton 'Ajouter un " \
                             "utilisateur' "
        self.liste_P.pack()
        for x in range(len(self.data_p)):
            self.liste_P.insert(END, "{0}-{1}-{2}".format(self.data_p[x]["Userid"], self.data_p[x]["firstName"],
                                                          self.data_p[x]["lastName"]))
        self.liste_P.focus_set()
        self.liste_P.index(2)
        self.liste_P.activate (2)
        self.liste_P.bind('<Return>', self.focusliste_p)

    def focusliste_p(self, event=None):
        self.liste_P.focus_set()

