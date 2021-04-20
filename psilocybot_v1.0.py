import discord
import random
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Init bot prefix and remove default help command
bot = commands.Bot(command_prefix='>', help_command=None)

# coroutines for dose command json sorting etc; messy :'D
class Tools:
	def tox_fix(tox):
		if tox != None:
			return "\n".join(str(x).capitalize() for x in tox)
		if tox == None:
			return "No data"
	def combo_fix(combos):
		if combos != None:
			return "\n".join(f"- {str(x)}" for x in [d['name'] for d in combos])
		if combos == None:
			return "- No data"
	def class_fix(s_class):
		if s_class != None:
			return s_class[0].replace('_', ' ').capitalize()
		if s_class == None:
			return "No data"
	def roas_fix(roas):
		durations = f""
		doses = f""
		if len(roas) == 1:
			temp_dur_text1 = f""
			temp_dose_text1 = f""
			name1 = roas[0]['name'].capitalize()
			dose1 = Tools.dose_fix(roas[0]['dose'])
			if roas[0]['duration'] != None:
				duration1 = Tools.duration_fix(roas[0]['duration'])
			if roas[0]['duration'] == None:
				duration1 = "- No data"
			temp_dose_text1 += f"**{name1} dose:**\n```\n{dose1}```"
			temp_dur_text1 += f"**{name1} duration:**\n```\n{duration1}```"
			doses += f"{temp_dose_text1}"
			durations += f"{temp_dur_text1}"
		if len(roas) == 2:
			temp_dur_text1 = f""
			temp_dur_text2 = f""
			temp_dose_text1 = f""
			temp_dose_text2 = f""
			name1 = roas[0]['name'].capitalize()
			name2 = roas[1]['name'].capitalize()
			dose1 = Tools.dose_fix(roas[0]['dose'])
			dose2 = Tools.dose_fix(roas[1]['dose'])
			if roas[0]['duration'] != None:
				duration1 = Tools.duration_fix(roas[0]['duration'])
			if roas[0]['duration'] == None:
				duration1 = "- No data"
			if roas[1]['duration'] != None:
				duration2 = Tools.duration_fix(roas[1]['duration'])
			if roas[1]['duration'] == None:
				duration2 = "- No data"
			temp_dose_text1 += f"**{name1} dose:**\n```\n{dose1}```"
			temp_dose_text2 += f"**{name2} dose:**\n```\n{dose2}```"
			temp_dur_text1 += f"**{name1} duration:**\n```\n{duration1}```"
			temp_dur_text2 += f"**{name2} duration:**\n```\n{duration2}```"
			doses += f"{temp_dose_text1}\n{temp_dose_text2}"
			durations += f"{temp_dur_text1}\n{temp_dur_text2}"
		if len(roas) == 3:
			temp_dur_text1 = f""
			temp_dur_text2 = f""
			temp_dur_text3 = f""
			temp_dose_text1 = f""
			temp_dose_text2 = f""
			temp_dose_text3 = f""
			name1 = roas[0]['name'].capitalize()
			name2 = roas[1]['name'].capitalize()
			name3 = roas[2]['name'].capitalize()
			dose1 = Tools.dose_fix(roas[0]['dose'])
			dose2 = Tools.dose_fix(roas[1]['dose'])
			dose3 = Tools.dose_fix(roas[2]['dose'])
			if roas[0]['duration'] != None:
				duration1 = Tools.duration_fix(roas[0]['duration'])
			if roas[0]['duration'] == None:
				duration1 = "- No data"
			if roas[1]['duration'] != None:
				duration2 = Tools.duration_fix(roas[1]['duration'])
			if roas[1]['duration'] == None:
				duration2 = "- No data"
			if roas[2]['duration'] != None:
				duration3 = Tools.duration_fix(roas[2]['duration'])
			if roas[2]['duration'] == None:
				duration3 = "- No data"
			temp_dose_text1 += f"**{name1} dose:**\n```\n{dose1}```"
			temp_dose_text2 += f"**{name2} dose:**\n```\n{dose2}```"
			temp_dose_text3 += f"**{name3} dose:**\n```\n{dose3}```"
			temp_dur_text1 += f"**{name1} duration:**\n```\n{duration1}```"
			temp_dur_text2 += f"**{name2} duration:**\n```\n{duration2}```"
			temp_dur_text3 += f"**{name3} duration:**\n```\n{duration3}```"
			doses += f"{temp_dose_text1}\n{temp_dose_text2}\n{temp_dose_text3}"
			durations += f"{temp_dur_text1}\n{temp_dur_text2}\n{temp_dur_text3}"
		return doses, durations
	def dose_fix(dose):
		dosage_fix = f""
		for dosage in dose:
			no_string = ['units', 'threshold', 'heavy']
			if dosage in no_string and dosage != 'units':
				dosage_fix += f"{dosage.capitalize()}:\n- {dose[dosage]} {dose['units']}\n\n"
			if dosage not in no_string and dosage != 'units':
				dosage_fix += f"{dosage.capitalize()}:\n- {dose[dosage]['min']}-{dose[dosage]['max']} {dose['units']}\n\n"
		return dosage_fix
	def duration_fix(durations):
		durations_fix = f""
		for time in durations:
			if durations[time] != None:
				durations_fix += f"{time.capitalize()}:\n- {durations[time]['min']}-{durations[time]['max']} {durations[time]['units']}\n\n"
			if durations[time] == None:
				durations[time] = "No data"
				durations_fix += f"{time.capitalize()}:\n- {durations[time]}\n\n"
		return durations_fix
	def effects_fix(effects):
		effect_fix_temp = f""
		for effect in effects:
			if effect != '':
				if effect.endswith('itchiness'):
					effect1 = effect.split(' ')[-1:][0].capitalize()
					effect2 = " ".join(effect.split(' ')[:-1]).capitalize()
					effect_fix_temp += f"- {effect1}\n"
					effect_fix_temp += f"- {effect2}\n"
				else:
					effect_fix_temp += f"- {effect.capitalize()}\n"
		effect_fix = f"**Effects:**\n```\n{effect_fix_temp}```"
		return effect_fix
	def crosstol_fix(crosstol):
		if crosstol != None:
			return "\n".join(f"- {str(x).capitalize()}" for x in crosstol)
		if crosstol == None:
			return "- No data"

