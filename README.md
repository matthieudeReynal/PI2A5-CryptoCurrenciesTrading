# PI2A5
Pour installer les dépendances:
python -m pip install -r requirements.txt

Pour créer le container docker et le lancer:
* ./postgres-docker/createContainer.sh
* ./postgres-docker/launchContainer.sh

Pour rafraichir les données:
* python3 02-refreshDataCandles-fast.py
* python3 02-refreshDataCandles.py

Choisissez les paires qui vous intéressent dans ces deux fichiers.

