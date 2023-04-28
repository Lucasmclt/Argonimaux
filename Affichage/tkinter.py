import GestionDonnees.gestionBD as gestion
import GestionDonnees.extractionCSV as e

import tkinter.font as font
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

import folium
import webbrowser
import sqlite3

nom = ""

#Dictionnaire contenant tout le nom des animaux et leur type (tortues, requins, bouées)
animaux = {
    "tortue": [
        "Anna Antimo",
        "Antioche",
        "Ashoka",
        "Bambi",
        "Bouton d'or",
        "Chacahe",
        "Danae",
        "Delta",
        "Domino",
        "Laura",
        "Moana",
        "Muse",
        "Neus",
        "Ninja-Balaeres",
        "Rosa",
        "Tikaf",
        "Tom",
        "Vita",
        "Zamzam",
    ],
    "requin": ["Anna Pelerine", "Marie B", "Gary"],
    "bouée": [
        "ChildOceans", "Coris", "Coris 2", "Zelisca", "Pegase 2019", "Phebus",
        "VenusExpe", "Meduse"
    ]
}

#Ouvre une connection avec la base de données
connection = sqlite3.connect("Argonimaux.db")

#À exécuter UNIQUEMENT lors de la première exécution
#gestion.creation(connection)

#Ajout chaque ligne de chaque animal dans la table
for k in animaux.keys():
    for i in range(len(animaux[k])):
        f = f"{animaux[k][i]}.txt"
        gestion.ajoutEnregistrement(e.extraction(f), connection)

#Créer le lien entre le nom, le type et le numéro de chaque animal et l'ajoute dans la table liens
gestion.Lien(connection, animaux)


#-------------------------------------------------------------------------------------------------------------------------------------
#Conversion des pixels en degré (valeurs x)
def conversion_pxx_coord(px):
    m = 340
    d = 0
    if px == m:
        return d
    elif px > m:
        d = (px - m) / (340 / 15)
    elif px < m:
        d = (px - m) / (340 / 15)
    return d


#Conversion des pixels en degré (valeurs y)
def conversion_pxy_coord(py):
    d = -((py / (1000 / 30)) - 60)
    return d


images = []


#La fonction permet de créer un rectancle sur un canvas
def create_rectangle(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = fenetre.winfo_rgb(fill) + (alpha, )
        image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=images[-1], anchor='nw')
    canvas.create_rectangle(x1, y1, x2, y2, **kwargs)


#--------------------------Création de la fenêtre--------------------------
#Définition de la fenetre principale
fenetre = Tk()
fenetre.geometry("1000x1000")
fenetre.minsize(1000, 1000)
fenetre.title('Argonimaux')
#fenetre.iconbitmap('icon.ico')

#Importation de la carte
photo = PhotoImage(file="Affichage/openstreetmap.png")
canvas = Canvas(fenetre, width=680, height=1000)
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack(side=LEFT)

#--------------------------Mise en place d'un quadrillage-------------------------------
#Définition du nombre de case sur les abscisses (longitude)
points_x = [i for i in range(0, 680, 23)]
points_x.append(points_x[-1] + 26)

#Définition du nombre de case sur les ordonées (latitude)
points_y = [i for i in range(0, 1000, 33)]
points_y.append(points_y[-1] + 66)

#Gestion subriance en fonction du nombre d'éléments présents
codes_couleur = ['Green', 'OrangeRed', 'Red', 'DarkRed']

for i in range(len(points_x) - 1):
    for j in range(len(points_y) - 1):
        nombre_animaux_zone = len(
            gestion.nomCoordonnees(connection,
                                   conversion_pxx_coord(points_x[i]),
                                   conversion_pxx_coord(points_x[i + 1]),
                                   conversion_pxy_coord(points_y[j]),
                                   conversion_pxy_coord(points_y[j + 1])))
        if nombre_animaux_zone >= 10:  #si le nombre de tortues présentes est supérieur ou égal à 10
            create_rectangle(points_x[i],
                             points_y[j],
                             points_x[i + 1],
                             points_y[j + 1],
                             fill=codes_couleur[3],
                             alpha=.2)
        elif nombre_animaux_zone < 10 and nombre_animaux_zone > 5:  #si le nombre de tortues présentes est supérieur à 5 et inférieur à 10
            create_rectangle(points_x[i],
                             points_y[j],
                             points_x[i + 1],
                             points_y[j + 1],
                             fill=codes_couleur[2],
                             alpha=.2)
        elif nombre_animaux_zone < 5 and nombre_animaux_zone > 1:  #si le nombre de tortues présentes est supérieur à 1 et inférieur à 5
            create_rectangle(points_x[i],
                             points_y[j],
                             points_x[i + 1],
                             points_y[j + 1],
                             fill=codes_couleur[1],
                             alpha=.2)
        elif nombre_animaux_zone == 1:  #si le nombre de tortues présentes est égal à 1
            create_rectangle(points_x[i],
                             points_y[j],
                             points_x[i + 1],
                             points_y[j + 1],
                             fill=codes_couleur[0],
                             alpha=.2)
        else:  #si le nombre de tortues est égal à 0
            create_rectangle(points_x[i],
                             points_y[j],
                             points_x[i + 1],
                             points_y[j + 1],
                             fill='black',
                             alpha=0)


