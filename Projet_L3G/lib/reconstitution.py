import matplotlib.image as mplimg
import numpy as np
import os
import lib.GFDtools
import lib.comparaison
import shutil
import pickle
from sklearn.neural_network import MLPClassifier


# transforme une image en niveau de gris en image couleur

def listeGFD(source) :
    result=[]
    listeTemplate = os.listdir(source)
    for i in listeTemplate :
        if "template" not in i :
            continue
        print("Calcul du GFD du template: " +i+" en cours...")
        v=lib.GFDtools.computeGFD(source+"\\"+i)
        result.append((v,i))
    return result


def indiceJaccardMax(vect, liste): 
    resultat=[0,'']
    for i in range ( len(liste) ):
        val = lib.comparaison.indiceJaccard(vect,liste[i][0])
        if val>resultat[0] :
            resultat[0] , resultat[1] = val , liste[i][1] 
    return resultat


def classification(source, listeGFD,clf) :
    listeDossierCCImage= os.listdir(source+"\\CCs\\valide\\")
    for dossierCcsImg in listeDossierCCImage :
        listeCCImage = os.listdir(source+"\\CCs\\valide\\"+dossierCcsImg)
        print("Traitement des CC de l'image: "+dossierCcsImg)
        for cc in listeCCImage :
            print("Traitement de la CC: "+cc)
            v= lib.GFDtools.computeGFD(source+"\\CCs\\valide\\"+dossierCcsImg+"\\"+cc)
            res = indiceJaccardMax(v, listeGFD)
            
            condition=0

            if clf==None:
                if res[0] >= 0.85 :
                    condition=1
            else:
                if clf.predict([v])==0:
                    condition=1
                
            if condition:

                nomCC = os.path.join (source+"\\CCs\\valide\\"+dossierCcsImg+"\\"+cc)
                nouveauNomCC = os.path.join (source+"\\CCs\\valide\\"+dossierCcsImg+"\\"+cc[:-4]+"_"+res[1])
                os.rename(nomCC, nouveauNomCC)
            else :
                
                shutil.move(source+"\\CCs\\valide\\"+dossierCcsImg+"\\"+cc , source+"\\CCs\\invalide\\"+dossierCcsImg)


def dictionnaire(source):
    dico={}
    listeTemplate= os.listdir(source+"\\src\\ref\\")
    for i in listeTemplate:
        if "template" not in i :
            continue
        dico[i]=( np.random.randint( low=0, high=256 ) , np.random.randint( low=0, high=256 ) , np.random.randint( low=0, high=256 ) )
    return dico


def convertGrayToColor(cheminImage) :
    image = mplimg.imread(cheminImage)
    lignes= np.shape(image)[0]
    colonnes= np.shape(image)[1]
    imageRecon = np.zeros((lignes,colonnes,3), dtype=np.uint8)
    for i in range (lignes) :
        for j in range(colonnes) :
            imageRecon[i][j][0]=image[i][j]
            imageRecon[i][j][1]=image[i][j]
            imageRecon[i][j][2]=image[i][j]
    return (imageRecon)


