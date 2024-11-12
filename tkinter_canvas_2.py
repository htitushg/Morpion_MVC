import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Canvas, Scrollbar, Button


class Application(tk.Tk):
    def __init__(self, data, entete):
        super().__init__()
        # calcul des dimensions et choix de la fonte
        width_column, total_width, total_height = self.calcul_des_dimensions(data, entete)
        taille_fonte = 14

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
        x = 30
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

if __name__ == "__main__":
    # Création des colonnes
    entete = ["Nom", "Date de l'essai", "Mode", "Niveau", "Résultat"]
    # Données d'exemple
    data = [
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"},
        {"Nom": "Joueur 1", "Date de l'essai": "2023-11-22", "Mode": "Facile", "Niveau": 1, "Résultat": "Succès"},
        {"Nom": "Joueur 2", "Date de l'essai": "2023-11-23", "Mode": "Difficile", "Niveau": 3, "Résultat": "Échec"}
    ]

    app = Application(data, entete)
    app.mainloop()