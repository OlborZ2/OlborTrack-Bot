from time import strftime

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import addtoFields, countRankCompare, createFields, embedAssert, sendEmbed
from Core.Fonctions.GetNom import getObj, nomsOptions
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Verification import verifCommands

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO","GL":"GL"}
dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC"}
dictTriField={"countAsc":"Compteur {0}/{1} croissant","countDesc":"Compteur {0}/{1} décroissant"}

async def comparePerso(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            liste=[]
            args=ctx.args[2:len(ctx.args)]
            connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
            while len(args)!=0 and len(liste)<2:
                detectPeriod(args,liste,curseur)
            assert len(liste)==2
            assert liste[0]!=liste[1]
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'comparePerso','{2}','{3}','{4}','None','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,liste[0],liste[1]))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()

        liste1=ligne["Args1"].split(" ")
        liste2=ligne["Args2"].split(" ")
        connexion1,curseur1=connectSQL(ctx.guild.id,option,"Stats",liste1[0],liste1[1])
        connexion2,curseur2=connectSQL(ctx.guild.id,option,"Stats",liste2[0],liste2[1])
        pagemax=setMax(curseur1.execute("SELECT COUNT() as Nombre FROM perso{0}{1}{2}".format(liste1[0],liste1[1],ligne["AuthorID"])).fetchone()["Nombre"])
        page=setPage(ligne["Page"],pagemax,turn)
        
        embed=embedCompare(liste1,liste2,option,curseur1,curseur2,ligne,page,guildOT,bot)
        user=ctx.guild.get_member(ligne["AuthorID"])
        if user!=None:
            embed=auteur(user.id,user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur(bot.user.id,"Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498db
        embed.title="Comparaison perso, entre {0}/{1} et {2}/{3}\n{4}".format(liste1[0],liste1[1],liste2[0],liste2[1],option)
        embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[ligne["Tri"]].format(liste1[0],liste1[1]),inline=True)
        embed.set_footer(text="Page {0}/{1}".format(page,pagemax))

        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
    except:
        if react:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe plus."))
        else:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe pas.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))
        

def detectPeriod(args,liste,curseur):
    if args[0].lower()=="mois":
        liste.append("{0} {1}".format(strftime("%m"),strftime("%y"))) 
    elif args[0].lower()=="annee":
        liste.append("TO {0}".format(strftime("%y"))) 
    elif args[0].lower()=="global":
        liste.append("TO GL") 
    else:
        try:
            assert curseur.execute("SELECT * FROM firstA WHERE Annee='{0}'".format(getAnnee(args[0]))).fetchone()!=None
            liste.append("TO {0}".format(getAnnee(args[0])))
        except:
            try:
                assert curseur.execute("SELECT * FROM firstM WHERE Mois='{0}' AND Annee='{1}'".format(tableauMois[getMois(args[0].lower())],getAnnee(args[1]))).fetchone()!=None
                liste.append("{0} {1}".format(tableauMois[getMois(args[0].lower())],getAnnee(args[1])))
                del args[1]
            except:
                pass
    del args[0]

def embedCompare(liste1,liste2,option,curseur1,curseur2,ligne,page,guildOT,bot):
    embed=discord.Embed()
    field1,field2,field3="","",""
    tri=ligne["Tri"]
    mobile=ligne["Mobile"]
    table=curseur1.execute("SELECT * FROM perso{0}{1}{2} ORDER BY {3} {4}".format(liste1[0],liste1[1],ligne["AuthorID"],dictTriArg[tri],dictTriSens[tri])).fetchall()
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        nom=nomsOptions(option,table[i]["ID"],guildOT,bot)
        table2=curseur2.execute("SELECT * FROM perso{0}{1}{2} WHERE ID={3}".format(liste2[0],liste2[1],ligne["AuthorID"],table[i]["ID"])).fetchone()
        rang1,rang2,count1,count2=countRankCompare(table,table2,i,option,guildOT)
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nom,"{0} | {1}".format(rang1,count1),"{0} | {1}".format(rang2,count2))

    embed=createFields(mobile,embed,field1,field2,field3,option,"{0}/{1}".format(liste1[0],liste1[1]),"{0}/{1}".format(liste2[0],liste2[1]))
    return embed