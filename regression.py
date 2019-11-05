import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter
import matplotlib as mpl
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from dataExtract import *
from fontTools.ttLib import TTFont

#what is the current week of play in the league (1-17)
def week():
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})
	try:
		#API permission checker (subscription key)
	    conn = http.client.HTTPSConnection('api.fantasydata.net')
	    conn.request("GET",  "https://api.fantasydata.net/v3/nfl/stats/JSON/UpcomingWeek%s" % params, "{body}", headers)
	    response = conn.getresponse()
	    temp = response.read()
	    currWeek =  int(temp.decode("utf-8"))
	except Exception as e:
			print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return currWeek

#some code from: 
#https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#sphx-glr-auto-examples-linear-model-plot-ols-py
def regressionModel(name, stat):
	stats = getData(name, stat)
	weeks = []
	d = []
	for i in range(len(stats)):
		weeks.append([stats[i][1]])
		d.append(stats[i][0])
	y = np.array(d)
	y1 = y[:-4]
	y2 = y[-4:]
	x1 = weeks[:-4]
	x2 = weeks[-4:]

	#from tutorial
	regr = linear_model.LinearRegression()
	regr.fit(weeks, y)
	pred = regr.predict(weeks)
	print('Coefficients: \n', regr.coef_)
	print("Mean squared error: %.2f"
	      % mean_squared_error(y, pred))
	print('Variance score: %.2f' % r2_score(y, pred))
	return regr.coef_

#----------------------------------------------------------------------------------------------------------

#Machine Learning to get slope of regression line (will be used for projection). Code written by me but with
#some help from online sources(formula for error distances)

#print(getStats("Todd Gurley", "RB" ,["RushingYards", "RushingTouchdowns"]))
s = {'"RushingYards"': [[0, 0], [121.7, 1], [169.0, 2], [287.3, 3], [380.8, 4], [467.6, 5], [702.0, 6], [773.0, 7], [901.5, 8], [978.1, 9], [1113.3, 10], [1175.3, 11]], 
'"RushingTouchdowns"': [[0, 0], [0.0, 1], [3.4, 2], [4.5, 3], [4.5, 4], [7.9, 5], [10.2, 6], [12.5, 7], [12.5, 8], [13.6, 9], [14.7, 10], [14.7, 11]]}

d = [[0, 0], [121.7, 1], [169.0, 2], [287.3, 3], [380.8, 4], [467.6, 5], [702.0, 6], [773.0, 7], [901.5, 8], [978.1, 9], [1113.3, 10], [1175.3, 11]]

#get regression line for season long performance
def coeff(stat, s):
	stats = s
	x = []
	y = []
	for i in range(len(stats)):
		x.append(stats[i][1])
		y.append(stats[i][0])
	slope = 0
	intercept = 0
	change = 0.001
	oldErr = 0
	changeErr = 1
	while abs(changeErr) > 0.0001:
	    error = 0
	    slopeErr = 0
	    interceptErr = 0
	    for j in range(len(x)):
	        error += (slope * x[j] + intercept - y[j])**2
	        slopeErr += 2 * (slope * x[j] + intercept - y[j]) * x[j]
	    slope -= slopeErr * change
	    changeErr = error - oldErr
	    oldErr = error

	return slope

#get slope for recent performance
def recent(stat, s):
	stats = s
	rec = stats[-6:]
	x, y = [], []
	for i in range(len(rec)):
		x.append(rec[i][1])
		y.append(rec[i][0])
	slope = 0
	intercept = 0
	change = 0.001
	oldErr = 0
	changeErr = 1
	while abs(changeErr) > 0.000001:
	    error = 0
	    slopeErr = 0
	    interceptErr = 0
	    for j in range(len(x)):
	        error += (slope * x[j] + intercept - y[j])**2
	        slopeErr += 2 * (slope * x[j] + intercept - y[j]) * x[j]
	        interceptErr += 2 * (slope * x[j] + intercept - y[j]) * 1
	    slope -= slopeErr * change
	    intercept -= interceptErr * change
	    changeErr = error - oldErr
	    oldErr = error
	return slope, intercept

