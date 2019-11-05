from tkinter import *
import os
import requests
import random
from io import BytesIO
import tkinter.messagebox
from PIL import Image, ImageTk
from fontTools.ttLib import TTFont

from FantasyData import *
from testImage import *
from regression import * 
from SeasonLeadersAPI import *
from dataExtract import *

#subscription keys for API. if quota is reached, switch key in code
#3cb884984b2141418eb885eb4809ea54 - test key
#43e46bd398a440c5a79007ac86b86d6f - final key
#9a14edc80cec45c09540a835dd539b37 - backup key

importantStats = ["PassingYards", "PassingTouchdowns", "RushingYards", "RushingTouchdowns", "Receptions", "ReceivingYards", "ReceivingTouchdowns"]
abbreviations = ['PassYd', 'PassTD', 'RushYd', 'RushTD', 'Rec', 'RecYd', 'RecTD', 'Proj']

#creating the main UI
def UI():
    #creating a projection based on stats and matchup information
    def projection(stats, matchup):
        final = 0
        strength = ranking[matchup]
        passRank = strength[0]
        rushRank = strength[1]
        for i in stats:
            s = stats[i]
            n = i[1:-1]
            if "PassingYards" in i:
                rec = recent(n, s)
                final += 0.025*((coeff(n, s)+rec[0])/2)*(1+passRank/150)
            elif "PassingTouchdowns" in i:
                rec = recent(n, s)
                final += 4*((coeff(n, s)+rec[0])/2)*(1+passRank/150)
            elif "ReceivingTouchdown" in i:
                rec = recent(n, s)
                final += 6*((coeff(n, s)+rec[0])/2)*(1+passRank/150)
            elif "ReceivingYards" in i:
                rec = recent(n, s)
                final += 0.1*((coeff(n, s)+rec[0])/2)*(1+passRank/150)
            elif "RushingTouchdown" in i:
                rec = recent(n, s)
                final += 6*((coeff(n, s)+rec[0])/2)*(1+rushRank/150)
            elif "RushingYards" in i:
                rec = recent(n, s)
                final += 0.1*((coeff(n, s)+rec[0])/2)*(1+rushRank/150)
        return round(final, 2)

    #creating the lineup window
    def lineup(qb, rb1, rb2, wr1, wr2, te):
        infont = "Dual"   
        #event for when the user clicks on the label to open the options window        
        def mouseClick(eff, name, stat, stats):
            new = Toplevel()
            new.title("Which display?")
            new.geometry('300x200')
            #when the user chooses which graph to display, it will open it accordingly
            def submit():
                if choice.get() == 'Graph':
                    graph(name, stat, stats)
                elif choice.get() == "Regression":
                    myRegress(name, stat, stats)
                elif choice.get() == "Recent":
                    recentRegression(name, stat, stats)
            #when the user chooses which graph to display, it will open it accordingly
            def choose(value):
                if value == 'Stats Graph':
                    graph(name, stat, stats)
                elif value == "Regression Plot":
                    myRegress(name, stat, stats)
                elif value == "Recent Regression Plot":
                    recentRegression(name, stat, stats)
            choice = Entry(new)
            choice.config(font = (infont, 30), relief=RIDGE)
            choice.place(x = 0, y = 100, width = 300, height = 50)

            one = Label(new, text = "Choices: Regression, Recent, Graph")
            one.config(font = (infont, 15))
            one.place(x = 0, y = 0, width = 300, height = 25)
            two = Label(new, text = "Or Enter Choice")
            two.config(font = (infont, 15))
            two.place(x = 0, y = 75, width = 300, height = 25)

            but = Button(new, text = "submit", command = submit)
            but.config(font = (infont, 15 ))
            but.place(x = 100, y =175, width = 100, height = 25)

            options = tk.StringVar()
            dropMenu1 = OptionMenu(new, options, "Regression Plot", "Stats Graph", "Recent Regression Plot", command = choose)
            dropMenu1.place(x=0, y=25, width = 300, height = 25)
            options.set('Choose')
            new.mainloop()

        font = "SIMPLIFICA"
        window = Toplevel()
        window.title("Your team")
        window.geometry('1665x590')
        bgColor = "gray13"
        textColor = "sea green"
        inputColor = "light salmon"

        inputs = {"Quarterback: ": [qb, 'QB'], "Runningback 1: ": [rb1, 'RB'], "Runningback 2:": [rb2, 'RB'], "Wide Receiver 1:" : [wr1, 'WR'], 
                "Wide Receiver 2:": [wr2, 'WR'], "Tight End:": [te, 'TE']}
        players = []
        for i in inputs:
            players.append(inputs[i][0])

        #this is extracting all the stats that are needed for the projection
        holder = {}
        stats = [[],[],[],[],[],[]]
        stat1, stat2, stat3, stat4, stat5, stat6 = stats[0], stats[1], stats[2], stats[3], stats[4], stats[5]
        URLs = getURL(players)
        print("Loading stats....")
        wr = getPositionStats("WR")
        print("	1/4")
        rb = getPositionStats("RB")
        print("	2/4")
        qb = getPositionStats("QB")
        print("	3/4")
        te = getPositionStats("TE")
        print("	4/4")
        print("Loaded!")
        count = 0
        matchups = {}
        for key in inputs:
            temp = {}
            info = inputs[key]
            player = info[0]
            position = info[1]
            if position == "WR": data = wr
            elif position == "RB": data = rb
            elif position == "QB": data = qb
            elif position == "TE": data = te
            x = getSeasonData(player, position, importantStats)
            for i in x:
                stats[count].append(x[i])
            projData = extract(player, position, importantStats, data)
            m = getMatchup(player, position)
            matchups[player] = m
            holder[player] = projData
            stats[count].append([projection(projData, m)])
            count += 1

        #Here it has gotten all the data and is working on displaying it for the user
        print("Displaying!")
        left = Label(window, text="Lineup", bg = bgColor, fg = "white")
        left.config(font=(font, 40))
        left.place(x = 0, y = 0, width=200, height=50)
        right = Label(window, text="Player", bg = bgColor, fg = "white")
        right.config(font=(font, 40))
        right.place(x = 200, y = 0, width=250, height=50)
        right = Label(window, text="Opp", bg = bgColor, fg = "white")
        right.config(font=(font, 40))
        right.place(x = 450, y = 0, width=50, height=50)
        right = Label(window, text="ID", bg = bgColor, fg = "white")
        right.config(font=(font, 40))
        right.place(x = 500, y = 0, width=65, height=50)
        for i in range(len(abbreviations)):
            l = Label(window, text = abbreviations[i], bg = bgColor, fg = 'white')
            l.config(font=(font, 40))
            l.place(x = 565+140*i, y = 0, width=140, height=50)

        count = 0
        images = []
        for i in inputs:
            intro = i
            into = inputs[i]
            player = into[0]
            url = URLs[player]
            URL = url.replace("\\", "")
            response = requests.get(URL)
            img = Image.open(BytesIO(response.content), 'r')
            bg = Image.open('bg2.jpg', 'r')
            bg = bg.resize((65, 90), Image.ANTIALIAS)
            #create clearer image (next 3 lines), got from: https://stackoverflow.com/questions/38627870/
            #how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white/38629258
            finalImg = Image.new('RGBA', (65,90), (0, 0, 0, 0))
            finalImg.paste(bg, (0,0))
            finalImg.paste(img, (0,0), mask=img)
            photoImg =  ImageTk.PhotoImage(finalImg)
            l1 = Label(window, image=photoImg)
            l1.image = photoImg
            l1.place(x = 500, y = 50+90*(count), width = 65, height = 90)

            left = Label(window, text=intro, bg = bgColor, fg = textColor)
            left.config(font=(font, 40))
            left.place(x = 0, y = 50 + 90*(count), width=200, height=90)
            right = Label(window, text=player, bg = bgColor, fg = inputColor)
            right.config(font=(font, 40))
            right.place(x = 200, y = 50 + 90*(count), width=250, height=90)
            right = Label(window, text=matchups[player], bg = bgColor, fg = "MediumPurple1")
            right.config(font=(font, 25))
            right.place(x = 450, y = 50 + 90*(count), width=50, height=90)

            for i in range(len(stats[count])):
                nums = stats[count]
                w = holder[player]
                s = Label(window, text =nums[i], bg = bgColor, fg = 'orange red')
                s.config(font=(font,40))
                if i <= 6:
                    x1 = importantStats[i]
                    x = "\"" + x1 + "\""
                    y = w[x]
                    s.bind( "<Button-1>", lambda eff = None, name = player, stat = x1, stats = y: mouseClick(eff, name, stat, stats))
                s.place(x = 565+140*i, y = 50 + 90*(count), width = 150, height = 90)
            count += 1


        # quit = Button(window, text='Finish', command=window.destroy, font=(font, 20), fg = bgColor)
        # quit.place(x=10, y=10, width = 40, height = 20)

    #this screen appears when the lineup is not fully inputted
    def errorScreen(dic):
        font = "Hero Light"
        err = Tk()
        err.title("INVALID INPUT")
        error = []
        for i in dic:
            if dic[i] == "":
                error.append(i)

        s = "Positions you are missing: "
        for j in error:
            s += "\n" + j

        l = Label(err, text=s)
        l.config(font = (font, 15))
        l.grid(row=0)
        Button(err, text='OK', command=err.destroy, font = (font, 15)).grid(row=6, column=0, sticky=S, pady=4)

    #this is the initial input screen with buttons for exitting, submitting, and menu
    def startScreen():
        font = "Hero Light"
        infont = "Hero Light"
        #checking to see if the lineup has been inputted correctly and passes the information on to be displayed
        def showEntry():
            for i in [QB.get(), RB1.get(), RB2.get(), WR1.get(), WR2.get(), TE.get()]:
                #find a way to check if player exists in player database
                if i == "":
                    d = {"Quarterback": QB.get(), "Runningback 1": RB1.get(), "Runningback 2": RB2.get(), 
                        "Wide Receiver 1": WR1.get(), "Wide Receiver 2": WR2.get(), "Tight End": TE.get()}
                    errorScreen(d)
                    return
            lineup(QB.get(), RB1.get(), RB2.get(), WR1.get(), WR2.get(), 
                TE.get())
        print("Initializing...")
        s = topWeeklyPlayers(week())
        s2 = topSeasonPlayers()
        print("Ready!")
        #the menu with the additional features
        def menu():
            #this is the weekly ranking system
            def weekRanking(event):
                choice2 = Toplevel()
                choice2.geometry("250x100")
                choice2.title("Input position")
                #shows ranking based on inputted position
                def show():
                    disp = Toplevel()
                    disp.geometry("300x625")
                    disp.title("Weekly Top 25")
                    d = dataSort(s, enter.get())
                    count = 1
                    colors = ["medium orchid", "green yellow", "gold", "coral", "orange red"]
                    for i in d:
                        if count <= 25:
                            l = str(count) + ". " + i
                            label = Label(disp, text = l, bg = "grey13", fg = colors[(count-1)//5])
                            label.config(font = (font, 20), anchor = "w")
                            label.place(x=0, y=25*(count-1), width = 250, height = 25)
                            label2 = Label(disp, text = str(d[i]), bg = "grey13", fg = colors[(count-1)//5])
                            label2.config(font = (font, 20), anchor = "w")
                            label2.place(x=250, y=25*(count-1), width = 75, height = 25)
                            count += 1
                enter = Entry(choice2)
                enter.focus()
                enter.config(font = (font, 30))
                enter.place(x = 0, y = 25, width = 250, height = 50)
                l = Label(choice2, text = "Choices: QB, RB, WR, TE")
                l.config(font = (font, 15))
                l.place(x = 0, y = 0, width = 250, height = 25)
                Button(choice2, text = "submit", command = show, font = (font, 15)).place(x = 0, y = 75, width = 250, height = 25)

            #this is the season-long ranking system
            def seasonRanking(event):
                choice2 = Toplevel()
                choice2.geometry("250x100")
                choice2.title("Input position")
                #shows ranking based on inputted position
                def show():
                    disp = Toplevel()
                    disp.geometry("315x625")
                    disp.title("Season Top 25")
                    d = dataSort(s2, enter.get())
                    count = 1
                    colors = ["medium orchid", "green yellow", "gold", "coral", "orange red"]
                    for i in d:
                        if count <= 25:
                            l = str(count) + ". " + i
                            label = Label(disp, text = l, bg = "grey13", fg = colors[(count-1)//5])
                            label.config(font = (font, 20), anchor = "w")
                            label.place(x=0, y=25*(count-1), width = 250, height = 25)
                            label2 = Label(disp, text = str(d[i]), bg = "grey13", fg = colors[(count-1)//5])
                            label2.config(font = (font, 20), anchor = "w")
                            label2.place(x=250, y=25*(count-1), width = 75, height = 25)
                            count += 1
                enter = Entry(choice2)
                enter.focus()
                enter.config(font = (font, 30))
                enter.place(x = 0, y = 25, width = 250, height = 50)
                l = Label(choice2, text = "Choices: QB, RB, WR, TE")
                l.config(font = (font, 15))
                l.place(x = 0, y = 0, width = 250, height = 25)
                Button(choice2, text = "submit", command = show, font = (font, 15)).place(x = 0, y = 75, width = 250, height = 25)

            #trade function that takes a trade and shows which team gains more from the trade
            def trade(event):
                choice2 = Toplevel()
                choice2.geometry("450x525")
                choice2.title("Input trade")
                #analyze the players inputted and show the value and trade status
                #positive values represent value above league average, negative values represent value below league average
                def tradeAnalyzer():
                    disp = Tk()
                    disp.geometry('500x450')
                    disp.config(bg = "gray45")
                    a, b = [], []
                    for i in range(len(entry1)):
                        if entry1[i][0].get() != '':
                            a.append([entry1[i][0].get(),entry1[i][1].get()])
                        if entry2[i][0].get() != '':
                            b.append([entry2[i][0].get(), entry2[i][1].get()])
                    teams = comparison(a, b)
                    a1 = teams[0]
                    a2 = teams[1]
                    total1, total2 = sum(a1), sum(a2)

                    teamA = Label(disp, text = "Team A gives:", bg = "gray45", fg = "black")
                    teamA.config(font = (font, 20), anchor = 'w')
                    teamA.place(x = 0, y = 10, width = 500, height = 25)
                    for i in range(len(a)):
                        one = Label(disp, text = a[i][0] + ", Value: " + str(a1[i]), bg = "gray45", fg = "white")
                        one.config(font = (font, 30), anchor = 'w')
                        one.place(x = 0, y = 35 + 50*i, width = 500, height = 50)

                    teamB = Label(disp, text = "Team B gives:", bg = "gray45", fg = "black")
                    teamB.config(font = (font, 20), anchor = 'w')
                    teamB.place(x = 0, y = 200, width = 500, height = 25)
                    for i in range(len(b)):
                        two = Label(disp, text = b[i][0] + ", Value: " + str(a2[i]), bg = "gray45", fg = "white")
                        two.config(font = (font, 30), anchor = 'w')
                        two.place(x = 0, y = 225 + 50*i, width = 500, height = 50)

                    if total1 > total2:
                        winner = Label(disp, text = "Team B should make this trade!", bg = "gray45", fg = "spring green")
                        winner.config(font = (font, 25), anchor = 'w')
                        winner.place(x = 0, y = 375, width = 500, height = 50)
                    elif total1 < total2:
                        winner = Label(disp, text = "Team A should make this trade!", bg = "gray45", fg = "spring green")
                        winner.config(font = (font, 25), anchor = 'w')
                        winner.place(x = 0, y = 375, width = 500, height = 50)
                    else:
                        winner = Label(disp, text = "It's a wash!", bg = "gray45", fg = "spring green")
                        winner.config(font = (font, 25), anchor = 'w')
                        winner.place(x = 0, y = 375, width = 500, height = 50)


                title = Label(choice2, text = "Enter potential trade")
                title.config(font = (font, 25))
                title.place(x=0, y=0, width = 450, height = 25)

                team1 = Label(choice2, text = "Team 1")
                team1.config(font = (font, 15), anchor = 'w')
                team1.place(x = 0, y = 30, width = 400, height = 25)

                pos1 = Label(choice2, text = "Pos.")
                pos1.config(font = (font, 15), anchor = 'w')
                pos1.place(x = 400, y = 30, width = 50, height = 25)
                
                entry1 = []
                for i in range(3):
                    enter = Entry(choice2)
                    enter.config(font = (font, 30))
                    enter.place(x = 0, y = 55+50*i, width = 400, height = 50)
                    pos = Entry(choice2)
                    pos.config(font = (font, 20))
                    pos.place(x = 400, y = 55+50*i, width = 50, height = 50)
                    entry1.append([enter, pos])
                img = Image.open('trade.png')
                img = img.resize((100,100), Image.ANTIALIAS)
                bg = Image.open('bg2.jpg', 'r')
                bg = bg.resize((100,100), Image.ANTIALIAS)
                finalImg = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
                finalImg.paste(bg, (0,0))
                finalImg.paste(img, (0,0), mask=img)
                photoImg =  ImageTk.PhotoImage(finalImg)
                l1 = Label(choice2, image=photoImg)
                l1.image = photoImg
                l1.place(x = 175, y = 210)
                team2 = Label(choice2, text = "Team 2")
                team2.config(font = (font, 15), anchor = 'w')
                team2.place(x = 0, y = 315, width = 400, height = 25)
                pos2 = Label(choice2, text = "Pos.")
                pos2.config(font = (font, 15), anchor = 'w')
                pos2.place(x = 400, y = 315, width = 50, height = 25)
                entry2 = []
                for i in range(3):
                    enter = Entry(choice2)
                    enter.config(font = (font, 30))
                    enter.place(x = 0, y = 340+50*i, width = 400, height = 50)
                    pos = Entry(choice2)
                    pos.config(font = (font, 20))
                    pos.place(x = 400, y =340+50*i, width = 50, height = 50)
                    entry2.append([enter, pos])
                Button(choice2, text = "submit", command = tradeAnalyzer, font = (font, 15)).place(x = 175, y = 500, width = 75, height = 25)

            #shows strength of each defense in the league on a plot and in a ranking
            def defensePlot(event):
                choice2 = Toplevel()
                choice2.geometry("325x100")
                choice2.title("Input defense")
                #displays everything to the user
                def show():
                    two = Toplevel()
                    two.geometry("315x800")
                    two.title("Defensive Rankings")
                    count = 1
                    colors = ["green yellow", "gold", "coral", "orange red"]
                    back = "grey13"
                    for i in range(len(sortedRating)):
                        if count <= 32:
                            l = str(count) + ". " + sortedRating[i][1]
                            if sortedRating[i][0] == enter.get() or sortedRating[i][1] == enter.get(): 
                                back = "black"
                                team = sortedRating[i][0]
                            else: back = "grey13"
                            label = Label(two, text = l, bg = back, fg = colors[(count-1)//8])
                            label.config(font = (font, 20), anchor = "w")
                            label.place(x=0, y=25*(count-1), width = 315, height = 25)
                            count += 1
                    plot(team)

                enter = Entry(choice2)
                enter.focus()
                enter.config(font = (font, 30))
                enter.place(x = 0, y = 25, width = 325, height = 50)
                l = Label(choice2, text = "Please enter a team name or abbreviation")
                l.config(font = (font, 15))
                l.place(x = 0, y = 0, width = 325, height = 25)
                Button(choice2, text = "submit", command = show, font = (font, 15)).place(x = 0, y = 75, width = 325, height = 25)

            #player comparison based on how the system thinks each player will perform
            def whoDoIStart(event):
                choice2 = Toplevel()
                choice2.geometry('450x250')
                choice2.title("Compare Players")
                #take projections and see which player is expected to perform better
                def compare():
                    disp = Toplevel()
                    disp.geometry('550x250')
                    disp.config(bg = "gray45")
                    one = [enter.get(), pos.get()]
                    two = [enter2.get(), pos2.get()]
                    print("Comparing players...")
                    oneData = getStats(one[0], one[1], importantStats)
                    oneMatch = getMatchup(one[0], one[1])
                    twoData = getStats(two[0], two[1], importantStats)
                    twoMatch = getMatchup(two[0], two[1])
                    proj = [[enter.get(), projection(oneData, oneMatch), oneMatch], [enter2.get(), projection(twoData, twoMatch), twoMatch]]
                    print("Done!")

                    for i in range(len(proj)):
                        pl = proj[i]
                        one = Label(disp, text = pl[0] + " vs " + pl[2] + " : " + str(pl[1]) + " points", bg = "gray45", fg = "white")
                        one.config(font = (font, 30), anchor = 'w')
                        one.place(x = 0, y = 10 + 75*i, width = 550, height = 50)

                    if proj[0][1] > proj[1][1]:
                        one = Label(disp, text = "You should start " + proj[0][0] + "!", bg = "gray45", fg = "spring green")
                        one.config(font = (font, 30), anchor = 'w')
                        one.place(x = 0, y = 175, width = 550, height = 50)
                    else:
                        one = Label(disp, text = "You should start \n" + proj[1][0] + "!", bg = "gray45", fg = "spring green")
                        one.config(font = (font, 30), anchor = 'c')
                        one.place(x = 0, y = 175, width = 550, height = 75)


                title = Label(choice2, text = "Enter Two Players")
                title.config(font = (font, 25))
                title.place(x=0, y=0, width = 450, height = 25)

                team1 = Label(choice2, text = "Player 1")
                team1.config(font = (font, 15), anchor = 'w')
                team1.place(x = 0, y = 30, width = 400, height = 25)
                pos1 = Label(choice2, text = "Pos.")
                pos1.config(font = (font, 15), anchor = 'w')
                pos1.place(x = 400, y = 30, width = 50, height = 25)
                enter = Entry(choice2)
                enter.config(font = (font, 30))
                enter.place(x = 0, y = 55, width = 400, height = 50)
                pos = Entry(choice2)
                pos.config(font = (font, 20))
                pos.place(x = 400, y = 55, width = 50, height = 50)


                team2 = Label(choice2, text = "Player 2")
                team2.config(font = (font, 15), anchor = 'w')
                team2.place(x = 0, y = 125, width = 400, height = 25)
                pos2 = Label(choice2, text = "Pos.")
                pos2.config(font = (font, 15), anchor = 'w')
                pos2.place(x = 400, y = 125, width = 50, height = 25)
                enter2 = Entry(choice2)
                enter2.config(font = (font, 30))
                enter2.place(x = 0, y = 150, width = 400, height = 50)
                pos2 = Entry(choice2)
                pos2.config(font = (font, 20))
                pos2.place(x = 400, y = 150, width = 50, height = 50)


                Button(choice2, text = "submit", command = compare, font = (font, 15)).place(x = 175, y = 215, width = 75, height = 25)

            men = Toplevel()
            men.geometry("365x750")
            men.title("Menu")
            men.config(bg = "SlateBlue4")
            options = ["Season Rankings", "Weekly Rankings", "Trade Analyzer", "Defense Rankings", "Who do I start?"]
            images = ["trend.png", "trend.png", "swap.png", "defense.png", "question.jpg"]
            for i in range(len(options)):
                x = Label(men, text = options[i], bg = "SlateBlue4", fg = "white", anchor = "w")
                x.config(font=(font, 30))
                x.place(x=85, y = 600/4*i, width = 300, height = 150)
                img = Image.open(images[i], 'r')
                img = img.resize((50, 57), Image.ANTIALIAS)
                bg = Image.open('purp.png', 'r')
                bg = bg.resize((50, 57), Image.ANTIALIAS)
                finalImg = Image.new('RGBA', (50, 60), (0, 0, 0, 0))
                finalImg.paste(bg, (0,0))
                finalImg.paste(img, (0,0), mask=img)
                photoImg =  ImageTk.PhotoImage(finalImg)
                l1 = Label(men, image=photoImg, bg = "SlateBlue4")
                l1.image = photoImg
                l1.place(x = 20, y = 150*i, width = 50, height = 150)
                if i == 0: 
                    x.bind("<Button-1>", seasonRanking)
                    l1.bind("<Button-1>", seasonRanking)
                elif i == 1: 
                    x.bind("<Button-1>", weekRanking)
                    l1.bind("<Button-1>", weekRanking)
                elif i == 2: 
                    x.bind("<Button-1>", trade)
                    l1.bind("<Button-1>", trade)
                elif i == 3: 
                    x.bind("<Button-1>", defensePlot)
                    l1.bind("<Button-1>", defensePlot)
                else:
                    x.bind("<Button-1>", whoDoIStart)
                    l1.bind("<Button-1>", whoDoIStart)


        #when enter is pressed, attempt to submit 
        def key(event):
            if repr(event.char) == "\'\\r\'":
                show_entry_fields()
            else: print(repr(event.char))

        #when clicked focus on the frame
        def callback(event):
            frame.focus_set()

        back = "papayawhip"
        master = Tk()
        master.title("Input your team")
        master.geometry('560x680')
        master.config(padx = 30, pady = 30)
        frame = Frame(master, width=520, height=620)
        frame.bind("<Key>", key)
        frame.bind("<Button-1>", callback)
        frame.pack()

        #create start screen UI
        words = ["Quarterback:", "Runningback 1:", "Runningback 2:","Wide Receiver 1:","Wide Receiver 2:", "Tight End:"]
        for i in range(6):
            t = words[i]
            Label(master, text = t, font = (font, 20), anchor = W).place(x = 0, y = 15+100*i, width = 500, height = 50)

        quit = Button(master, text='Exit', font = (font, 15), command=master.quit, fg="red").place(x = 20, y = 0, width = 50)
        show = Button(master, text='Show', font = (font, 15), command=showEntry, fg="green").place(x = 430, y = 0, width = 50)
        menu = Button(master, text='Menu', font = (font, 15), command=menu, fg="blue").place(x = 230, y = 0, width = 50)

        QB = Entry(master)
        QB.focus()
        QB.config(font = (infont, 30), relief=RIDGE)
        QB.place(x = 0, y = 50, width = 500, height = 50)
        RB1 = Entry(master)
        RB1.config(font = (infont, 30), relief=RIDGE)
        RB1.place(x = 0, y = 150, width = 500, height = 50)
        RB2 = Entry(master)
        RB2.config(font = (infont, 30), relief=RIDGE)
        RB2.place(x = 0, y = 250, width = 500, height = 50)
        WR1 = Entry(master)
        WR1.config(font = (infont, 30), relief=RIDGE)
        WR1.place(x = 0, y = 350, width = 500, height = 50)
        WR2 = Entry(master)
        WR2.config(font = (infont, 30), relief = RIDGE)
        WR2.place(x = 0, y = 450, width = 500, height = 50)
        TE = Entry(master)
        TE.config(font = (infont, 30), relief = RIDGE)
        TE.place(x = 0, y = 550, width = 500, height = 50)

        master.mainloop( )

    startScreen()

UI()


