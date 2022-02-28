from nextcord.ext import commands
import nextcord
from config import TOKEN
import os
import wavelink

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Eco DJ pronto para a ação.")
    bot.loop.create_task(node_connect())

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")


async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='lavalinkinc.ml', port=443, password='incognito', https=True)



@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client
        

    await vc.play(search)
    await ctx.send(f"Tocando: `{search.title}`")

@bot.command()
async def pause(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Se não está tocando nenhuma música.... Como eu irei pausar alguma coisa?")
    # elif not getattr(ctx.author.voice, "channel", None):
    #     return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.pause()
    await ctx.send("Música pausada Lol")


@bot.command()
async def resume(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Se não está tocando nenhuma música.... Como eu irei pausar alguma coisa?")
    # elif not getattr(ctx.author.voice, "channel", None):
    #     return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.resume()
    await ctx.send("Opa rodando a música de novo :D")


@bot.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Se não está tocando nenhuma música.... Como eu irei pausar alguma coisa?")
    # elif not getattr(ctx.author.voice, "channel", None):
    #     return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    await ctx.send("Parando a musica")


@bot.command()
async def disconnect(ctx: commands.Context):
    if not ctx.voice_client:
        return await ctx.send("Se não está tocando nenhuma música.... Como eu irei pausar alguma coisa?")
    # elif not getattr(ctx.author.voice, "channel", None):
    #     return await ctx.send("Se conecte a um canal de voz fazendo o favor meu camarada")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.disconnect()
    await ctx.send("Ate mais tarde")

bot.run(TOKEN)