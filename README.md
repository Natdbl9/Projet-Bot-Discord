# 🤖 DataStructBot : Assistant d'Apprentissage et de Révision (Projet B2)

## 🌟 Présentation

**DataStructBot** est un bot Discord conçu pour le projet B2, dont l'objectif principal est de démontrer la maîtrise des structures de données fondamentales en informatique, de la persistance des données et de l'intégration des commandes Slash (`/`).

| Exigence | Structure / Fonctionnalité Démontrée |
| :--- | :--- |
| **1. Historique des commandes** | **Pile (Stack)** implémentée avec Liste Chaînée (LIFO). |
| **2. Système de discussion** | **Arbre Binaire** 

[Image of Binary Tree structure]
 pour le questionnaire de décision. |
| **3. Sauvegarde persistante** | **Fichier JSON** (`history_bot_data.json`) lors de l'arrêt du bot. |
| **4. Fonctionnalités additionnelles** | Quiz, Définition rapide, Statistiques. |

---

## 🚀 Lancement du Projet

1.  **Prérequis :** Python 3.8+, `discord.py`, `python-dotenv`.
2.  **Configuration :** Créez un fichier **`.env`** à la racine avec votre jeton :
    ```env
    DISCORD_TOKEN="VOTRE_TOKEN_SECRET_ICI"
    SAVE_FILE="history_bot_data.json" 
    ```
3.  **Exécution :**
    ```bash
    python3 main.py
    ```

---

## 📜 Commandes du Bot (`/`)

### I. Historique (Pile)

| Commande | Rôle |
| :--- | :--- |
| `/last_command` | Affiche la dernière commande utilisée. |
| `/all_commands` | Affiche l'historique complet des commandes. |
| `/clear_history` | Vide l'historique personnel. |

### II. Discussion (Arbre Binaire)

| Commande | Rôle |
| :--- | :--- |
| `/help_me_choose` | Lance le questionnaire de décision (réponses par `Oui`/`Non` dans le chat). |
| `/reset_discussion` | Réinitialise la discussion en cours. |
| `/speak_about [sujet]` | Vérifie si le sujet existe dans les conclusions de l'Arbre. |

### III. Utilitaires

| Commande | Rôle |
| :--- | :--- |
| `/define [terme]` | Fournit une définition rapide. |
| `/quiz` | Démarre un mini-quiz interactif. |
| `/bot_stats` | Affiche les statistiques (preuve de persistance). |
