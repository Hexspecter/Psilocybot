# Psilocybot
Small and simple Discord bot for pulling harm reduction information from Tripsit.me and PsychonautWiki APIs

You have to replace few variables in the `commands` folder to get the fork owner ID to proper place

The files in question are:
* `psi_admintools.py`
* `psi_substance.py`

## First major overhaul version!
Moved things into classes, changed into cogs and added dev commands for reloading the entire commands folder without having to take the bot offline!

Cleaner output embeds implemented as well, with better API handling (still not perfect, have to edit the entire tools class to be clearer and have less variables)


## Commands
* **Useful commands**
  * `>help`
  * Gives short help of the commands
  * `>dose substance`
  * Gives prettified dosage information
  * and general information about substance

### To do:
- [x] Create code for pulling information from Psychonaut wiki API
- [x] Create prettier menus
- [x] Add commands for usage methods
- [x] Create additional "fun" commands, such as toke, dab, drink, shot etc.
- [ ] Add changeable prefix