#--------------------------Détection du clic de l'utilisateur--------------------------
#Séléction de la zone en valeurs x1, x2, y1, y2 du clic de l'utilisateur
def coord_clic(evt):

    zone_select = [[None, None], [None, None]]

    posx, posy = evt.x, evt.y  #récupération des coordonnées du cuseur de l'utilisateur
    rangx = posx // 23
    rangy = posy // 33
    zone_select = [[points_x[rangx], points_x[rangx + 1]],
                   [points_y[rangy], points_y[rangy + 1]]]

    insertionvaleurslistbox(zone_select[0][0], zone_select[0][1],
                            zone_select[1][0], zone_select[1][1])
    return zone_select


#------------------------------------BOUTONS-----------------------------------------------------------
#------------------------------------BOUTON 2----------------------------------------------------------
#Le bouton 2 permet de fermer la page
f1 = font.Font(
    family='Courier', size=10, weight="bold"
)  # définition de 2 styles d'écriture (pour le titre et le texte)
f2 = font.Font(family='Courier', size=30, weight="bold")


def BoutQuit():
    fenetre.destroy(
    )  # Fonction qui permet de fermer la page en détruisant les widgets


boutQuitter = Button(fenetre,
                     bg='red',
                     fg='white',
                     text="QUITTER",
                     relief=FLAT,
                     command=BoutQuit)  # création du bouton quitter
boutQuitter.pack(side=BOTTOM, padx=10)  #position du bouton
boutQuitter['font'] = f1  #style du bouton

#-------------------------------------------------------------------------------------------------------------------------------------
#Affiche le titre de la page
Titre = Label(fenetre,
              text="ARGONIMAUX",
              justify=CENTER,
              padx=100,
              pady=10,
              bg='LawnGreen',
              fg='Black',
              relief=SUNKEN)
Titre.pack()
Titre['font'] = f2

#Variable permettant de stocker l'animal sélection ; une valeur est déjà sélectionné par defaut
AnimalSelect = ""


#---------------------------------------COMBOBOX---------------------------------------------------------------------------------------
#Création d'une combobox avec les élémnts présents dans la zone sélectionnée
def Selection(event):
    #Obtenir l'élément sélectionné
    global AnimalSelect
    AnimalSelect = str(listeCombo.get())


Texte1 = Label(fenetre,
               text="Cliquer sur une zone et choisir un élément à localiser")
Texte1.pack(pady=10)
Texte1['font'] = f1

AnimauxCombo = ["Aucune case sélectionnée"]  # Choix de l'

listeCombo = ttk.Combobox(
    fenetre, values=AnimauxCombo,
    width=50)  #Création de la Combobox via la méthode ttk.Combobox()

listeCombo.current(0)  #Choix de l'élément qui s'affiche par défaut

listeCombo.pack(pady=10)
listeCombo.bind("<<ComboboxSelected>>",
                Selection)  # Application de la fonction selection à l'élément

print(nom)

#------------------------------------BOUTON 1----------------------------------------------------------
#Le bouton 1 permet afficher la carte avec le trajet complet d'un élément
def AfficherCarte():

    #Liste contenant les coordonnées de l'élèment sélectionné
    table = gestion.coordonnesAnimal(connection, AnimalSelect)

    #Création d'une carte
    fmap = folium.Map(location=[43.604598, 1.445456],
                      tiles="OpenStreetMap",
                      zoom_start=4.5)

    #Ajout d'un marqueur
    folium.Marker([43.604598, 1.445456])

    #Ajout d'une ligne brisée définie à partir de 5 points
    folium.PolyLine(table, color="blue", weight=2.5, opacity=0.8).add_to(fmap)

    fmap.save("carte.html")  #Génération du fichier HTML contenant la carte
    webbrowser.open("carte.html")  #Ouverture d'une nouvelle page avec la carte


