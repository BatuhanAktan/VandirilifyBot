import discord, time, pickle, requests
from discord.ext import commands
from discord.utils import get

key = 'AIzaSyCVHLbDSo8SMYhAqko1jRRf9j0BMHn6okQ'
token = 'ODA0MzQ4NDk4Nzc3ODY2MzAx.YBLB6g.LZ6OYCoc1TETiMvLsKAAEaQFGMI'



client  = commands.Bot(command_prefix = '.')




@client.event

async def on_ready():
	while True:
		oldNumVids = pickle.load(open('numVids.pickle', 'rb'))
		numVidResponse = requests.get('https://youtube.googleapis.com/youtube/v3/channels?part=statistics&forUsername=Vandiril&key={}'.format(key)).json()
		numVids = int(numVidResponse['items'][0]['statistics']['videoCount'])

		print("Old Vid: ", oldNumVids, "Num Vids:", numVids)

		if oldNumVids < numVids:
			print("New Video Uploaded")

			pickleOut = open("numVids.pickle", "wb")
			pickle.dump(numVids, pickleOut)
			pickleOut.close()

			print("Getting Video Url")
			vid = requests.get('https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults=20'.format(key,'UCZ-oWkpMnHjTJpeOOlD80OA')).json()
			url = 'https://www.youtube.com/watch?v={}&ab_channel=Vandiril'.format(vid['items'][0]['id']['videoId'])
			print("Vid Url:", url)
			await client.get_channel(622483122373787652).send("<@&641790384095232000>","New Vandiril vid: ", url)

		elif oldNumVids > numVids:
			print("Video has been deleted, adjusting data")
			pickleOut = open("numVids.pickle", "wb")
			pickle.dump(numVids, pickleOut)
			pickleOut.close()

		else: 
			print("No New Vids")

		print("Bot is running")
		time.sleep(600)


client.run(token)

