import discord
import random
from discord.ext import commands

class Fun_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['smoke'])
    async def toke(ctx):
        tokelist = (f"{ctx.message.author.mention} sparked up a joint, join and smoke with them!", f"{ctx.message.author.mention} grabbed their weed and smoked a bowl, join and smoke with them!", f"{ctx.message.author.mention} just lit up, join and smoke with them!")
        await ctx.send(random.choice(tokelist))

    @commands.command(aliases=['oil'])
    async def dab(ctx):
        await ctx.send(f"{ctx.message.author.mention} is about to heat up their nail or banger, join and dab with them!")

    @commands.command(aliases=['shotglass'])
    async def shot(ctx):
        await ctx.send(f"{ctx.message.author.mention} is about to take a shot, join and take a shot with them!")

    @commands.command(aliases=['opi'])
    async def opiate(ctx):
        await ctx.send(f"{ctx.message.author.mention} is about to get noddy with some opiates.\nEmpty your grandparents med cabinet and join them with the nods.")

    @commands.command(aliases=['beer', 'cider', 'wine', 'cheers'])
    async def drink(ctx):
        await ctx.send(f"{ctx.message.author.mention} is cracking open a cold one, join them and crack open a cold one!")

    @commands.command(aliases=['stealthsmoke'])
    async def stealthtoke(ctx):
        await ctx.send(f"{ctx.author.name} just lit up, join and smoke with them!")

    @commands.command(aliases=['stealthoil'])
    async def stealthdab(ctx):
        await ctx.send(f"{ctx.author.name} is about to heat up their nail or banger, join and dab with them!")

    @commands.command(aliases=['stealthshotglass'])
    async def stealthshot(ctx):
        await ctx.send(f"{ctx.author.name} is about to take a shot, join and take a shot with them!")

    @commands.command(aliases=['stealthbeer', 'stealthcider', 'stealthwine', 'stealthcheers'])
    async def stealthdrink(ctx):
        await ctx.send(f"{ctx.author.name} is cracking open a cold one, join them and crack open a cold one!")


    @commands.command(aliases=['hugging'])
    async def hug(ctx, user):
        user = ctx.message.mentions[0]
        guild = bot.get_guild(ctx.guild.id)
        if guild.get_member(user.id) is not None:
            await ctx.send(f"{user.mention}, you just got hugged by {ctx.message.author.mention}")
        else:
            await ctx.send("You didn't mention anyone, try again and mention someone.")

def setup(bot):
    bot.add_cog(Fun_commands(bot))