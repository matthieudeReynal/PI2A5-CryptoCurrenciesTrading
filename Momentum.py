import numpy as np
from numpy.core.overrides import verify_matching_signatures
taille_roll_win=2
pairs = ['LEND/USDT', 'LRC/USDT', 'SNX/USDT', 'KNC/USDT', 'BNT/USDT', 'REN/USDT', 'ENJ/USDT', 'ETH/USDT']
Nb_pair=len(pairs)

def moment(data,taille_rolling_window):
    mom_roll_wind=[[]]
    j=0
    for monnaie,L_price in data.items():
        for i in range(len(L_price)-taille_rolling_window):
            mom_roll_wind[i][j]=L_price[i+taille_rolling_window]/L_price[i])-1
        j+=1
    return(mom_roll_wind)

def rendement(data):
    rendement=[[]]
    j=0
    for monnaie,L_price in data.items():
        for i in range(len(L_price)):
            rendement[i][j]=(L_price[i+1]/L_price[i])-1
        j+=1
    return(rendement)

def contribution_matrice(mom_data,rendement_data,prct_top,prct_flop,int_rw):
    mom_top=0
    mom_flop=0
    test_poids=0
    var_mom_temp=[]
    Contr_mat=list(mom_data)
    for i in range(len(Contr_mat)):
        test_poids=0
        var_mom_temp=list(Contr_mat[i])
    
        mom_top=np.percentile(var_mom_temp,1-prct_top)
        mom_flop=np.percentile(var_mom_temp,prct_flop)

        for k in range(len(Contr_mat[0])):
            if(var_mom_temp(k)<mom_top and var_mom_temp[k]>mom_flop):
                var_mom_temp[k]=0
            
            elif(var_mom_temp[k]>=mom_top):
                var_mom_temp[k]=1/(round(prct_top*len(Contr_mat[0]))*rendement_data[i+int_rw-1][k])
                #test_poids=test_poids+1/(round(prct_top*len(Contr_mat[0])))
            elif(var_mom_temp[k]<=mom_flop):
                var_mom_temp[k]=-1/(round(prct_flop*len(Contr_mat[0]))*rendement_data[i+int_rw-1][k])
                #test_poids=test_poids-1/(round(prct_flop*len(Contr_mat[0])))
        Contr_mat[i]=list(var_mom_temp)
    return(Contr_mat)

def Rmom(contr_mat):
    Somme=0
    V_Rmom=[]
    for i in range(len(contr_mat)):
        Somme=0
        for j in range(contr_mat[0]):
            Somme=Somme+contr_mat[i][j]
        V_Rmom.append(Somme)
    return(V_Rmom)