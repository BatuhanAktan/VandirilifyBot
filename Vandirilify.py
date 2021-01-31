import discord, time, pickle, requests, re, asyncio
from discord.ext import commands
from discord.utils import get

regex = "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com]*)?"
key = ''
token = ''

loop = asyncio.get_event_loop()
client  = commands.Bot(command_prefix = '.')

following = pickle.load(open('following.pickle', 'rb'))

def save():
	pickleOut = open("following.pickle", "wb")
	pickle.dump(following, pickleOut)
	pickleOut.close()


async def check():
	while True:
		following = pickle.load(open('following.pickle', 'rb'))
		for element in following:
			oldNumVids = element['numVids']
			numVidResponse = requests.get('https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}'.format(element['chnnlid'],key)).json()
			numVids = int(numVidResponse['items'][0]['statistics']['videoCount'])

			print("Old Vid: ", oldNumVids, "Num Vids:", numVids)

			if oldNumVids < numVids:
				print("New Video Uploaded")
				element['numVids'] = numVids

				save()

				print("Getting Video Url")
				vid = requests.get('https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults=20'.format(key,element['chnnlid'])).json()
				print(vid)
				url = 'https://www.youtube.com/watch?v={}&ab_channel={}'.format(vid['items'][0]['id']['videoId'],element['name'])
				print("Vid Url:", url)
				await client.get_channel(622483122373787652).send("<@&641790384095232000> New {} vid: ".format(element['name']) + url)

			elif oldNumVids > numVids:
				print("Video has been deleted, adjusting data")
				element['numVids'] = numVids
				save()
			else: 
				print("No New Vids")
		await asyncio.sleep(60*15)
loop.create_task(check())

@client.event

async def on_ready():
	print("Bot is running")

@client.command()

async def add(ctx, url):
	if re.search(regex,url):
		chnnlId = url.split('/')
		response = requests.get('https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}'.format(chnnlId[-1],key)).json()
		try:
			if {'name':response['items'][0]['snippet']['title'],'chnnlid': response['items'][0]['id'],'numVids': int(response['items'][0]['statistics']['videoCount'])} not in following:
				following.append({
					'name':response['items'][0]['snippet']['title'],
					'chnnlid': response['items'][0]['id'],
					'numVids': int(response['items'][0]['statistics']['videoCount'])
					})
				await ctx.send("Channel Added")
				print("Channel Added")
			else: 
				await ctx.send("Channel Already in List")
				print("Channel Already in")
		except:
			response = requests.get('https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={}&key={}'.format(chnnlId[-1],key)).json()
			if {'name':response['items'][0]['snippet']['title'],'chnnlid': response['items'][0]['id'],'numVids': int(response['items'][0]['statistics']['videoCount'])} not in following:
				following.append({
					'name':response['items'][0]['snippet']['title'],
					'chnnlid': response['items'][0]['id'],
					'numVids': int(response['items'][0]['statistics']['videoCount'])
					})
				await ctx.send("Channel Added")
				print("Channel Added")
			else: 
				await ctx.send("Channel Already in List")
				print("Channel Already in")
	else:
		try:
			response = requests.get('https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={}&key={}'.format(url.strip(),key)).json()
		except:
			await ctx.send("That doesn't look right try again!")
			return
		if {'name':response['items'][0]['snippet']['title'],'chnnlid': response['items'][0]['id'],'numVids': int(response['items'][0]['statistics']['videoCount'])} not in following:
			following.append({
				'name':response['items'][0]['snippet']['title'],
				'chnnlid': response['items'][0]['id'],
				'numVids': int(response['items'][0]['statistics']['videoCount'])
				})
			await ctx.send("Channel Added")
			print("Channel Added")
		else: 
			await ctx.send("Channel Already in List")
			print("Channel Already in")
	save()

@client.command()

async def list(ctx):
	if len(following) <= 0:
		await ctx.send("List Empty")
		return
	else:
		followList =""	
		i = 1
		for element in following:
			print(element)
			followList += (str(i)+ ".   " + element['name']+'\n')
			i += 1
		await ctx.send(followList)
		return


@client.command()

async def remove(ctx, *, chnnl):
	for element in following:
		if element['name'] == chnnl:
			following.remove(element)
			await ctx.send("Removed " + chnnl + " from your list.")
			print("Element removed")
			save()
			return
	await ctx.send("That is not in your list")
	print('Element not found')



@client.command()

async def h(ctx):
	f = open('help.txt', 'r')
	data = f.read()
	await ctx.send(data)
	f.close()

client.run(token)
loop.run_forever()
