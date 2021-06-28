import discord
import requests
import json
from discord.ext import commands
from json_tools import Cleaner_tools

class Substance_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['dosage', 'drugs', 'drug', 'substance'])
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
        # pretty_name = tripsit_data['data'][0]['pretty_name']
        pretty_name = s_data['name']
        url = s_data['url']
        summary = tripsit_data['data'][0]['properties']['summary']
        if 'links' in tripsit_data['data'][0]:
            experiences = tripsit_data['data'][0]['links']['experiences']
        else:
            experiences = "No data"
        if 'formatted_effects' in tripsit_data['data'][0]:
            effects = Cleaner_tools.Tools.effects_fix(tripsit_data['data'][0]['formatted_effects'])
        else:
            effects = "**Effects**\n```\n- No data```"
        s_tox = Cleaner_tools.Tools.tox_fix(s_data['toxicity'])
        if s_data['tolerance'] != None:
            if 'full' in s_data['tolerance'] and s_data['tolerance']['full'] != None:
                t_full = s_data['tolerance']['full'].capitalize()
            if 'half' in s_data['tolerance'] and s_data['tolerance']['half'] != None:
                t_half = s_data['tolerance']['half'].capitalize()
            if 'zero' in s_data['tolerance'] and s_data['tolerance']['zero'] != None:
                t_zero = s_data['tolerance']['zero'].capitalize()
            if 'full' in s_data['tolerance'] and s_data['tolerance']['full'] == None:
                t_full = "No data"
            if 'half' in s_data['tolerance'] and s_data['tolerance']['half'] == None:
                t_half = "No data"
            if 'zero' in s_data['tolerance'] and s_data['tolerance']['zero'] == None:
                t_zero = "No data"
        if s_data['tolerance'] == None:
            t_full = "No data"
            t_half = "No data"
            t_zero = "No data"
        crosstol = Cleaner_tools.Tools.crosstol_fix(s_data['crossTolerances'])
        categories = "\n".join(f"- {str(x).capitalize()}" for x in tripsit_data['data'][0]['categories'])
        c_chemical = Cleaner_tools.Tools.class_fix(s_data['class']['chemical'])
        c_psychoactive = Cleaner_tools.Tools.class_fix(s_data['class']['psychoactive'])
        roas_fixed = Cleaner_tools.Tools.roas_fix(s_data['roas'])
        doses = roas_fixed[0]
        durations = roas_fixed[1]
        c_uncertain = Cleaner_tools.Tools.combo_fix(s_data['uncertainInteractions'])
        c_unsafe = Cleaner_tools.Tools.combo_fix(s_data['unsafeInteractions'])
        c_dangerous = Cleaner_tools.Tools.combo_fix(s_data['dangerousInteractions'])
        if s_data['addictionPotential'] != None:
            addictivity = s_data['addictionPotential'].capitalize()
        if s_data['addictionPotential'] == None:
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

def setup(bot):
    bot.add_cog(Substance_commands(bot))