#draw scatter plot and regression line for recent performance (past 6 weeks)
def recentRegression(name, stat, s):
	f = recent(stat, s)
	stat = "\"" + stat + "\""
	reg = tkinter.Tk()
	fig = Figure(figsize=(6,6))
	d = s[-6:]
	slope, interp = f[0], f[1]
	x, v, p = [], [], []
	for i in range(len(d)):
		f = d[i]
		x.append([f[1]])
		v.append([f[0]])
	curr = 0
	for i in range(17):
		p.append([slope * i + interp])
		curr = i
	a = fig.add_subplot(111)
	a.scatter(x, v, color='black')
	a.set_xlim([x[0][0], 18])
	a.set_ylim([0, slope*30])
	a.plot(p,color='blue')
	a.set_title ("Recent Performance", fontsize=16)
	a.set_ylabel("Total " + stat[1:-1], fontsize=14)
	a.set_xlabel("Week", fontsize=14)
	legendLabel={"y = " +str(round(slope, 3))+"x + " + str(round(interp,3))}
	a.legend(legendLabel, fontsize = 10)
	canvas = FigureCanvasTkAgg(fig, master=reg)
	canvas.get_tk_widget().pack()
	canvas.draw()
	reg.mainloop()

#draw a scatterplot and regression line for full season
def myRegress(name, stat, s):
	x, v, p = [], [], [[0]]
	slope = coeff(stat, s)
	reg = tkinter.Tk()
	fig = Figure(figsize=(6,6))
	a = fig.add_subplot(111)
	for i in range(len(s)):
		v.append([s[i][0]])
		x.append([s[i][1]])
	for i in range(17):
		p.append([slope * (i+1)])
	
	a.scatter(x, v, color='black')
	a.set_xlim([0, 18])
	a.set_ylim([0, slope*20])
	a.plot(p,color='blue')
	a.set_title (name + " " + stat + " projection", fontsize=16)
	a.set_ylabel("Total " + stat, fontsize=14)
	a.set_xlabel("Week", fontsize=14)
	legendLabel={"y = " +str(round(slope, 3))+"x"}
	a.legend(legendLabel, fontsize = 10)
	canvas = FigureCanvasTkAgg(fig, master=reg)
	canvas.get_tk_widget().pack()
	canvas.draw()
	reg.mainloop()

#----------------------------------------------------------------------------------------------------------

import numpy as np
import sys
import tkinter as tk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

#draw_figure() is from: 
#https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_canvas_sgskip.html
def draw_figure(canvas, figure, loc=(0, 0)):
	figure_canvas_agg = FigureCanvasAgg(figure)
	figure_canvas_agg.draw()
	figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
	figure_w, figure_h = int(figure_w), int(figure_h)
	photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
	canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
	tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
	return photo

#get data from dataset
def extractData(stats, stat):
	weeks = []
	d = []
	for i in range(len(stats)):
		weeks.append([stats[i][1]])
		d.append(stats[i][0])
	return (weeks, d)

#graph points given, connect all points
def graph(name, stat, s):
	dat = extractData(s, stat)
	X = dat[0]
	Y = dat[1]
	w, h = 500, 500
	window = tk.Tk()
	window.title(name + ": " + stat)
	canvas = tk.Canvas(window, width=w, height=h)
	canvas.pack()

	new = mpl.figure.Figure(figsize=(4, 4))
	ax = new.add_axes([0, 0, 1, 1])
	ax.plot(X, Y)
	new.suptitle(name + " " + stat, fontsize=10)
	newX, newY = 50, 50
	newPhoto = draw_figure(canvas, new, loc=(newX, newY))
	tk.mainloop()

#----------------------------------------------------------------------------------------------------------

