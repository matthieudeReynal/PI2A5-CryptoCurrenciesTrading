# PI2A5
Pour installer les dépendances:
python -m pip install -r requirements.txt

Pour créer le container docker et le lancer:
* ./postgres-docker/createContainer.sh
* ./postgres-docker/launchContainer.sh

Il faut aussi cloner le repo contenant des commandes de l'API de Binance sous la forme de fonctions Python : $git clone https://github.com/Binance-docs/Binance_Futures_python

Notre stratégie la plus avancée à cette heure est le Mean Reversion on pairs, implémentée dans le notebook MRPair. Pour la lancer sur le live il suffit de lancer les dernières cellules du notebook, celles-ci sont indiquées dans le notebook. 
Il nous reste encore quelques problèmes d'implémentation à gérer, par exemple au niveau des appels de marge.
