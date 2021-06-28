import discord
import os
import asyncio
from discord.ext import commands

class Admin_tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['reload_extensions'])
    @commands.has_guild_permissions(administrator=True)
    async def reload(self, ctx):
        if ctx.message.author.id == OWNER_DISCORD_ID_HERE:
            reloaded_extensions = []
            reload_embed=discord.Embed(title="Reloading extensions!", description="Refreshing all extension files, this might take some time")
            reload_embed.add_field(name='List of reloaded extensions:', value=f"No extensions reloaded.", inline=False)
            message = await ctx.send(embed=reload_embed)
            for filename in os.listdir('./commands'):
                if filename.endswith('.py'):
                    if filename[:-3] != 'psi_admintools':
                        self.bot.reload_extension(f'commands.{filename[:-3]}')
                        reloaded_extensions.append(f"commands.{filename}")
                        await asyncio.sleep(0.5)
                        r_embed=discord.Embed(title="Reloading extensions!", description="Refreshing all extension files, this might take some time")
                        test = '\n'.join(reloaded_extensions.copy())
                        r_embed.add_field(name='List of reloaded extensions:', value=f"{test} ", inline=False)
                        await message.edit(embed=r_embed)
                    if filename[:-3] == 'psi_admintools':
                        pass
                else:
                    print(f'Unable to reload extension {filename}')
                    continue
        else:
            await ctx.send("You don't have the required permissions to use this command!")

def setup(bot):
    bot.add_cog(Admin_tools(bot))
