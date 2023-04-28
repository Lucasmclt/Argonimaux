import GestionDonnees.extractionCSV as E


#----------------------CRÉATION DE LA BASE DE DONNÉES-------------------------------
#Création de la base de données Argonimaux et des tables
def creation(connection):
    """
    La fonction créer toutes les tables dans la base de données Argonomaux.db
    Le parametre connection est un objet permettant de se connecter avec la base de données
    À éxecuter uniquement lors de la première compilation du code
    Ne renvoie rien, modifie uniquement la base de données
    """

    cursor = connection.cursor()
    #Création de la table tortues dans la base Argonimaux
    cursor.execute(
        "CREATE TABLE animaux (id int PRIMARY KEY, num int, cl varchar, jour varchar, heure varchar, latitude float, longitude float)"
    )

    #Création de la table faisant le lien entrte le nom de l'animal et son numéro
    cursor.execute(
        "CREATE TABLE liens(num int PRIMARY KEY, nom varchar, type VARCHAR)")


#-----------AJOUT DES LIENS ENTRE LE NUMÉRO, LE NOM ET LE TYPE DE L'ANIMAL----------
def Lien(connection, d):
    """
    La fonction ajoute dans la table liens tout les éléments qui sont relatifs à chaque animal
    Le parametre connection est un objet permettant de se connecter avec la base de données
    d est de type dictionnaire
    Ne renvoie rien, modifie uniquement la table liens
    """

    cursor = connection.cursor()

    ajout = "INSERT INTO liens VALUES(?, ?, ?)"

    for k in d.keys():

        for i in range(len(d[k])):
            f = f"{d[k][i]}.txt"
            extract = E.extraction(f)

            cursor.execute(ajout, (extract[0][0], d[k][i], k))


#------------------AJOUT DES ENREGISTREMENTS DANS LA TABLE TORTUES------------------
def ajoutEnregistrement(fichier, connection):
    """
    La fonction ajoute dans la base de données chaque ligne contenue dans le fichier
    Le parametre fichier est une liste de listes ; les données extraitent d'un fichier .txt
    Le parametre connection est un objet permettant de se connecter avec la base de données
    La fonction ne renvoie rien
    """

    #id pour identifier chaque enregistrement dans la table
    id = 0

    cursor = connection.cursor()

    c = cursor.execute("SELECT COUNT(*) FROM animaux")
    count = cursor.fetchall()

    if count[0][0] == 0:
        id = 1
    else:
        id += count[0][0] + 1

    ajout = "INSERT INTO animaux VALUES(?,?,?,?,?,?,?)"

    for ligne in fichier:

        cursor.execute(
            ajout,
            (id, ligne[0], ligne[1], ligne[2], ligne[3], ligne[4], ligne[5]))

        id += 1



#---------------------------EXTRACTION NOM ET TYPE---------------------------
def nomCoordonnees(connection, x1, x2, y1, y2):
    """
    La fonction renvoie le nom et le type des animaux présents entre les coordonnées passées en paramètre
    Les paramètres x1, x2, y1, y2 sont de type float et convertits en degrés au préalable
    Le parametre connection est un objet permettant de se connecter avec la base de données
    La fonction renvoi la selection des animaux sous forme de liste de tuples
    """

    cursor = connection.cursor()

    cursor.execute(
        "SELECT DISTINCT nom FROM liens INNER JOIN animaux ON liens.num = animaux.num WHERE longitude>:lo1 AND longitude<:lo2 AND latitude<:la1 AND latitude>:la2",
        {
            "lo1": x1,
            "lo2": x2,
            "la1": y1,
            "la2": y2
        })

    selection = cursor.fetchall()

    return selection


#-------------------------EXTRACTION COORDONNES D'UN ANIMAL------------------
def coordonnesAnimal(connection, nomAnimal):
    """
    La fonction renvoie les coordonées (longitude, latitude) selon le nom d'un animal
    Le paramètre nom est de type string
    Le parametre connection est un objet permettant de se connecter avec la base de données
    La fonction renvoi la selection des coordonnées sous forme de liste tuples
    """

    cursor = connection.cursor()

    #cursor.execute(
    #"SELECT latitude, longitude FROM liens INNER JOIN animaux ON liens.num = animaux.num WHERE nom=:n",
    #{"n": nomAnimal})

    cursor.execute("SELECT longitude, latitude FROM liens INNER JOIN animaux ON liens.num = animaux.num WHERE nom=:n", {"n": nomAnimal})

    selection = cursor.fetchall()

    print(selection)
    
    return selection
