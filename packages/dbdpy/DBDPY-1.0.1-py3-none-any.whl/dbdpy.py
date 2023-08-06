class _variables():
	def __init__(self):
		self.path=None
		self.data={"server":{}, "global":{}, "user":{}}
		self.vars={}
	def save(self):
		import json
		if self.path is not None:
			json.dump(self.data,open(self.path+"vars.json","w"))
	def load(self):
		import json
		self.data={"server":{}, "global":{}, "user":{}}
		if self.path is not None:
			try:
				self.data=json.load(open(self.path+"vars.json","r"))
			except:
				with open(self.path+"vars.json","w") as f:
						f.write('{"server":{}, "global":{}, "user":{}}')
	def get(self,type,name,id,server=None):
		try:
			if type=="user":
				return self.data[type][str(server)][str(id)][name]
			else:
				return self.data[type][str(id)][name]
		except:
			return "none"
		
	def set(self,type,name,data,id,server=None):
		try:
			if type=="user":
				self.data[type][str(server)][str(id)][name]=data
			else:
				self.data[type][str(id)][name]=data
		except:
			pass

class dbd_bot():
	def __init__(self, info):
		import os
		try:
			import discord
			from discord.ext import commands
		except:
			print("Нет модуля discord, начинаем установку!")
			os.system("pip install discord")
		try:
			import asyncio
		except:
			print("Нет модуля asyncio, начинаем установку!")
			os.system("pip install asyncio")
		import discord
		from discord.ext import commands
		self._prefix=info["prefix"]
		self._token=info["token"]
		self._codes={}
		self._cooldown={}
		self._db=_variables()
		try:
			self._db.path=name.rstrip(os.path.basename(info["path"]))
			self._db.load()
		except:
			pass
		try:
			self._style=info["style"]
		except:
			self._style="[]"
		self._client=commands.Bot(command_prefix=self._prefix, intents=discord.Intents.all())

	def command(self, info):
		self._codes["command:"+info["name"]]={}
		code=[]
		for n in info:
			if not n in ["name","prefix","program"]:
				code.append(info[n])
		try:
			if info["program"]=="unstable":
				code=reversed(code)
		except:
			info["program"]="classic"
		self._codes["command:"+info["name"]]["name"]=info["name"]
		self._codes["command:"+info["name"]]["code"]=code
		try:
			self._codes["command:"+info["name"]]["prefix"]=info["prefix"]
		except:
			self._codes["command:"+info["name"]]["prefix"]=self._prefix
		
	def event(self, info):
		self._codes[info["name"]]={}
		code=[]
		for n in info:
			if not n in ["name","program"]:
				code.append(info[n])
		try:
			if info["program"]=="unstable":
				code=reversed(code)
		except:
			info["program"]="classic"
		self._codes[info["name"]]["name"]=info["name"]
		self._codes[info["name"]]["code"]=code

	def var(self, info):
		self._db.vars[info["name"]]=info["value"]

	def run(self):
		for g in self._client.guilds:
			if not str(g.id) in self._db.data["server"]:
				self._db.data["server"][str(g.id)]=self._db.vars
			else:
				for v in self._db.vars:
					if not v in self._db.data["server"][str(g.id)]:
						self._db.data["server"][str(g.id)][v]=self._db.vars[v]
			if not str(g.id) in self._db.data["user"]:
				self._db.data["user"][str(g.id)]={}
			for m in g.members:
				if not str(m.id) in self._db.data["user"][str(g.id)]:
					self._db.data["user"][str(g.id)][str(m.id)]=self._db.vars
				else:
					for v in self._db.vars:
						if not v in self._db.data["user"][str(g.id)][str(m.id)]:
							self._db.data["user"][str(g.id)][str(m.id)][v]=self._db.vars[v]
				if not str(m.id) in self._db.data["global"]:
					self._db.data["global"][str(m.id)]=self._db.vars
				else:
					for v in self._db.vars:
						if not v in self._db.data["global"][str(m.id)]:
							self._db.data["global"][str(m.id)][v]=self._db.vars[v]
		self._db.save()
		_start(self._client, self)

