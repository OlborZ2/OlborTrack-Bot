from Core.Reactions.ChangePage import reactStats
from Core.Reactions.Plus import reactPlus
from Core.Reactions.Tri import changeTri
from Core.Reactions.Mobile import changeMobile
from Core.Reactions.Graphiques import reactGraph
from Admin.DeleteStats import confirmDel
import discord
from discord.ext import commands
from Core.OTGuild import OTGuild
from Core.Fonctions.SeekMessage import seekMessage

async def exeReactOT(emoji:discord.Reaction, message:discord.Message, bot:commands.Bot, guildOT:OTGuild, payload):
    """En fonction de la réaction utilisée, dispatche vers quelle fonction se servir pour effectuer l'action."""
    
    if emoji.id in (772766034376523776,772766034335236127,772766034356076584,835930140571729941,835928773718835260,835928773740199936,835928773705990154,835928773726699520,835929144579326003,836947337808314389):
        await reactStats(message,emoji,bot,guildOT,payload)
    elif emoji.id==772766034558058506:
        await reactGraph(message,bot,guildOT,payload,emoji)
    elif emoji.id==772766034163400715:
        message,user=await seekMessage(bot,message)
        await reactPlus(message,user)
        await message.clear_reaction(emoji)
    elif emoji.id==833666016491864114:
        await changeTri(message,emoji,bot,guildOT,payload)
    elif emoji.id==833736320919797780:
        await changeMobile(message,emoji,bot,guildOT,payload)
    elif emoji.id==866705696505200691:
        ctx=await bot.get_context(message)
        await confirmDel(ctx,ctx.author,bot)
    else:
        return