#get the team of a player based on name and position
def getTeam(name, position, data):
	first = ""
	last = ""
	index = name.index(" ")
	first = name[0] + "."
	last = name[index+1:]
	name = first+last
	for player in data.decode("utf-8").split("\"PlayerID\""):
		p = player[1:]
		for s in p.split(','):
			if "\"Team\"" in s:
				team = s[8:-1]
			if "\"Name\"" in s:
				key = s[8:-1]
				if key == name:
					return team
	return None

#team's opponent for a given week
def opponent(team, week, d):
	curr = 0
	home = "" 
	away = ""
	for game in d.decode("utf-8").split("\"GameKey\""):
		g = game[1:]
		for s in g.split(','):
			if "\"Week\"" in s:
				key = s[7:]
				curr = int(key)
			if curr == week:
				if "\"HomeTeam\"" in s:
					t = s[12: -1]
					home = t
				elif "\"AwayTeam\"" in s:
					t = s[12: -1]
					away = t
		if home == team:
			return away
		elif away == team:
			return home
	return None

#get player matchup
def getMatchup(player, position):
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})
	try:
		#API permission checker (subscription key)
	    conn = http.client.HTTPSConnection('api.fantasydata.net')
	    conn.request("GET",  "/v3/nfl/stats/JSON/SeasonLeagueLeaders/2018/" + position + "/Touchdowns%s" % params, "{body}", headers)
	    response = conn.getresponse()
	    data = response.read()
	    conn.request("GET",  "https://api.fantasydata.net/v3/nfl/stats/JSON/Schedules/2018%s" % params, "{body}", headers)
	    response = conn.getresponse()
	    schedule = response.read()
	    conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
	count = 0	
	his = getTeam(player, position, data)
	matchup = opponent(his, week(), schedule)
	return matchup

#get full defensive stats
def defenseStats(defense):
	relevantStats = {"\"OpponentPassingTouchdowns\"": 0, "\"OpponentPassingYards\"": 0, "\"OpponentPasserRating\"": 0, 
		"\"OpponentRushingTouchdowns\"": 0, "\"OpponentRushingYardsPerAttempt\"": 0, "\"OpponentRushingYards\"": 0}
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})
	try:
		#API permission checker (subscription key)
	    conn = http.client.HTTPSConnection('api.fantasydata.net')
	    conn.request("GET", "/v3/nfl/stats/JSON/TeamSeasonStats/2018?%s" % params, "{body}", headers)
	    response = conn.getresponse()
	    data = response.read()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
	extract = False
	for team in data.decode("utf-8").split("\"Season\""): #fix
		for s in team.split(","):
			if "\"Team\"" in s:
				p = s[8: -1]
				if p == defense:
					extract = True
				else:
					extract = False
			if extract:
				for stat in relevantStats:
					if stat in s:
						num = ""
						for char in s:
							if char.isdigit() or char == ".":
								num += char
						relevantStats[stat] += float(num)
	return relevantStats


#got these from using the above function except adding all teams together and dividing accordingly to get
#average and per week average
nflTotal = {'"OpponentPassingTouchdowns"': 685.0, '"OpponentPassingYards"': 97806.0, '"OpponentPasserRating"': 3355.10, 
'"OpponentRushingTouchdowns"': 325.0, '"OpponentRushingYardsPerAttempt"': 158.50, '"OpponentRushingYards"': 44554.0}

nflAvg = {'"OpponentPassingTouchdowns"': 21.406, '"OpponentPassingYards"': 3056.438, '"OpponentPasserRating"': 104.847, 
'"OpponentRushingTouchdowns"': 10.156, '"OpponentRushingYardsPerAttempt"': 4.953, '"OpponentRushingYards"': 1392.3125}

nflPerWeekAvg = {'"OpponentPassingTouchdowns"': 1.946, '"OpponentPassingYards"': 277.858, '"OpponentPasserRating"': 104.847, 
'"OpponentRushingTouchdowns"': 0.923, '"OpponentRushingYardsPerAttempt"': 4.953, '"OpponentRushingYards"': 126.574}

