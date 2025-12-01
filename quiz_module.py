import discord
from discord import app_commands

class QuizView(discord.ui.View):
    def __init__(self, quiz_data):
        super().__init__(timeout=30)
        self.quiz_data = quiz_data
        self.correct_answer_index = quiz_data['answer_index']
        self.answered_users = set()

        for i, option in enumerate(quiz_data['options']):
            button = discord.ui.Button(label=option, style=discord.ButtonStyle.secondary, custom_id=f"quiz_{i}")
            
            async def callback(interaction):
                user_id = interaction.user.id
                if user_id in self.answered_users:
                    await interaction.response.send_message("Vous avez déjà répondu.", ephemeral=True); return
                
                self.answered_users.add(user_id)
                clicked_index = int(interaction.custom_id.split('_')[1])
                is_correct = clicked_index == self.correct_answer_index
                
                if is_correct: 
                    await interaction.response.send_message(f"🎉 **Correct !**", ephemeral=True)
                else: 
                    correct_label = self.quiz_data['options'][self.correct_answer_index]
                    await interaction.response.send_message(f"❌ **Faux.** La bonne réponse était `{correct_label}`.", ephemeral=True)
            
            button.callback = callback
            self.add_item(button)

@app_commands.command(name="quiz", description="Lance un mini-quiz sur l'histoire de l'informatique.")
async def start_quiz(interaction: discord.Interaction):
    """Commande pour lancer le quiz."""
    quiz_data = {
        "question": "Quel inventeur est associé à la 'Machine Analytique' au 19ème siècle ?",
        "options": ["Alan Turing", "Charles Babbage", "Ada Lovelace", "John von Neumann"],
        "answer_index": 1 # Charles Babbage
    }
    view = QuizView(quiz_data)
    await interaction.response.send_message(
        f"🧠 **Mini-Quiz :**\n{quiz_data['question']}", view=view, ephemeral=False
    )
