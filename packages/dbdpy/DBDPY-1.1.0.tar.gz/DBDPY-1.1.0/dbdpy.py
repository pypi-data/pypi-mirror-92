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
				pass
	def get(self,type,name,id,server=None):
		try:
			if type=="user":
				if not str(server) in self.data[type]:
					self.data[type][str(server)]={}
				if not str(id) in self.data[type][str(server)]:
					self.data[type][str(server)][str(id)]=self.vars
				if not str(name) in self.data[type][str(server)][str(id)]:
					self.data[type][str(server)][str(id)][name]=self.vars[name]
				return self.data[type][str(server)][str(id)][name]
			else:
				if not str(id) in self.data[type]:
					self.data[type][str(id)]=self.vars
				if not str(name) in self.data[type][str(id)]:
					self.data[type][str(id)][name]=self.vars[name]
				return self.data[type][str(id)][name]
		except Exception as e:
			return "none"
		
	def set(self,type,name,data,id,server=None):
		try:
			if type=="user":
				if not str(server) in self.data[type]:
					self.data[type][str(server)]={}
				if not str(id) in self.data[type][str(server)]:
					self.data[type][str(server)][str(id)]=self.vars
				self.data[type][str(server)][str(id)][name]=data
			else:
				if not str(id) in self.data[type]:
					self.data[type][str(id)]=self.vars
				self.data[type][str(id)][name]=data
		except Exception as e:
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
			self._separator=info["sep"]
		except:
			self._separator=";"
		try:
			self._self=info["self"]=="true"
		except:
			self._self=False
		try:
			self._help=info["help"]=="true"
		except:
			self._help=True
		try:
			self._db.path=info["path"].rstrip(os.path.basename(info["path"]))
		except:
			self._db.path=None
		self._db.load()
		try:
			self._style=info["style"]
		except:
			self._style="[]"
		if self._self:
			self._client=commands.Bot(command_prefix=self._prefix, intents=discord.Intents.all())
		else:
			self._client=commands.Bot(command_prefix=self._prefix, intents=discord.Intents.all())
		self._client.remove_command(help)

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
		_start(self._client, self)

