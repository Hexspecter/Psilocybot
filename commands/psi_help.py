import discord
from discord.ext import commands

class Help_commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['h', 'guide', 'info'])
	async def help(self, ctx):
		embed=discord.Embed(title="Commands and info", description="Information about the different commands and arguments", color=0xff00ff)
		embed.add_field(name="Information", value="This bot is using Tripsit.me and Psychonautwiki APIs for searches and requires specific substance names.\nDatabases:\nhttps://drugs.tripsit.me/\nhttps://psychonautwiki.org/wiki/Main_Page", inline=False)
		embed.add_field(name=">dose", value="Prettified information for dose and summary\nAliases: dosage, drugs, drug, substance\nUsage: >dose Caffeine", inline=True)
		embed.add_field(name=">funhelp", value="Gives you information about the fun commands, aliases: fh, funguide, funinfo", inline=True)
		embed.add_field(name=">doge", value="Gives you dogecoin (DOGE_USDT) price data from Binance", inline=True)
		embed.add_field(name=">help", value="Shows you this list, aliases: h, guide, info", inline=True)
		await ctx.send(embed=embed)

	@commands.command(aliases=['fh', 'funguide', 'funinfo'])
	async def funhelp(self, ctx):
		embed=discord.Embed(title="Fun commands and info", description="Information about the different fun commands", color=0xff00ff)
		embed.add_field(name="Information", value="These are just the fun commands that I added in for no reason, really.\nStealth variants don't tag you.", inline=False)
		embed.add_field(name=">toke", value="Tags you and tells others you're about to smoke, aliases: smoke.", inline=True)
		embed.add_field(name=">dab", value="Tags you and tells others you're about to do a dab, aliases: oil.", inline=True)
		embed.add_field(name=">shot", value="Tags you and tells others you're about to do a shot, aliases: shotglass.", inline=True)
		embed.add_field(name=">drink", value="Tags you and tells others you're about to drink a lighter drink, aliases: beer, cider, wine.", inline=True)
		embed.add_field(name='\u200b', value="Stealth commands\nStealth commands, duh.", inline=False)
		embed.add_field(name=">stealthtoke", value="Tags you and tells others you're about to smoke, aliases: stealthsmoke.", inline=True)
		embed.add_field(name=">stealthdab", value="Tags you and tells others you're about to do a dab, aliases: stealthoil.", inline=True)
		embed.add_field(name=">stealthshot", value="Tags you and tells others you're about to do a shot, aliases: stealthshotglass.", inline=True)
		embed.add_field(name=">stealthdrink", value="Tags you and tells others you're about to drink a lighter drink, aliases: stealthbeer, stealthcider, stealthwine.", inline=True)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Help_commands(bot))
