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
		# Get units
		units = doses["units"]
		# Get threshold dose info
		threshold = doses["threshold"]
		# Generate pretty doses (0-999 mg)
		thresholdstr = str(threshold)
		thresholdf = thresholdstr, units
		# Get light dose info
		light = doses["light"]
		# Get light dose min and max values as ints
		lightmin = light["min"]
		lightmax = light["max"]
		# Convert ints to strings
		lightminstr = str(lightmin)
		lightmaxstr = str(lightmax)
		# Create a tuple for joining with units info
		lightuple = (lightminstr, lightmaxstr)
		lightx = "-".join(lightuple)
		lighty = lightx, units
		# Get common dose info
		common = doses["common"]
		# Get common dose min and max values as ints
		commonmin = common["min"]
		commonmax = common["max"]
		# Convert ints to strings
		commonminstr = str(commonmin)
		commonmaxstr = str(commonmax)
		# Create a tuple for joining with units info
		commontuple = (commonminstr, commonmaxstr)
		commonx = "-".join(commontuple)
		commony = commonx, units
		# Get strong dose info
		strong = doses["strong"]
		# Get strong dose min and max values as ints
		strongmin = strong["min"]
		strongmax = strong["max"]
		# Convert ints to strings
		strongminstr = str(strongmin)
		strongmaxstr = str(strongmax)
		# Create a tuple for joining with units info
		strongtuple = (strongmaxstr, strongminstr)
		strongx = "-".join(strongtuple)
		strongy = strongx, units

		# Get heavy dose info
		heavy = doses["heavy"]
		# Convert int to str
		heavystr = str(heavy)
		heavyf = heavystr, units

		#	Duration Data Gathering
		duration = subs["roas"][0]["duration"]

		afterglow = duration["afterglow"]
		if afterglow == None:
			afterglow = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			afterglow = afterglow
		afterglowmin = afterglow["min"]
		afterglowmax = afterglow["max"]
		afterglowunit = afterglow["units"]
		afterglowminstr = str(afterglowmin)
		afterglowmaxstr = str(afterglowmax)
		afterglowtuple1 = (afterglowminstr, afterglowmaxstr)
		afterglowx = "-".join(afterglowtuple1)
		afterglowtuple2 = (afterglowx, afterglowunit)

		comeup = duration["comeup"]
		if comeup == None:
			comeup = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			comeup = comeup
		comeupmin = comeup["min"]
		comeupmax = comeup["max"]
		comeupunit = comeup["units"]
		comeupunit2 = "minutes"
		comeupminstr = str(comeupmin)
		comeupmaxstr = str(comeupmax)
		comeuptuple1 = (comeupminstr, comeupmaxstr)
		comeupx = "-".join(comeuptuple1)
		if comeupunit == None:
			comeuptuple2 = (comeupx, comeupunit2)
		else:
			comeuptuple2 = (comeupx, comeupunit)

		offset = duration["offset"]
		if offset == None:
			offset = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			offset = offset
		offsetmin = offset["min"]
		offsetmax = offset["max"]
		offsetunit = offset["units"]
		offminstr = str(offsetmin)
		offmaxstr = str(offsetmax)
		offtuple1 = (offminstr, offmaxstr)
		offsetx = "-".join(offtuple1)
		offtuple2 = (offsetx, offsetunit)

		onset = duration["onset"]
		if onset == None:
			onset = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			onset = onset
		onsetmin = onset["min"]
		onsetmax = onset["max"]
		onsetunit = onset["units"]
		onsetminstr = str(onsetmin)
		onsetmaxstr = str(onsetmax)
		ontuple1 = (onsetminstr, onsetmaxstr)
		onsetx = "-".join(ontuple1)
		ontuple2 = (onsetx, onsetunit)

		peak = duration["peak"]
		if peak == None:
			peak = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			peak = peak
		peakmin = peak["min"]
		peakmax = peak["max"]
		peakunit = peak["units"]
		peakminstr = str(peakmin)
		peakmaxstr = str(peakmax)
		peaktuple1 = (peakminstr, peakmaxstr)
		peakx = "-".join(peaktuple1)
		peaktuple2 = (peakx, peakunit)

		total = duration["total"]
		if total == None:
			total = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			total = total
		totalmin = total["min"]
		totalmax = total["max"]
		totalunit = total["units"]
		totalminstr = str(totalmin)
		totalmaxstr = str(totalmax)
		totaltuple1 = (totalminstr, totalmaxstr)
		totalx = "-".join(totaltuple1)
		totaltuple2 = (totalx, totalunit)


	# Create pretty embed
	embed=discord.Embed(title=name, description=summ, url=link, color=0x00ff00)
	embed.add_field(name="-", value="-----------------", inline=False)
	embed.add_field(name="Dosage", value=method, inline=False)
	embed.add_field(name="Threshold", value=" ".join(thresholdf), inline=True)
	embed.add_field(name="Light", value=" ".join(lighty), inline=True)
	embed.add_field(name="Common", value=" ".join(commony), inline=True)
	embed.add_field(name="Strong", value=" ".join(strongy), inline=True)
	embed.add_field(name="Heavy", value=" ".join(heavyf), inline=True)
	embed.add_field(name="-", value="-----------------", inline=False)
	embed.add_field(name="Duration", value="common durations", inline=False)
	embed.add_field(name="Onset", value=" ".join(ontuple2), inline=True)
	embed.add_field(name="Comeup", value=" ".join(comeuptuple2), inline=True)
	embed.add_field(name="Peak", value=" ".join(peaktuple2), inline=True)
	embed.add_field(name="Offset", value=" ".join(offtuple2), inline=True)
	embed.add_field(name="Total", value=" ".join(totaltuple2), inline=True)
	embed.add_field(name="After effects", value=" ".join(afterglowtuple2), inline=True)
	await ctx.send(embed=embed)

