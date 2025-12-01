import discord
from discord import app_commands
from structures import get_root, traverse_tree

def setup_discussion_commands(tree, user_discussion_state):
    """Enregistre les commandes de discussion sur la bot.tree."""

    @tree.command(name="help_me_choose", description="Lance un questionnaire pour choisir le bon langage de programmation.")
    async def start_discussion(interaction: discord.Interaction):
        root_node = get_root() 
        user_id = interaction.user.id
        user_discussion_state[user_id] = root_node
        await interaction.response.send_message(
            f"👋 **Début du guide !** Répondez dans le chat par **Oui** ou **Non**.\n\n"
            f"**Question 1 :** {root_node.question}"
        )

    @tree.command(name="reset_discussion", description="Recommence le questionnaire depuis le début.")
    async def reset_discussion(interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in user_discussion_state:
            del user_discussion_state[user_id]
            await interaction.response.send_message("✅ Discussion réinitialisée.", ephemeral=True)
        else:
            await interaction.response.send_message("Pas de discussion en cours.", ephemeral=True)

    @tree.command(name="speak_about", description="Vérifie si le sujet (langage) X existe dans les conclusions de l'arbre.")
    @app_commands.describe(sujet="Le sujet (ex: Python, Java) à vérifier.")
    async def speak_about(interaction: discord.Interaction, sujet: str):
        found = traverse_tree(get_root(), sujet) 
        if found:
            await interaction.response.send_message(f"✅ **OUI**, « **{sujet}** » est une conclusion possible.")
        else:
            await interaction.response.send_message(f"❌ **NON**, « **{sujet}** » n'est pas une conclusion directe dans l'arbre.")
