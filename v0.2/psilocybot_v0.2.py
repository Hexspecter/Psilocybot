import discord
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Init bot prefix and remove default help command
bot = commands.Bot(command_prefix='>', help_command=None)

# Create custom help command
@bot.command(aliases=['h', 'guide', 'info'])
async def help(ctx):
    embed=discord.Embed(title="Commands and info", description="Information about the different commands and arguments", color=0xff00ff)
    embed.add_field(name="Information", value="This bot is using the Tripsit.me and Psychonautwiki APIs for searches and requires specific substance names.\nDatabase: https://drugs.tripsit.me/", inline=False)
    embed.add_field(name=">tripsitme", value="Searches info and dosage of a substance from Tripsit.me, aliases: tripsit, ts, tsdose. \nUsage: >tripsitme LSD", inline=True)
    embed.add_field(name=">psychonautwiki", value="Searches info and dosage of a substance from Psychonautwiki, aliases: psychonaut, psych, psw, pswdose. \nUsage: >psychonautwiki LSD", inline=True)
    await ctx.send(embed=embed)

# Fun commands!


# Tripsitme API json get + sorting
@bot.command(aliases=['tripsit', 'ts', 'tsdose'])
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

# Psychonautwiki JSON post + sorting
@bot.command(aliases=['psychonaut', 'psych', 'psw', 'pswdose'])
async def psychonautwiki(ctx, query: str):
	headers = {
		"accept-type": "application/json",
		"content-type": "application/json"
	}
	# Create JSON post payload
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

	# Make it into a JSON dump
	json_payload = json.dumps(payload)

	# Init API payload for posting
	api = requests.post("https://api.psychonautwiki.org/?",data=json_payload,headers=headers)

	# Convert data into json
	y = api.json()

	# Sort through the JSON data
	for subs in y["data"]["substances"]:

		# Get substance name for embed
		name = subs["name"]

		# See if a summary exists (usually empty)
		summary = subs["summary"]

		# Get link for the wiki page
		link = subs["url"]

		# JSON sorting informations from POST
		doses = subs["roas"][0]["dose"]

		# Get units
		units = doses["units"]

		# Get threshold dose info
		threshold = doses["threshold"]

		# Generate pretty doses (0-999 mg)
		thresholdstr = str(threshold)
		thresholdf = thresholdstr, units

		# Get light dose info
		light = doses["light"]
		# Generate pretty doses (0-999 mg)
		lightmin = light["min"]
		lightmax = light["max"]
		lightminstr = str(lightmin)
		lightmaxstr = str(lightmax)
		lightuple = (lightminstr, lightmaxstr)
		lightx = "-".join(lightuple)
		lighty = lightx, units

		# Get common dose info
		common = doses["common"]
		# Generate pretty doses (0-999 mg)	
		commonmin = common["min"]
		commonmax = common["max"]
		commonminstr = str(commonmin)
		commonmaxstr = str(commonmax)
		commontuple = (commonminstr, commonmaxstr)
		commonx = "-".join(commontuple)
		commony = commonx, units

		# Get strong dose info
		strong = doses["strong"]
		# Generate pretty doses (0-999 mg)
		strongmin = strong["min"]
		strongmax = strong["max"]
		strongminstr = str(strongmin)
		strongmaxstr = str(strongmax)
		strongtuple = (strongmaxstr, strongminstr)
		strongx = "-".join(strongtuple)
		strongy = strongx, units

		# Get heavy dose info
		heavy = doses["heavy"]
		# Generate pretty doses (0-999 mg)
		heavystr = str(heavy)
		heavyf = heavystr, units

	# Create pretty embed
	embed=discord.Embed(title=name, description=summary, color=0x00ff00)
	embed.add_field(name="Dosage", value="Average dosages", inline=False)
	embed.add_field(name="Threshold", value=" ".join(thresholdf), inline=True)
	embed.add_field(name="Light", value=" ".join(lighty), inline=True)
	embed.add_field(name="Common", value=" ".join(commony), inline=True)
	embed.add_field(name="Strong", value=" ".join(strongy), inline=True)
	embed.add_field(name="Heavy", value=" ".join(heavyf), inline=True)
	embed.add_field(name="More information", value=link, inline=False)
	await ctx.send(embed=embed)

# Basic error catching
@tripsitme.error
async def tripsitme_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("You don't even know what you're searching for. No drugs for you!\n(jk, but your command was probably wrong, try >help")

@psychonautwiki.error
async def psychonautwiki_error(ctx, error):
	if isinstance(error, commands.CommandInvokeError):
		await ctx.send("You don't even know what you're searching for. No drugs for you!\n(jk, but your command was probably wrong, try >help")

# :) No tokens for you
bot.run(TOKEN)
