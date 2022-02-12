import discord

client = discord.Client()

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return
    if message.content.startswith("eae eco dj"):

        if str(message.author) == "Eco#0745":
            await message.channel.send("Eae meu criador, quando é que eu vou poder banir geral?")
        else:
            await message.channel.send("salve salve camarada, rola uma musiquinha?")


client.run('Your Token Bot')


