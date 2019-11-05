import http.client, urllib.request, urllib.parse, urllib.error, base64

#gets dictionary to rank players based on certain stat category

def getPositionLeaders(position, stat):
	stats = "\"" + stat + "\""
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})
	try:
		#API permission checker (subscription key)
	    conn = http.client.HTTPSConnection('api.fantasydata.net')
	    url = "/v3/nfl/stats/JSON/SeasonLeagueLeaders/2018/" + position + "/Touchdowns%s"
	    conn.request("GET",  url % params, "{body}", headers)
	    response = conn.getresponse()
	    data = response.read()
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))


	d = dict()
	count = 0
	count1 = 0
	value = ""
	for player in data.decode("utf-8").split("\"PlayerID\""):
		p = player[1:]
		for s in p.split(','):
			if "\"Name\"" in s:
				key = s[8:-1]
				d[count] = [key, 0]
				count += 1
			if stats in s:
				player = d[count1]
				for char in s:
					if char.isdigit() or char == ".":
						value += char
				player[1] += float(value)
				count1 += 1
				value = ""
	new = dict()
	for i in d:
		i = d[i]
		player = i[0]
		touchdowns = i[1]
		new[player] = touchdowns

	return(new)




#get a specific player's statistics for a certain statistical category
def getSeasonData(name, position, stats):
	first = ""
	last = ""
	index = name.index(" ")
	first = name[0] + "."
	last = name[index+1:]
	name = first+last
	temp = {}
	for i in range(len(stats)):
		stat = "\"" + stats[i] + "\""
		temp[stat] = ""
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})

	try:
	    conn = http.client.HTTPSConnection('api.fantasydata.net')
	    conn.request("GET",  "/v3/nfl/stats/JSON/SeasonLeagueLeaders/2018/" + position + "/Touchdowns%s" % params, "{body}", headers)
	    response = conn.getresponse()
	    data = response.read()
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	d = []
	count = 0
	value = ""
	for player in data.decode("utf-8").split("\"PlayerID\""):
		p = player[1:]
		for s in p.split(','):
			if "\"Name\"" in s:
				key = s[8:-1]
				if key == name:
					d.append(0)
					count += 1
				else:
					count = 0
			if count == 1:
				for i in temp:
					value = ""
					if i in s:
						for char in s:
							if char.isdigit() or char == ".":
								value += char
						temp[i] = float(value)
	return temp


#gets all data for a position
def getAllSeasonData(position):
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})

	try:
	    conn = http.client.HTTPSConnection('api.fantasydata.net')
	    conn.request("GET",  "/v3/nfl/stats/JSON/SeasonLeagueLeaders/2018/" + position + "/Touchdowns%s" % params, "{body}", headers)
	    response = conn.getresponse()
	    data = response.read()
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return data

#takes dataset and extracts data for specific name and statistical categories
def playerStats(name, stats, data):
	first = ""
	last = ""
	index = name.index(" ")
	first = name[0] + "."
	last = name[index+1:]
	name = first+last
	temp = {}
	for i in range(len(stats)):
		stat = "\"" + stats[i] + "\""
		temp[stat] = ""
	d = []
	count = 0
	value = ""
	for player in data.decode("utf-8").split("\"PlayerID\""):
		p = player[1:]
		for s in p.split(','):
			if "\"Name\"" in s:
				key = s[8:-1]
				if key == name:
					d.append(0)
					count += 1
				else:
					count = 0
			if count == 1:
				for i in temp:
					value = ""
					if i in s:
						for char in s:
							if char.isdigit() or char == ".":
								value += char
						temp[i] = float(value)
	return temp
