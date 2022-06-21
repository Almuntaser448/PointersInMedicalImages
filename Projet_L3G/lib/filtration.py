import matplotlib.image as mplimg
import numpy as np
import os
import shutil

# Permet de filtrer les images en fonctions des dimensions des templates
	
def filtration(cheminDossierSource) :
    nbLigneMax = 0
    nbLigneMin = 2000
    nbColonneMax = 0
    nbColonneMin = 2000
    aireMax=0
    aireMin=10000
	# Cree une liste des fichiers des images et des templates
    fichiersTemplate = os.listdir(cheminDossierSource + "\\src\\ref\\") 
	# Cree une liste des dossiers des CC obtenues pour chaque image (sans tri)
    dossierCC = os.listdir(cheminDossierSource + "\\stock\\" )
	#Boucle modifiant l'aire, le nombre maximal et le nombre minimal de lignes et de colonnes en fonction des dimensions des templates 
    for element in fichiersTemplate :
        if "template" not in element :
            continue
        template = mplimg.imread (cheminDossierSource + "\\src\\ref\\" +element).astype(np.uint8)
        nbLigne=np.shape(template)[0]
        nbColonne=np.shape(template)[1]
        aire = np.shape(template)[0] * np.shape(template)[1]
        aireMax = aire if aire > aireMax else aireMax
        aireMin = aire if aire < aireMin else aireMin
        nbLigneMax = nbLigne if nbLigne > nbLigneMax else nbLigneMax
        nbLigneMin = nbLigne if nbLigne < nbLigneMin else nbLigneMin
        nbColonneMax = nbColonne if nbColonne > nbColonneMax else nbColonneMax
        nbColonneMin = nbColonne if nbColonne < nbColonneMin else nbColonneMin
    #Boucle permettant de déplacer les CC et les placer dans un dossier de CC valides ou invalides
    for image in dossierCC :
        if "template" in image :
            continue
        fichiersCC = os.listdir(cheminDossierSource + "\\stock\\"+image)
        for element in fichiersCC :
            if "template" in element :
                continue
            cc = mplimg.imread (cheminDossierSource + "\\stock\\"+image+"\\"+element).astype(np.uint8)
            nbLigneElem = np.shape(cc)[0]
            nbColElem = np.shape(cc)[1]
            aireCC = np.shape(cc)[0] * np.shape(cc)[1]

           
            if ( nbLigneElem < nbLigneMax and nbLigneElem > nbLigneMin ) or ( nbColElem < nbColonneMax and nbColElem > nbColonneMin ) or (aireCC < aireMax and aireCC > aireMin) :
                shutil.move(cheminDossierSource + "\\stock\\"+image+"\\"+element , cheminDossierSource+"\\CCs\\valide\\" +image)
            else :
                shutil.move(cheminDossierSource + "\\stock\\"+image+"\\"+element , cheminDossierSource+"\\CCs\\invalide\\" +image)
            
