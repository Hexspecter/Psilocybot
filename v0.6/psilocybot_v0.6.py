import discord
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Init bot prefix and remove default help command
bot = commands.Bot(command_prefix='>', help_command=None)

# Create custom help commands
@bot.command(aliases=['h', 'guide', 'info'])
async def help(ctx):
	embed=discord.Embed(title="Commands and info", description="Information about the different commands and arguments", color=0xff00ff)
	embed.add_field(name="Information", value="This bot is using the Tripsit.me and Psychonautwiki APIs for searches and requires specific substance names.\nDatabase: https://drugs.tripsit.me/", inline=False)
	embed.add_field(name=">dose", value="Prettified information for dose and summary.", inline=True)
	embed.add_field(name=">tripsitme", value="Searches info and dosage of a substance from Tripsit.me, aliases: tripsit, ts, tsdose\nUsage: >tripsitme LSD", inline=True)
	embed.add_field(name=">psychonautwiki", value="Searches info and dosage of a substance from Psychonautwiki, aliases: psychonaut, psych, psw, pswdose. \nUsage: >psychonautwiki LSD", inline=True)
	embed.add_field(name=">funhelp", value="Gives you information about the fun commands, aliases: fh, funguide, funinfo", inline=True)
	embed.add_field(name=">help", value="Shows you this list, aliases: h, guide, info", inline=True)
	await ctx.send(embed=embed)

# Create fun command help menu
@bot.command(aliases=['fh', 'funguide', 'funinfo'])
async def funhelp(ctx):
	embed=discord.Embed(title="Fun commands and info", description="Information about the different fun commands", color=0xff00ff)
	embed.add_field(name="Information", value="These are just the fun commands that I added in for no reason, really.\nStealth variants don't tag you.", inline=False)
	embed.add_field(name=">toke", value="Tags you and tells others you're about to smoke, aliases: smoke.", inline=True)
	embed.add_field(name=">dab", value="Tags you and tells others you're about to do a dab, aliases: oil.", inline=True)
	embed.add_field(name=">shot", value="Tags you and tells others you're about to do a shot, aliases: shotglass.", inline=True)
	embed.add_field(name=">drink", value="Tags you and tells others you're about to drink a lighter drink, aliases: beer, cider, wine.", inline=True)
	embed.add_field(name="Stealth commands", value="Stealth commands, duh.", inline=False)
	embed.add_field(name=">stealthtoke", value="Tags you and tells others you're about to smoke, aliases: stealthsmoke.", inline=True)
	embed.add_field(name=">stealthdab", value="Tags you and tells others you're about to do a dab, aliases: stealthoil.", inline=True)
	embed.add_field(name=">stealthshot", value="Tags you and tells others you're about to do a shot, aliases: stealthshotglass.", inline=True)
	embed.add_field(name=">stealthdrink", value="Tags you and tells others you're about to drink a lighter drink, aliases: stealthbeer, stealthcider, stealthwine.", inline=True)
	await ctx.send(embed=embed)

# Fun commands! (Self-explanatory, really)
@bot.command(aliases=['smoke'])
async def toke(ctx):
	await ctx.send(f"{ctx.message.author.mention} just lit up, join and smoke with them!")
@bot.command(aliases=['oil'])
async def dab(ctx):
	await ctx.send(f"{ctx.message.author.mention} is about to heat up their nail or banger, join and dab with them!")
@bot.command(aliases=['shotglass'])
async def shot(ctx):
	await ctx.send(f"{ctx.message.author.mention} is about to take a shot, join and take a shot with them!")
@bot.command(aliases=['beer', 'cider', 'wine'])
async def drink(ctx):
	await ctx.send(f"{ctx.message.author.mention} is cracking open a cold one, join them and crack open a cold one!")

# Stealth fun commands! (Self-explanatory, really, stealthy)
@bot.command(aliases=['stealthsmoke'])
async def stealthtoke(ctx):
	await ctx.send(f"{ctx.author.name} just lit up, join and smoke with them!")
