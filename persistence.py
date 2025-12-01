import json
import os
import atexit
from structures import Stack

def load_data(save_file, user_history):
    """Charge l'historique de l'utilisateur au démarrage."""
    try:
        if not os.path.exists(save_file): return
        with open(save_file, 'r') as f: data = json.load(f)

        for user_id_str, command_list in data.get('history', {}).items():
            stack = Stack()
            for command in command_list:
                stack.push(command) 
            user_history[int(user_id_str)] = stack
        print("Persistence : Historique chargé.")
    except Exception as e:
        print(f"Erreur de chargement des données : {e}")

def save_data(save_file, user_history):
    """Sauvegarde l'historique des commandes à l'arrêt du bot."""
    data_to_save = {'history': {
        str(user_id): stack.to_list() 
        for user_id, stack in user_history.items()
    }}
    try:
        with open(save_file, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print("Persistence : Données sauvegardées.")
    except Exception as e:
        print(f"Erreur de sauvegarde des données : {e}")
