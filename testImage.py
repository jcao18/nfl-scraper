import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
from io import BytesIO
import tkinter as tk
from urllib.request import urlopen
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageDraw, ImageFont
import copy

#get image headshot for specific player

def getURL(names):
	temp = copy.copy(names)
	URLs = {}
	headers = {
		'Ocp-Apim-Subscription-Key': '3cb884984b2141418eb885eb4809ea54',
	}

	params = urllib.parse.urlencode({
	})
	try:
		#API permission checker (subscription key)
		conn = http.client.HTTPSConnection('api.fantasydata.net')
		conn.request("GET",  "https://api.fantasydata.net/v3/nfl/stats/JSON/Players%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	#my code
	want = False
	for player in data.decode("utf-8").split("\"PlayerID\""):
		if len(temp) > 0:
			p = player[1:]
			for s in p.split(','):
				if "\"Name\"" in s:
					key = s[8:-1]
					if key in temp:
						want = True
				if "\"PhotoUrl\"" in s:
					if want:
						URL = s[12:-1]
						URLs[key]= URL
						want = False
						temp.remove(key)
		else:
			break
	return URLs


