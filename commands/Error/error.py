from discord.ext import commands
from commands.mod import warning
from commands.utils import temp_ban


class errors(commands.Cog):
    global warning

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I seem to lack some permissions to do dat")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command doesn't work here lmao ded")
        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.NotOwner):
                pass
            else:
                await ctx.send("U miss required permissions")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Lode lag gye funwaa xDDDD")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Lode lag gye funwaa wD")
        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id in warning:
                warning[ctx.author.id] += 1
            else:
                warning[ctx.author.id] = 1
            print(warning)
            await ctx.send(f"You are sending commands too fast send after {round(error.retry_after,1)}")
            if warning[ctx.author.id] >= 2:
                print("temp_banning")
                temp_ban(userid=ctx.author.id)


def setup(client):
    client.add_cog(errors(client))
