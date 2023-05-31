import GestionDonnees.gestionBD as gestion
import GestionDonnees.extractionCSV as e

import tkinter.font as font
from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont

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
    "requin": ["Anna Pelerine", "Gary", "Marie B"],
    "bouée": [
        "ChildOceans", "Coris", "Coris 2", "Zelisca", "Pegase 2019", "Phebus",
        "VenusExpe", "Meduse"
    ]
}

#Ouvre une connection avec la base de données
connection = sqlite3.connect("Argonimaux.db")


#Tentative de création des tables de la base de données, s'il elles existent déjà, le code continue sont éxecution
try:
    gestion.creation(connection)
except:
    print("Les tables existent déjà")

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


#-------------------------------Création de la fenêtre--------------------------
#Définition de la fenetre principale
fenetre = Tk()
fenetre.geometry("1000x1000")
fenetre.minsize(1000, 1000)
fenetre.configure(bg = "White", padx = 8, pady = 8)
fenetre.overrideredirect(False)
fenetre.title('Argonimaux')
fenetre.iconbitmap('icon.ico')
fenetre.state("zoomed")


#-------------------------------------------------------------------------------
#Création d'un canvas pour la carte
imageFrame = Frame(fenetre, width=678, height=998, borderwidth = 5, bg = "Black")
imageFrame.pack(side="left")

#Importation de la carte
photo = PhotoImage(file="Affichage/openstreetmap.png")
canvas = Canvas(imageFrame, width=680, height=1000)
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack()


#-------------------------------------------------------------------------------
#Définition de la police
police = tkfont.Font(family="Onest-Regular.ttf", size = 10,  weight = "bold")

#-------------------------------------------------------------------------------
#Fonction servant à réaliser des rectangles avec des coins arrondis
def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):

    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

#my_rectangle = round_rectangle(50, 50, 150, 100, radius=20, fill="blue")

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
                             alpha=.3)
        elif nombre_animaux_zone < 10 and nombre_animaux_zone > 5:  #si le nombre de tortues présentes est supérieur à 5 et inférieur à 10
            create_rectangle(points_x[i],
                             points_y[j],
                             points_x[i + 1],
                             points_y[j + 1],
                             fill=codes_couleur[2],
                             alpha=.3)
        elif nombre_animaux_zone < 5 and nombre_animaux_zone > 1:  #si le nombre de tortues présentes est supérieur à 1 et inférieur à 5
            create_rectangle(points_x[i],
                             points_y[j],
                             points_x[i + 1],
                             points_y[j + 1],
                             fill=codes_couleur[1],
                             alpha=.3)
        elif nombre_animaux_zone == 1:  #si le nombre de tortues présentes est égal à 1
            create_rectangle(points_x[i],
                             points_y[j],
                             points_x[i + 1],
                             points_y[j + 1],
                             fill=codes_couleur[0],
                             alpha=.3)
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


#------------------------------------BOUTONS------------------------------------
#------------------------------------BOUTON 2-----------------------------------
#Le bouton 2 permet de fermer la page
def BoutQuit():
    fenetre.destroy()  #Fonction qui permet de fermer la page en détruisant les widgets


boutQuitter = Button(fenetre, bg = 'red', fg = 'white', text = "QUITTER", relief = FLAT, command = BoutQuit, font = police)  #Création du bouton quitter
boutQuitter.pack(side=BOTTOM, padx=10)  #Position du bouton

#-------------------------------------LOGO--------------------------------------
logo = PhotoImage(file = "Affichage/logoPage.png")

canvasLogo = Canvas(fenetre, width = 500, height = 100, borderwidth = 0, highlightthickness = 0, bg = "white")
canvasLogo.create_image(250, 50, image = logo)
canvasLogo.pack()


#-------------------------------------COMBOBOX----------------------------------
#Variable permettant de stocker l'animal sélection ; une valeur est déjà sélectionné par defaut
AnimalSelect = ""

#Création d'une combobox avec les élémnts présents dans la zone sélectionnée
def Selection(event):
    #Obtenir l'élément sélectionné
    global AnimalSelect
    AnimalSelect = str(listeCombo.get())


selectionFrame = Frame(fenetre, width = 700, height = 200, bg = "white", padx = 10, pady = 10)
selectionFrame.pack()



Texte1 = Label(selectionFrame, text = "Cliquer sur une zone et choisir un élément à localiser", font = police, bg = "white")
Texte1.pack()

