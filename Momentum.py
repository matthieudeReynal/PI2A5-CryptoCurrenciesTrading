taille_roll_win=2
pairs = ['LEND/USDT', 'LRC/USDT', 'SNX/USDT', 'KNC/USDT', 'BNT/USDT', 'REN/USDT', 'ENJ/USDT', 'ETH/USDT']
Nb_pair=len(pairs)

def moment(data,taille_rolling_window):
    mom_roll_wind={}
    for monnaie,L_price in data.items():
        for i in range(len(L_price)-taille_rolling_window):
            mom_roll_wind[monnaie][i]=L_price[i+taille_rolling_window]/L_price[i])-1
    return(mom_roll_wind)

def rendement(data):
    rendement={}
    for monnaie,L_price in data.items():
        for i in range(len(L_price)):
            rendement[monnaie][i]=(L_price[i+1]/L_price[i])-1
    return(rendement)

def contribution_matrice(mom_data,rendement_data,prct_top,prct_flop,prct_rw):
    mom_top=0
    mom_flop=0
    test_poids=0
    var_mom_temp=[]
    for i in range(len(mom_data)):
        test_poids=0
        for j in range(len(mom_data[0])):
            var_mom_temp[j]=mom_data[i][j]
        
