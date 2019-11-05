import json
import requests


#gets the stats of each player's past fantasy performances (season points and weekly points)

def topWeeklyPlayers(week):
	URL = "http://api.fantasy.nfl.com/v1/players/stats?statType=seasonStats&season=2018&week=" + str(week) + "&format=json"
	data = requests.get(URL).json()
	# print(data)
	qb = dict()
	rb = dict()
	wr = dict()
	te = dict()

	for position in [["RB", 9, rb], ["WR", 8, wr], ["QB", 14, qb], ["TE", 3, te]]:
		for s in data["players"]:
			pos = position[0]
			threshold = position[1]
			d = position[2]
			if "name" in s:
				if s['position'] == pos:
					if s['weekProjectedPts'] >= threshold:
						d[s['name']] = s['weekProjectedPts']
						tabs = ((20 - len(s['name'])) // 4) + 2
	return (qb, rb, wr, te)

def topSeasonPlayers():
	rankqb = dict()
	rankrb = dict()
	rankwr = dict()
	rankte = dict()
	URL = "http://api.fantasy.nfl.com/v1/players/stats?statType=seasonStats&season=2018&week=13&format=json"
	data = requests.get(URL).json()
	for position in [["RB", 50, rankrb], ["WR", 50, rankwr], ["QB", 75, rankqb], ["TE", 20, rankte]]:
		for s in data["players"]:
			pos = position[0]
			threshold = position[1]
			d = position[2]
			if "name" in s:
				if s['position'] == pos:
					if s['seasonPts'] >= threshold:
						d[s['name']] = str(s["seasonPts"])
						tabs = ((20 - len(s['name'])) // 4) + 2

	return (rankqb, rankrb, rankwr, rankte)

def dataSort(s, position):
	pos = ['QB', 'RB', "WR", "TE"]
	rank = {}
	i = pos.index(position)
	d = s[i]
	while len(rank) < len(d):
		largest = 0
		name = ""
		for i in d:
			if float(d[i]) > largest and i not in rank:
				name = i
				largest = float(d[i])
		rank[name] = largest

	return rank