# Commands start here
class commands():
	def __init__(self, bot):
		self.bot = bot
    
    # Define help menu, still gotta remake this at some point I guess
	@bot.command(aliases=['h', 'guide', 'info'])
	async def help(ctx):
		embed=discord.Embed(title="Commands and info", description="Information about the different commands and arguments", color=0xff00ff)
		embed.add_field(name="Information", value="This bot is using the Tripsit.me and Psychonautwiki APIs for searches and requires specific substance names.\nDatabases:\nhttps://drugs.tripsit.me/\nhttps://psychonautwiki.org/wiki/Main_Page", inline=False)
		embed.add_field(name=">dose", value="Prettified information for dose and summary\nAliases: dosage, drugs, drug, substance\nUsage: >dose Caffeine", inline=True)
		embed.add_field(name=">tripsitme", value="Searches info and dosage of a substance from Tripsit.me\nAliases: tripsit, ts, tsdose\nUsage: >tripsitme Caffeine", inline=True)
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
		embed.add_field(name='\u200b', value="Stealth commands\nStealth commands, duh.", inline=False)
		embed.add_field(name=">stealthtoke", value="Tags you and tells others you're about to smoke, aliases: stealthsmoke.", inline=True)
		embed.add_field(name=">stealthdab", value="Tags you and tells others you're about to do a dab, aliases: stealthoil.", inline=True)
		embed.add_field(name=">stealthshot", value="Tags you and tells others you're about to do a shot, aliases: stealthshotglass.", inline=True)
		embed.add_field(name=">stealthdrink", value="Tags you and tells others you're about to drink a lighter drink, aliases: stealthbeer, stealthcider, stealthwine.", inline=True)
		await ctx.send(embed=embed)

	# Fun commands! (Self-explanatory, really)
	@bot.command(aliases=['smoke'])
	async def toke(ctx):
		tokelist = (f"{ctx.message.author.mention} sparked up a joint, join and smoke with them!", f"{ctx.message.author.mention} grabbed their weed and smoked a bowl, join and smoke with them!", f"{ctx.message.author.mention} just lit up, join and smoke with them!")
		await ctx.send(random.choice(tokelist))
	@bot.command(aliases=['oil'])
	async def dab(ctx):
		await ctx.send(f"{ctx.message.author.mention} is about to heat up their nail or banger, join and dab with them!")
	@bot.command(aliases=['shotglass'])
	async def shot(ctx):
		await ctx.send(f"{ctx.message.author.mention} is about to take a shot, join and take a shot with them!")
	@bot.command(aliases=['beer', 'cider', 'wine', 'cheers'])
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
	@bot.command(aliases=['stealthbeer', 'stealthcider', 'stealthwine', 'stealthcheers'])
	async def stealthdrink(ctx):
		await ctx.send(f"{ctx.author.name} is cracking open a cold one, join them and crack open a cold one!")

	# Dose command
	@bot.command(aliases=['dosage', 'drugs', 'drug', 'substance'])
	async def dose(ctx, query: str):
		search = {'name': query}
		tripsit = requests.get('http://tripbot.tripsit.me/api/tripsit/getDrug', params=search)
		tripsit_data = tripsit.json()
		headers = {
			"accept-type": "application/json",
			"content-type": "application/json"
		}
		payload = {
		    "query": """
		{
			substances(query: "%s") {
				name
				url
				tolerance {
					full
		      		half
					zero
				}
				class {
					chemical
					psychoactive
				}
				roas {
					name
					dose {
						units
						threshold
						light { min max }
						common { min max }
						strong { min max }
						heavy
					}
					duration {
						comeup { min max units }
						onset { min max units }
						peak { min max units }
						offset { min max units }
						total { min max units }
						afterglow { min max units }
					}
				}
				toxicity
				addictionPotential
				crossTolerances
				uncertainInteractions {
					name
				}
				unsafeInteractions {
					name
				}
				dangerousInteractions {
					name
				}
			}
		}
			""" % query
		}
		json_payload = json.dumps(payload)
		api = requests.post("https://api.psychonautwiki.org/?",data=json_payload,headers=headers)
		pswapi = api.json()
		s_data = pswapi['data']['substances'][0]
		pretty_name = tripsit_data['data'][0]['pretty_name']
		url = s_data['url']
		summary = tripsit_data['data'][0]['properties']['summary']
		if 'links' in tripsit_data['data'][0]:
			experiences = tripsit_data['data'][0]['links']['experiences']
		else:
			experiences = "No data"
		effects = Tools.effects_fix(tripsit_data['data'][0]['formatted_effects'])
		s_tox = Tools.tox_fix(s_data['toxicity'])
		t_full = s_data['tolerance']['full'].capitalize()
		t_half = s_data['tolerance']['half'].capitalize()
		t_zero = s_data['tolerance']['zero'].capitalize()
		crosstol = Tools.crosstol_fix(s_data['crossTolerances'])
		categories = "\n".join(f"- {str(x).capitalize()}" for x in tripsit_data['data'][0]['categories'])
		c_chemical = Tools.class_fix(s_data['class']['chemical'])
		c_psychoactive = Tools.class_fix(s_data['class']['psychoactive'])
		roas_fixed = Tools.roas_fix(s_data['roas'])
		doses = roas_fixed[0]
		durations = roas_fixed[1]
		c_uncertain = Tools.combo_fix(s_data['uncertainInteractions'])
		c_unsafe = Tools.combo_fix(s_data['unsafeInteractions'])
		c_dangerous = Tools.combo_fix(s_data['dangerousInteractions'])
		addictivity = s_data['addictionPotential']
		embed2=discord.Embed(title=pretty_name, url=url, description=summary)
		embed2.set_author(name="-- Psilocybot --", url="https://github.com/Hexspecter/Psilocybot")
		embed2.add_field(name='\u200b', value=f"""**Experiences**\n{experiences}\n\n**Class**\n```\nChemical:\n- {c_chemical}\n\nPsychoactive:\n- {c_psychoactive}```\n\n**Toxicity**\n```\n{s_tox}```""", inline=False)
		embed2.add_field(name='\u200b', value=f"""{doses}""", inline=True)
		embed2.add_field(name='\u200b', value=f"""{durations}""", inline=True)
		embed2.add_field(name='\u200b', value=f"""**Interactions**\n```\nUncertain:\n{c_uncertain}\n\nUnsafe:\n{c_unsafe}\n\nDangerous:\n{c_dangerous}```""")
		embed2.add_field(name='\u200b', value="""**More information**""", inline=False)
		embed2.add_field(name='\u200b', value=f"""**Tolerance**\n```\nFull:\n{t_full}\n\nHalf:\n{t_half}\n\nZero:\n{t_zero}```\n**Crosstolerance**\n```\n{crosstol}```""", inline=True)
		embed2.add_field(name='\u200b', value=f"""**Categories**\n```\n{categories}```\n\n**Addictivity**\n```\n{addictivity.capitalize()}```""", inline=True)
		embed2.add_field(name='\u200b', value=f"""{effects}""", inline=True)
		await ctx.send(embed=embed2)

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

	@dose.error
	async def dose_error(ctx, error):
		if isinstance(error, commands.CommandInvokeError):
			await ctx.send("You don't even know what you're searching for. No drugs for you!\n(jk, but the databases are down \n or your command was probably wrong, try >help)")
	@tripsitme.error
	async def tripsitme_error(ctx, error):
		if isinstance(error, commands.CommandInvokeError):
			await ctx.send("You don't even know what you're searching for. No drugs for you!\n(jk, but your command was probably wrong, try >help)")

bot.run(TOKEN)
