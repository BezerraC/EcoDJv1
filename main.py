import os
import discord
import wavelink
from discord.ext import commands
from discord import Intents
from essentials.player import WebPlayer
from dotenv import load_dotenv

load_dotenv(".env")

os.environ["JISHAKU_NO_DM_TRACEBACK"] = "true"

class MusicBot(commands.AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

        self.can_function = False
        self.error_message = (
            "Eco DJ não está pronto para ouvir seus comandos. Por favor, tente depois de alguns momentos."
        )

        if not hasattr(self, "wavelink"):
            self.wavelink = wavelink.Client(bot=self)

        self.loop.create_task(self.start_nodes())

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Bem vindo {member.mention} ao {guild.name} e eu sou seu bot de música! 🥳'
        await guild.system_channel.send(to_send)

    async def on_ready(self):
        print(f"{self.user} pronto, vamo com TUDO!!!")
        await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = "!help"))

    async def start_nodes(self):
        await self.wait_until_ready()

        await self.wavelink.initiate_node(
            host="bot-ecodj.herokuapp.com",
            port=80,
            rest_uri="http://bot-ecodj.herokuapp.com:80",
            password="youshallnotpass",
            identifier="MAIN",
            region="singapore",
        )

        for guild in self.guilds:
            if guild.me.voice:
                player: WebPlayer = self.wavelink.get_player(guild.id, cls=WebPlayer)
                try:
                    await player.connect(guild.me.voice.channel.id)
                    print(f"Conectado ao canal voz -> {guild.me.voice.channel.id}")
                except Exception as e:
                    print(e)

        self.can_function = True

intents = Intents.default()
intents.members = True

PREFIX = os.getenv("PREFIX")
bot = MusicBot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('🤔 Comando inválido. use `!help` para ver a lista de comandos')

@bot.event
async def on_guild_join(guild):
    await guild.text_channels[0].send("Opa eae, sou seu novo bot de música\npara começar digite !help")


bot.load_extension("cogs.music")
bot.load_extension("cogs.meme")
bot.load_extension("cogs.events")
bot.load_extension("cogs.help")
bot.load_extension("cogs.error_handler")

bot.load_extension("jishaku") # uncomment this if you want to debug
bot.load_extension("cog_reloader") # Uncomment this if you want to hot reload extensions whenever they get editted

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
