import discord
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>', help_command=None)

@bot.command(aliases=['h', 'guide', 'info'])
async def help(ctx):
    embed=discord.Embed(title="Commands and info", description="Information about the different commands and arguments", color=0xff00ff)
    embed.add_field(name="Information", value="This bot is using the Tripsit.me API for searches and requires specific substance names.\nDatabase: https://drugs.tripsit.me/", inline=False)
    embed.add_field(name=">dose", value="Searches info and dosage of a substance, aliases: d, dosage. \nUsage: >dose LSD", inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=['dosage', 'd'])
async def dose(ctx, text: str):
    search = {'name': text}
    r = requests.get('http://tripbot.tripsit.me/api/tripsit/getDrug', params=search)
    x = r.json()
    for author in x["data"]:
        desc = author["pretty_name"]
        prop = author["properties"]
        dose = prop["dose"]
        summ = prop["summary"]
    embed=discord.Embed(title=desc, description=summ, color=0x0000ff)
    embed.add_field(name="Dosage", value=dose, inline=False)
    await ctx.send(embed=embed)
        
@dose.error
async def dose_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You don't even know what you're searching for. No drugs for you! (jk, but your command was prob wrong)")
        
bot.run(TOKEN)
