import http.client, urllib.request, urllib.parse, urllib.error, base64

#Week by week data
def getData(name, stat):
	stat = "\"" + stat + "\""
	#subscription checker: https://developer.fantasydata.com/docs/services/57a01ec514338d17388660cb/operations/5943f7d78a940ff458b40dfe
	#used in multiple methods.
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})

	d = []
	count = 1
	count1 = 1
	total = 0
	for i in range(1, 17):
		try:
			#API permission checker (subscription key)
		    conn = http.client.HTTPSConnection('api.fantasydata.net')
		    conn.request("GET",  "https://api.fantasydata.net/v3/nfl/stats/JSON/GameLeagueLeaders/2018/" + str(i) + "/OFFENSE/RushingYards%s" % params, "{body}", headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	#my code
		value = ""
		for player in data.decode("utf-8").split("\"PlayerID\""):
			p = player[1:]
			for s in p.split(','):
				if "\"Name\"" in s:
					key = s[8:-1]
					if key == name:
						d.append([0, i])
						count += 1
				if stat in s:
					if count1 == count-1:
						player = d[count1-1]
						for char in s:
							if char.isdigit() or char == ".":
								value += char
						total += float(value)
						player[0] += total
						count1 += 1
						value = ""
	return d

#Week by week data
def getStats(name, position, stats):
	final = {}
	for i in stats:
		stat = "\"" + i + "\""
		final[stat] = [[0,0]]
	#subscription checker: https://developer.fantasydata.com/docs/services/57a01ec514338d17388660cb/operations/5943f7d78a940ff458b40dfe
	#used in multiple methods.
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})
	want = False
	count = 0
	for i in range(1, 17):
		try:
			#API permission checker (subscription key)
		    conn = http.client.HTTPSConnection('api.fantasydata.net')
		    conn.request("GET",  "https://api.fantasydata.net/v3/nfl/stats/JSON/GameLeagueLeaders/2018/" + str(i) + "/"+ position + "/RushingYards%s" % params, "{body}", headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))
		    break
	#my code
		value = ""
		for player in data.decode("utf-8").split("\"PlayerID\""):
			p = player[1:]
			for s in p.split(','):
				if "\"Name\"" in s:
					key = s[8:-1]
					if key == name:
						want = True
						count += 1
					else: want = False
				for stat in final:
					p = final[stat]
					if stat in s:
						if want:
							temp = [0, count]
							for char in s:
								if char.isdigit() or char == ".":
									value += char
							c = float(value)
							prev = p[count-1][0]
							new = prev + c
							temp[0] = new
							p.append(temp)
							value = ""
	return final


def getPositionStats(position):
	#subscription checker: https://developer.fantasydata.com/docs/services/57a01ec514338d17388660cb/operations/5943f7d78a940ff458b40dfe
	#used in multiple methods.
	headers = {
	    'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})
	want = False
	count = 0
	for i in range(1, 17):
		try:
			#API permission checker (subscription key)
		    conn = http.client.HTTPSConnection('api.fantasydata.net')
		    conn.request("GET",  "https://api.fantasydata.net/v3/nfl/stats/JSON/GameLeagueLeaders/2018/" + str(i) + "/"+ position + "/RushingYards%s" % params, "{body}", headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))
		    break
	#my code
		if i == 1: final = data
		else: final += data
	return final

def extract(name, position, stats, data):
	final = {}
	for i in stats:
		stat = "\"" + i + "\""
		final[stat] = [[0,0]]
	want = False
	count = 0
	value = ""
	for player in data.decode("utf-8").split("\"PlayerID\""):
			p = player[1:]
			for s in p.split(','):
				if "\"Name\"" in s:
					key = s[8:-1]
					if key == name:
						want = True
						count += 1
					else: want = False
				for stat in final:
					p = final[stat]
					if stat in s:
						if want:
							temp = [0, count]
							for char in s:
								if char.isdigit() or char == ".":
									value += char
							c = float(value)
							prev = p[count-1][0]
							new = prev + c
							temp[0] = new
							p.append(temp)
							value = ""
	return final