@bot.command(aliases=['stealthoil'])
async def stealthdab(ctx):
	await ctx.send(f"{ctx.author.name} is about to heat up their nail or banger, join and dab with them!")
@bot.command(aliases=['stealthshotglass'])
async def stealthshot(ctx):
	await ctx.send(f"{ctx.author.name} is about to take a shot, join and take a shot with them!")
@bot.command(aliases=['stealthbeer', 'stealthcider', 'stealthwine'])
async def stealthdrink(ctx):
	await ctx.send(f"{ctx.author.name} is cracking open a cold one, join them and crack open a cold one!")

# Psychonautwiki JSON post + sorting
@bot.command(aliases=['psychonaut', 'psych', 'psw', 'pswdose'])
async def psychonautwiki(ctx, query: str):

	# Create header info for POSTing
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
				duration {
					afterglow { min max units }
					comeup { min max units }
					offset { min max units }
					onset { min max units }
					peak { min max units }
					total { min max units }
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

		# Get link for the wiki page
		link = subs["url"]

		# Get the use method
		method = subs["roas"][0]["name"]

		# JSON sorting informations from POST
		doses = subs["roas"][0]["dose"]

		# Get threshold dose info
		threshold = f"{doses['threshold']} {doses['units']}"

		# Get light dose info
		light = doses["light"]
		lightf = f"{light['min']}-{light['max']} {doses['units']}"

		# Get common dose info
		common = doses["common"]
		commonf = f"{common['min']}-{common['max']} {doses['units']}"

		# Get strong dose info
		strong = doses["strong"]
		strongf = f"{strong['min']}-{strong['max']} {doses['units']}"

		# Get heavy dose info
		heavy = f"{doses['heavy']} {doses['units']}"

		#	Duration Data Gathering
		duration = subs["roas"][0]["duration"]

		afterglow = duration["afterglow"]
		if afterglow == None:
			afterglow = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			afterglow = afterglow
		afterglowf = f"{afterglow['min']}-{afterglow['max']} {afterglow['units']}"

		comeup = duration["comeup"]
		if comeup == None:
			comeup = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			comeup = comeup
		comeupunit2 = "minutes"
		if comeupunit == None:
			comeupf = f"{comeup['min']}-{comeup['max']} comeupunit2"
		else:
			comeupf = f"{comeup['min']}-{comeup['max']} {comeup['units']}"

		offset = duration["offset"]
		if offset == None:
			offset = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			offset = offset
		offsetf = f"{offset['min']}-{offset['max']} {offset['units']}"

		onset = duration["onset"]
		if onset == None:
			onset = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			onset = onset
		onsetf = f"{onset['min']}-{onset['max']} {onset['units']}"

		peak = duration["peak"]
		if peak == None:
			peak = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			peak = peak
		peakf = f"{peak['min']}-{peak['max']} {peak['units']}"

		total = duration["total"]
		if total == None:
			total = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			total = total
		totalf = f"{total['min']}-{total['max']} {total['units']}"
		# Create pretty embed
		embed=discord.Embed(title=name, description=summ, url=link, color=0x00ff00)
		embed.add_field(name="-", value="-----------------", inline=False)
		embed.add_field(name="Dosage", value=method, inline=False)
		embed.add_field(name="Threshold", value=threshold, inline=True)
		embed.add_field(name="Light", value=lightf, inline=True)
		embed.add_field(name="Common", value=commonf, inline=True)
		embed.add_field(name="Strong", value=strongf, inline=True)
		embed.add_field(name="Heavy", value=heavy, inline=True)
		embed.add_field(name="-", value="-----------------", inline=False)
		embed.add_field(name="Duration", value="common durations", inline=False)
		embed.add_field(name="Onset", value=onsetf, inline=True)
		embed.add_field(name="Comeup", value=comeupf, inline=True)
		embed.add_field(name="Peak", value=peakf, inline=True)
		embed.add_field(name="Offset", value=offsetf, inline=True)
		embed.add_field(name="Total", value=totalf, inline=True)
		embed.add_field(name="After effects", value=afterglowf, inline=True)
		await ctx.send(embed=embed)

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

# Mash both together to get even prettier menus!
@bot.command(aliases=['drug', 'substance'])
async def dose(ctx, query: str):
	search = {'name': query}
	r = requests.get('http://tripbot.tripsit.me/api/tripsit/getDrug', params=search)
	x = r.json()
	for author in x["data"]:
		prop = author["properties"]
		summ = prop["summary"]
	headers = {
		"accept-type": "application/json",
		"content-type": "application/json"
	}
	payload = {
	    "query": """
	{
		substances(query: "%s") {
			name
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
				duration {
					afterglow { min max units }
					comeup { min max units }
					offset { min max units }
					onset { min max units }
					peak { min max units }
					total { min max units }
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
		doses = subs["roas"][0]["dose"]
		light = doses["light"]
		common = doses["common"]
		strong = doses["strong"]
		duration = subs["roas"][0]["duration"]
		afterglow = duration["afterglow"]
		if afterglow == None:
			afterglow = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			afterglow = afterglow
		comeup = duration["comeup"]
		if comeup == None:
			comeup = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			comeup = comeup
		comeupunit2 = "minutes"
		if comeup["units"] == None:
			comeupf = f"{comeup['min']}-{comeup['max']} comeupunit2"
		else:
			comeupf = f"{comeup['min']}-{comeup['max']} {comeup['units']}"
		offset = duration["offset"]
		if offset == None:
			offset = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			offset = offset
		onset = duration["onset"]
		if onset == None:
			onset = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			onset = onset
		peak = duration["peak"]
		if peak == None:
			peak = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			peak = peak
		total = duration["total"]
		if total == None:
			total = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			total = total
		embed=discord.Embed(title=f"subs['name']", description=summ, url=f"{subs['url']}", color=0x00ff00)
		embed.add_field(name="-", value="-----------------", inline=False)
		embed.add_field(name="Dosage", value=f"{subs['roas'][0]['name']}", inline=False)
		embed.add_field(name="Threshold", value=f"{doses['threshold']} {doses['units']}", inline=True)
		embed.add_field(name="Light", value=f"{light['min']}-{light['max']} {doses['units']}", inline=True)
		embed.add_field(name="Common", value=f"{common['min']}-{common['max']} {doses['units']}", inline=True)
		embed.add_field(name="Strong", value=f"{strong['min']}-{strong['max']} {doses['units']}", inline=True)
		embed.add_field(name="Heavy", value=f"{doses['heavy']} {doses['units']}", inline=True)
		embed.add_field(name="-", value="-----------------", inline=False)
		embed.add_field(name="Duration", value="common durations", inline=False)
		embed.add_field(name="Onset", value=f"{onset['min']}-{onset['max']} {onset['units']}", inline=True)
		embed.add_field(name="Comeup", value=comeupf, inline=True)
		embed.add_field(name="Peak", value=f"{peak['min']}-{peak['max']} {peak['units']}", inline=True)
		embed.add_field(name="Offset", value=f"{offset['min']}-{offset['max']} {offset['units']}", inline=True)
		embed.add_field(name="Total", value=f"{total['min']}-{total['max']} {total['units']}", inline=True)
		embed.add_field(name="After effects", value=f"{afterglow['min']}-{afterglow['max']} {afterglow['units']}", inline=True)
		await ctx.send(embed=embed)

@dose.error
async def dose_error(ctx, error):
	if isinstance(error, commands.CommandInvokeError):
		await ctx.send("You don't even know what you're searching for. No drugs for you!\n(jk, but your command was probably wrong, try >help")
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