#Création bouton 1
btn1 = Button(fenetre,
              bg='green',
              fg='white',
              text="Afficher le chemin",
              relief=FLAT,
              command=AfficherCarte)

btn1.pack(side=BOTTOM, padx=10, pady=10)
btn1['font'] = f1

#-----------------------------------Légende----------------------------------------------------------------------------------------
#Affichage de la légende qui permet de comprendre la signification des surbrillances présentes sur la carte

Legende = Label(
    fenetre,
    text=
    "La couleur varie du vert au rouge selon le nombre d'éléments présents dans la zone :"
)
Legende.pack()
Legende['font'] = f1

Legende2 = Label(fenetre, text="- Vert = 1 élément présent dans la zone")
Legende2.pack()
Legende2['font'] = f1

Legende3 = Label(fenetre,
                 text="- Orange = entre 2 et 4 éléments présents dans la zone")
Legende3.pack()
Legende3['font'] = f1

Legende4 = Label(fenetre,
                 text="- Rouge = entre 5 et 10 éléments présents dans la zone")
Legende4.pack()
Legende4['font'] = f1

Legende5 = Label(
    fenetre, text="- Rouge Foncé = plus de 10 éléments présents dans la zone")
Legende5.pack()
Legende5['font'] = f1

#-----------------------------------------------------LISTBOX-----------------------------------------------------------------------------
#Création des listes permettant de visualiser tout les éléments géolocalisable
#Listbox Tortues

Texte2 = Label(fenetre,
               text='Ensemble des éléments géolocalisables :',
               underline=1)
Texte2.pack(pady=10)
Texte2['font'] = f1

Texte3 = Label(fenetre, text='Tortues :')
Texte3.pack()
Texte3['font'] = f1

listboxT = Listbox(fenetre)  # création le la listbox
listboxT.insert(0, 'Anna Antimo')  # ajout des différents éléments
listboxT.insert(1, 'Antioche')
listboxT.insert(2, 'Ashoka')
listboxT.insert(3, 'Bambi')
listboxT.insert(4, 'Bouton d’or')
listboxT.insert(5, 'Chacaé')
listboxT.insert(6, 'Danaé')
listboxT.insert(7, 'Delta')
listboxT.insert(8, 'Domino')
listboxT.insert(9, 'Ecume')
listboxT.insert(10, 'Tika')
listboxT.insert(11, 'Lora')
listboxT.insert(12, 'Tom')
listboxT.insert(13, 'Zamzam')
listboxT.insert(14, 'Rosa')
listboxT.insert(15, 'Vita')
listboxT.insert(16, 'Ninja-Baleores')
listboxT.insert(17, 'Neus')
listboxT.insert(18, 'Muse')
listboxT.insert(19, 'Maona')
listboxT.pack()

#Listbox Balises
Texte5 = Label(fenetre, text='Balises :')
Texte5.pack()
Texte5['font'] = f1

listboxT = Listbox(fenetre)  # création le la listbox
listboxT.insert(0, 'ChildOceans')  # ajout des différents éléments
listboxT.insert(1, 'Coris')
listboxT.insert(2, 'Coris 2')
listboxT.insert(3, 'Zelisca')
listboxT.insert(4, 'Pégasse 2019')
listboxT.insert(5, 'Phébus')
listboxT.insert(6, 'Théthyse')
listboxT.insert(7, 'Venus Expe')
listboxT.insert(8, 'Méduse')
listboxT.pack()

#Listbox Requins
Texte4 = Label(fenetre, text='Requins :')
Texte4.pack()
Texte4['font'] = f1

listboxT = Listbox(fenetre)  #Création le la listbox
listboxT.insert(0, 'Anna Pèlerine')  #Ajout des différents éléments
listboxT.insert(1, 'Marie B')
listboxT.insert(2, 'Gary')
listboxT.pack()

#-----------------------------------------------------------------------------------------------------------------------------------------
#Détection des clics de la souris sur la carte
canvas.bind("<Button-1>", coord_clic)


#Insertion du nom des animaux dans la liste à afficher (cf. COMBOBOX)
def insertionvaleurslistbox(posx1, posx2, posy1, posy2):

    AnimauxCombo = gestion.nomCoordonnees(connection,
                                          conversion_pxx_coord(posx1),
                                          conversion_pxx_coord(posx2),
                                          conversion_pxy_coord(posy1),
                                          conversion_pxy_coord(posy2))

    listeCombo.configure(values=AnimauxCombo)


#--------------------------
#Actualisation de la fenêtre graphique
fenetre.mainloop()
