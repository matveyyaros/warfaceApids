#основные импорта для ds
import discord
from discord.ext import commands
# парсер данных
import json
import requests
#данные для работы
import config

bot = commands.Bot(command_prefix = config.prefix)
client=discord.Client()
print('Батут работает')
#команды бота
@bot.command()
async def claninfo(ctx, clan, server):
	if server not in config.servers:
		await ctx.send('Неправильная форма. Пример: (префикс)claninfo [клан] [сервер]')
		return 0
	url=f'http://api.warface.ru/rating/monthly?server={config.servers[server]}&clan={clan}'
	info=requests.get(url)
	info=info.json()
	for i in info:
		if 'message' in info:

			await ctx.send('Такого клана не существует')
			return 0

		if i['clan']:
			if i['clan']==clan:
				info=i
				break
	await ctx.send(f'''Информация:\n
		Название - {info['clan']}\n
		Глава - {info['clan_leader']}\n
		Игроков - {info['members']}\n
		Очков клана за месяц - {info['points']}\n
		Ранг - {info['rank']}\n
		{config.leagues[info['league']]} лига''')

@bot.command()
async def userstats(ctx, name, server):
	#print(0)
	if server not in config.servers:
		await ctx.send('Неправильная форма. Пример: (префикс)userstats [имя] [сервер]')
		return 0
	#print(1)	
	url=f'http://api.warface.ru/user/stat/?name={name}&server={config.servers[server]}' 
	info=requests.get(url)
	#print(2)
	info=info.json()
	#print(3.4)
	
	#print(3.5)
	if 'message' in info.keys():
		if info['message']=='Игрок скрыл свою статистику':
			await ctx.send('Игрок скрыл свою статистику')
			return 0
		else:
			await ctx.send('Такого игрока не существует.')
			return 0
	#print(3)
	if 'clan_name' in info:
		clan=info['clan_name']
	else:
		clan='не состоит'
	await ctx.send(f'''Информация:\n
		Имя - {info['nickname']}\n
		Ранг - {info['rank_id']} ({info['experience']} очков опыта)\n
		Клан - {clan}\n
		Часов игры - {info['playtime_h']} ч.\n
		Cыграно PvP матчей - {info['pvp_all']}\n
		Коэффициент побед в PvP - {info['pvpwl']} ({info['pvp_wins']}/{info['pvp_lost']})
		У/С - {info['pvp']} ({info['kill']}/{info['death']})\n
		Любимый класс(PvP) - {config.classes[info['favoritPVP']]}\n
		Любимый класс(PvE) - {config.classes[info['favoritPVE']]}''')

@bot.command()
async def info(ctx):
	txt=config.listOftext['commands']
	await ctx.send(f'список команд:\n{txt}')

@bot.command()
async def xxx(ctx):
	vc = message.author.voice.channel
	await vc.connect()



@bot.event#неправильная команда
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(embed = discord.Embed(description = f'команда не найдена. для ознакомления введине(префикс)info', colour = discord.Color.red()))

@bot.event#при приглашении на сервер
async def on_guild_join(guild):
	#channel = discord.utils.get(member.guild.channels, name="👋│arrivals") #нахождение такого канала
	#await channel.send(переменная с вашим сообщением) # сообщение по id
    if guild.system_channel is not None: # если у сервера есть системный канал то мы отправляем туда сообщение
    	txt=config.listOftext['commands']
    	guild.system_channel.send(f'Здраствуй сервер, я бот и вот мой список команд:\n{txt}') # если нет, то владельцу сервера
    elif guild.system_channel is None:
        user = client.get_user(guild.owner.id)
        txt=config.listOftext['commands']
        user.send(f'Здраствуй сервер, я бот и вот мой список команд:\n{txt}')


bot.run(config.TOKEN)