#weekly stats
def weekly(team):
	stats = defenseStats(team)
	final = {}
	for i in stats:
		if i != '"OpponentPasserRating"' and i != '"OpponentRushingYardsPerAttempt"':
			final[i] = stats[i]/(12-1)
		else: final[i] = stats[i]
	return final

#percentage compared to league average
def percentage(team):
	stats = weekly(team)
	average = nflPerWeekAvg
	percent = {}
	for i in stats:
		percent[i] = [(stats[i]-average[i])/average[i]*100, average[i]]
	return percent

#get team rank vs each category
def rank(team):
	passing, rushing = 0, 0
	perf = percentage(team)
	for i in perf:
		l = perf[i]
		if "Pass" in i:
			passing += l[0]
		if "Rush" in i:
			rushing += l[0]
	return round(passing, 3), round(rushing, 3)


teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL',
'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LAC', 'LAR', 'MIA', 'MIN',
'NE', 'NO', 'NYG', 'NYJ', 'OAK', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN',
'WAS']

# ranking = {}
# for i in teams:
# 	ranking[i] = rank(i)
# print(ranking)

ranking ={'ARI': (-23.271, 109.177), 'ATL': (52.636, 63.077), 'BAL': (-55.378, -40.571), 'BUF': (-58.285, 21.977), 
'CAR': (41.297, -32.727), 'CHI': (-24.563, -105.93), 'CIN': (56.417, 85.966), 'CLE': (-3.055, 83.972), 
'DAL': (-26.722, -62.943), 'DEN': (8.282, 5.179), 'DET': (43.529, -0.135), 'GB': (-5.362, 18.678), 
'HOU': (-8.967, -77.75), 'IND': (-0.026, -25.84), 'JAX': (-50.772, 5.223), 'KC': (18.303, 55.599), 
'LAC': (-32.183, -44.215), 'LAR': (39.685, 14.492), 'MIA': (9.428, 31.987), 'MIN': (-48.813, -72.793), 
'NE': (14.01, -53.921), 'NO': (30.537, -43.736), 'NYG': (-26.901, 42.765), 'NYJ': (-7.401, 33.267), 
'OAK': (40.796, 54.126), 'PHI': (3.414, 1.757), 'PIT': (-3.88, -25.824), 'SEA': (-10.632, 27.653), 
'SF': (24.5, -29.072), 'TB': (72.805, 58.673), 'TEN': (-20.961, -6.767), 'WAS': (-1.757, -15.32)}

#plot all defensive teams based on strength vs pass and strength vs rush
#highlight given team
def plot(team):
	reg = tkinter.Tk()
	x, y = [],[]
	fig = Figure(figsize=(6,6))
	a = fig.add_subplot(111)
	for i in ranking:
		coord = ranking[i]
		if i == team:
			color = 'black'
		else:
			if -(coord[1] + coord[0]) > 75: color = 'green'
			elif -(coord[1] + coord[0]) < -20: color = 'red'
			else: color = 'blue'
		x = np.array([-coord[0]])
		v = np.array([-coord[1]])
		a.scatter(x, v, color=color)
	a.set_title ("Defensive Matchup Ranking", fontsize=16)
	a.set_ylabel("Strength Against the Rush", fontsize=14)
	a.set_xlabel("Strength Against the Pass", fontsize=14)
	canvas = FigureCanvasTkAgg(fig, master=reg)
	canvas.get_tk_widget().pack()
	canvas.draw()
	reg.mainloop()


def distance(team):
	coord = rank(team)
	disX = coord[0]
	disY = coord[1]
	strength = -(disX + disY)/(abs(disX + disY))
	distance = (disX**2 + disY**2)**0.5
	return distance * strength


# ratings = {}
# for i in teams:
# 	ratings[i] = round(distance(i), 3)

# print(ratings)

