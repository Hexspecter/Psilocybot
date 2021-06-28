import random
import json

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
        if len(roas) == 4:
            temp_dur_text1 = f""
            temp_dur_text2 = f""
            temp_dur_text3 = f""
            temp_dur_text4 = f""
            temp_dose_text1 = f""
            temp_dose_text2 = f""
            temp_dose_text3 = f""
            temp_dose_text4 = f""
            name1 = roas[0]['name'].capitalize()
            name2 = roas[1]['name'].capitalize()
            name3 = roas[2]['name'].capitalize()
            name4 = roas[3]['name'].capitalize()
            dose1 = Tools.dose_fix(roas[0]['dose'])
            dose2 = Tools.dose_fix(roas[1]['dose'])
            dose3 = Tools.dose_fix(roas[2]['dose'])
            dose4 = Tools.dose_fix(roas[3]['dose'])
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
            if roas[3]['duration'] != None:
                duration4 = Tools.duration_fix(roas[3]['duration'])
            if roas[3]['duration'] == None:
                duration4 = "- No data"
            temp_dose_text1 += f"**{name1} dose:**\n```\n{dose1}```"
            temp_dose_text2 += f"**{name2} dose:**\n```\n{dose2}```"
            temp_dose_text3 += f"**{name3} dose:**\n```\n{dose3}```"
            temp_dose_text4 += f"**{name4} dose:**\n```\n{dose4}```"
            temp_dur_text1 += f"**{name1} duration:**\n```\n{duration1}```"
            temp_dur_text2 += f"**{name2} duration:**\n```\n{duration2}```"
            temp_dur_text3 += f"**{name3} duration:**\n```\n{duration3}```"
            temp_dur_text4 += f"**{name4} duration:**\n```\n{duration4}```"
            doses += f"{temp_dose_text1}\n{temp_dose_text2}\n{temp_dose_text3}\n{temp_dose_text4}"
            durations += f"{temp_dur_text1}\n{temp_dur_text2}\n{temp_dur_text3}\n{temp_dur_text4}"
        if len(roas) == 5:
            temp_dur_text1 = f""
            temp_dur_text2 = f""
            temp_dur_text3 = f""
            temp_dur_text4 = f""
            temp_dur_text5 = f""
            temp_dose_text1 = f""
            temp_dose_text2 = f""
            temp_dose_text3 = f""
            temp_dose_text4 = f""
            temp_dose_text5 = f""
            name1 = roas[0]['name'].capitalize()
            name2 = roas[1]['name'].capitalize()
            name3 = roas[2]['name'].capitalize()
            name4 = roas[3]['name'].capitalize()
            name5 = roas[4]['name'].capitalize()
            dose1 = Tools.dose_fix(roas[0]['dose'])
            dose2 = Tools.dose_fix(roas[1]['dose'])
            dose3 = Tools.dose_fix(roas[2]['dose'])
            dose4 = Tools.dose_fix(roas[3]['dose'])
            dose5 = Tools.dose_fix(roas[4]['dose'])
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
            if roas[3]['duration'] != None:
                duration4 = Tools.duration_fix(roas[3]['duration'])
            if roas[3]['duration'] == None:
                duration4 = "- No data"
            if roas[4]['duration'] != None:
                duration5 = Tools.duration_fix(roas[4]['duration'])
            if roas[4]['duration'] == None:
                duration5 = "- No data"
            temp_dose_text1 += f"**{name1} dose:**\n```\n{dose1}```"
            temp_dose_text2 += f"**{name2} dose:**\n```\n{dose2}```"
            temp_dose_text3 += f"**{name3} dose:**\n```\n{dose3}```"
            temp_dose_text4 += f"**{name4} dose:**\n```\n{dose4}```"
            temp_dose_text5 += f"**{name5} dose:**\n```\n{dose5}```"
            temp_dur_text1 += f"**{name1} duration:**\n```\n{duration1}```"
            temp_dur_text2 += f"**{name2} duration:**\n```\n{duration2}```"
            temp_dur_text3 += f"**{name3} duration:**\n```\n{duration3}```"
            temp_dur_text4 += f"**{name4} duration:**\n```\n{duration4}```"
            temp_dur_text5 += f"**{name5} duration:**\n```\n{duration5}```"
            doses += f"{temp_dose_text1}\n{temp_dose_text2}\n{temp_dose_text3}\n{temp_dose_text4}\n{temp_dose_text5}"
            durations += f"{temp_dur_text1}\n{temp_dur_text2}\n{temp_dur_text3}\n{temp_dur_text4}\n{temp_dur_text5}"
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