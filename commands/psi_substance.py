import discord
import aiohttp
import asyncio
import json
from discord.ext import commands
from json_tools import Cleaner_tools

owner_discord = "replace with your Discord tag"

class Substance_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(aliases=['dosage', 'drugs', 'drug', 'substance'])
    async def dose(self, ctx, query: str):
        search = {'name': query}
        header = {
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
        dumped_payload = json.dumps(payload)
        api_url = "https://api.psychonautwiki.org/?"
        api2_url = "http://tripbot.tripsit.me/api/tripsit/getDrug?"
        async with self.session.post(api_url, data=dumped_payload, headers=header) as resp:
            content = await resp.json()
        async with self.session.get(api2_url, params=search) as tripsit:
            tripsit_content = await tripsit.json()
        subs_data = content['data']['substances'][0]
        pretty_name = subs_data['name']
        url = subs_data['url']
        summary = tripsit_content['data'][0]['properties']['summary']
        t_full = "No data"
        t_half = "No data"
        t_zero = "No data"
        if 'links' in tripsit_content['data'][0]:
            experiences = tripsit_content['data'][0]['links']['experiences']
        else:
            experiences = "No data"
        if 'formatted_effects' in tripsit_content['data'][0]:
            effects = Cleaner_tools.Tools.effects_fix(tripsit_content['data'][0]['formatted_effects'])
        else:
            effects = "**Effects**\n```\n- No data```"
        s_tox = Cleaner_tools.Tools.tox_fix(subs_data['toxicity'])
        if subs_data['tolerance']:
            if 'full' in subs_data['tolerance'] and subs_data['tolerance']['full']:
                t_full = subs_data['tolerance']['full'].capitalize()
            if 'half' in subs_data['tolerance'] and subs_data['tolerance']['half']:
                t_half = subs_data['tolerance']['half'].capitalize()
            if 'zero' in subs_data['tolerance'] and subs_data['tolerance']['zero']:
                t_zero = subs_data['tolerance']['zero'].capitalize()
            if 'full' not in subs_data['tolerance']:
                t_full = "No data"
            if 'half' not in subs_data['tolerance']:
                t_half = "No data"
            if 'zero' not in subs_data['tolerance']:
                t_zero = "No data"
        if not subs_data['tolerance']:
            t_full = "No data"
            t_half = "No data"
            t_zero = "No data"
        crosstol = Cleaner_tools.Tools.crosstol_fix(subs_data['crossTolerances'])
        c_chemical = Cleaner_tools.Tools.class_fix(subs_data['class']['chemical'])
        c_psychoactive = Cleaner_tools.Tools.class_fix(subs_data['class']['psychoactive'])
        roas_fixed = Cleaner_tools.Tools.roas_fix(subs_data['roas'])
        doses = roas_fixed[0]
        durations = roas_fixed[1]
        c_uncertain = Cleaner_tools.Tools.combo_fix(subs_data['uncertainInteractions'])
        c_unsafe = Cleaner_tools.Tools.combo_fix(subs_data['unsafeInteractions'])
        c_dangerous = Cleaner_tools.Tools.combo_fix(subs_data['dangerousInteractions'])
        if subs_data['addictionPotential']:
            addictivity = subs_data['addictionPotential'].capitalize()
        if not subs_data['addictionPotential']:
            addictivity = "No data"
        embed2=discord.Embed(title=pretty_name, url=url, description=f"{summary}")
        embed2.set_author(name="-- Psilocybot --", url="https://github.com/Hexspecter/Psilocybot")
        embed2.add_field(name='\u200b', value=f"**Experiences**\n{experiences}", inline=False)
        embed2.add_field(name='\u200b', value=f"""**Class**\n```\nChemical:\n- {c_chemical}\n\nPsychoactive:\n- {c_psychoactive}```\n\n**Toxicity**\n```\n{s_tox}```""", inline=False)
        embed2.add_field(name='\u200b', value=f"""{doses}""", inline=True)
        embed2.add_field(name='\u200b', value=f"""{durations}""", inline=True)
        embed2.add_field(name='\u200b', value=f"""**Interactions**\n```\nUncertain:\n{c_uncertain}\n\nUnsafe:\n{c_unsafe}\n\nDangerous:\n{c_dangerous}```""")
        embed2.add_field(name='\u200b', value="""**More information**""", inline=False)
        embed2.add_field(name='\u200b', value=f"""**Tolerance**\n```\nFull:\n{t_full}\n\nHalf:\n{t_half}\n\nZero:\n{t_zero}```\n**Crosstolerance**\n```\n{crosstol}```""", inline=True)
        embed2.add_field(name='\u200b', value=f"""**Addictivity**\n```\n{addictivity}```""", inline=True)
        embed2.add_field(name='\u200b', value=f"""{effects}""", inline=True)
        await ctx.send(embed=embed2)

    @dose.error
    async def dose_error(self, ctx, error):
        if isinstance(error, Exception):
            print(error)
            embed=discord.Embed(title="Error or Bug found!", description="Whoops, something went wrong here")
            embed.add_field(name="Substance not found or databases down", value=f"Please ping {owner_discord} if problems persist and the substance can be found from PsychonautWiki", inline=False)
            embed.add_field(name="Please send this string when reporting an error", value=f"`Error message: {error}, raised by [{ctx.message.content}]`", inline=False)
            embed.add_field(name="Please don't try spamming the command", value="If the command gave this error, it's more than likely that the database is either down, or the substance was not found from the database", inline=False)
            await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Substance_commands(bot))
