import discord
from discord import app_commands
from discord.ext import commands
from io import BytesIO
from warps.inventory_view import inventory_view

class pom6(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="my_characters", description="View all the characters you own.")
    async def my_charas(self, interaction: discord.Interaction):
        await interaction.response.defer()
        pompomParentDB = self.client.mongoConnect['PomPomDB']
        pompomCollection = pompomParentDB['characters']

        user_id = interaction.user.id
        filter = {'_id': user_id}

        if await pompomCollection.find_one(filter) == None:
            new_user = {"_id": user_id, "ten_pulls": 0, "characters": {}}
            await pompomCollection.insert_one(new_user)

        user_data = await pompomCollection.find_one(filter)
        selected_user = user_data['characters']

        result = inventory_view(selected_user)

        if not result == None:
            middle_man = BytesIO()
            result.save(middle_man, format="PNG", optimize=True)
            middle_man.seek(0)
            file = discord.File(middle_man, filename="charas.png")

            my_charas_embed = discord.Embed(title=f"{interaction.user.name}'s Characters", color=0xffffff)
            my_charas_embed.set_image(url="attachment://charas.png")

            await interaction.followup.send(file=file, embed=my_charas_embed)
        else:
            my_charas_embed = discord.Embed(title=f"{interaction.user.name}'s Characters", description="You do not have any characters at the moment :( Start collecting by doing `/warp` now!",color=0xffffff)

            await interaction.followup.send(embed=my_charas_embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(pom6(client))
