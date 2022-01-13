import os
import asyncio
import discord
from discord.ext import commands

OWNER_ID = "Replace with your owner id"

class AdminTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send("Chat cleared by {}".format(ctx.author.mention))
        await ctx.send(str(limit) + " messages were deleted")
        print("The purge command was used by {} {} to delete {} messages".format(ctx.author.id, ctx.author.name, str(limit)))
        print(str(limit) + " messages were deleted")

    @commands.command(aliases=['reload_extensions'])
    @commands.is_owner()
    async def reload(self, ctx):
        """Support for hot reloading all extension files except admin tools"""
        if ctx.message.author.id == OWNER_ID:
            reloaded_extensions = []
            reload_embed=discord.Embed(title="Reloading extensions!", description="Refreshing all extension files, this might take some time")
            reload_embed.add_field(name='List of reloaded extensions:', value="No extensions reloaded.", inline=False)
            message = await ctx.send(embed=reload_embed)
            for filename in os.listdir('./commands'):
                if filename.endswith('.py'):
                    if filename[:-3] != 'psi_admintools':
                        self.bot.reload_extension(f'commands.{filename[:-3]}')
                        reloaded_extensions.append(f"commands.{filename}")
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

    @commands.command(aliases=['reload_file'])
    @commands.is_owner()
    async def reload_single(self, ctx, extension):
        """Support for hot reloading a single extension file except admin tools"""
        if ctx.message.author.id == OWNER_ID:
            unload_embed=discord.Embed(title="Reloading extension!", description="Reloading extension file, this might take some time")
            unload_embed.add_field(name='Reloaded extension:', value="No reloaded extension.", inline=False)
            message = await ctx.send(embed=unload_embed)
            for filename in os.listdir('./commands'):
                if filename.endswith('.py'):
                    if filename[:-3] == extension:
                        self.bot.reload_extension(f'commands.{filename[:-3]}')
                        ul_embed=discord.Embed(title="Reloading extension!", description="Reloading extension file, this might take some time")
                        ul_embed.add_field(name='Reloaded extension:', value=f"\ncommands.{filename} loaded!", inline=False)
                        await message.edit(embed=ul_embed)
                    if filename[:-3] and extension == 'psi_admintools':
                        ul_embed=discord.Embed(title="Warning!", description="This is a core file, this file cannot be hotloaded!")
                        await message.edit(embed=ul_embed)
        else:
            await ctx.send("You don't have the required permissions to use this command!")

    @commands.command(aliases=['load_extension'])
    @commands.is_owner()
    async def load(self, ctx, extension):
        """Support for hotloading a single extension file except admin tools"""
        if ctx.message.author.id == OWNER_ID:
            unload_embed=discord.Embed(title="Loading extension!", description="Loading extension file, this might take some time")
            unload_embed.add_field(name='Loaded extension:', value="No loaded extension.", inline=False)
            message = await ctx.send(embed=unload_embed)
            for filename in os.listdir('./commands'):
                if filename.endswith('.py'):
                    if filename[:-3] == extension:
                        self.bot.load_extension(f'commands.{filename[:-3]}')
                        ul_embed=discord.Embed(title="Loading extension!", description="Loading extension file, this might take some time")
                        ul_embed.add_field(name='Loaded extension:', value=f"\ncommands.{filename} loaded!", inline=False)
                        await message.edit(embed=ul_embed)
                    if filename[:-3] and extension == 'psi_admintools':
                        ul_embed=discord.Embed(title="Warning!", description="This is a core file, this file cannot be hotloaded!")
                        await message.edit(embed=ul_embed)
        else:
            await ctx.send("You don't have the required permissions to use this command!")

    @commands.command(aliases=['unload_extension'])
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """Support for hot unloading a single extension file except admin tools"""
        if ctx.message.author.id == OWNER_ID:
            print(extension)
            unload_embed=discord.Embed(title="Unloading extension!", description="Unloading extension file, this might take some time")
            unload_embed.add_field(name='Unloaded extension:', value=f"No unloaded extension.", inline=False)
            message = await ctx.send(embed=unload_embed)
            for filename in os.listdir('./commands'):
                if filename.endswith('.py'):
                    if filename[:-3] == extension:
                        self.bot.unload_extension(f'commands.{filename[:-3]}')
                        ul_embed=discord.Embed(title="Unloading extension!", description="Unloading extension file, this might take some time")
                        ul_embed.add_field(name='Unloaded extension:', value=f"\ncommands.{filename} unloaded!", inline=False)
                        await message.edit(embed=ul_embed)
                    if filename[:-3] and extension == 'psi_admintools':
                        ul_embed=discord.Embed(title="Warning!", description="This is a core file, this file cannot be hotloaded!")
                        await message.edit(embed=ul_embed)
        else:
            await ctx.send("You don't have the required permissions to use this command!")

def setup(bot):
    bot.add_cog(AdminTools(bot))
