import csv

#--------------------------EXTRACTION DES DONNES--------------------------
#Extraction des données du fichier .txt
#Chaque ligne du fichier est une liste python
def extraction(fichier):
    """
    La fonction extraction extrait chaque ligne d'un fichier .txt et les ajoute dans une liste 
    Le paramètre fichier est un fichier .txt
    Renvoie une liste de listes
    """

    listeFichier = []

    with open(fichier, 'r') as f:
        file = csv.reader(f, delimiter="\t")

        for ligne in file:
            listeFichier.append(ligne)

    
    return listeFichier