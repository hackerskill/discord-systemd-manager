import os
from dotenv import load_dotenv
import discord
from discord import app_commands
import subprocess

load_dotenv()
 
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree= app_commands.CommandTree(client)

def discover_services():
    services = subprocess.check_output(["systemctl", "list-unit-files", "--type=service", "--no-legend", "--no-pager"]).decode("utf-8").splitlines()
    choices = []
    for service in services:
        service = service.split()[0]
        if service.startswith("user-") and "@" not in service:
            choices.append(service)
    return choices

def servicesChoices():
    choices = []
    for service in services:
        choice = app_commands.Choice(name=service, value=service)
        choices.append(choice)
    return choices

services_list=discover_services()
services_choices=servicesChoices()

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}", flush=True)

@tree.command(name="services", description="Get information about all services running on the server")
async def services(interaction: discord.Interaction):
    await interaction.response.send_message("Getting information about all services...")
    await interaction.followup.send("\n".join(services_list))

@tree.command(name="about", description="Get information about this bot")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message("This is a discord systemd manager, built for managing systemd services on a server directly from discord chats."
    "\n\n_Built by hackerskills_")

client.run(token)