# Tripsitme API json get + sorting
@bot.command(aliases=['tripsit', 'ts', 'tsdose'])
async def tripsitme(ctx, text: str):
	search = {'name': text}
	r = requests.get('http://tripbot.tripsit.me/api/tripsit/getDrug', params=search)
	x = r.json()
	# Sort JSON and prep vars for pretty embeds
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
	# Sort JSON and prep vars for pretty embeds
	for author in x["data"]:
		desc = author["pretty_name"]
		prop = author["properties"]
		dosageas = prop["dose"]
		summ = prop["summary"]
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
		# Get units
		units = doses["units"]
		# Get threshold dose info
		threshold = doses["threshold"]
		# Generate pretty doses (0-999 mg)
		thresholdstr = str(threshold)
		thresholdf = thresholdstr, units
		# Get light dose info
		light = doses["light"]
		# Get light dose min and max values as ints
		lightmin = light["min"]
		lightmax = light["max"]
		# Convert ints to strings
		lightminstr = str(lightmin)
		lightmaxstr = str(lightmax)
		# Create a tuple for joining with units info
		lightuple = (lightminstr, lightmaxstr)
		lightx = "-".join(lightuple)
		lighty = lightx, units
		# Get common dose info
		common = doses["common"]
		# Get common dose min and max values as ints
		commonmin = common["min"]
		commonmax = common["max"]
		# Convert ints to strings
		commonminstr = str(commonmin)
		commonmaxstr = str(commonmax)
		# Create a tuple for joining with units info
		commontuple = (commonminstr, commonmaxstr)
		commonx = "-".join(commontuple)
		commony = commonx, units
		# Get strong dose info
		strong = doses["strong"]
		# Get strong dose min and max values as ints
		strongmin = strong["min"]
		strongmax = strong["max"]
		# Convert ints to strings
		strongminstr = str(strongmin)
		strongmaxstr = str(strongmax)
		# Create a tuple for joining with units info
		strongtuple = (strongmaxstr, strongminstr)
		strongx = "-".join(strongtuple)
		strongy = strongx, units

		# Get heavy dose info
		heavy = doses["heavy"]
		# Convert int to str
		heavystr = str(heavy)
		heavyf = heavystr, units

		#	Duration Data Gathering
		duration = subs["roas"][0]["duration"]

		afterglow = duration["afterglow"]
		if afterglow == None:
			afterglow = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			afterglow = afterglow
		afterglowmin = afterglow["min"]
		afterglowmax = afterglow["max"]
		afterglowunit = afterglow["units"]
		afterglowminstr = str(afterglowmin)
		afterglowmaxstr = str(afterglowmax)
		afterglowtuple1 = (afterglowminstr, afterglowmaxstr)
		afterglowx = "-".join(afterglowtuple1)
		afterglowtuple2 = (afterglowx, afterglowunit)

		comeup = duration["comeup"]
		if comeup == None:
			comeup = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			comeup = comeup
		comeupmin = comeup["min"]
		comeupmax = comeup["max"]
		comeupunit = comeup["units"]
		comeupunit2 = "minutes"
		comeupminstr = str(comeupmin)
		comeupmaxstr = str(comeupmax)
		comeuptuple1 = (comeupminstr, comeupmaxstr)
		comeupx = "-".join(comeuptuple1)
		if comeupunit == None:
			comeuptuple2 = (comeupx, comeupunit2)
		else:
			comeuptuple2 = (comeupx, comeupunit)

		offset = duration["offset"]
		if offset == None:
			offset = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			offset = offset
		offsetmin = offset["min"]
		offsetmax = offset["max"]
		offsetunit = offset["units"]
		offminstr = str(offsetmin)
		offmaxstr = str(offsetmax)
		offtuple1 = (offminstr, offmaxstr)
		offsetx = "-".join(offtuple1)
		offtuple2 = (offsetx, offsetunit)

		onset = duration["onset"]
		if onset == None:
			onset = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			onset = onset
		onsetmin = onset["min"]
		onsetmax = onset["max"]
		onsetunit = onset["units"]
		onsetminstr = str(onsetmin)
		onsetmaxstr = str(onsetmax)
		ontuple1 = (onsetminstr, onsetmaxstr)
		onsetx = "-".join(ontuple1)
		ontuple2 = (onsetx, onsetunit)

		peak = duration["peak"]
		if peak == None:
			peak = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			peak = peak
		peakmin = peak["min"]
		peakmax = peak["max"]
		peakunit = peak["units"]
		peakminstr = str(peakmin)
		peakmaxstr = str(peakmax)
		peaktuple1 = (peakminstr, peakmaxstr)
		peakx = "-".join(peaktuple1)
		peaktuple2 = (peakx, peakunit)

		total = duration["total"]
		if total == None:
			total = {'min': 0, 'max': 0, 'units': 'Data not found'}
		else:
			total = total
		totalmin = total["min"]
		totalmax = total["max"]
		totalunit = total["units"]
		totalminstr = str(totalmin)
		totalmaxstr = str(totalmax)
		totaltuple1 = (totalminstr, totalmaxstr)
		totalx = "-".join(totaltuple1)
		totaltuple2 = (totalx, totalunit)


	# Create pretty embed
	embed=discord.Embed(title=name, description=summ, url=link, color=0x00ff00)
	embed.add_field(name="-", value="-----------------", inline=False)
	embed.add_field(name="Dosage", value=method, inline=False)
	embed.add_field(name="Threshold", value=" ".join(thresholdf), inline=True)
	embed.add_field(name="Light", value=" ".join(lighty), inline=True)
	embed.add_field(name="Common", value=" ".join(commony), inline=True)
	embed.add_field(name="Strong", value=" ".join(strongy), inline=True)
	embed.add_field(name="Heavy", value=" ".join(heavyf), inline=True)
	embed.add_field(name="-", value="-----------------", inline=False)
	embed.add_field(name="Duration", value="common durations", inline=False)
	embed.add_field(name="Onset", value=" ".join(ontuple2), inline=True)
	embed.add_field(name="Comeup", value=" ".join(comeuptuple2), inline=True)
	embed.add_field(name="Peak", value=" ".join(peaktuple2), inline=True)
	embed.add_field(name="Offset", value=" ".join(offtuple2), inline=True)
	embed.add_field(name="Total", value=" ".join(totaltuple2), inline=True)
	embed.add_field(name="After effects", value=" ".join(afterglowtuple2), inline=True)
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