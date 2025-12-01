import discord
from discord import app_commands

def setup_history_commands(tree, user_history):
    """Enregistre les commandes d'historique sur la bot.tree."""

    @tree.command(name="last_command", description="Affiche la dernière commande que vous avez exécutée.")
    async def last_command(interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in user_history and not user_history[user_id].is_empty():
            last = user_history[user_id].peek()
            await interaction.response.send_message(f"Votre **dernière commande** est : `{last}`")
        else:
            await interaction.response.send_message("Historique vide.")

    @tree.command(name="all_commands", description="Affiche toutes les commandes que vous avez exécutées.")
    async def all_commands(interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in user_history and not user_history[user_id].is_empty():
            commands_list = user_history[user_id].to_list() 
            history_str = "\n".join([f"{i+1}. `{cmd}`" for i, cmd in enumerate(commands_list)])
            await interaction.response.send_message(
                f"**📜 Historique des commandes** ({len(commands_list)}) :\n{history_str}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("Historique vide.", ephemeral=True)

    @tree.command(name="clear_history", description="Vide votre historique de commandes.")
    async def clear_history(interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in user_history:
            del user_history[user_id] 
            await interaction.response.send_message("✅ Historique vidé.", ephemeral=True)
        else:
            await interaction.response.send_message("Historique déjà vide.", ephemeral=True)
