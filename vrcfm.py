import requests
from pythonosc.udp_client import SimpleUDPClient
import time
import json

# CONFIG =========================================
API_KEY = 'GET-YOUR-OWN-KEY-STEPS-IN-README'
# replace everything between the 'quotes'
# with your key
USER_AGENT = 'VRCFM'
USER_NAME = 'YOUR_USERNAME'
# your lastfm username
VRC_IP = '127.0.0.1'
# only change VRC_IP if you are running this
# on a different machine than the one you play
# vrchat on !!!!
VRC_PORT = 9000
# ================================================

headers = { 'user-agent': USER_AGENT }
request = f"https://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&limit=1&user={USER_NAME}&api_key={API_KEY}&format=json"
client = SimpleUDPClient(VRC_IP, VRC_PORT)
msgStr = ["", True]

while True:
	r = requests.get(request, headers=headers)
	# monitor playing status, fallback to false when the playing attr doesn't exist
	try:
		isPlaying = r.json()['recenttracks']['track'][0]['@attr']['nowplaying']
	except:
		isPlaying = "false"
	# if it's playing, send it, otherwise clear
	match isPlaying:
		case "true":
			artist = r.json()['recenttracks']['track'][0]['artist']['#text']
			title = r.json()['recenttracks']['track'][0]['name']
			msgStr[0] = f"Scrobbling:\n{artist} - {title}"
			client.send_message("/chatbox/input", msgStr)
		case _:
			msgStr[0] = ""
			client.send_message("/chatbox/input", msgStr)
	time.sleep(5)
