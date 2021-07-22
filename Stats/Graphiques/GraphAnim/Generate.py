from time import time
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Stats.Graphiques.GraphAnim.Create import createDict, createEvol
from Stats.Graphiques.GraphAnim.Animate import animateGraph 
from matplotlib import animation
import discord
from Core.Fonctions.Embeds import exeErrorExcept
from Core.Fonctions.GraphTheme import setThemeGraph

dictNameX={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps"}
dictNameY={"Messages":"Membres","Salons":"Salons","Freq":"Heures","Mots":"Membres","Emotes":"Emotes","Reactions":"Réactions","Voice":"Membres","Voicechan":"Salons"}

def generatePlot(graph):
    listeL,listeY,listeC=[],[],[]
    for i in graph[0]:
        listeL.append(i["x"])
        listeY.append(i["y"])
        listeC.append(i["color"])
    return listeL,listeY,listeC


async def getGraph(ctx,bot,guildOT,option):
    try:
        import matplotlib.pyplot as plt
        setThemeGraph(plt)
        temps=time()
        try:
            mois,annee=getMois(ctx.args[1]),getAnnee(ctx.args[2])
            assert mois!=None
        except:
            raise AssertionError
        await ctx.send("Veuillez patienter, votre graphique arrive !")

        ligne={"Args1":mois,"Args2":annee}

        fig=plt.figure()
        
        data=createEvol(ctx,bot,guildOT,ligne,option)
        graphiqueOT=createDict(data,bot,ctx,option)
        
        zero=generatePlot(graphiqueOT)
        barcollection = plt.barh(zero[0],zero[1],color=zero[2],fill=True)
        plt.subplots_adjust(left=0.25)
        plt.xlabel(dictNameX[option])
        plt.ylabel(dictNameY[option])
        ranks=15 if len(graphiqueOT[0])>15 else len(graphiqueOT[0])
        plt.ylim(0.8,ranks+0.8)

        anim=animation.FuncAnimation(fig,animateGraph,repeat=False,blit=False,fargs=[ranks,barcollection,graphiqueOT,plt,option],frames=len(graphiqueOT)+100,interval=33)

        anim.save(filename='Graphs/mymovie{0}.mp4'.format(ctx.message.id),writer="ffmpeg")

        await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/mymovie{0}.mp4".format(ctx.message.id))) 
        await ctx.send(file=discord.File("Graphs/mymovie{0}.mp4".format(ctx.message.id)))
        await bot.get_channel(786175275418517554).send(time()-temps)  
    except AssertionError:
        await ctx.send("La période donnée n'est pas bonne.")
    except:
        embed=await exeErrorExcept(ctx,bot,ctx.args)
        await ctx.send(embed=embed)