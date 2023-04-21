# importing the libraries
import discord
from discord import app_commands
from utils import (
    getResponse,
    initializeConversation,
)  # importing the functions from util.py / by Soham
import functools
import typing
import asyncio

# Setting up the global variables
GUILD_ID=1098489281380614226
MY_GUILD = discord.Object(id=GUILD_ID)  # replace with your guild id
AI_LOADED = False
BOT_TOKEN="MTA5ODQ5MDM3MDcxNjg2ODYzOA.GAd92j.q3fTQNtaf__KBj4ZbQzKp2zrG-CmeEtnbVS6F8"/prom


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

# We need to use asyncio.to_thread to run the functions in a separate thread
def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper

# Get response from the AI
@to_thread
def get_ai(promt):
    resp = getResponse(promt)
    return resp

# Initialize/Reload the conversation
@to_thread
def start_ai():
    global AI_LOADED
    initializeConversation()
    AI_LOADED = True
    return



@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")



# admin only
# reloads the AI
@client.tree.command()
@app_commands.default_permissions()
@app_commands.guild_only()
async def start(interaction: discord.Interaction):
    """Reloads/Starts the AI"""
    await interaction.response.defer()
    await start_ai()
    embed = discord.Embed(color=discord.colour.Color.yellow(), title="AI Reloaded")
    embed.description = "To use the AI, use the `/prompt` command"
    return await interaction.followup.send(embed=embed)




# Used to send a prompt to the AI
@client.tree.command()
@app_commands.guild_only()
@app_commands.describe(prompt="The prompt you want to send to the AI")
async def prompt(interaction: discord.Interaction, prompt: str):
    """Sends a prompt to the AI."""
    await interaction.response.defer()
    if not AI_LOADED:
        embed = discord.Embed(
            color=discord.colour.Color.dark_orange(), title="AI Not Loaded"
        )
        embed.description = "Ask the bot owner to reload the AI"
        return await interaction.followup.send(embed=embed)

    resp = await get_ai(prompt)
    # if len(resp) > 1024:
    embed = discord.Embed(color=discord.colour.Color.teal(), title=prompt)

    embed.description = resp
    embed.set_author(
        name=interaction.user.display_name,
        icon_url=interaction.user.display_avatar.url,
    )
    embed.timestamp = interaction.created_at

    return await interaction.followup.send(embed=embed)