def reconstitution(cheminDossierRessources,choix) :
    # liste des elements dansle dossier ImagesReconstitutees ( images reconstituées + dossiers des CC )
    dossierImages = os.listdir(cheminDossierRessources+"\\src\\ref\\")
    dossierImageCC= os.listdir(cheminDossierRessources+"\\CCs\\valide\\")
    # Boucle permettant de modifier la couleur des pixels d'une image en fonction des ses CC valides
    for element in dossierImages :
        if 'template' in element : 
            continue
        imageRecon= convertGrayToColor(cheminDossierRessources+"\\src\\ref\\"+element)
        destination = (cheminDossierRessources+"\\ImagesReconstituees\\"+element)[:-3] +"png"
        for dossierCC in dossierImageCC :
            if element[:-4] in dossierCC :
                break 
        CCsImage = os.listdir(cheminDossierRessources+"\\CCs\\valide\\"+dossierCC)
        for cc in CCsImage:
            chaine= ( cc[1:] ).split(']')[0]
            tab= chaine.split(',')
            colonne= int(tab[0])
            ligne = int(tab[1])
            colonneFin=int(tab[0]) + int(tab[2])
            ligneFin= int(tab[1]) + int(tab[3])
            if choix == 1 :
                for i in range(colonne, colonneFin+1 ) :
                    imageRecon[ligne][i][0] , imageRecon[ligneFin][i][0] =255, 255
                    imageRecon[ligne][i][1] , imageRecon[ligne][i][2] , imageRecon[ligneFin][i][1] , imageRecon[ligneFin][i][2] = 0,0,0,0
                for i in range(ligne, ligneFin+1) :
                    imageRecon[i][colonne][0] , imageRecon[i][colonneFin][0] =255, 255
                    imageRecon[i][colonne][1] , imageRecon[i][colonne][2] , imageRecon[i][colonneFin][1] , imageRecon[i][colonneFin][2] = 0,0,0,0
            else :
                image= mplimg.imread(cheminDossierRessources+"\\CCs\\valide\\"+dossierCC+"\\"+cc)
                for i in range(ligneFin-ligne) :
                    for j in range(colonneFin-colonne) :
                        if image[i][j] > 240 :
                            imageRecon[ligne+i][colonne+j][0] = 255
                            imageRecon[ligne+i][colonne+j][1] = 0
                            imageRecon[ligne+i][colonne+j][2] = 0
        mplimg.imsave(destination, imageRecon)


def reconstitutionClasse(cheminDossierRessources,choix) :
    # liste des elements dansle dossier ImagesReconstitutees ( images reconstituées + dossiers des CC )
    dossierImages = os.listdir(cheminDossierRessources+"\\src\\ref\\")
    dossierImageCC= os.listdir(cheminDossierRessources+"\\CCs\\valide\\")
    dico=dictionnaire(cheminDossierRessources)
    # Boucle permettant de modifier la couleur des pixels d'une image en fonction des ses CC valides
    for element in dossierImages :
        if 'template' in element : 
            continue
        imageRecon= convertGrayToColor(cheminDossierRessources+"\\src\\ref\\"+element)
        destination = (cheminDossierRessources+"\\ImagesReconstituees\\"+element)[:-3] +"png"
        for dossierCC in dossierImageCC :
            if element[:-4] in dossierCC :
                break 
        CCsImage = os.listdir(cheminDossierRessources+"\\CCs\\valide\\"+dossierCC)
        for cc in CCsImage:
            chaine= ( cc[1:] ).split(']')[0]
            tab= chaine.split(',')
            colonne= int(tab[0])
            ligne = int(tab[1])
            colonneFin=int(tab[0]) + int(tab[2])
            ligneFin= int(tab[1]) + int(tab[3])
            template= ((cc.split('_'))[1])
            couleur=dico[template]
            if choix == 1 :
                for i in range(colonne, colonneFin+1 ) :
                    imageRecon[ligne][i][0] , imageRecon[ligneFin][i][0] = couleur[0] , couleur[0]
                    imageRecon[ligne][i][1] , imageRecon[ligne][i][2] , imageRecon[ligneFin][i][1] , imageRecon[ligneFin][i][2] = couleur[1],couleur[2],couleur[1],couleur[2]
                for i in range(ligne, ligneFin+1) :
                    imageRecon[i][colonne][0] , imageRecon[i][colonneFin][0] = couleur[0] , couleur[0]
                    imageRecon[i][colonne][1] , imageRecon[i][colonne][2] , imageRecon[i][colonneFin][1] , imageRecon[i][colonneFin][2] = couleur[1],couleur[2],couleur[1],couleur[2]
            else :
                image= mplimg.imread(cheminDossierRessources+"\\CCs\\valide\\"+dossierCC+"\\"+cc)
                for i in range(ligneFin-ligne) :
                    for j in range(colonneFin-colonne) :
                        if image[i][j] > 240 :
                            imageRecon[ligne+i][colonne+j][0] = couleur[0]
                            imageRecon[ligne+i][colonne+j][1] = couleur[1]
                            imageRecon[ligne+i][colonne+j][2] = couleur[2]
        mplimg.imsave(destination, imageRecon)
