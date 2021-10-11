import nextcord as discord
from nextcord.ext import commands

class Core(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="출력")
    async def printit(self,ctx):
        await ctx.send(":) Python Bot에 의해 출력됨.")


def setup(bot):
    bot.add_cog(Core(bot))
    