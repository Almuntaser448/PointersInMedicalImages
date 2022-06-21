import subprocess
import os
import shutil
import lib.filtration 
import lib.GFDtools
import lib.comparaison
import lib.reconstitution
import pickle

if __name__ == '__main__' :

    choix=0

    while choix not in (1,2):
        choix=int(input("Approche avec ou sans réseau de neurone? (1: avec / 2: sans): "))

    path = os.getcwd()+"\\"
    
    
    try:
        os.makedirs('ImagesReconstituees')
    except:
        shutil.rmtree('ImagesReconstituees')
        os.makedirs('ImagesReconstituees')

    try:
        os.makedirs('CCs')
        print("cc recréé")
        
    except:
        print("cc supprimé")
        shutil.rmtree('CCs')
        os.makedirs('CCs')
    
    os.makedirs('CCs\\valide' )
    os.makedirs('CCs\\invalide')
    
    try:
        os.makedirs('stock')
    except:
        shutil.rmtree('stock')
        os.makedirs('stock')

    p = subprocess.Popen(["java","-Djava.library.path="+path,"-jar",path+"\\BoiteNoir.jar"], stdin=subprocess.PIPE) #cree un processus enfant grace a la comande de la CMD qui lance le programme java de Boite noir dans la format JAR en donnanet le chemain de la DLL de OpenCv et le chemain de JAR
                                                                                                                  
    p.wait()

    images= os.listdir(path+'\\src\\ref')
    source= path+"\\stock\\"
    dossier1=os.listdir(source)
 
    for image in dossier1 :
        dossier2 = os.listdir(source+""+image)
        for element in dossier2 :
            if "infos" in element :
                os.remove(source+image+"\\"+element)

    for element in dossier1 :
        if 'template' in element :
            continue
        os.makedirs(path + '\\CCs\\valide\\' + element)
        os.makedirs(path + '\\CCs\\invalide\\' + element)

    clf=None
    if choix==1:
        clf = pickle.load(open(path+"lib\MODEL.MOD", 'rb')) 

    GFDs = lib.reconstitution.listeGFD(path+'\\src\\ref')
    lib.filtration.filtration(path)
    lib.reconstitution.classification(path, GFDs,clf)
    lib.reconstitution.reconstitutionClasse(path, 2)