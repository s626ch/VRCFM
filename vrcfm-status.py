import requests
import time
import json
import sys

# CONFIG =========================================
LFM_API_KEY = 'GET-YOUR-OWN'
VRC_AUTH = 'authcookie_00000000-0000-0000-0000-000000000000' # your vrc auth cookie goes here
VRC_USR_ID = 'usr_00000000-0000-0000-0000-000000000000' # your usr id goes here
USER_AGENT = 'VRCFM-STATUS @s626ch (PLEASE DONT HURT ME VRC I LOVE YOU GUYS <3)'
LFM_USER_NAME = 'USERNAME' # your lastfm username goes here
NOT_LIST = "﮳" # empty char, replace with whatever shows up when no song is playing
POLL_INT = 15 # in seconds, be wary!
# ================================================
HEADERS = { 'user-agent': USER_AGENT }
LFM_URL = f"https://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&limit=1&user={LFM_USER_NAME}&api_key={LFM_API_KEY}&format=json"
VRC_URL = f"https://api.vrchat.cloud/api/1/users/{VRC_USR_ID}"
# ================================================
def fetchTrack() -> dict:
	try:
		resp = requests.get(LFM_URL, headers=HEADERS, timeout=10)
		resp.raise_for_status()
		data = resp.json()
		tracks = data['recenttracks']['track']
		if not tracks:
			return {'is_playing': False}
		track = tracks[0]
		is_playing = '@attr' in track and 'nowplaying' in track['@attr']
		if is_playing:
			artist = track['artist']['#text']
			title = track['name']
			return {
				'is_playing': True,
				'artist': artist,
				'title': title
			}
		else:
			return {'is_playing': False}
	except Exception as e:
		print(f"error fetching from lastfm: {e}", file=sys.stderr)
		return None

def setStatus(song: str) -> bool:
	body = json.dumps({"statusDescription": song})
	headers = {**HEADERS, 'Content-Type': 'application/json'}
	try:
		resp = requests.put(VRC_URL, headers=headers, data=body, cookies={"auth":VRC_AUTH},timeout=10)
		resp.raise_for_status()
		return True
	except Exception as e:
		print(f"error updating status: {e}", file=sys.stderr)
		return False

def statusStr(track: dict) -> str:
	if track['is_playing']:
		return f"{track['artist']} - {track['title']}"
	else:
		return f"{NOT_LIST}"

def main():
	cachedTrack = None
	while True:
		currentTrack = fetchTrack()
		if currentTrack is None:
			print(f"lastfm fetch failed, waiting {POLL_INT} sec")
			time.sleep(POLL_INT)
			continue
		if cachedTrack == currentTrack:
			time.sleep(POLL_INT)
			continue
		status = statusStr(currentTrack)
		if len(status) > 29:
			status = status[:29] + "..."
		if setStatus(status):
			cachedTrack = currentTrack
		else:
			print(f"status update failed, will retry in {POLL_INT} sec")
		time.sleep(POLL_INT)

if __name__ == '__main__':
	main()
