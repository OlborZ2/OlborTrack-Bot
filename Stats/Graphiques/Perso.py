from matplotlib import pyplot as plt
import pandas as pd
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.DichoTri import triPeriod
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.VoiceAxe import voiceAxe
from Core.Fonctions.TempsVoice import formatCount
colorOT=(110/256,200/256,250/256,1)
dictNameAxis={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Mentions":"Mentions","Mentionne":"Mentions","Divers":"Nombre","Voice":"Temps en vocal","Voicechan":"Temps en vocal"}

def graphPerso(ligne,ctx,option,bot,period,guildOT,categ,curseur):
    author,nomTable=ligne["AuthorID"],ligne["AuthorID"]
    if ligne["Args1"]!="None":
        nomTable="{0}{1}".format(ligne["AuthorID"],ligne["Args1"])
    plt.subplots(figsize=(6.4,4.8))
    theme=setThemeGraph(plt)
    if period=="mois":
        table=triPeriod(curseur,"persoM{0}".format(nomTable),"periodAsc")
    else:
        table=curseur.execute("SELECT * FROM persoA{0} WHERE Annee<>'GL' ORDER BY Annee ASC".format(nomTable)).fetchall()
    listeX,listeY=[],[]
    somme=0

    for i in table:
        dictX={"Compteur":"{0}e".format(i["Rank"]),"Rang":formatCount(option,i["Count"])}
        dictY={"Compteur":i["Count"],"Rang":i["Rank"]}
        listeX.append("{0}/{1} - {2}".format(i["Mois"],i["Annee"],dictX[categ]))
        listeY.append(dictY[categ])
    
    if ligne["Args1"]=="None":
        user=getNomGraph(ctx,bot,option,author)
        plus=""
    else:
        user=getNomGraph(ctx,bot,"Messages",author)
        plus="\n{0}".format(getNomGraph(ctx,bot,option,int(ligne["Args1"])))

    if categ=="Rang":
        label="Rang"
        labelx=dictNameAxis[option]
    else:
        label=dictNameAxis[option]
        labelx="Rang"
    
    voiceAxe(option,listeY,plt,"y")

    df=pd.DataFrame({'date': listeX, categ: listeY})
    
    if user==None:
        plt.plot('date', categ, data=df, linestyle='-', marker='o',color=colorOT)
        plt.title("Ancien membre - Périodes{0}".format(plus),fontsize=12)
    else:
        if option in ("Messages","Mots","Voice","Mentions","Mentionne"):
            plt.plot('date', categ, data=df, linestyle='-', marker='o',color=(user.color.r/256,user.color.g/256,user.color.b/256,1))
            plt.title("{0} - Périodes{1}".format(user.name,plus),fontsize=12)
        else:
            plt.plot('date', categ, data=df, linestyle='-', marker='o',color=colorOT)
            plt.title("{0} - Périodes{1}".format(user,plus),fontsize=12)
    
    for i in range(len(listeX)):
        plt.text(x=i, y=listeY[i], s=listeY[i],size=8) 

    for i in listeY:
        somme+=i
    dictColor={"light":"black","dark":"white"}
    df2=pd.DataFrame({'date': listeX, 'Moyenne': [somme/len(table) for i in range(len(listeX))]})
    plt.plot("date","Moyenne",data=df2, linestyle="--", color=dictColor[theme],label="Moyenne ({0})".format(round(somme/len(table),2)))
    plt.legend()
    plt.xlabel("Date - {0}".format(labelx))
    if categ=="Rang":
        plt.ylabel(categ)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()