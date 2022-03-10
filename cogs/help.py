import discord
from discord.ext import commands


class HelpCog(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        self.color = discord.Color(0x2F3136)

    async def send_bot_help(self, mapping):
        ctx = self.context
        prefix = ctx.prefix

        embed = discord.Embed(title="Ajuda do Eco DJ", color=self.color)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)

        description = f"Para obter ajuda mais detalhada escreva: `{prefix}help <categoria>` \n\n"
        description += "**Music** \nplay, pause, volume.....\n\n"
        description += "**Meme** \nmeme "

        embed.description = description

        await ctx.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        pre = self.clean_prefix

        embed = discord.Embed(
            color=self.color, timestamp=ctx.message.created_at, description=""
        )

        if await ctx.bot.is_owner(ctx.author):
            shown_commands = [command for command in cog.get_commands()]
        else:
            shown_commands = [
                command
                for command in cog.get_commands()
                if command.hidden == False and command.enabled == True
            ]

        if len(shown_commands) == 0:
            return await ctx.send("Sem comandos.")

        if cog.description:
            cog_help = cog.description
        else:
            cog_help = "Sem comandos fornecidos"

        embed.title = f"{cog.qualified_name}"
        embed.description += f"{cog_help}\nUse `{pre}help <comando>` para mais detalhes.\n\n**Comandos :** \n"

        for command in shown_commands:
            embed.description += f"▪︎ {pre}{command.qualified_name} "
            if command.signature:
                embed.description += f"{command.signature} \n"
            else:
                embed.description += "\n"

        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)

    # Command Help
    async def send_command_help(self, command):
        ctx = self.context

        embed = discord.Embed(
            color=self.color,
            timestamp=ctx.message.created_at,
            description="",
        )

        if (
            command.hidden == True or command.enabled == False
        ) and await ctx.bot.is_owner(ctx.author) == False:
            return await ctx.send(
                f'Nenhum comando chamado "{command.qualified_name}" encontrado.'
            )

        if command.signature:
            embed.title = f"{command.qualified_name} {command.signature} \n"
        else:
            embed.title = f"{command.qualified_name}\n"

        embed.description = command.help or "Nenhuma descrição fornecida."

        if len(command.aliases) > 0:
            embed.description += "\nAbreviação : " + ", ".join(command.aliases)

        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)

    # Group Help
    async def send_group_help(self, group):
        ctx = self.context
        pre = ctx.clean_prefix

        embed = discord.Embed(color=self.color, timestamp=ctx.message.created_at)

        if group.signature:
            embed.title = f"{group.qualified_name} {group.signature}"
        else:
            embed.title = group.qualified_name + " - group"

        embed.description = group.help or "Nenhuma descrição fornecida."
        embed.description += f"\nUse `{pre}help {group.qualified_name} <sub_command>` para mais detalhes do grupo de comandos. \n\n**Subcommands : **\n"

        if await ctx.bot.is_owner(ctx.author):
            group_commands = [command for command in group.commands]
            if len(group_commands) == 0:
                return await ctx.send("Este grupo não tem nenhum subcomando")
        else:
            group_commands = [
                command
                for command in group.commands
                if command.hidden == False and command.enabled == True
            ]

        if len(group_commands) == 0:
            return await ctx.send(f'Nenhum comando chamado "{group.qualified_name}" encontrado.')

        for command in group_commands:
            if command.signature:
                command_help = (
                    f"▪︎ {pre}{command.qualified_name} {command.signature} \n"
                )
            else:
                command_help = f"▪︎ {pre}{command.qualified_name} \n"

            embed.description += command_help

        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)


class Help(commands.Cog):
    """Comandos de ajuda"""

    def __init__(self, client):
        self.client = client
        self.client._original_help_command = client.help_command
        client.help_command = HelpCog()
        client.help_command.cog = self

    def cog_unload(self):
        self.client.help_command = self.client._original_help_command


def setup(client):
    client.add_cog(Help(client))
