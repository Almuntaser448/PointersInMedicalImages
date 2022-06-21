def indiceJaccard(vect1,vect2): # renvoie l'indice de Jaccard de deux listes de flottants. 
    inter,union=0,0
    
    for i in range(len(vect1)):
        inter+=min(vect1[i],vect2[i])
        union+=max(vect1[i],vect2[i])
    return inter/union
