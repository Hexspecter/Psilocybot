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

@bot.command(aliases=['tripsit', 'ts', 'dosets'])
async def tripsitme(ctx, text: str):
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

@bot.command(aliases=['psychonaut', 'psych', 'psw', 'dosepsw'])
async def psychonautwiki(ctx, query: str):
	headers = {
		"accept-type": "application/json",
		"content-type": "application/json"
	}
	payload = {
	    "query": """
	{
	    substances(query: "%s") {
	        name
	        summary
	        # routes of administration
	        roas {
	            name
	            dose {
	                units
	                threshold
	                heavy
	                common { min max }
	                light { min max }
	                strong { min max }
	            }
			        }
		        url
			    }
			}
			""" % query
		}
	json_payload = json.dumps(payload)

	api = requests.post("https://api.psychonautwiki.org/?",data=json_payload,headers=headers)
	y = api.json()
	for subs in y["data"]["substances"]:
		name = subs["name"]
		summary = subs["summary"]
		link = subs["url"]
		doses = subs["roas"][0]["dose"]
		units = doses["units"]
		threshold = doses["threshold"]
		thresholdstr = str(threshold)
		thresholdf = thresholdstr, units

		light = doses["light"]
		lightmin = light["min"]
		lightmax = light["max"]
		lightminstr = str(lightmin)
		lightmaxstr = str(lightmax)
		lightuple = (lightminstr, lightmaxstr)
		lightx = "-".join(lightuple)
		lighty = lightx, units

		common = doses["common"]
		commonmin = common["min"]
		commonmax = common["max"]
		commonminstr = str(commonmin)
		commonmaxstr = str(commonmax)
		commontuple = (commonminstr, commonmaxstr)
		commonx = "-".join(commontuple)
		commony = commonx, units

		strong = doses["strong"]
		strongmin = strong["min"]
		strongmax = strong["max"]
		strongminstr = str(strongmin)
		strongmaxstr = str(strongmax)
		strongtuple = (strongmaxstr, strongminstr)
		strongx = "-".join(strongtuple)
		strongy = strongx, units

		heavy = doses["heavy"]
		heavystr = str(heavy)
		heavyf = heavystr, units

	embed=discord.Embed(title=name, description=summary, color=0x00ff00)
	embed.add_field(name="Dosage:", value="Average dosages", inline=False)
	embed.add_field(name="Threshold", value=" ".join(thresholdf), inline=True)
	embed.add_field(name="Light", value=" ".join(lighty), inline=True)
	embed.add_field(name="Common", value=" ".join(commony), inline=True)
	embed.add_field(name="Strong", value=" ".join(strongy), inline=True)
	embed.add_field(name="Heavy", value=" ".join(heavyf), inline=True)
	embed.add_field(name="More information", value=link, inline=False)
	await ctx.send(embed=embed)

@tripsitme.error
async def tripsitme_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You don't even know what you're searching for. No drugs for you!")
        
bot.run(TOKEN)
