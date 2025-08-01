import discord
from discord.ext import tasks, commands
import aiohttp
import os
from datetime import datetime

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
    await enviar_precio_y_mensaje(canal)

async def enviar_precio_y_mensaje(canal):
    url = 'https://data.wowtoken.app/v2/current/retail.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                eu_data = data.get('eu')
                if eu_data and len(eu_data) == 2:
                    timestamp_str, precio = eu_data
                    # Convertir ISO8601 a timestamp UNIX
                    dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    timestamp_unix = int(dt.timestamp())
                    mensaje = f"💰 **Token WoW (EU)**: {precio:,}g\n🕒 Actualizado: <t:{timestamp_unix}:R>"
                    await canal.send(mensaje)
                else:
                    await canal.send("❌ No se encontró información válida para EU.")
            else:
                await canal.send("❌ Error al obtener el precio del token.")

@bot.command(name="precio")
async def precio(ctx):
    await enviar_precio_y_mensaje(ctx.channel)

bot.run(TOKEN)
