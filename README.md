🤖 Projet-Bot-Discord: 
Assistant d'Apprentissage (Projet B2)
🌟 PrésentationDataStructBot est un bot Discord conçu pour le projet B2, démontrant la maîtrise des structures de données et de la persistance.ExigenceStructure / Fonctionnalité Démontrée1. Historique des commandesPile (Stack) implémentée avec Liste Chaînée (LIFO).
2. Système de discussionArbre Binaire pour le questionnaire de décision.
3. Sauvegarde persistanteFichier JSON (history_bot_data.json) lors de l'arrêt du bot.4. Fonctionnalités additionnellesQuiz, Définition rapide, Statistiques.
🚀 Démarrage RapidePrérequis : Python 3.8+, discord.py, python-dotenv.Configuration : 
Créez un fichier .env à la racine avec votre jeton :Extrait de code DISCORD_TOKEN="VOTRE_TOKEN_SECRET_ICI"
SAVE_FILE="history_bot_data.json"
Lancement : Bash python3 main.py
📜 Commandes du Bot (/)I. Historique (Pile)CommandeRôle/last_commandAffiche la dernière commande utilisée./all_commandsAffiche l'historique complet des commandes./clear_historyVide l'historique personnel.II. Discussion (Arbre Binaire)CommandeRôle/help_me_chooseLance le questionnaire de décision (réponses par Oui/Non dans le chat)./reset_discussionRéinitialise la discussion en cours./speak_about [sujet]Vérifie si le sujet (conclusion) existe dans l'Arbre.III. UtilitairesCommandeRôle/define [terme]Fournit une définition rapide./quizDémarre un mini-quiz interactif./bot_statsAffiche les statistiques (preuve de persistance).
