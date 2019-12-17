import json
import discord
import requests

client = discord.Client()

bot_token = '' #Add Your Bot Token
tk = '' #From https://du.duoerpu.com 's headers

@client.event
async def on_ready():
    print("DU Price bot")
    print('Logged in as %s' %client.user.name)
    print("Client User ID: %s" %client.user.name)
    print('------')
    game = discord.Game("查询毒的价格")
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.event
async def on_message(message):
    if message.content.startswith('!du'):
        kw = message.content.split(" ")[1]
        prices = []
        headers =  {
            'tk': str(tk),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        search_html = requests.get('https://du.duoerpu.com/api/du/api/search?title='+kw+'&page=0&limit=20&sortType=0&sortMode=1&unionId=',headers=headers)
        search_json = json.loads(search_html.text)
        search_json = json.loads(search_json['data'])
        product_id = search_json['data']['productList'][0]['productId']
        product_url = 'https://du.duoerpu.com/api/du/api/detail?productId='+str(product_id)+'&productSourceName=wx'
        response = requests.get(product_url,headers=headers)
        response_json = json.loads(response.text)
        response_json = json.loads(response_json['data'])
        size_list = response_json['data']['sizeList']
        for size in size_list:
            if len(str(size['item']['price'])) > 5:
                price = str(size['item']['price']).replace('00','')
            else:
                price = str(size['item']['price'])
            prices.append(size['size']+' - ' + price)
        embed = discord.Embed(title='毒价格'+ str(response_json['data']['detail']['title']),description='',color=0x36393F)
        embed.add_field(name='价格', value='\n'.join(prices),inline=True)
        embed.add_field(name='销售量',value=response_json['data']['detail']['soldNum'])
        img = (response_json['data']['detail']['images'][0]['url'])
        embed.set_thumbnail(url=img)
        embed.set_author(name='@zyx898')
        embed.set_footer(text='@SkrNotify | SkrNotify',icon_url='https://pbs.twimg.com/profile_images/1134245182738718721/N12NVkrt_400x400.jpg')
        await message.channel.send(embed=embed)



client.run(bot_token) # Add your bot token here