def _start(client, bot):
	import time
	import re
	import asyncio
	import discord
	import random
	from discord.ext import commands
	startTime=time.time()
	def embed(line):
		line=line.split(bot._separator)
		emb=discord.Embed()
		for l in line:
			cd=l.split("=")[0]
			cd2=l[len(l.split("=")[0]+"="):]
			if cd.startswith("title"):
				emb.title=cd2
			if cd.startswith("description"):
				try:
					emb.description=cd2
				except:
					pass
			if cd.startswith("icon"):
				try:
					emb.set_thumbnail(url=cd2)
				except:
					pass
			if cd.startswith("image"):
				try:
					emb.set_image(url=cd2)
				except:
					pass
			if cd.startswith("author"):
				t=cd2.split("|")
				try:
					emb.set_author(name=t[0], icon_url=t[1])
				except:
					emb.set_author(name=t[0])
			if cd.startswith("footer"):
				t=cd2.split("|")
				try:
					emb.set_footer(text=t[0], icon_url=t[1])
				except Exception as e:
					emb.set_footer(text=t[0])
			if cd.startswith("field"):
				t=cd2.split("|")
				try:
					emb.add_field(name=t[0],value=t[1],inline=True)
				except:
					pass
			if cd.startswith("color"):
				try:
					rgb=list(int(cd2[i:i+2], 16) for i in (0, 2, 4))
					emb.color=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
				except:
					pass
		return emb
	def get_vars(line, guild, vars):
		nowloop=""
		while "$getLocalVar"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				line=line.replace("$getLocalVar"+bot._style[0]+line.split("$getLocalVar"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],vars[line.split("$getLocalVar"+bot._style[0])[-1].split(bot._style[1])[0]])
		while "$getVar"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				line=line.replace("$getVar"+bot._style[0]+line.split("$getVar"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],bot._db.get("global",line.split("$getVar"+bot._style[0])[-1].split(bot._style[1])[0].split(qbot._separator)[0],line.split("$getVar"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[1]))
		while "$getServerVar"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				line=line.replace("$getServerVar"+bot._style[0]+line.split("$getServerVar"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],bot._db.get("server",line.split("$getServerVar"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[0],line.split("$getServerVar"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[1]))
		while "$getUserVar"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					line=line.replace("$getUserVar"+bot._style[0]+line.split("$getUserVar"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],bot._db.get("user",line.split("$getUserVar"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[0],line.split("$getUserVar"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[1], str(guild.id)))
				except:
					try:
						line=line.replace("$getUserVar"+bot._style[0]+line.split("$getUserVar"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],bot._db.get("user",line.split("$getUserVar"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[0],line.split("$getUserVar"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[1], line.split("$getUserVar"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[2]))
					except:
						break
		return line
	async def replaces(line, message, guild, content, msg, vars, timerep):
		nowloop=""
		content2=content
		try:
			for m in message.mentions:
				content2=content2.replace(str(m.mention).replace("!",""),"")
			if content2[0]==" ":
				content2=content2[1:]
		except:
			pass
		content2=re.sub("\s\s+", " ", content2)
		line=line.replace("%time%",str(timerep))
		line=line.replace("$uptime",str(int(time.time() - startTime)))
		line=line.replace("$ping",str(round(client.latency*800)))
		try:
			line=line.replace("$serverID",str(guild.id))
		except:
			pass
		try:
			line=line.replace("$channelID",str(message.channel.id))
			line=line.replace("$authorID",str(message.author.id))
			line=line.replace("$triggerID",str(message.id))
			line=line.replace("$messageID",str(msg.id))
		except:
			pass
		while "$message"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					line=line.replace("$message"+bot._style[0]+line.split("$message"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], content.split(" ")[int(line.split("$message"+bot._style[0])[-1].split(bot._style[1])[0])-1])
				except:
					line=line.replace("$message"+bot._style[0]+line.split("$message"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"")
		while "$noMentionMessage"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					line=line.replace("$noMentionMessage"+bot._style[0]+line.split("$noMentionMessage"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], content2.split(" ")[int(line.split("$noMentionMessage"+bot._style[0])[-1].split(bot._style[1])[0])-1])
				except:
					line=line.replace("$noMentionMessage"+bot._style[0]+line.split("$noMentionMessage"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"")
		line=line.replace("$noMentionMessage", content2)
		line=line.replace("$message", content)
		while "$mentioned"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					line=line.replace("$mentioned"+bot._style[0]+line.split("$mentioned"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], str(message.mentions[int(line.split("$mentioned"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[0])-1].id))
				except Exception as e:
					try:
						if line.split("$mentioned"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[1]=="yes":
							line=line.replace("$mentioned"+bot._style[0]+line.split("$mentioned"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], str(message.author.id))
						else:
							line=line.replace("$mentioned"+bot._style[0]+line.split("$mentioned"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], "none")
					except:
						line=line.replace("$mentioned"+bot._style[0]+line.split("$mentioned"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], "none")
		while "$roleID"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					role = discord.utils.get(guild.roles, name=line.split("$roleID"+bot._style[0])[-1].split(bot._style[1])[0])
					line=line.replace("$roleID"+bot._style[0]+line.split("$roleID"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(role.id))
				except Exception as e:
					line=line.replace("$roleID"+bot._style[0]+line.split("$roleID"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$boostCount"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					need = discord.utils.get(client.guilds, id=int(line.split("$boostCount"+bot._style[0])[-1].split(bot._style[1])[0]))
					line=line.replace("$boostCount"+bot._style[0]+line.split("$boostCount"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(need.premium_subscription_count))
				except Exception as e:
					line=line.replace("$boostCount"+bot._style[0]+line.split("$boostCount"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$userID"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					user = discord.utils.get(guild.members, name=line.split("$userID"+bot._style[0])[-1].split(bot._style[1])[0])
					line=line.replace("$userID"+bot._style[0]+line.split("$userID"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(user.id))
				except Exception as e:
					line=line.replace("$userID"+bot._style[0]+line.split("$userID"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$username"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					user = discord.utils.get(guild.members, id=int(line.split("$username"+bot._style[0])[-1].split(bot._style[1])[0]))
					line=line.replace("$username"+bot._style[0]+line.split("$username"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(user.name))
				except Exception as e:
					line=line.replace("$username"+bot._style[0]+line.split("$username"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$nickname"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					user = discord.utils.get(guild.members, id=int(line.split("$nickname"+bot._style[0])[-1].split(bot._style[1])[0]))
					line=line.replace("$nickname"+bot._style[0]+line.split("$nickname"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(user.display_name))
				except Exception as e:
					line=line.replace("$nickname"+bot._style[0]+line.split("$nickname"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$getReactions"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					userstr=""
					mes=await message.channel.fetch_message(int(line.split("$getReactions"+bot._style[0])[-1].split(bot._style[1])[0].split(";")[0]))
					mes=mes.reactions
					for react in mes:
						if react.emoji==line.split("$getReactions"+bot._style[0])[-1].split(bot._style[1])[0].split(";")[1]:
							users = await react.users().flatten()
							for user in users:
								if user.id!=client.user.id:
									userstr+=str(user.id)+";"
					userstr=userstr[:-1]
					line=line.replace("$getReactions"+bot._style[0]+line.split("$getReactions"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],userstr)
				except Exception as e:
					line=line.replace("$getReactions"+bot._style[0]+line.split("$getReactions"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$randomText"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					r=random.choice(line.split("$randomText"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator))
					line=line.replace("$randomText"+bot._style[0]+line.split("$randomText"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(r))
				except:
					line=line.replace("$randomText"+bot._style[0]+line.split("$randomText"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$random"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					r=random.randint(int(line.split("$random"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[0]),int(line.split("$random"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[1]))
					line=line.replace("$random"+bot._style[0]+line.split("$random"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(r))
				except:
					line=line.replace("$random"+bot._style[0]+line.split("$random"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$isAdmin"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					user = discord.utils.get(guild.members, id=int(line.split("$isAdmin"+bot._style[0])[-1].split(bot._style[1])[0]))
					if user.guild_permissions.administrator:
						line=line.replace("$isAdmin"+bot._style[0]+line.split("$isAdmin"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"true")
					else:
						line=line.replace("$isAdmin"+bot._style[0]+line.split("$isAdmin"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"false")
				except:
					line=line.replace("$isAdmin"+bot._style[0]+line.split("$isAdmin"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$hasRole"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					user = discord.utils.get(guild.members, id=int(line.split("$hasRole"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[0]))
					role = discord.utils.get(user.roles, id=int(line.split("$hasRole"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[1]))
					if not role is None:
						line=line.replace("$hasRole"+bot._style[0]+line.split("$hasRole"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"true")
					else:
						line=line.replace("$hasRole"+bot._style[0]+line.split("$hasRole"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"false")
				except:
					line=line.replace("$hasRole"+bot._style[0]+line.split("$hasRole"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$discriminator"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					user = discord.utils.get(guild.members, id=int(line.split("$discriminator"+bot._style[0])[-1].split(bot._style[1])[0]))
					line=line.replace("$discriminator"+bot._style[0]+line.split("$discriminator"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(user.discriminator))
				except Exception as e:
					line=line.replace("$discriminator"+bot._style[0]+line.split("$discriminator"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		while "$avatar"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					user = discord.utils.get(guild.members, id=int(line.split("$avatar"+bot._style[0])[-1].split(bot._style[1])[0]))
					line=line.replace("$avatar"+bot._style[0]+line.split("$avatar"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(user.avatar_url))
				except Exception as e:
					line=line.replace("$avatar"+bot._style[0]+line.split("$avatar"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none")
		line=get_vars(line, guild, vars)
		while "$replaceText"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					r=line.split("$replaceText"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[0].replace(line.split("$replaceText"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[1],line.split("$replaceText"+bot._style[0])[-1].split(bot._style[1])[0].split(bot._separator)[2])
					line=line.replace("$replaceText"+bot._style[0]+line.split("$replaceText"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],str(r))
				except:
					line=line.replace("$replaceText"+bot._style[0]+line.split("$replaceText"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"none") 
		while "$math"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:
					line=line.replace("$math"+bot._style[0]+line.split("$math"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], str(eval(line.split("$math"+bot._style[0])[-1].split(bot._style[1])[0],{'__builtins__':None})))
				except Exception as e:
					line=line.replace("$math"+bot._style[0]+line.split("$math"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], "none")
		while "$checkCondition"+bot._style[0] in line:
			if nowloop==line:
				break
			else:
				nowloop=line
				try:	
					check=line.split("$checkCondition"+bot._style[0])[-1].split(bot._style[1])[0]
					t=True
					n=False
					if check.startswith("not"):
						n=True
						check=check.lstrip("not")
						check=check.lstrip(" ")
					if "==" in check:
						t=check.split("==")
						if t[0]==t[1]:
							t=True
						else:
							t=False
					elif "!=" in check:
						t=check.split("!=")
						if t[0]!=t[1]:
							t=True
						else:
							t=False
					elif ">=" in check:
						t=check.split(">=")
						if int(t[0])>=int(t[1]):
							t=True
						else:
							t=False
					elif "<=" in check:
						t=check.split("<=")
						if int(t[0])<=int(t[1]):
							t=True
						else:
							t=False
					elif ">" in check:
						t=check.split(">")
						if int(t[0])>int(t[1]):
							t=True
						else:
							t=False
					elif "<" in check:
						t=check.split("<")
						if int(t[0])<int(t[1]):
							t=True
						else:
							t=False
					elif " in " in check:
						t=check.split(" in ")
						if t[0] in t[1]:
							t=True
						else:
							t=False
					if n:
						t=not t
					if t:
						line=line.replace("$checkCondition"+bot._style[0]+line.split("$checkCondition"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"true")
					else:
						line=line.replace("$checkCondition"+bot._style[0]+line.split("$checkCondition"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1],"false")
				except Exception as e:
					line=line.replace("$checkCondition"+bot._style[0]+line.split("$checkCondition"+bot._style[0])[-1].split(bot._style[1])[0]+bot._style[1], "none")
		return line
	
	async def use(message, name, trigger=""):
		vars={}
		restart=True
		while restart:
			stop=False
			timerep="0"
			restart=False
			go=0
			lines=[]
			msg=""
			if name=="bot_ready":
				content="$message"
			else:
				ctx=message.channel
				content=message.content.lstrip(trigger).lstrip(" ")
			for line in bot._codes[name]["code"]:
				if "$eval" in line:
					for l in content.split("\n"):
						lines.append(l)
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
							if line[-1]==bot._style[1]:
								line=line[len("$cooldown"+bot._style[0]):]
								line=line[:-1]
								if not name in bot._cooldown:
									bot._cooldown[name]={"user":{},"server":{}, "global":0}
								if not str(message.author.id) in bot._cooldown[name]["user"]:
									bot._cooldown[name]["user"][str(message.author.id)]=0
								if not str(guild.id) in bot._cooldown[name]["server"]:
									bot._cooldown[name]["server"][str(guild.id)]=0
								try:
									if bot._cooldown[name]["user"][str(message.author.id)]-int(time.time() - startTime)<0:
										timerep="0"
									else:
										timerep=str(bot._cooldown[name]["user"][str(message.author.id)]-int(time.time() - startTime))
								except:
									timerep="0"
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								cd=line.split(bot._separator)[1]
								if bot._cooldown[name]["user"][str(message.author.id)]>int(time.time() - startTime):
									go+=int(line.split(bot._separator)[0])
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
									bot._cooldown[name]["user"][str(message.author.id)]=int(time.time() - startTime)+int(cd)
						elif line.startswith("$deletemessage"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$deletemessage"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								mes=await ctx.fetch_message(int(line))
								await mes.delete()
						elif line.startswith("$serverCooldown"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$serverCooldown"+bot._style[0]):]
								line=line[:-1]
								if not name in bot._cooldown:
									bot._cooldown[name]={"user":{},"server":{}, "global":0}
								if not str(message.author.id) in bot._cooldown[name]["user"]:
									bot._cooldown[name]["user"][str(message.author.id)]=0
								if not str(guild.id) in bot._cooldown[name]["server"]:
									bot._cooldown[name]["server"][str(guild.id)]=0
								try:
									if bot._cooldown[name]["server"][str(guild.id)]-int(time.time() - startTime)<0:
										timerep="0"
									else:
										timerep=str(bot._cooldown[name]["server"][str(guild.id)]-int(time.time() - startTime))
								except:
									timerep="0"
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								cd=line.split(bot._separator)[1]
								if bot._cooldown[name]["server"][str(guild.id)]>int(time.time() - startTime):
									go+=int(line.split(bot._separator)[0])
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
									bot._cooldown[name]["server"][str(guild.id)]=int(time.time() - startTime)+int(cd)
						elif line.startswith("$globalCooldown"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$globalCooldown"+bot._style[0]):]
								line=line[:-1]
								if not name in bot._cooldown:
									bot._cooldown[name]={"user":{},"server":{}, "global":0}
								if not str(message.author.id) in bot._cooldown[name]["user"]:
									bot._cooldown[name]["user"][str(message.author.id)]=0
								if not str(guild.id) in bot._cooldown[name]["server"]:
									bot._cooldown[name]["server"][str(guild.id)]=0
								try:
									if bot._cooldown[name]["global"]-int(time.time() - startTime)<0:
										timerep="0"
									else:
										timerep=str(bot._cooldown[name]["global"]-int(time.time() - startTime))
								except:
									timerep="0"
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								cd=line.split(bot._separator)[0]
								if bot._cooldown[name]["global"]>int(time.time() - startTime):
									go+=int(line.split(bot._separator)[0])
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
									bot._cooldown[name]["global"]=int(time.time() - startTime)+int(cd)
						elif line.startswith("$reply"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$reply"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								mes=await ctx.fetch_message(int(line.split(bot._separator)[0]))
								msg=await mes.reply(content=line.split(bot._separator)[1])
						elif line.startswith("$embedReply"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$embedReply"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								mes=await ctx.fetch_message(int(line.split("&")[0]))
								emb=embed(line.split("&")[1])
								msg=await mes.reply(embed=emb)
						elif line.startswith("$useChannel"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$useChannel"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								if discord.utils.get(guild.channels, id=int(line)):
									ctx=discord.utils.get(guild.channels, id=int(line))
						elif line.startswith("$reactionPages"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$reactionPages"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								userid = str(message.author.id)
								previuspage = line.split("&")[0].split(bot._separator)[0]
								nextpage = line.split("&")[0].split(bot._separator)[1]
								page = 0
								descript=descript=line[len(line.split("&")[0].split(bot._separator)[0]+bot._separator+line.split("&")[0].split(bot._separator)[1]+"&"):].split("&")
								zeropage=descript[page]
								mesg = await message.channel.send(zeropage)
								await mesg.add_reaction(previuspage)
								await mesg.add_reaction(nextpage)
								def checkforreaction(reaction, user):
									return str(user.id) == userid and str(reaction.emoji) in [previuspage,nextpage]
								loopclose = 0
								while loopclose == 0:
									try:
										reaction, user = await client.wait_for('reaction_add', timeout=8,check = checkforreaction)
										if reaction.emoji == nextpage:
											if page+1<=len(descript)-1:
												page=page+1
											else:
												page=page
											r=nextpage
										elif reaction.emoji == previuspage:
											if page-1>=0:
												page-=1
											else:
												page=page
											r=previuspage
										nowpage=descript[page]
										await mesg.remove_reaction(r,message.author)
										await mesg.edit(content=nowpage)
									except asyncio.TimeoutError:
										try:
											await mesg.remove_reaction(previuspage,client.user)
										except:
											pass
										try:
											await mesg.remove_reaction(nextpage,client.user)
										except:
											pass
										loopclose = 1
						elif line.startswith("$embedReactionPages"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$embedReactionPages"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								userid = str(message.author.id)
								previuspage = line.split("&")[0].split(bot._separator)[0]
								nextpage = line.split("&")[0].split(bot._separator)[1]
								page = 0
								descript=descript=line[len(line.split("&")[0].split(bot._separator)[0]+bot._separator+line.split("&")[0].split(bot._separator)[1]+"&"):].split("&")
								zeropage=embed(descript[page])
								mesg = await message.channel.send(embed=zeropage)
								await mesg.add_reaction(previuspage)
								await mesg.add_reaction(nextpage)
								def checkforreaction(reaction, user):
									return str(user.id) == userid and str(reaction.emoji) in [previuspage,nextpage]
								loopclose = 0
								while loopclose == 0:
									try:
										reaction, user = await client.wait_for('reaction_add', timeout=8,check = checkforreaction)
										if reaction.emoji == nextpage:
											if page+1<=len(descript)-1:
												page=page+1
											else:
												page=page
											r=nextpage
										elif reaction.emoji == previuspage:
											if page-1>=0:
												page-=1
											else:
												page=page
											r=previuspage
										nowpage=embed(descript[page])
										await mesg.remove_reaction(r,message.author)
										await mesg.edit(embed=nowpage)
									except asyncio.TimeoutError:
										try:
											await mesg.remove_reaction(previuspage,client.user)
										except:
											pass
										try:
											await mesg.remove_reaction(nextpage,client.user)
										except:
											pass
										loopclose = 1
						elif line.startswith("$useServer"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$useServer"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								if discord.utils.get(client.guilds, id=int(line)):
									ctx=discord.utils.get(client.guilds, id=int(line))
						elif line.startswith("$stop"):
							stop=True
							break
						elif line.startswith("$onlyIDs"+bot._style[0]):
							line=line[len("$onlyIDs"+bot._style[0]):]
							if line[-1]==bot._style[1]:
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								line=line.split(bot._separator)
								users=line
								users.remove(line[-1])
								if not str(message.author.id) in users:
									if line!="":
										await ctx.send(line)
									break
						elif line.startswith("$giveRole"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$giveRole"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								line=line.split(bot._separator)
								role = discord.utils.get(guild.roles, id=int(line[1]))
								user=discord.utils.get(guild.members, id=int(line[0]))
								await user.add_roles(role)
						elif line.startswith("$takeRole"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$takeRole"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								line=line.split(bot._separator)
								role = discord.utils.get(guild.roles, id=int(line[1]))
								user=discord.utils.get(guild.members, id=int(line[0]))
								await user.remove_roles(role)
						elif line.startswith("$kick"+bot._style[0]):
							line=line[len("$kick"+bot._style[0]):]
							if line[-1]==bot._style[1]:
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								user=discord.utils.get(message.guild.members, id=int(line))
								await user.kick(reason="")
						elif line.startswith("$ban"+bot._style[0]):
							line=line[len("$ban"+bot._style[0]):]
							if line[-1]==bot._style[1]:
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								user=discord.utils.get(message.guild.members, id=int(line))
								await user.ban(reason="")
						elif line.startswith("$editEmbed"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$editEmbed"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								emb=embed(line)
								try:
									await msg.edit(embed=emb)
								except:
									pass
						elif line.startswith("$sendEmbed"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$sendEmbed"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								emb=embed(line)
								try:
									msg=await ctx.send(embed=emb)
								except:
									pass
						elif line.startswith("$unban"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$unban"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								banned_users = await message.bans()
								for ban_entry in banned_users:
									user = ban_entry.user
									if user.id==int(line):
										await user.unban(user)
						elif line.startswith("$setServerVar"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$setServerVar"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								line=line.split(bot._separator)
								bot._db.set("server",line[0],line[1],line[2])
						elif line.startswith("$setVar"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$setVar"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								line=line.split(bot._separator)
								bot._db.set("global",line[0],line[1],line[2])
						elif line.startswith("$setLocalVar"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$setLocalVar"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								line=line.split(bot._separator)
								vars[line[0]]=line[1]
						elif line.startswith("$setStatus"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$setStatus"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								line=[line.split(bot._separator)[0],line.split(bot._separator)[1], line[len(line.split(bot._separator)[0]+bot._separator+line.split(bot._separator)[1]+bot._separator):]]
								status=discord.Status.online
								if line[2]=="dnd":
									status=discord.Status.dnd
								if line[2]=="idle":
									status=discord.Status.idle
								if line[2]=="offline":
									status=discord.Status.offline
								if line[2]=="online":
									status=discord.Status.online
								if line[0]=="play":
									await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=line[1]),status=status)
								if line[0]=="watch":
									await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=line[1]),status=status)
								if line[0]=="listen":
									await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=line[1]),status=status)
								if line[0]=="stream":
									await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=line[1]),status=status)
						elif line.startswith("$setUserVar"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$setUserVar"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								line=line.split(bot._separator)
								try:
									bot._db.set("user",line[0],line[1],line[2],guild.id)
								except:
									bot._db.set("user",line[0],line[1],line[2],line[3])
						elif line.startswith("$addReactions"+bot._style[0]):
							if line[-1]==bot._style[1]:
								line=line[len("$addReactions"+bot._style[0]):]
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								for react in line.split(bot._separator):
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
							if line[-1]==bot._style[1]:
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								print(line)
						elif line.startswith("$send"+bot._style[0]):
							line=line[len("$send"+bot._style[0]):]
							if line[-1]==bot._style[1]:
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								msg=await ctx.send(line)
						elif line.startswith("$edit"+bot._style[0]):
							line=line[len("$edit"+bot._style[0]):]
							if line[-1]==bot._style[1]:
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								await msg.edit(content=line)
						elif line.startswith("$wait"+bot._style[0]):
							line=line[len("$wait"+bot._style[0]):]
							if line[-1]==bot._style[1]:
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
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
							if line[-1]==bot._style[1]:
								line=line[:-1]
								t=True
								n=False
								cd=line.split(bot._separator)[0]
								line=line.lstrip(line.split(bot._separator)[0]+bot._separator)
								if line.startswith("not"):
									n=True
									line=line.lstrip("not")
									line=line.lstrip(" ")
								if "==" in line:
									t=line.split("==")
									t[0]=await replaces(t[0], message, guild, content, msg, vars, timerep)
									t[1]=await replaces(t[1], message, guild, content, msg, vars, timerep)
									if t[0]==t[1]:
										t=True
									else:
										t=False
								elif "!=" in line:
									t=line.split("!=")
									t[0]=await replaces(t[0], message, guild, content, msg, vars, timerep)
									t[1]=await replaces(t[1], message, guild, content, msg, vars, timerep)
									if t[0]!=t[1]:
										t=True
									else:
										t=False
								elif ">=" in line:
									t=line.split(">=")
									t[0]=await replaces(t[0], message, guild, content, msg, vars, timerep)
									t[1]=await replaces(t[1], message, guild, content, msg, vars, timerep)
									if int(t[0])>=int(t[1]):
										t=True
									else:
										t=False
								elif "<=" in line:
									t=line.split("<=")
									t[0]=await replaces(t[0], message, guild, content, msg, vars, timerep)
									t[1]=await replaces(t[1], message, guild, content, msg, vars, timerep)
									if int(t[0])<=int(t[1]):
										t=True
									else:
										t=False
								elif ">" in line:
									t=line.split(">")
									t[0]=await replaces(t[0], message, guild, content, msg, vars, timerep)
									t[1]=await replaces(t[1], message, guild, content, msg, vars, timerep)
									if int(t[0])>int(t[1]):
										t=True
									else:
										t=False
								elif "<" in line:
									t=line.split("<")
									t[0]=await replaces(t[0], message, guild, content, msg, vars, timerep)
									t[1]=await replaces(t[1], message, guild, content, msg, vars, timerep)
									if int(t[0])<int(t[1]):
										t=True
									else:
										t=False
								elif " in " in line:
									t=line.split(" in ")
									t[0]=await replaces(t[0], message, guild, content, msg, vars, timerep)
									t[1]=await replaces(t[1], message, guild, content, msg, vars, timerep)
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
							if line[-1]==bot._style[1]:
								line=line[:-1]
								line=await replaces(line, message, guild, content, msg, vars, timerep)
								await message.channel.purge(limit=int(line)+1)
						elif line.startswith("$replay"):
							restart=True
							break
						else:
							print(f"Неизвестная функция {line}")
					except Exception as e:
						print(f"Ошибка в функции {line}")
						raise e
				else:
					go-=1
			if stop:
				break
			bot._db.save()

	@client.event
	async def on_ready():
		mems=[]
		for g in client.guilds:
			if not str(g.id) in bot._db.data["server"]:
				bot._db.data["server"][str(g.id)]=bot._db.vars
			else:
				for v in bot._db.vars:
					if not v in bot._db.data["server"][str(g.id)]:
						bot._db.data["server"][str(g.id)][v]=bot._db.vars[v]
			if not str(g.id) in bot._db.data["user"]:
				bot._db.data["user"][str(g.id)]={}
			for m in g.members:
				if not str(m.id) in bot._db.data["user"][str(g.id)]:
					bot._db.data["user"][str(g.id)][str(m.id)]=bot._db.vars
				else:
					for v in bot._db.vars:
						if not v in bot._db.data["user"][str(g.id)][str(m.id)]:
							bot._db.data["user"][str(g.id)][str(m.id)][v]=bot._db.vars[v]
				if not str(m.id) in bot._db.data["global"]:
					bot._db.data["global"][str(m.id)]=bot._db.vars
				else:
					for v in bot._db.vars:
						if not v in bot._db.data["global"][str(m.id)]:
							bot._db.data["global"][str(m.id)][v]=bot._db.vars[v]
		bot._db.save()
		try:
			await use("", "bot_ready", "")
		except Exception as e:
			pass

	@client.event
	async def on_message(message):
		if not message.author.bot:
			if str(message.content).startswith(bot._client.user.mention):
				if bot._help:
					cmds=""
					for c in bot._codes:
						if c.startswith("command:"):
							cmds+=bot._codes[c]["name"]+"\n"
					await message.channel.send(embed=discord.Embed(title="Комманды("+str(len(cmds.split("\n"))-1)+")",description=f"```py\n{cmds}\n```"))
			for cmd in bot._codes:
				if cmd.startswith("command:"):
					if "$case" in bot._codes[cmd]["code"]:
						if str(bot._codes[cmd]["name"]).startswith("[") and str(bot._codes[cmd]["name"]).endswith("]"):
							triggers=bot._codes[cmd]["name"].lstrip("[")
							triggers=triggers.rstrip("]")
							triggers=triggers.split(bot._separator)
							for trigger in triggers:
								trigger=await replaces(str(bot._codes[cmd]["prefix"]+trigger), message, message.guild, message.content.lstrip(str(bot._codes[cmd]["prefix"]+trigger).lower()).lstrip(" "), "", {}, 0)
								if str(message.content).lower().startswith(str(trigger).lower()):
									await use(message, cmd, bot._codes[cmd]["prefix"]+trigger)
						else:
							trigger=await replaces(str(bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"]), message, message.guild, message.content.lstrip(str(bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"])).lstrip(" "), "", {}, 0)
							if str(message.content).lower().startswith(trigger.lower()):
								await use(message, cmd, bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"])
					else:
						if str(bot._codes[cmd]["name"]).startswith("[") and str(bot._codes[cmd]["name"]).endswith("]"):
							triggers=bot._codes[cmd]["name"].lstrip("[")
							triggers=triggers.rstrip("]")
							triggers=triggers.split(bot._separator)
							for trigger in triggers:
								trigger=await replaces(str(bot._codes[cmd]["prefix"]+trigger), message, message.guild, message.content.lstrip(trigger).lstrip(" "), "", {}, 0)
								if str(message.content).startswith(trigger):
									await use(message, cmd, bot._codes[cmd]["prefix"]+trigger)
						else:
							trigger=await replaces(str(bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"]), message, message.guild, message.content.lstrip(str(bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"])).lstrip(" "), "", {}, 0)
							if str(message.content).startswith(trigger):
								await use(message, cmd, bot._codes[cmd]["prefix"]+bot._codes[cmd]["name"])
	if bot._self:
		client.run(bot._token, bot=False)
	else:
		client.run(bot._token)