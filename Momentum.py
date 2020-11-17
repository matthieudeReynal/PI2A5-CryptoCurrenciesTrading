import numpy as np
from numpy.core.overrides import verify_matching_signatures
taille_roll_win=2
pairs = ['LEND/USDT', 'LRC/USDT', 'SNX/USDT', 'KNC/USDT', 'BNT/USDT', 'REN/USDT', 'ENJ/USDT', 'ETH/USDT']
Nb_pair=len(pairs)


#La fonction recup_moment permet de retourner le tableau des moments avec chacune des valeurs calculées en fonction de
#la rolling window calculée préalablement.
def moment(data,taille_rolling_window): #les données de moments sont sous forme de liste de liste pour une question de simplicité lors de leur utilisation ulterieur
    mom_roll_wind=[[]]
    j=0
    for monnaie,L_price in data.items():
        for i in range(len(L_price)-taille_rolling_window):
            mom_roll_wind[i][j]=L_price[i+taille_rolling_window]/L_price[i]-1
        j+=1
    return(mom_roll_wind)

#La fonction recup_rendement fonctionne sur le même principe que la fonction recup_moment, à la seule différence qu'il
#n'y a pas de rolling windows à prendre en compte.
def rendement(data):#les donnée de rendement sont sous forme de liste de liste pour une question de simplicité lors de leur utilisation ulterieur
    rendement=[[]]
    j=0
    for monnaie,L_price in data.items():
        for i in range(len(L_price)):
            rendement[i][j]=(L_price[i+1]/L_price[i])-1
        j+=1
    return(rendement)

#La fonction contribution_matrix permet de retourner toute la matrice de contribution. Les calculs des poids et des
#condtributions se font donc directement à l'intérieur de cette fonction. Elle prends plusieurs arguments en compte
#dont: db_mom_array, la matrice des moments sur laquelle vont se faire l'ensemble des calculs. C'est donc celle-ci
#qui sera retournée en fin de fonction, mais elle correspondra à ce moment à la matrice de contribution.
def contribution_matrice(mom_data,rendement_data,prct_top,prct_flop,int_rw):
    mom_top=0
    mom_flop=0
    test_poids=0
    var_mom_temp=[]
    Contr_mat=list(mom_data)
    for i in range(len(Contr_mat)):
        test_poids=0
        var_mom_temp=list(Contr_mat[i])
    
        #Dans les lignes qui suivent: db_mom_top correspond à la valeur au dessus de laquelle les moments sont dans le top,
        #et db_mom_flop correspond à la valeur en dessous de laquelle les moments sont considérés dans le flop.
        #REMARQUE pour db_mom_top: on oublie pas d'utiliser 1-prct_top, puisque, on parle de percentile, la personne va de-
        #-mander les 40% meilleurs, ce qui correspond à 60% en percentile en partant du début.
        mom_top=np.percentile(var_mom_temp,1-prct_top)
        mom_flop=np.percentile(var_mom_temp,prct_flop)

        for k in range(len(Contr_mat[0])):
            if(var_mom_temp(k)<mom_top and var_mom_temp[k]>mom_flop):#Cas où notre valeur doit etre à 0
                var_mom_temp[k]=0
            
            elif(var_mom_temp[k]>=mom_top):#Cas où on est dans les tops
                var_mom_temp[k]=1/(round(prct_top*len(Contr_mat[0]))*rendement_data[i+int_rw-1][k])
                #test_poids=test_poids+1/(round(prct_top*len(Contr_mat[0])))
            elif(var_mom_temp[k]<=mom_flop):#Cas où on est dans les flops
                var_mom_temp[k]=-1/(round(prct_flop*len(Contr_mat[0]))*rendement_data[i+int_rw-1][k])
                #test_poids=test_poids-1/(round(prct_flop*len(Contr_mat[0])))
        Contr_mat[i]=list(var_mom_temp)
    return(Contr_mat)

#La fonction vecteur_Rmom permet de retourner de manière simple le vecteur des Rmom en faisant la somme sur chaque ligne
#de la matrice de contribution.
def Rmom(contr_mat):
    Somme=0
    V_Rmom=[]
    for i in range(len(contr_mat)):
        Somme=0
        for j in range(contr_mat[0]):
            Somme=Somme+contr_mat[i][j]
        V_Rmom.append(Somme)
    return(V_Rmom)

#On cherche maintanant a calculer les betas

#beta_computing_function prends en paramètre les tableaux de rendements des conversion ainsi que celui des indice(a voir)
#, et retourne un vecteur comportant tous les betas.

def beta_computing_function(rendement_data , index_data):
    rendement_temp=[]
    beta_data=[]
    a=0
    x=np.array([])
    y=np.array([])
    for j in range(len(rendement_data[0])):
        for i in range(len(rendement_data)):
            rendement_temp[i]=rendement_data[i][j]
        y=np.array(rendement_temp)
        x=np.array(index_data)
        x = x[:,np.newaxis]
        a, _, _, _ = np.linalg.lstsq(x, y)
        beta_data[j]=a
    return(beta_data)


#La fonction beta_computing_function_bis reprends le même principe que la fonction beta_computing_function de la question 2 à
#la différence qu'ici nous avons 2 betas à calculer.
#Remarque Importante:
    #La première valeur du vecteur V_Rmom correspond à la "rw"ème journée (ex: rw = 252), hors, les premières valeurs de rendements que nous avons
    #correspondent à la 2ème journée. Il est donc important de penser à déplacer notre fenêtre de travail de "rw - 1" valeurs (ex: 251), lorsque nous
    #utiliserons tableaux de rendements: rendement_firms, et rendement_index
def beta_computing_function_bis(rendement_data , index_data, V_Rmom,int_rw):
    v_rm_rmom=[]
    beta_data=[[]]
    x=np.array([])
    y=np.array([])
    rendement_temp=[]
    for j in range(len(rendement_data[0])):
        for i in range(len(rendement_data)):    
            rendement_temp[i]=rendement_data[i + int_rw - 1][j]
        y=np.array(rendement_temp)
        x=np.array(index_data,V_Rmom)
        X = X.T  # transpose so input vectors are along the rows
        X = np.c_[X, np.ones(X.shape[0])]  # add bias term
        beta_hat = np.linalg.lstsq(X, y, rcond=None)[0]
        beta_data[j][0]=beta_hat[0]
        beta_data[j][1]=beta_hat[1]
    return(beta_data)