def _start(client, bot):
	import time
	import asyncio
	import discord
	from discord.ext import commands
	startTime=time.time()
	def replaces(line, message, guild, content):
		line=line.replace("$uptime",str(int(time.time() - startTime)))
		line=line.replace("$ping",str(round(client.latency*1000)))
		try:
			line=line.replace("$serverID",str(guild.id))
		except:
			pass
		try:
			line=line.replace("$channelID",str(message.channel.id))
			line=line.replace("$authorID",str(message.author.id))
			line=line.replace("$nickname",str(message.author.display_name))
			line=line.replace("$username",str(message.author.name))
		except:
			pass
		line=line.replace("$message", content)
		while "$roleID"+bot._style[0] in line:
			try:
				role = discord.utils.get(guild.roles, name=line.split("$roleID"+bot._style[0])[1].split(bot._style[1])[0].replace("$message", content))
				line=line.replace("$roleID"+bot._style[0]+line.split("$roleID"+bot._style[0])[1].split(bot._style[1])[0]+bot._style[1],str(role.id))
			except Exception as e:
				line=line.replace("$roleID"+bot._style[0]+line.split("$roleID"+bot._style[0])[1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$userID"+bot._style[0] in line:
			try:
				user = discord.utils.get(guild.members, name=line.split("$userID"+bot._style[0])[1].split(bot._style[1])[0].replace("$message", content))
				line=line.replace("$userID"+bot._style[0]+line.split("$userID"+bot._style[0])[1].split(bot._style[1])[0]+bot._style[1],str(user.id))
			except Exception as e:
				line=line.replace("$userID"+bot._style[0]+line.split("$userID"+bot._style[0])[1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$discriminator"+bot._style[0] in line:
			try:
				user = discord.utils.get(guild.members, name=line.split("$discriminator"+bot._style[0])[1].split(bot._style[1])[0].replace("$message", content))
				line=line.replace("$discriminator"+bot._style[0]+line.split("$discriminator"+bot._style[0])[1].split(bot._style[1])[0]+bot._style[1],str(user.discriminator))
			except Exception as e:
				line=line.replace("$discriminator"+bot._style[0]+line.split("$discriminator"+bot._style[0])[1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$avatar"+bot._style[0] in line:
			try:
				user = discord.utils.get(guild.members, name=line.split("$avatar"+bot._style[0])[1].split(bot._style[1])[0].replace("$message", content))
				line=line.replace("$avatar"+bot._style[0]+line.split("$avatar"+bot._style[0])[1].split(bot._style[1])[0]+bot._style[1],str(user.avatar_url))
			except Exception as e:
				line=line.replace("$avatar"+bot._style[0]+line.split("$avatar"+bot._style[0])[1].split(bot._style[1])[0]+bot._style[1],"none")
		return line
	
	async def use(message, name, trigger=""):
		go=0
		lines=[]
		if name=="bot_ready":
			content="$message"
		else:
			ctx=message.channel
			content=message.content.lstrip(trigger).lstrip(" ")
		for line in bot._codes[name]["code"]:
			if "$eval" in line:
				lines=content.split("\n")
				break
			lines.append(line)
		if "" in lines:
			lines.remove("")
		for line in lines:
			if go==0:
				guild=message
				try:
					message.roles
				except:
					try:
						guild=message.guild
					except:
						guild=""
				line=line.lstrip(" ")
				try:
					if line.startswith("$cooldown"+bot._style[0]):
						line=line[len("$cooldown"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						cd=line.split(";")[0]
						line=line.lstrip(cd+";")
						if not cmd in cooldown:
							cooldown[cmd]={"user":{},"server":{}, "global":0}
						if not str(message.author.id) in cooldown[cmd]["user"]:
							cooldown[cmd]["user"][str(message.author.id)]=0
						if not str(guild.id) in cooldown[cmd]["server"]:
							cooldown[cmd]["server"][str(guild.id)]=0
						if cooldown[cmd]["user"][str(message.author.id)]>int(time.time() - startTime):
							if line!="":
								await ctx.send(line)
							break
						else:
							if cd.endswith("s"):
								cd=cd.rstrip("s")
							elif cd.endswith("m"):
								cd=cd.rstrip("m")
								cd=int(cd)*60
							elif cd.endswith("h"):
								cd=cd.rstrip("h")
								cd=int(cd)*60*60
							elif cd.endswith("d"):
								cd=cd.rstrip("d")
								cd=int(cd)*60*60*24
							cooldown[cmd]["user"][str(message.author.id)]=int(time.time() - startTime)+int(cd)
					elif line.startswith("$serverCooldown"+bot._style[0]):
						line=line[len("$serverCooldown"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						cd=line.split(";")[0]
						line=line.lstrip(cd+";")
						if not cmd in cooldown:
							cooldown[cmd]={"user":{},"server":{}, "global":0}
						if not str(message.author.id) in cooldown[cmd]["user"]:
							cooldown[cmd]["user"][str(message.author.id)]=0
						if not str(guild.id) in cooldown[cmd]["server"]:
							cooldown[cmd]["server"][str(guild.id)]=0
						if cooldown[cmd]["server"][str(guild.id)]>int(time.time() - startTime):
							if line!="":
								await ctx.send(line)
							break
						else:
							if cd.endswith("s"):
								cd=cd.rstrip("s")
							elif cd.endswith("m"):
								cd=cd.rstrip("m")
								cd=int(cd)*60
							elif cd.endswith("h"):
								cd=cd.rstrip("h")
								cd=int(cd)*60*60
							elif cd.endswith("d"):
								cd=cd.rstrip("d")
								cd=int(cd)*60*60*24
							cooldown[cmd]["server"][str(guild.id)]=int(time.time() - startTime)+int(cd)
					elif line.startswith("$globalCooldown"+bot._style[0]):
						line=line[len("$globalCooldown"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						cd=line.split(";")[0]
						line=line.lstrip(cd+";")
						if not cmd in cooldown:
							cooldown[cmd]={"user":{},"server":{}, "global":0}
						if not str(message.author.id) in cooldown[cmd]["user"]:
							cooldown[cmd]["user"][str(message.author.id)]=0
						if not str(guild.id) in cooldown[cmd]["server"]:
							cooldown[cmd]["server"][str(guild.id)]=0
						if cooldown[cmd]["global"]>int(time.time() - startTime):
							if line!="":
								await ctx.send(line)
							break
						else:
							if cd.endswith("s"):
								cd=cd.rstrip("s")
							elif cd.endswith("m"):
								cd=cd.rstrip("m")
								cd=int(cd)*60
							elif cd.endswith("h"):
								cd=cd.rstrip("h")
								cd=int(cd)*60*60
							elif cd.endswith("d"):
								cd=cd.rstrip("d")
								cd=int(cd)*60*60*24
							cooldown[cmd]["global"]=int(time.time() - startTime)+int(cd)
					elif line.startswith("$useChannel"+bot._style[0]):
						line=line[len("$useChannel"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						if discord.utils.get(guild.channels, id=int(line)):
							ctx=discord.utils.get(guild.channels, id=int(line))
					elif line.startswith("$onlyAdmin"+bot._style[0]):
						line=line[len("$onlyAdmin"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						if not message.author.guild_permissions.administrator:
							if line!="":
								await ctx.send(line)
							break
					elif line.startswith("$onlyIDs"+bot._style[0]):
						line=line[len("$onlyIDs"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						line=line.split(";")
						users=line
						users.remove(line[-1])
						if not str(message.author.id) in users:
							if line!="":
								await ctx.send(line)
							break
					elif line.startswith("$giveRole"+bot._style[0]):
						line=line[len("$giveRole"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						line=line.split(";")
						role = discord.utils.get(guild.roles, id=int(line[1]))
						user=discord.utils.get(guild.members, id=int(line[0]))
						await user.add_roles(role)
					elif line.startswith("$takeRole"+bot._style[0]):
						line=line[len("$takeRole"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						line=line.split(";")
						role = discord.utils.get(guild.roles, id=int(line[1]))
						user=discord.utils.get(guild.members, id=int(line[0]))
						await user.remove_roles(role)
					elif line.startswith("$kick"+bot._style[0]):
						line=line[len("$kick"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						user=discord.utils.get(message.guild.members, id=int(line))
						await user.kick(reason="")
					elif line.startswith("$ban"+bot._style[0]):
						line=line[len("$ban"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						user=discord.utils.get(message.guild.members, id=int(line))
						await user.ban(reason="")
					elif line.startswith("$unBan"+bot._style[0]):
						line=line[len("$unban"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						banned_users = await message.bans()
						for ban_entry in banned_users:
							user = ban_entry.user
							if user.id==int(line):
								await user.unban(user)
					elif line.startswith("$addReactions"+bot._style[0]):
						line=line[len("$addReactions"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						for react in line.split(";"):
							try:
								await msg.add_reaction(react)
							except:
								pass
					elif line.startswith("$typing"):
						line=line[len("$typing"):]
						async with message.channel.typing():
							await asyncio.sleep(1)
					elif line.startswith("$print"+bot._style[0]):
						line=line[len("$print"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						print(line)
					elif line.startswith("$send"+bot._style[0]):
						line=line[len("$send"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						msg=await ctx.send(line)
					elif line.startswith("$wait"+bot._style[0]):
						line=line[len("$wait"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						if line.endswith("s"):
							line=line.rstrip("s")
						elif line.endswith("m"):
							line=line.rstrip("m")
							line=int(line)*60
						elif line.endswith("h"):
							line=line.rstrip("h")
							line=int(line)*60*60
						elif line.endswith("d"):
							line=line.rstrip("d")
							line=int(line)*60*60*24
						await asyncio.sleep(int(line))
					elif line.startswith("$if"+bot._style[0]):
						line=line[len("$if"+bot._style[0]):]
						line=line[:-1]
						t=True
						n=False
						cd=line.split(";")[0]
						line=line.lstrip(line.split(";")[0]+";")
						if line.startswith("not "):
							n=True
							line=line.lstrip("not ")
						if " == " in line:
							t=line.split(" == ")
							t[0]=replaces(t[0], message, guild, content)
							t[1]=replaces(t[1], message, guild, content)
							if t[0]==t[1]:
								t=True
							else:
								t=False
						elif " != " in line:
							t=line.split(" != ")
							t[0]=replaces(t[0], message, guild, content)
							t[1]=replaces(t[1], message, guild, content)
							if t[0]!=t[1]:
								t=True
							else:
								t=False
						elif " >= " in line:
							t=line.split(" >= ")
							t[0]=replaces(t[0], message, guild, content)
							t[1]=replaces(t[1], message, guild, content)
							if int(t[0])>=int(t[1]):
								t=True
							else:
								t=False
						elif " <= " in line:
							t=line.split(" <= ")
							t[0]=replaces(t[0], message, guild, content)
							t[1]=replaces(t[1], message, guild, content)
							if int(t[0])<=int(t[1]):
								t=True
							else:
								t=False
						elif " > " in line:
							t=line.split(" > ")
							t[0]=replaces(t[0], message, guild, content)
							t[1]=replaces(t[1], message, guild, content)
							if int(t[0])>int(t[1]):
								t=True
							else:
								t=False
						elif " < " in line:
							t=line.split(" < ")
							t[0]=replaces(t[0], message, guild, content)
							t[1]=replaces(t[1], message, guild, content)
							if int(t[0])<int(t[1]):
								t=True
							else:
								t=False
						elif " in " in line:
							t=line.split(" in ")
							t[0]=replaces(t[0], message, guild, content)
							t[1]=replaces(t[1], message, guild, content)
							if t[0] in t[1]:
								t=True
							else:
								t=False
						if n:
							t=not t
						if t==False:
								go+=int(cd)
					elif line.startswith("$clear"+bot._style[0]):
						line=line[len("$clear"+bot._style[0]):]
						line=line[:-1]
						line=replaces(line, message, guild, content)
						await message.channel.purge(limit=int(line)+1)
					elif line.startswith("$replay"):
						await use(message, name, trigger)
					else:
						print(f"Неизвестная функция {line}")
				except Exception as e:
					print(f"Ошибка в функции {line}")
			else:
				go-=1
	
	@client.event
	async def on_ready():
		try:
			await use("", "bot_ready", "")
		except Exception as e:
			pass

	@client.event
	async def on_message_delete(message):
		if message.author.id!=client.user.id and not message.author.bot:
			try:
				await use(message, "message_delete", "")
			except Exception as e:
				pass

	@client.event
	async def on_message(message):
		if message.author.id!=client.user.id and not message.author.bot:
			for cmd in bot._codes:
				if cmd.startswith("command:"):
					if "$case" in bot._codes[cmd]["code"]:
						if str(bot._codes[cmd]["name"]).startswith("[") and str(bot._codes[cmd]["name"]).endswith("]"):
							triggers=bot._codes[cmd]["name"].lstrip("[")
							triggers=triggers.rstrip("]")
							triggers=triggers.split(";")
							for trigger in triggers:
								if str(message.content).lower().startswith(str(bot._codes[cmd]["prefix"]+trigger).lower()):
									await use(message, cmd, bot._codes[cmd]["prefix"]+trigger)
						else:
							if str(message.content).lower().startswith(str(bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"]).lower()):
								await use(message, cmd, bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"])
					else:
						if str(bot._codes[cmd]["name"]).startswith("[") and str(bot._codes[cmd]["name"]).endswith("]"):
							triggers=bot._codes[cmd]["name"].lstrip("[")
							triggers=triggers.rstrip("]")
							triggers=triggers.split(";")
							for trigger in triggers:
								if str(message.content).startswith(bot._codes[cmd]["prefix"]+trigger):
									await use(message, cmd, bot._codes[cmd]["prefix"]+trigger)
						else:
							if str(message.content).startswith(bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"]):
								await use(message, cmd, bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"])

	client.run(bot._token)