ratings = {'ARI': -111.63, 'ATL': -82.154, 'BAL': 68.649, 'BUF': 62.291, 'CAR': -52.692, 'CHI': 108.741, 'CIN': -102.825, 
'CLE': -84.028, 'DAL': 68.38, 'DEN': -9.768, 'DET': -43.529, 'GB': -19.432, 'HOU': 78.265, 'IND': 25.84, 'JAX': 51.04, 
'KC': -58.534, 'LAC': 54.687, 'LAR': -42.248, 'MIA': -33.347, 'MIN': 87.644, 'NE': 55.711, 'NO': 53.342, 'NYG': -50.522, 
'NYJ': -34.08, 'OAK': -67.779, 'PHI': -3.84, 'PIT': 26.114, 'SEA': -29.626, 'SF': 38.019, 'TB': -93.504, 'TEN': 22.026, 
'WAS': 15.42}
# sortedRating = []
# while len(sortedRating) < len(ratings):
# 	largest = -99999
# 	team = ""
# 	for i in ratings:
# 		if ratings[i] > largest and i not in sortedRating:
# 			largest = ratings[i]
# 			team = i
# 	sortedRating.append(team)
# print(sortedRating)
sortedRating = [['CHI',"Chicago Bears"], ['MIN', "Minnesota Vikings"], ['HOU', "Houston Texans"], ['BAL', "Baltimore Ravens"],
['DAL',"Dallas Cowboys"], ['BUF', "Buffalo Bills"], ['NE', "New England Patriots"], ['LAC', "Los Angeles Chargers"],
['NO', "New Orleans Saints"], ['JAX', "Jaxonville Jaguars"], ['SF', "San Fransisco 49ers"], ['PIT', "Pittsburgh Steelers"],
['IND', "Indianapolis Colts"], ['TEN', "Tennessee Titans"], ['WAS', "Washington Redskins"], ['PHI', "Philadelphia Eagles"], 
['DEN', "Denver Broncos"], ['GB', "Green Bay Packers"], ['SEA', "Seattle Seahawks"], ['MIA', "Miami Dolphins"],
['NYJ', "New York Jets"], ['LAR', "Los Angeles Rams"], ['DET', "Detroits Lions"], ['NYG', "New York Giants"], ['CAR', "Carolina Panthers"],
['KC', "Kansas City Chiefs"], ['OAK', "Oakland Raiders"], ['ATL', "Atlanta Falcons"], ['CLE', "Cleveland Browns"], 
['TB', "Tampa Bay Buccaneers"], ['CIN', "Cincinnati Bengals"], ['ARI', "Arizona Cardinals"]]
#rating scale is -120 to 120


#----------------------------------------------------------------------------------------------------------
from SeasonLeadersAPI import *

importantStats = ["PassingYards", "PassingTouchdowns", "RushingYards", "RushingTouchdowns", "Receptions", "ReceivingYards", "ReceivingTouchdowns"]
#get player's "value" based on performance
def value(stats):
	final = 0
	largest = 0
	pos = ""
	for i in stats:
		if "PassingYards" in i:
			final += stats[i]*0.025
			if stats[i]>largest:
				largest = stats[i]
				pos = i
		elif "RushingYards" in i or "ReceivingYards" in i:
			final += stats[i]*0.1
			if stats[i]>largest:
				largest = stats[i]
				pos = i
		elif "PassingTouchdowns" in i:
			final += stats[i]*4
			if stats[i]>largest:
				largest = stats[i]
				pos = i
		elif "RushingTouchdowns" in i or "ReceivingTouchdowns" in i:
			final += stats[i]*6
			if stats[i]>largest:
				largest = stats[i]
				pos = i

	if "Receiving" in pos:
		pos = "WR/TE"
		value = ((final - 30)/30 * 100)/5
	elif "Passing" in pos:
		pos = "QB"
		value = ((final - 70)/70 * 100)/5
	else:
		pos = "RB"
		value = ((final - 40)/40 * 100)/5

	return round(value, 3)

#compare value of 2 sets of players
def comparison(a, b):
	final1, final2 = [], []
	for player in a:
		s = getSeasonData(player[0], player[1], importantStats)
		final1.append(value(s))
	for player in b:
		s = getSeasonData(player[0], player[1], importantStats)
		final2.append(value(s))

	return final1, final2
