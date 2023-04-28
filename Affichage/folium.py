import folium
import webbrowser
import sqlite3
import GestionDonnees.gestionBD as gestion

connection = sqlite3.connect("Argonimaux.db")

nom = "Rosa"
table = gestion.coordonnesAnimal(connection, nom)

#****************************************************************
tableau1 = [[float(ligne["Lat"]), float(ligne["Long"])] for ligne in table]
""" A Faire : Enlever les # afin d'afficher le résultats des 2 exemples ci-cessous :"""
print('t1 = ', tableau1)

# Création d'une carte
fmap = folium.Map(location=[43.604598, 1.445456],
                  tiles="OpenStreetMap",
                  zoom_start=4.5)

# Ajout d'un marqueur
folium.Marker([43.604598, 1.445456])

# Ajout d'une ligne brisée définie à partir de 5 points

folium.PolyLine(tableau1, color="blue", weight=2.5, opacity=0.8).add_to(fmap)

# Génération du fichier HTML contenant la carte
fmap.save("carte.html")
webbrowser.open("carte.html")

connection.close()
