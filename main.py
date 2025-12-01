import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import atexit

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def peek(self):
        return self.top.data if self.top else None

    def is_empty(self):
        return self.top is None

    def to_list(self):
        elements = []
        current = self.top
        while current:
            elements.append(current.data)
            current = current.next
        return elements[::-1]

class ArbreNode:
    def __init__(self, question, conclusion=None):
        self.question = question
        self.conclusion = conclusion
        self.yes = None
        self.no = None

C_QUEUE = ArbreNode("Fin : Utilisez une **FILE (Queue)**.", conclusion="FILE (Queue)")
C_STACK = ArbreNode("Fin : Utilisez une **PILE (Stack)**.", conclusion="PILE (Stack)")
C_BST = ArbreNode("Fin : Envisagez un **ARBRE BINAIRE DE RECHERCHE (BST)**.", conclusion="ARBRE BINAIRE DE RECHERCHE (BST)")
C_LIST = ArbreNode("Fin : Une simple **LISTE CHAÎNÉE** pourrait suffire.", conclusion="LISTE CHAÎNÉE")

Q_QUEUE = ArbreNode("Les données doivent-elles être traitées une seule fois dans cet ordre exact (ex: attente) ?")
Q_QUEUE.yes = C_QUEUE; Q_QUEUE.no = C_LIST

Q_STACK = ArbreNode("Avez-vous besoin de n'interagir qu'avec le dernier élément ajouté (LIFO) ?")
Q_STACK.yes = C_STACK; Q_STACK.no = C_BST

Q_ROOT = ArbreNode("Avez-vous besoin d'accéder aux données dans l'ordre où elles sont arrivées (FIFO) ?")
Q_ROOT.yes = Q_QUEUE; Q_ROOT.no = Q_STACK

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SAVE_FILE = os.getenv("SAVE_FILE")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

user_history = {}
user_discussion_state = {}

def load_data():
    global user_history
    try:
        if not os.path.exists(SAVE_FILE): return
        with open(SAVE_FILE, 'r') as f: data = json.load(f)

        for user_id_str, command_list in data.get('history', {}).items():
            stack = Stack()
            for command in command_list:
                stack.push(command)
            user_history[int(user_id_str)] = stack
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        user_history = {}

def save_data():
    data_to_save = {}
    history_data = {
        str(user_id): stack.to_list()
        for user_id, stack in user_history.items()
    }
    data_to_save['history'] = history_data
    
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")