AnimauxCombo = ["Aucune case sélectionnée"]  # Choix de l'animal

listeCombo = ttk.Combobox(selectionFrame, values = AnimauxCombo, width = 50, font = police)  #Création de la Combobox via la méthode ttk.Combobox()
listeCombo.current(0)  #Choix de l'élément qui s'affiche par défaut

listeCombo.pack(pady = 10)
listeCombo.bind("<<ComboboxSelected>>", Selection)  # Application de la fonction selection à l'élément



#------------------------------------BOUTON 1----------------------------------------------------------
#Le bouton 1 permet afficher la carte avec le trajet complet d'un élément
def AfficherCarte():

    #Liste contenant les coordonnées de l'élèment sélectionné
    table = gestion.coordonnesAnimal(connection, AnimalSelect)

    #Création d'une carte
    fmap = folium.Map(location = [43.604598, 1.445456], tiles="OpenStreetMap", zoom_start = 4.5)

    #Ajout d'un marqueur
    folium.Marker([43.604598, 1.445456])

    #Ajout d'une ligne brisée définie à partir de 5 points
    folium.PolyLine(table, color="blue", weight=2.5, opacity=0.8).add_to(fmap)

    fmap.save("carte.html")  #Génération du fichier HTML contenant la carte
    webbrowser.open("carte.html")  #Ouverture d'une nouvelle page avec la carte

    # placement des marqueurs
    for i in range(0,len(date),50):

        print(date[i][0])
        x = date[i][0][::-1]
        j = date[-1]
        m = date[5:6]
        a = date[0:3]
        date = j/m/a
        print(date)



        folium.Marker(table[i], x, icon=folium.Icon(color='darkblue')).add_to(fmap)
    # Ajout d'un marqueur
    
    
#Création bouton 1
btn1 = Button(fenetre,
              bg='green',
              fg='white',
              text="Afficher le chemin",
              relief=FLAT,
              command=AfficherCarte,
              font = police)

btn1.pack(side = BOTTOM, padx = 10, pady = 10)

#-----------------------------------Légende----------------------------------------------------------------------------------------
#Affichage de la légende qui permet de comprendre la signification des surbrillances présentes sur la carte

Legende = Label(
    fenetre,
    text=
    "La couleur varie du vert au rouge selon le nombre d'éléments présents dans la zone :", font = police)
Legende.pack()


Legende2 = Label(fenetre, text="- Vert = 1 élément présent dans la zone", font = police)
Legende2.pack()

Legende3 = Label(fenetre,
                 text="- Orange = entre 2 et 4 éléments présents dans la zone")
Legende3.pack()
Legende3['font'] = police

Legende4 = Label(fenetre, text = "- Rouge = entre 5 et 10 éléments présents dans la zone")
Legende4.pack()
Legende4['font'] = police

Legende5 = Label(fenetre, text = "- Rouge Foncé = plus de 10 éléments présents dans la zone")
Legende5.pack()
Legende5['font'] = police

#-----------------------------------------------------LISTBOX-----------------------------------------------------------------------------
#Création des listes permettant de visualiser tout les éléments géolocalisable
#Listbox Tortues

Texte2 = Label(fenetre, text = 'Ensemble des éléments géolocalisables :', underline = 1)
Texte2.pack(pady = 10)
Texte2['font'] = police

Texte3 = Label(fenetre, text='Tortues :')
Texte3.pack()
Texte3['font'] = police

listboxT = Listbox(fenetre)#Création le la listbox

for i in range(len(animaux['tortue'])):
    listboxT.insert(i, animaux['tortue'][i])
listboxT.pack()
listboxT.configure(state = DISABLED)


#Listbox Balises
Texte5 = Label(fenetre, text='Balises :')
Texte5.pack()
Texte5['font'] = police

listboxT = Listbox(fenetre)  # création le la listbox

for i in range(len(animaux['bouée'])):
    listboxT.insert(i, animaux['bouée'][i])
listboxT.pack()
listboxT.configure(state = DISABLED)


#Listbox Requins
Texte4 = Label(fenetre, text='Requins :')
Texte4.pack()
Texte4['font'] = police

listboxT = Listbox(fenetre)  #Création le la listbox
for i in range(len(animaux['requin'])):
    listboxT.insert(i, animaux['requin'][i])
listboxT.pack()
listboxT.configure(state = DISABLED)

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
