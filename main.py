import os
from unittest import result
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
    for service in services_list:
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

@tree.command(name="restart", description="Restart a service on the server")
@app_commands.choices(service=services_choices)
async def restart(interaction: discord.Interaction, service: app_commands.Choice[str]):
    await interaction.response.send_message(f"Restarting {service.value}...")
    subprocess.run(["systemctl", "restart", service.value])
    await interaction.followup.send("Service restarted successfully.")

@tree.command(name="start", description="Start any service running on the server")
@app_commands.choices(service=services_choices)
async def start(interaction: discord.Interaction, service: app_commands.Choice[str]):
    await interaction.response.send_message(f"Starting {service.value}...")
    subprocess.run(["systemctl", "start", service.value])
    await interaction.followup.send("Service started successfully.")

@tree.command(name="stop", description="Stop a service running on the server")
@app_commands.choices(service=services_choices)
async def stop(interaction: discord.Interaction, service: app_commands.Choice[str]):
    await interaction.response.send_message(f"Stopping {service.value}...")
    subprocess.run(["systemctl", "stop", service.value])
    await interaction.followup.send("Service stopped successfully.")

@tree.command(name="status", description="See status of any service running on the server")
@app_commands.choices(service=services_choices)
async def status(interaction: discord.Interaction, service: app_commands.Choice[str]):
    await interaction.response.send_message(f"Checking status of {service.value}...")
    result = subprocess.run(["systemctl", "status", service.value], capture_output=True, text=True)
    output = result.stdout.strip()
    if result.stderr.strip():
        output += f"\n{result.stderr.strip()}"
    await interaction.followup.send(f"```text\n{output}\n```")

@tree.command(name="logs", description="Get logs of any service running on the server")
@app_commands.choices(service=services_choices)
async def logs(interaction: discord.Interaction, service: app_commands.Choice[str]):
    await interaction.response.send_message(f"Getting live logs for {service.value}...")
    result = subprocess.run(["journalctl", "-u", service.value, "--no-pager", "-n", "50"], capture_output=True, text=True)
    output = result.stdout.strip()
    if result.stderr.strip():
        output += f"\n{result.stderr.strip()}"
    await interaction.followup.send(f"```text\n{output}\n```")

@tree.command(name="about", description="Get information about this bot")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message("This is a discord systemd manager, built for managing systemd services on a server directly from discord chats."
    "\n\n_Built by hackerskills_")

client.run(token)
