from turtle import title
from unicodedata import name
from discord import Embed
from nextcord.ext import commands
from nextcord.utils import find
from nextcord import Interaction
import os, wavelink, urllib, json, random, nextcord, asyncio

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Bem vindo {member.mention} ao {guild.name} e eu sou seu bot de música! 🥳'
            await guild.system_channel.send(to_send)


intents = nextcord.Intents.default()
intents.members = True

bot = Bot(command_prefix='!', intents=intents)


#Events------------------------------------------------
@bot.event
async def on_ready():
    print("Eco DJ pronto para a ação.")
    bot.loop.create_task(node_connect())
    await bot.change_presence(activity=nextcord.Activity(type = nextcord.ActivityType.listening, name = "!comandos"))

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} pronto pra tocar música!")

@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'geral', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Olá que bom está aqui abaixo segue algumas informações: \n\nMeus comandos: \n!play - Procura por uma música tanto por palavra quanto pela URL \n!pause - Pausa a música que está tocando \n!resume - Da continuidade a música de onde ela parou \n!stop - Para a música que está tocando e desconecta o Bot em seguida \n!meme - Para ver alguma coisa engraçada, ou quase \n!comandos - Para acessar a lista de comandos \n\n Essa é minha versão 0.1 então pegue leve xD \nNôs aceitamos um café para incentivar no meu desenvolvimento para está cada vez mais aprimorado: https://www.buymeacoffee.com/ecodj.')


async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='losingtime.dpaste.org', port=2124, password='SleepingOnTrains')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('🤔 Comando inválido. Tente usar algum desses: \n!play | !pause | !resume | !stop | !meme')
#End Events------------------------------------------------


#Show Command------------------------------------------------
@bot.command()
async def comandos(ctx: commands.Context):
    embed = nextcord.Embed()
    embed.description = "Meus comandos: \n!play - Procura por uma música tanto por palavra quanto pela URL \n!pause - Pausa a música que está tocando \n!resume - Da continuidade a música de onde ela parou \n!stop - Para a música que está tocando e desconecta o Bot em seguida \n!meme - Para ver alguma coisa engraçada \n\n Essa é minha versão 0.1 então pegue leve xD \nNôs aceitamos um café para incentivar no meu desenvolvimento para está cada vez mais aprimorado: [buymeacoffee.com/ecodj](https://www.buymeacoffee.com/ecodj)."
    await ctx.send(embed=embed)


#Play Command------------------------------------------------
@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.play(search)
    await ctx.send(f"Tocando agora: `{search.title}` 🎶🎶")

#Pause Command------------------------------------------------
@bot.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Se não está tocando nenhuma música.... Como eu irei pausar alguma coisa?")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.pause()
    await ctx.send("Música pausada 🥱")


#Resume Command------------------------------------------------
@bot.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Sem música para prosseguir com a melodia...")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.resume()
    await ctx.send("Opa rodando a música de novo 😁")


#Stop Command------------------------------------------------
@bot.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Não achei nenhuma música que esteja tocando/pausada para interrompe-la!")
    elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    await ctx.send("Parando a música 😴, até logo...")
    # se desconecta logo depois de parar a música
    await vc.disconnect()


#Meme Command------------------------------------------------
@bot.command()
async def meme(ctx):
    memeAPI = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme/MemesBrasil')
    memeData = json.load(memeAPI)

    memeUrl = memeData['url']
    memeName = memeData['title']

    embed = nextcord.Embed(title=memeName, colour=nextcord.Colour.purple())
    embed.set_image(url=memeUrl)

    phases = ['Olha isso KK', 'Essa vai ser melhor', 'KKK QuE IsSo', 'análise', 'Seraci nãorir', '🤣🤣🤣🤣🤣🤣']
    r = random.choice(phases)
    await ctx.send("{}".format(r))
    await ctx.send(embed=embed)


# o bot ira se desconectar no comando !stop logo o comando !disconnect esta sem uso
@bot.command()
async def disconnect(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Não estou conectado em um canal de voz!")
    # elif not getattr(ctx.author.voice, "channel", None):
    #     return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.disconnect()
    await ctx.send("Até mais tarde 😉 ")

bot.run("YOUR_TOKEN")