atexit.register(save_data)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    load_data()
    try:
        synced = await bot.tree.sync()
        print(f"Synchronisé {len(synced)} commandes slash.")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes slash : {e}")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    """
    Intercepte toutes les interactions (y compris les commandes slash)
    pour enregistrer l'historique.
    """
    if interaction.type == discord.InteractionType.application_command:
        command_name = interaction.command_name if interaction.command_name else "unknown_command"
        user_id = interaction.user.id
        full_command = f"/{command_name}"
        
        if user_id not in user_history:
            user_history[user_id] = Stack()
            
        user_history[user_id].push(full_command)

        await bot.process_application_commands(interaction)
        return

    await bot.process_application_commands(interaction)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    user_id = message.author.id

    if user_id in user_discussion_state:
        current_node = user_discussion_state[user_id]
        user_response = message.content.lower().strip()
        next_node = None
        
        if user_response in ('oui', 'o', 'yes', 'y'):
            next_node = current_node.yes
            response_text = f"Entendu, **OUI**. "
        elif user_response in ('non', 'n', 'no'):
            next_node = current_node.no
            response_text = f"Entendu, **NON**. "
        else:
            await message.channel.send(f"Veuillez répondre par **Oui** ou **Non**.")
            return

        if next_node:
            user_discussion_state[user_id] = next_node
            
            if next_node.conclusion:
                response_text += next_node.question
                del user_discussion_state[user_id]
            else:
                response_text += "Question suivante : " + next_node.question
                
            await message.channel.send(response_text)
            
        return

    await bot.process_commands(message) 

@bot.tree.command(name="last_command", description="Affiche la dernière commande que vous avez exécutée.")
async def last_command(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in user_history and not user_history[user_id].is_empty():
        last = user_history[user_id].peek()
        await interaction.response.send_message(f"Votre **dernière commande** exécutée est : `{last}`")
    else:
        await interaction.response.send_message("Vous n'avez pas encore exécuté de commande que je puisse suivre.")

@bot.tree.command(name="all_commands", description="Affiche toutes les commandes que vous avez exécutées.")
async def all_commands(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in user_history and not user_history[user_id].is_empty():
        commands_list = user_history[user_id].to_list()
        history_str = "\n".join([f"{i+1}. `{cmd}`" for i, cmd in enumerate(commands_list)])
        await interaction.response.send_message(
            f"**📜 Historique des {len(commands_list)} commandes** :\n{history_str}",
            ephemeral=True
        )
    else:
        await interaction.response.send_message("Votre historique de commandes est vide.", ephemeral=True)

@bot.tree.command(name="clear_history", description="Vide votre historique de commandes.")
async def clear_history(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in user_history:
        del user_history[user_id]
        await interaction.response.send_message("✅ Votre historique de commandes a été vidé.", ephemeral=True)
    else:
        await interaction.response.send_message("Votre historique est déjà vide.", ephemeral=True)

@bot.tree.command(name="help_me_choose", description="Lance un questionnaire pour vous aider à choisir une structure de données.")
async def start_discussion(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_discussion_state[user_id] = Q_ROOT
    await interaction.response.send_message(
        "👋 **Bienvenue dans le guide de sélection !**\n"
        "Veuillez répondre par **Oui** ou **Non**.\n\n"
        f"**Question 1 :** {Q_ROOT.question}"
    )

@bot.tree.command(name="reset_discussion", description="Recommence le questionnaire depuis le début.")
async def reset_discussion(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in user_discussion_state:
        del user_discussion_state[user_id]
        await interaction.response.send_message("✅ Discussion réinitialisée. Utilisez `/help_me_choose` pour recommencer.", ephemeral=True)
    else:
        await interaction.response.send_message("Vous n'êtes pas en cours de discussion.", ephemeral=True)

def traverse_tree(node, target_subject):
    if node is None:
        return False
    if node.conclusion and target_subject.lower() in node.conclusion.lower():
        return True
    return traverse_tree(node.yes, target_subject) or traverse_tree(node.no, target_subject)

@bot.tree.command(name="speak_about", description="Vérifie si le bot peut parler d'une structure de données (ex: Pile).")
@discord.app_commands.describe(sujet="Le sujet (ex: File, Pile, Arbre) à vérifier.")
async def speak_about(interaction: discord.Interaction, sujet: str):
    found = traverse_tree(Q_ROOT, sujet)
    if found:
        await interaction.response.send_message(f"✅ **OUI**, le sujet « **{sujet}** » est une conclusion possible dans mon arbre de décision !")
    else:
        await interaction.response.send_message(f"❌ **NON**, le sujet « **{sujet}** » n'est pas une conclusion directe dans mon arbre actuel.")

@bot.tree.command(name="define", description="Obtenez une définition rapide d'une structure de données.")
@discord.app_commands.describe(terme="La structure à définir (ex: Pile, File, Arbre Binaire).")
async def define_structure(interaction: discord.Interaction, terme: str):
    definitions = {
        "pile": "Une **Pile (Stack)** est LIFO.",
        "file": "Une **File (Queue)** est FIFO.",
        "liste chaînée": "Une **Liste Chaînée** est flexible pour les insertions/suppressions.",
        "arbre binaire": "Un **Arbre Binaire** est une structure hiérarchique."
    }
    terme_lower = terme.lower()
    if terme_lower in definitions:
        await interaction.response.send_message(f"📚 **Définition de {terme.upper()}** :\n{definitions[terme_lower]}")
    else:
        await interaction.response.send_message(f"Je ne connais pas de définition pour le terme : **{terme}**.", ephemeral=True)

class QuizView(discord.ui.View):
    def __init__(self, quiz_data):
        super().__init__(timeout=30)
        self.quiz_data = quiz_data
        self.correct_answer_index = quiz_data['answer_index']
        self.answered_users = set()

        for i, option in enumerate(quiz_data['options']):
            button = discord.ui.Button(label=option, style=discord.ButtonStyle.secondary, custom_id=f"quiz_{i}")
            
            async def callback(interaction):
                 if interaction.user.id in self.answered_users:
                     await interaction.response.send_message("Déjà répondu.", ephemeral=True); return
                 self.answered_users.add(interaction.user.id)
                 is_correct = int(interaction.custom_id.split('_')[1]) == self.correct_answer_index
                 if is_correct: await interaction.response.send_message(f"🎉 **Correct !**", ephemeral=True)
                 else: await interaction.response.send_message(f"❌ **Faux.** La bonne réponse est `{self.quiz_data['options'][self.correct_answer_index]}`.", ephemeral=True)
                 
            button.callback = callback
            self.add_item(button)

@bot.tree.command(name="quiz", description="Lance un mini-quiz sur les structures de données.")
async def start_quiz(interaction: discord.Interaction):
    quiz_data = {
        "question": "Quelle structure de données est utilisée pour implémenter un mécanisme d'annulation ('Undo') ?",
        "options": ["Pile (Stack)", "File (Queue)", "Liste Chaînée", "Arbre Binaire"],
        "answer_index": 0 
    }
    view = QuizView(quiz_data)
    await interaction.response.send_message(
        f"🧠 **Mini-Quiz :**\n{quiz_data['question']}", view=view, ephemeral=False
    )

@bot.tree.command(name="bot_stats", description="Affiche les statistiques sur l'utilisation du bot.")
async def bot_stats(interaction: discord.Interaction):
    total_users_logged = len(user_history)
    total_commands = sum(stack._size for stack in user_history.values())
    await interaction.response.send_message(
        f"📊 **Statistiques du DataStructBot**\n"
        f"--- \n"
        f"👤 Utilisateurs avec historique : **{total_users_logged}**\n"
        f"📜 Commandes totales enregistrées : **{total_commands}**\n"
        f"💾 Les données sont sauvegardées à l'arrêt du bot."
    )


if __name__ == '__main__':
    bot.run(TOKEN)
