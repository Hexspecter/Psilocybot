import random
import json

class Tools:
    def tox_fix(tox):
        if tox:
            return "\n".join(str(x).capitalize() for x in tox)
        else:
            return "No data"
            
    def combo_fix(combos):
        if combos:
            return "\n".join(f"- {str(x)}" for x in [d['name'] for d in combos])
        else:
            return "- No data"

    def class_fix(s_class):
        if s_class:
            return s_class[0].replace('_', ' ').capitalize()
        else:
            return "No data"

    def roas_fix(roas):
        durations = f""
        doses = f""
        if len(roas) == 1:
            temp_dur_text = f""
            temp_dose_text = f""
            name = roas[0]['name'].capitalize()
            dose = Tools.dose_fix(roas[0]['dose'])
            if roas[0]['duration']:
                duration = Tools.duration_fix(roas[0]['duration'])
            if not roas[0]['duration']:
                duration = "- No data"
            temp_dose_text += f"**{name} dose:**\n```\n{dose}```"
            temp_dur_text += f"**{name} duration:**\n```\n{duration}```"
            doses += f"{temp_dose_text}"
            durations += f"{temp_dur_text}"
        if len(roas) > 1:
            for item in roas:
                temp_dur_text = f""
                temp_dose_text = f""
                name = item['name'].capitalize()
                dose = Tools.dose_fix(item['dose'])
                if item['duration']:
                    duration = Tools.duration_fix(item['duration'])
                if not item['duration']:
                    duration = "- No data"
                temp_dose_text += f"**{name} dose:**\n```\n{dose}```"
                temp_dur_text += f"**{name} duration:**\n```\n{duration}```"
                doses += f"{temp_dose_text}"
                durations += f"{temp_dur_text}"
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
        if crosstol:
            return "\n".join(f"- {str(x).capitalize()}" for x in crosstol)
        else:
            return "- No data"
