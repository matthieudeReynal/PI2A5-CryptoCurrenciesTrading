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
    for i in range(len(mom_data)):
        test_poids=0
        var_mom_temp=list(mom_data[i])
    
        mom_top=np.percentile(var_mom_temp,1-prct_top)
        mom_flop=np.percentile(var_mom_temp,prct_flop)

        for k in range(len(mom_data[0])):
            if(var_mom_temp(k)<mom_top and var_mom_temp[k]>mom_flop):
                var_mom_temp[k]=0
            
            elif(var_mom_temp[k]>=mom_top):
                var_mom_temp[k]=1/(round(prct_top*len(mom_data[0]))*rendement_data[i+int_rw-1][k])
                #test_poids=test_poids+1/(round(prct_top*len(mom_data[0])))
            elif(var_mom_temp[k]<=mom_flop):
                var_mom_temp[k]=-1/(round(prct_flop*len(mom_data[0]))*rendement_data[i+int_rw-1][k])
                #test_poids=test_poids-1/(round(prct_flop*len(mom_data[0])))
        mom_data[i]=list(var_mom_temp)
    return(mom_data)