import discord
from discord.ext import tasks, commands
import aiohttp
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CANAL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    enviar_precio_token.start()

@tasks.loop(hours=1)
async def enviar_precio_token():
    canal = bot.get_channel(CANAL_ID)
    if not canal:
        print("❌ Canal no encontrado.")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get('https://wowtoken.info/data.json') as resp:
            if resp.status == 200:
                data = await resp.json()
                eu_data = data['eu']
                precio = eu_data['buy']
                timestamp = eu_data['updated']
                mensaje = f"💰 **Token WoW (EU)**: {precio:,}g\n🕒 Actualizado: <t:{int(timestamp)}:R>"
                await canal.send(mensaje)
            else:
                await canal.send("❌ Error al obtener el precio del token.")

bot.run(TOKEN)
