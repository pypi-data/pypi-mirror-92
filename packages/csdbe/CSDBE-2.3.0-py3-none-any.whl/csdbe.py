_stat=[False,"watch","статус"]
_costat="online"
_fprefix="$"
_functions=[]

def funcprefix(prefix="$"):
	global _fprefix
	_fprefix=prefix

def function(name=None, code=""):
	if name is None:
		print("Укажите имя функции с кодом: "+code)
	else:
		_functions.append([name,code])

def status(type="watch",name="статус"):
	global _stat
	_stat=[True,type,name]

def costatus(type="online"):
	try:
		import discord
	except:
		import os
		os.system("pip install discord")
	if type in ["online","offline","idle","dnd"]:
		exec("global _costat\n_costat=discord.Status."+type)
	else:
		print("Указан неправильный ко статус бота")
		exec("global _costat\n_costat=discord.Status."+_costat)

_codown=0
class _variables():
	def __init__(self):
		self.path=None
		self.data={"server":{}, "global":{}}
		self.vars={}
	def save(self):
		import json
		if self.path is not None:
			json.dump(self.data,open(self.path,"w"))
	def load(self):
		import json
		self.data={"server":{}, "global":{}}
		if self.path is not None:
			try:
				self.data=json.load(open(self.path,"r"))
			except:
				with open(self.path,"w") as f:
						f.write("{}")
_Vars=_variables()
def path(path=None):
	import json
	if path is not None:
		_Vars.path=path
		_Vars.load()
	else:
		if self.path is not None:
			_Vars.path=path
			_Vars.load()
		else:
			print("У вас не указан путь к файлу с переменными!\nИспользуйте: `path(путь к файлу)`")
def var(name,new):
	_Vars.vars[name]=new
def _getVar(type,id,name):
	try:
		return _Vars.data[type][str(id)][name]
	except:
		return "empty"
def _setVar(type,id,name,data):
	_Vars.data[type][str(id)][name]=data
_commdprefix=""
class command:
	comms=[]
	def __init__(self,name=None,code=None):
		if name is not None:
			self.name=name
		else:
			print(f"Вы не указали тригер у комманды, тригер был выбран программой: dbd.cmd{len(command.comms)}")
			self.name=f"dbd.cmd{len(command.comms)}"
		if code is not None:
			self.code=code
		else:
			self.code=""
		self.error=None
		self.err="print"
		self.vars={}
		self.split=[]
		self.reactions={}
		self.waitfor=""
		self.cooldown={}
		self.cderror="Кулдаун"
		command.comms.append(self)
	def add(self,code=None):
		if code is not None:
			self.code=self.code+code
		else:
			print("Вы не указали код!")

class event:
	evnts=[]
	def __init__(self,name=None,code=None):
		if name is not None:
			self.name=name
			if code is not None:
				self.code=code
			else:
				self.code=""
			self.error=None
			self.err="print"
			self.vars={}
			self.split=[]
			command.comms.append(self)
		else:
			print("Вы не указали эвент")
	def add(self,code=None):
		if code is not None:
			self.code=self.code+code
		else:
			print("Вы не указали код!")

def cogs(path=None):
	if path is not None:
		import os
		files_path = [os.path.abspath(x) for x in os.listdir(path)]
		paths=[]
		for pathd in files_path:
			pathf=pathd.split("/")
			pathd=pathd.replace(pathf[-1],path+"/"+pathf[-1])
			paths.append(pathd)
		try:
			import importlib.util
		except:
			import os
			os.system("pip install importlib.util")
		for path in paths:
			if path.endswith(".py"):
				spec = importlib.util.spec_from_file_location("module.name", path)
				m = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(m)
				for v in dir(m):
					if not v.startswith("_"):
						try:
							exec(f"command(m.{v}.name,m.{v}.code)")
						except:
							pass

def cog(path=None):
	if path is None:
		print("У вас не указан путь к когу!")
	else:
		try:
			import importlib.util
		except:
			import os
			os.system("pip install importlib.util")
		spec = importlib.util.spec_from_file_location("module.name", path)
		m = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(m)
		for v in dir(m):
			if not v.startswith("_"):
				try:
					exec(f"command(m.{v}.name,m.{v}.code)")
				except:
					pass

def cmdprefix(prefix=None):
	global _commdprefix
	if prefix is not None:
		_commdprefix=prefix

def start(token,help_type="none",help_trigger=None):
	import os
	import random
	import json
	try:
		import requests
	except:
		os.system("pip install requests")
	try:
		import asyncio
	except:
		os.system("pip install asyncio")
	try:
		import discord
		from discord.ext import commands
	except:
		os.system("pip install discord")
	try:
		from googletrans import Translator
	except:
		os.system("pip install googletrans")
	if help_type not in ["no","none","color","advance","ultra"]:
		print("Укажите (no, none, color, advance или ultra) в help_type!")
	else:
		ver=str(discord.__version__).split(".")
		err=0
		if int(ver[0])<1:
			print("У вас установлена старая версия дискорд модуля, сейчас начнётся установка новой!")
			os.system("pip uninstall discord")
			os.system("pip install discord")
			err=1
		if int(ver[1])<6 and err!=1:
			print("У вас установлена старая версия дискорд модуля, сейчас начнётся установка новой!")
			os.system("pip uninstall discord")
			os.system("pip install discord")
		client=commands.Bot(command_prefix="dbd.",intents=discord.Intents.all())
		
		@client.event
		async def on_ready():
			if _stat[0]:
				if _stat[1] in ["play","watch","listen","stream"]:
					if _stat[1]=="play":
						await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,name=_stat[2]),status=_costat)
					elif _stat[1]=="watch":
						await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=_stat[2]),status=_costat)
					elif _stat[1]=="listen":
						await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=_stat[2]),status=_costat)
					elif _stat[1]=="stream":
						await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,name=_stat[2]),status=_costat)
					print(f"🄲🅂🄳🄱🄴 🄼🄾🄳🅄🄻🄴\n--------------------\nХостинг: локальный\n--------------------\nИмя: {client.user.name}\n--------------------\nИнтенты: включены\n--------------------\nСтатус: {_stat[1].replace('play','Играет в ').replace('watch','Смотрит ').replace('listen','Слушает ').replace('stream','Стримит ')}{_stat[2]}")
				else:
					print(f"🄲🅂🄳🄱🄴 🄼🄾🄳🅄🄻🄴\n--------------------\nХостинг: локальный\n--------------------\nИмя: {client.user.name}\n--------------------\nИнтенты: включены\n❌Указан несуществующий тип статуса: {_stat[1]}\nСтатусы: play, watch, listen, stream")
			else:
				print(f"🄲🅂🄳🄱🄴 🄼🄾🄳🅄🄻🄴\n--------------------\nХостинг: локальный\n--------------------\nИмя: {client.user.name}\n--------------------\nИнтенты: включены")
			global _codown
			while True:
				_codown+=1
				await asyncio.sleep(1)

		@client.event
		async def on_message(message):
			global _commdprefix
			global _codown
			global _fprefix
			for g in client.guilds:
				for v in _Vars.vars:
					if not g.id.__str__() in _Vars.data:
						_Vars.data["server"][g.id.__str__()]=_Vars.vars
					else:
						for me in _Vars.data:
							try:
								_Vars.data["server"][me][v]
							except:
								_Vars.data["server"][me][v]=_Vars.vars[v]
				for m in g.members:
					for v in _Vars.vars:
						if not m.id.__str__() in _Vars.data:
							_Vars.data["global"][m.id.__str__()]=_Vars.vars
						else:
							for me in _Vars.data:
								try:
									_Vars.data["global"][me][v]
								except:
									_Vars.data["global"][me][v]=_Vars.vars[v]
								
			if message.author.id!=client.user.id:
				cmms=""
				def translate(cde):
					translator=Translator()
					re=cde
					while "#trans[" in re:
						cde=cde.split("#trans[")
						cde=cde[1].split("]")
						n=cde[0]
						cde=cde[0].split(";")
						lang=cde[0].replace('ua','uk')
						result=0
						while result==0:
							try:
								result = translator.translate(cde[1], cde[0])
								re=re.replace(f"#trans[{n}]",result.text)
							except:
								re=re
					return re
				for cmd in command.comms:
					if help_type=="advance":
						cmms=cmms+f"Имя: `{cmd.name.replace('#cmdprefix#',_commdprefix)}`\nКод `{cmd.code}`\n"
					elif help_type=="color":
						cmms=cmms+f"Имя: `{cmd.name.replace('#cmdprefix#',_commdprefix)}`\n"
					else:
						cmms=cmms+cmd.name.replace("#cmdprefix#",_commdprefix)+"\n"
					while len(cmms)>1024:
						cmms=cmms[:1021]
						cmms+="..."
					ex=False
					cde=str(cmd.code)
					for f in _functions:
						cde=cde.replace(f[0],f[1])
					global _codown
					try:
						cmd.cooldown[str(message.author.id)]
					except:
						cmd.cooldown[str(message.author.id)]=_codown
					def math(cde):
						while "#math[" in cde:
							tl=cde.split("#math[")
							tl=tl[1]
							tl=tl.split("]")[0]
							try:
								cde=cde.replace(f"#math[{tl}]",str(eval(tl)))
							except Exception as e:
								print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#math[{tl}]`\nПодробнее: {e}")
								break
						while "#replaceText[" in cde:
							tool=cde.split("#replaceText[")[1]
							tool=tool.split("]")[0]
							re=tool
							tool=tool.split(";")
							tool=tool[0].replace(tool[1],tool[2])
							try:
								cde=cde.replace(f"#replaceText[{re}]",tool)
							except Exception as e:
								print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#replaceText[{re}]`\nПодробнее: {e}")
								break
						return cde
					def getEmbed(cd):
						re=cd
						col=discord.Color.orange()
						try:
							while "#color[" in re:
								color=cd.split("#color[")
								color=color[1]
								color=color.split("]")
								color=color[0]
								n=color
								color=translate(color)
								try:
									rgb=list(int(color[i:i+2], 16) for i in (0, 2, 4))
									col=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
									re=re.replace(f"#color[{n}]","")
								except:
									pass
							while "#embed[" in re :
								emb=re.split("#embed[")
								emb=emb[1]
								emb=translate(emb)
								emb=emb.split("]")
								emb=emb[0]
								n=emb
								emb=emb.split(";")
								try:
									re=re.replace(f"#embed[{n}]","")
									emb=discord.Embed(title=emb[0].replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"),description=emb[1].replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"),color=col)
								except:
									re=re.replace(f"#embed[{n}]","")
									emb=discord.Embed(title=emb[0].replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"),description=emb[1].replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"),color=col)
							while "#footer[" in re:
								footer=re.split("#footer[")
								footer=footer[1]
								footer=footer.split("]")
								footer=footer[0]
								n=footer
								footer=translate(footer)
								footer=footer.split(";")
								try:
									re=re.replace(f"#footer[{n}]","")
									if len(footer)==1:
										emb.set_footer(text=footer[0])
									elif len(footer)==2:
										emb.set_footer(text=footer[0], icon_url=footer[1])
								except:
									pass
							while "#author[" in re :
								author=re.split("#author[")
								author=author[1]
								author=author.split("]")
								author=author[0]
								n=author
								author=translate(author)
								author=author.split(";")
								try:
									re=re.replace(f"#author[{n}]","")
									if len(author)==1:
										emb.set_author(name=author[0])
									elif len(author)==2:
										emb.set_author(name=author[0], icon_url=author[1])
								except:
									pass
							while "#field[" in re :
								field=re.split("#field[")
								field=field[1]
								field=field.split("]")
								field=field[0]
								n=field
								field=translate(field)
								field=field.split(";")
								try:
									re=re.replace(f"#field[{n}]","")
									if len(field)==1:
										emb.add_field(name=field[0].replace("#n","\n"),value="",inline=True)
									elif len(field)==2:
										emb.add_field(name=field[0].replace("#n","\n"), value=field[1].replace("#n","\n"),inline=True)
									elif len(field)==3:
										emb.add_field(name=field[0].replace("#n","\n"), value=field[1].replace("#n","\n"),inline=field[2])
								except:
									pass
							while "#image[" in re :
								image=re.split("#image[")
								image=image[1]
								image=image.split("]")
								image=image[0]
								n=image
								image=translate(image)
								try:
									re=re.replace(f"#image[{n}]","")
									emb.set_image(url=image)
								except:
									pass
							while "#thumb[" in re:
								thumb=re.split("#thumb[")
								thumb=thumb[1]
								thumb=thumb.split("]")
								thumb=thumb[0]
								n=thumb
								thumb=translate(thumb)
								try:
									re=re.replace(f"#thumb[{n}]","")
									emb.set_thumbnail(url=thumb)
								except:
									pass
							return ["embed=",emb]
						except:
							ee=1
							return["say=",re]
					if "$typing(" in cde:
						need=cde.split("$typing(")
						need=need[1].split(")")
						n=need[0]
						if "$case" in cde:
							trig=str(cmd.name).replace("#cmdprefix#",_commdprefix).lower()
							trig=trig.replace("#serverID",str(message.guild.id))
							trig=trig.replace("#authorID",str(message.author.id))
							while "#getGlobalVar[" in trig:
								tl2=trig.split("#getGlobalVar[")[1]
								re=tl2.split("]")[0]
								
								tl2=tl2.split("]")[0]
								tl=tl2.split(";")
								try:
									trig=trig.replace(f"#getGlobalVar[{tl2}]",str(_getVar(tl[0],int(tl[1]),tl[2])))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getGlobalVar[{re}]`\nПодробнее: {e}")
									break
							if str(str(message.content).lower()).startswith(trig):
								if _codown<cmd.cooldown[str(message.author.id)]:
									tool=math(cmd.cderror)
									tool=getEmbed(tool)
									if tool[0]=="embed=":
										await message.channel.send(embed=tool[1])
									elif tool[0]=="say=":
										await message.channel.send(tool[1].replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"))
								else:
									ex=True
									cde=cde.replace(f"$typing({n})","")
									async with message.channel.typing():
										await asyncio.sleep(int(n))
									cde=str(cmd.code).replace("$case","")
									
						elif "$messageHas(" in cde:
							m=cde.split("$messageHas(")
							m=m[1].split(")")[0]
							m=m.replace("#serverID",str(message.guild.id))
							m=m.replace("#authorID",str(message.author.id))
							while "#getGlobalVar[" in m:
								tl2=m.split("#getGlobalVar[")[1]
								re=tl2.split("]")[0]
								tl2=tl2.split("]")[0]
								tl=tl2.split(";")
								try:
									m=m.replace(f"#getGlobalVar[{tl2}]",str(_getVar(tl[0],int(tl[1]),tl[2])))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getGlobalVar[{re}]`\nПодробнее: {e}")
									break
							if m in str(message.content):
								if _codown<cmd.cooldown[str(message.author.id)]:
									tool=math(cmd.cderror)
									tool=getEmbed(tool)
									if tool[0]=="embed=":
										await message.channel.send(embed=tool[1])
									elif tool[0]=="say=":
										await message.channel.send(tool[1].replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"))
								else:
									ex=True
									cde=cde.replace(f"$typing({n})","")
									async with message.channel.typing():
										await asyncio.sleep(int(n))
									cde=cde.replace(f"$messageHas({m})","")
						else:
							trig=str(cmd.name).replace("#cmdprefix#",_commdprefix)
							trig=trig.replace("#serverID",str(message.guild.id))
							trig=trig.replace("#authorID",str(message.author.id))
							while "#getGlobalVar[" in trig:
								tl2=trig.split("#getGlobalVar[")[1]
								re=tl2.split("]")[0]
								tl2=tl2.split("]")[0]
								tl=tl2.split(";")
								try:
									trig=trig.replace(f"#getGlobalVar[{tl2}]",str(_getVar(tl[0],int(tl[1]),tl[2])))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getGlobalVar[{re}]`\nПодробнее: {e}")
									break
							if str(str(message.content)).startswith(trig):
								if _codown<cmd.cooldown[str(message.author.id)]:
									tool=math(cmd.cderror)
									tool=getEmbed(tool)
									if tool[0]=="embed=":
										await message.channel.send(embed=tool[1])
									elif tool[0]=="say=":
										await message.channel.send(tool[1].replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"))
								else:
									ex=True
									cde=cde.replace(f"$typing({n})","")
									async with message.channel.typing():
										await asyncio.sleep(int(n))
								
					else:
						if "$case" in cde:
							trig=str(cmd.name).replace("#cmdprefix#",_commdprefix).lower()
							trig=trig.replace("#serverID",str(message.guild.id))
							trig=trig.replace("#authorID",str(message.author.id))
							while "#getGlobalVar[" in trig:
								tl2=trig.split("#getGlobalVar[")[1]
								re=tl2.split("]")[0]
								tl2=tl2.split("]")[0]
								tl=tl2.split(";")
								try:
									trig=trig.replace(f"#getGlobalVar[{tl2}]",str(_getVar(tl[0],int(tl[1]),tl[2])))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getGlobalVar[{re}]`\nПодробнее: {e}")
									break
							if str(str(message.content).lower()).startswith(trig):
								if _codown<cmd.cooldown[str(message.author.id)]:
									tool=math(cmd.cderror)
									tool=getEmbed(tool)
									if tool[0]=="embed=":
										await message.channel.send(embed=tool[1])
									elif tool[0]=="say=":
										await message.channel.send(tool[1].replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"))
								else:
									ex=True
									cde=str(cmd.code).replace("$case","")
						elif "$messageHas(" in cde:
							m=cde.split("$messageHas(")
							m=m[1].split(")")[0]
							m=m.replace("#serverID",str(message.guild.id))
							m=m.replace("#authorID",str(message.author.id))
							while "#getGlobalVar[" in m:
								tl2=m.split("#getGlobalVar[")[1]
								re=tl2.split("]")[0]
								tl2=tl2.split("]")[0]
								tl=tl2.split(";")
								try:
									m=m.replace(f"#getGlobalVar[{tl2}]",str(_getVar(tl[0],int(tl[1]),tl[2])))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getGlobalVar[{re}]`\nПодробнее: {e}")
									break
							if m in str(message.content):
								if _codown<cmd.cooldown[str(message.author.id)]:
									tool=math(cmd.cderror)
									tool=getEmbed(tool)
									if tool[0]=="embed=":
										await message.channel.send(embed=tool[1])
									elif tool[0]=="say=":
										await message.channel.send(tool[1].replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"))
								else:
									ex=True
									cde=cde.replace(f"$messageHas({m})","")
						else:
							trig=str(cmd.name).replace("#cmdprefix#",_commdprefix)
							trig=trig.replace("#serverID",str(message.guild.id))
							trig=trig.replace("#authorID",str(message.author.id))
							while "#getGlobalVar[" in trig:
								tl2=trig.split("#getGlobalVar[")[1]
								re=tl2.split("]")[0]
								tl2=tl2.split("]")[0]
								tl=tl2.split(";")
								try:
									trig=trig.replace(f"#getGlobalVar[{tl2}]",str(_getVar(tl[0],int(tl[1]),tl[2])))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getGlobalVar[{re}]`\nПодробнее: {e}")
									break
							if str(str(message.content)).startswith(trig):
								if _codown<cmd.cooldown[str(message.author.id)]:
									tool=math(cmd.cderror)
									tool=getEmbed(tool)
									if tool[0]=="embed=":
										await message.channel.send(embed=tool[1])
									elif tool[0]=="say=":
										await message.channel.send(tool[1].replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#cooldownLeft",str(cmd.cooldown[str(message.author.id)]-_codown)).replace("#n","\n"))
								else:
									ex=True
					if ex:
						_everyone = "";
						for m in message.guild.members:
							if m == message.guild.members[0]:
								_everyone += str( m.id )
							else:
								_everyone += ","+ str( m.id )
						cde=cde.replace("#everyone", _everyone )
						cde=cde.replace("#serverID",str(message.guild.id))
						cde=cde.replace("#authorID",str(message.author.id))
						cde=cde.replace("#authorAvatar",str(message.author.avatar_url))
						cde=cde.replace("#messageID","#msgID")
						def give_msg():
							arg=str(message.content).lstrip(cmd.name)
							arg=arg.replace("#messageID","#msgID")
							arg=arg.lstrip(" ")
							return arg
						def get_ments(cde):
							ment=[]
							mstr=""
							for m in message.mentions:
								if m==message.mentions[0]:
									mstr=mstr+str(m.id)
								else:
									mstr=mstr+","+str(m.id)
								ment.append(str(m.id))
							for me in range(1,len(ment)+1):
								if f"#mentioned[{me};yes]" in cde:
									cde=str(cde).replace(f"#mentioned[{me};yes]",ment[me-1])
								if f"#mentioned[{me}]" in cde:
									cde=str(cde).replace(f"#mentioned[{me}]",ment[me-1])
							try:
								n=str(cmd.code).split("#mentioned[")
								n=n[1]
								n=n[0]
							except:
								n=0
							if int(n)>len(ment):
								cde=str(cde).replace(f"#mentioned[{n};yes]",str(message.author.id))
								cde=str(cde).replace(f"#mentioned[{n}]","")
							cde=str(cde).replace("#mentioned",mstr)
							return str(cde)
						def get_nomentmsg(cde):
							noment=str(message.content).lstrip(cmd.name)
							for m in message.mentions:
								noment=noment.replace(m.mention,"")
							arg=noment.lstrip(" ")
							import re
							arg=re.sub('\s+',' ', arg)
							rga=arg.split(" ")
							if rga[0]=="":
								rga.remove("")
							for me in range(1,len(rga)+1):
								if f"#noMentionMessage[{me}]" in cde:
									cde=str(cde).replace(f"#noMentionMessage[{me}]",rga[me-1])
							try:
								n=str(cmd.code).split("#noMentionMessage[")
								n=n[1]
								n=n[0]
							except:
								n=0
							if int(n)>len(rga):
								cde=str(cde).replace(f"#noMentionMessage[{n}]","")
							cde=str(cde).replace("#noMentionMessage",arg)
							return str(cde)
						def get_msg(cde):
							cde=cde.replace("#messageID","#msgID")
							trig=str(cmd.name).replace("#cmdprefix#",_commdprefix)
							trig=trig.replace("#serverID",str(message.guild.id))
							trig=trig.replace("#authorID",str(message.author.id))
							while "#getGlobalVar[" in trig:
								tl2=trig.split("#getGlobalVar[")[1]
								re=tl2.split("]")[0]
								tl2=tl2.split("]")[0]
								tl=tl2.split(";")
								try:
									trig=trig.replace(f"#getGlobalVar[{tl2}]",str(_getVar(tl[0],int(tl[1]),tl[2])))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getGlobalVar[{re}]`\nПодробнее: {e}")
									break
							if "$case" in cmd.code:
								arg=str(message.content).lstrip(str(trig).lower())
							else:
								arg=str(message.content).lstrip(str(trig).lower())
							arg=arg.lstrip(" ")
							rga=arg.split(" ")
							if rga[0]=="":
								rga.remove("")
							for me in range(1,len(rga)+1):
								if f"#message[{me}]" in cde:
									cde=str(cde).replace(f"#message[{me}]",rga[me-1])
							try:
								n=str(cmd.code).split("#message[")
								n=n[1]
								n=n[0]
							except:
								n=0
							if int(n)>len(rga):
								cde=str(cde).replace(f"#message[{n}]","")
							cde=str(cde).replace("#message",arg)
							return str(cde)
						cde=cde.replace("$eval",give_msg())
						cde=get_ments(cde)
						cde=cde.replace("#membersCount",str(len(message.guild.members)-1))
						mems=0-len(client.guilds)
						for guild in client.guilds:
							mems+=len(guild.members)
						cde=cde.replace("#allMembersCount",str(mems))
						if "#noMentionMessage" in cmd.code:
							cde=get_nomentmsg(cde)
						if "#message" in cmd.code:
							cde=get_msg(cde)
						if "#mentioned" in cmd.code:
							cde=get_ments(cde)
						cde=cde.replace("#authorID",str(message.author.id))
						cde=cde.replace("#triggerID",str(message.id))
						while "#randomText[" in cde:
							tl=cde.split("#randomText[")
							tl=tl[1]
							tl=tl.split("]")
							tl=tl[0]
							tl=tl.split(";")
							r=[]
							re=""
							for an in tl:
								r.append(an)
								re=re+";"+an
							re=re.lstrip(";")
							cde=cde.replace(f"#randomText[{re}]",random.choice(r))
						while "#random[" in cde:
							tl=cde.split("#random[")
							tl=tl[1]
							tl=tl.split("]")
							tl=tl[0]
							tl=tl.split(";")
							cde=cde.replace(f"#random[{tl[0]};{tl[1]}]",str(random.randint(int(tl[0]),int(tl[1]))))
						def getEmbed(cd):
							re=cd
							col=discord.Color.orange()
							while "#color[" in re:
								color=re.split("#color[")
								color=color[1]
								color=color.split("]")
								color=color[0]
								n=color
								color=translate(color)
								try:
									rgb=list(int(color[i:i+2], 16) for i in (0, 2, 4))
									col=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
									re=re.replace(f"#color[{n}]","")
								except:
									pass
							while "#embed[" in re :
								emb=re.split("#embed[")
								emb=emb[1]
								emb=translate(emb)
								emb=emb.split("]")
								emb=emb[0]
								n=emb
								emb=emb.split(";")
								try:
									re=re.replace(f"#embed[{n}]","")
									emb=discord.Embed(title=emb[0].replace("#n","\n").replace("#message",give_msg()),description=emb[1].replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix),color=col)
								except:
									re=re.replace(f"#embed[{n}]","")
									emb=discord.Embed(title=emb[0].replace("#msgID",str(msg.id)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix),description=emb[1].replace("#message",give_msg()).replace("#msgID",str(msg.id)).replace("#waitForInfo",str(cmd.waitfor)).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix),color=col)
							while "#footer[" in re:
								footer=re.split("#footer[")
								footer=footer[1]
								footer=footer.split("]")
								footer=footer[0]
								n=footer
								footer=translate(footer)
								footer=footer.split(";")
								try:
									re=re.replace(f"#footer[{n}]","")
									if len(footer)==1:
										emb.set_footer(text=footer[0])
									elif len(footer)==2:
										emb.set_footer(text=footer[0], icon_url=footer[1])
								except:
									pass
							while "#author[" in re :
								author=re.split("#author[")
								author=author[1]
								author=author.split("]")
								author=author[0]
								n=author
								author=translate(author)
								author=author.split(";")
								try:
									re=re.replace(f"#author[{n}]","")
									if len(author)==1:
										emb.set_author(name=author[0])
									elif len(author)==2:
										emb.set_author(name=author[0], icon_url=author[1])
								except:
									pass
							while "#field[" in re :
								field=re.split("#field[")
								field=field[1]
								field=field.split("]")
								field=field[0]
								n=field
								field=translate(field)
								field=field.split(";")
								try:
									re=re.replace(f"#field[{n}]","")
									if len(field)==1:
										emb.add_field(name=field[0].replace("#n","\n"),value="",inline=True)
									elif len(field)==2:
										emb.add_field(name=field[0].replace("#n","\n"), value=field[1].replace("#n","\n"),inline=True)
									elif len(field)==3:
										emb.add_field(name=field[0].replace("#n","\n"), value=field[1].replace("#n","\n"),inline=field[2])
								except:
									pass
							while "#image[" in re :
								image=re.split("#image[")
								image=image[1]
								image=image.split("]")
								image=image[0]
								n=image
								image=translate(image)
								try:
									re=re.replace(f"#image[{n}]","")
									emb.set_image(url=image)
								except:
									pass
							while "#thumb[" in re:
								thumb=re.split("#thumb[")
								thumb=thumb[1]
								thumb=thumb.split("]")
								thumb=thumb[0]
								n=thumb
								thumb=translate(thumb)
								try:
									re=re.replace(f"#thumb[{n}]","")
									emb.set_thumbnail(url=thumb)
								except:
									pass
							try:
								return ["embed=",emb]
							except:
								return ["say=",cd]
						def getAllVars(cde):
							while "#userID[" in cde:
								tl1=cde.split("#userID[")
								tl1=tl1[1]
								tl1=tl1.split("]")
								tl1=tl1[0]
								tl1=getAllVars(tl1)
								tl1=translate(tl1)
								nm=discord.utils.get(message.guild.members, name=tl1)
								try:
									nm=nm.id
								except:
									nm="empty"
								cde=cde.replace(f"#userID[{tl1}]",nm)
							while "#channelID[" in cde:
								try:
									tl1=cde.split("#channelID[")[1]
									tl1=tl1.split("]")[0]
									re=tl1
									tl1=getAllVars(tl1)
									tl1=translate(tl1)
									i=discord.utils.get(message.guild.channels, name=tl1)
									cde=cde.replace(f"#channelID[{tl1}]",str(i.id))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#channelID[{re}]`\nПодробнее: {e}")
									break
							while "#roleID[" in cde:
								try:
									tl1=cde.split("#roleID[")[1]
									tl1=tl1.split("]")[0]
									re=tl1
									tl1=getAllVars(tl1)
									tl1=translate(tl1)
									i=discord.utils.get(message.guild.roles, name=tl1)
									cde=cde.replace(f"#roleID[{tl1}]",str(i.id))
								except:
									cde=cde.replace(f"#roleID[{tl1}]","empty")
							while "#getLocalVar[" in cde:
								tl1=cde.split("#getLocalVar[")[1]
								re=tl1.split("]")[0]
								tl1=getAllVars(tl1)
								tl1=tl1.split("]")[0]
								try:
									cde=cde.replace(f"#getLocalVar[{re}]",cmd.vars[tl1])
								except:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getLocalVar[{re}]`\nПодробнее: {e}")
									break
							while "#getGlobalVar[" in cde:
								tl2=cde.split("#getGlobalVar[")[1]
								re=tl2.split("]")[0]
								tl2=getAllVars(tl2)
								tl2=tl2.split("]")[0]
								tl=tl2.split(";")
								try:
									cde=cde.replace(f"#getGlobalVar[{tl2}]",str(_getVar(tl[0],int(tl[1]),tl[2])))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#getGlobalVar[{re}]`\nПодробнее: {e}")
									break
							while "#userAvatar[" in cde:
								tl1=cde.split("#userAvatar[")
								tl1=tl1[1]
								tl1=tl1.split("]")
								tl1=tl1[0]
								tl1=getAllVars(tl1)
								tl1=translate(tl1)
								nm=discord.utils.get(message.guild.members, id=int(tl1))
								try:
									nm=nm.avatar_url
								except:
									nm="empty"
								cde=cde.replace(f"#userAvatar[{tl1}]",str(nm))
							while "#kot[" in cde:
								try:
									tl1=cde.split("#kot[")
									tl1=tl1[1]
									tl1=tl1.split("]")
									tl1=tl1[0]
									re=tl1
									tl1=getAllVars(tl1)
									tl1=translate(tl1)
									cde=cde.replace("#kot[{tl1}]",tl1[::-1])
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#kot[{re}]`\nПодробнее: {e}")
									break
							while "#roleName[" in cde:
								try:
									tl1=cde.split("#roleName[")[1]
									tl1=tl1.split("]")[0]
									re=tl1
									tl1=getAllVars(tl1)
									tl1=translate(tl1)
									i=discord.utils.get(message.guild.roles, name=tl1)
									cde=cde.replace(f"#roleName[{tl1}]",str(i.name))
								except:
									cde=cde.replace(f"#roleName[{tl1}]","empty")
							while "#username[" in cde:
								tl1=cde.split("#username[")
								tl1=tl1[1]
								tl1=tl1.split("]")
								tl1=tl1[0]
								tl1=getAllVars(tl1)
								tl1=translate(tl1)
								nm=discord.utils.get(message.guild.members, id=int(tl1))
								try:
									nm=nm.name
								except:
									nm="empty"
								cde=cde.replace(f"#username[{tl1}]",nm)
							while "#servername[" in cde:
								tl1=cde.split("#servername[")
								tl1=tl1[1]
								tl1=tl1.split("]")
								tl1=tl1[0]
								tl1=getAllVars(tl1)
								tl1=translate(tl1)
								nm=discord.utils.get(message.guild.members, id=int(tl1))
								try:
									nm=nm.display_name
								except:
									nm="empty"
								cde=cde.replace(f"#servername[{tl1}]",nm.replace(_fprefix,"#fprefix#"))
							while "#discriminator[" in cde:
								tl1=cde.split("#discriminator[")
								tl1=tl1[1]
								tl1=tl1.split("]")
								tl1=tl1[0]
								tl1=getAllVars(tl1)
								tl1=translate(tl1)
								nm=discord.utils.get(message.guild.members, id=int(tl1))
								try:
									nm=nm.discriminator
								except:
									nm="empty"
								cde=cde.replace(f"#discriminator[{tl1}]",nm)
							while "#categoryID[" in cde:
								try:
									tl1=cde.split("#categoryID[")
									tl1=tl1[1]
									tl1=tl1.split("]")
									tl1=tl1[0]
									re=tl1
									tl1=getAllVars(tl1)
									tl1=translate(tl1)
									i=discord.utils.get(message.guild.categories, name=tl1)
									cde=cde.replace(f"#categoryID[{tl1}]",str(i.id))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#categoryID[{re}]`\nПодробнее: {e}")
									break
							while "#len[" in cde:
								tl2=cde.split("#len[")[1]
								re=tl2.split("]")[0]
								tl2=tl2.split("]")[0]
								try:
									if tl2=="split":
										cde=cde.replace(f"#len[{tl2}]",str(len(cmd.split)))
									elif tl2=="reacts":
										cde=cde.replace(f"#len[{tl2}]",str(len(cmd.reactions)))
								except:
									cde=cde.replace(f"#len[{tl2}]","0")
									break
							while "#split[" in cde:
								tl2=cde.split("#split[")[1]
								re=tl2.split("]")[0]
								tl2=getAllVars(tl2)
								tl2=tl2.split("]")[0]
								try:
									cde=cde.replace(f"#split[{tl2}]",str(cmd.split[int(tl2)-1]))
								except:
									cde=cde.replace(f"#split[{tl2}]","")
									break
							while "#reacts[" in cde:
								tl2=cde.split("#reacts[")[1]
								re=tl2.split("]")[0]
								tl2=getAllVars(tl2)
								tl2=tl2.split("]")[0]
								try:
									cde=cde.replace(f"#reacts[{tl2}]",str(cmd.reactions[tl2]))
								except:
									cde=cde.replace(f"#reacts[{tl2}]","empty")
								break
							return cde
						def math(cde):
							while "#math[" in cde:
								tl=cde.split("#math[")
								tl=tl[1]
								tl=tl.split("]")[0]
								try:
									cde=cde.replace(f"#math[{tl}]",str(eval(tl)))
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#math[{tl}]`\nПодробнее: {e}")
									break
							while "#replaceText[" in cde:
								tool=cde.split("#replaceText[")[1]
								tool=tool.split("]")[0]
								re=tool
								tool=tool.split(";")
								tool=tool[0].replace(tool[1],tool[2])
								try:
									cde=cde.replace(f"#replaceText[{re}]",tool)
								except Exception as e:
									print(f"❌Ошибка\nКомманда: {cmd.name.replace('#cmdprefix#',_commdprefix)}\nФункция: `#replaceText[{re}]`\nПодробнее: {e}")
									break
							return cde
						cde=get_ments(cde=cde)
						cde=cde.split(_fprefix)
						if "" in cde:
							cde.remove("")
						code={}
						msg=""
						p=0
						trans=""
						for cd in cde:
							try:
								if p!=0:
									p-=1
								else:
									if cd.startswith("typeerror"):
										if cd[10:-1] in ["print","say"]:
											cmd.err=cd[10:-1]
										else:
											print("❌Указан несуществующий тип ошибки в `typeerror`\nТипы ошибки: print, say")
									elif cd.startswith("ban"):
										member=discord.utils.get(message.guild.members, id=int(cd[4:-1]))
										await member.ban(reason = "ban")
									elif cd.startswith("unban"):
										banned_users = await message.guild.bans()
										for ban_entry in banned_users:
											user = ban_entry.user
											if user.id==int(cd[6:-1]):
												await message.guild.unban(user)
									elif cd.startswith("botedit"):
										n=cd[8:-1].split(";")
										if n[0]=="name":
											await client.user.edit(username=n[1])
										elif n[0]=="avatar":
											with open(n[1], 'rb') as f:
												image = f.read()
												await client.user.edit(avatar=image)
									elif cd.startswith("cooldown"):
										tool=cd[9:-1].split(";")
										num=tool[0]
										text=cd[9:-1].replace(num+";","")
										if num[-1] == "s":
											cmd.cooldown[str(message.author.id)]=_codown+(int(num.replace( num[-1], "")))
										elif num[-1] == "m":
											cmd.cooldown[str(message.author.id)]=_codown+(int(num.replace( num[-1], "")*60))
										elif num[-1] == "h":
											cmd.cooldown[str(message.author.id)]=_codown+(int(num.replace( num[-1], "")*60*60))
										elif num[-1] == "d":
											cmd.cooldown[str(message.author.id)]=_codown+(int(num.replace( num[-1], "")*60*60*24))
										else:
											cmd.cooldown[str(message.author.id)]=_codown+int(num)
										cmd.cderror=text
									elif cd.startswith("print"):
										tool=getAllVars(cd[6:-1])
										tool=translate(tool)
										tool=math(tool)
										try:
											print(tool.replace("#msgID",str(msg.id)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix))
										except:
												print(tool.replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#message",give_msg()))
									elif cd.startswith("status"):
										st=cd[7:-1].split(";")
										if st[0] in ["play","watch","listen","stream"]:
											if st[0]=="play":
												await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,name=st[1]))
											elif st[0]=="watch":
												await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=st[1]))
											elif st[0]=="listen":
												await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=st[1]))
											elif st[0]=="stream":
												await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,name=st[1]))
										else:
											print(f"❌Ошибка\nКомманда: {cmd.name}\nФункция: `$status({cd[7:-1]})`\nПодробнее: Несуществующий тип статуса: {_stat[1]}\nСтатусы: play, watch, listen, stream")
									elif cd.startswith("deletemessage"):
										try:
											mes=await message.channel.fetch_message(int(cd[14:-1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor))))
										except:
											mes=await message.channel.fetch_message(int(cd[14:-1]))
										await mes.delete()
									elif cd.startswith("setGlobalVar"):
										v=getAllVars(cd[13:-1])
										v=math(v)
										v=v.split(";")
										_setVar(v[0],v[1],v[2],v[3])
									elif cd.startswith("setLocalVar"):
										v=getAllVars(cd[12:-1])
										v=math(v)
										v=v.split(";")
										cmd.vars[v[0]]=v[1]
									elif cd.startswith("forReactionAdd"):
										tool=cd[8:-1]
										tool=getAllVars(tool)
										tool=math(tool)
										tool=tool.split(";")
										try:
											reaction, user= await client.wait_for("reaction_add", timeout=int(tool[1]))
											cmd.waitfor=f"{reaction.emoji},{user.id}"
										except asyncio.TimeoutError:
											p+=int(tool[0])
									elif cd.startswith("forReactionRemove"):
										tool=cd[8:-1]
										tool=getAllVars(tool)
										tool=math(tool)
										tool=tool.split(";")
										try:
											reaction, user= await client.wait_for("reaction_remove", timeout=int(tool[1]))
											cmd.waitfor=f"{reaction.emoji},{user.id}"
										except asyncio.TimeoutError:
											p+=int(tool[0])
									elif cd.startswith("forMessage"):
										tool=cd[8:-1]
										tool=getAllVars(tool)
										tool=math(tool)
										tool=tool.split(";")
										try:
											mess = await client.wait_for("message", timeout=int(tool[1]))
											cmd.waitfor=f"{mess.content},{mess.author.id}"
										except asyncio.TimeoutError:
											p+=int(tool[0])
									elif cd.startswith("newChannel"):
										tool=cd[11:-1]
										tool=getAllVars(tool)
										tool=math(tool)
										tool=tool.split(";")
										if tool[0]=="text":
											if len(tool)==1:
												await message.guild.create_text_channel("Текст "+random.randint(1,9)+random.randint(1,9)+random.randint(1,9)+random.randint(1,9))
											elif len(tool)==2:
												await message.guild.create_text_channel(tool[1])
											elif len(tool)==3:
												catg = discord.utils.get(message.guild.categories, id=int(tool[2]))
												await message.guild.create_text_channel(tool[1],category=catg)
										elif tool[0]=="voice":
											if len(tool)==1:
												await message.guild.create_voice_channel("Текст "+random.randint(1,9)+random.randint(1,9)+random.randint(1,9)+random.randint(1,9))
											elif len(tool)==2:
												await message.guild.create_voice_channel(tool[1])
											elif len(tool)==3:
												catg = discord.utils.get(message.guild.categories, id=int(tool[2]))
												await message.guild.create_voice_channel(tool[1],category=catg)
									elif cd.startswith("onlyAdmin"):
										if not message.author.guild_permissions.administrator:
											tool=translate(cd[10:-1])
											tool=math(tool)
											tool=getAllVars(tool)
											tool=getEmbed(tool)
											if tool[0]=="embed=":
												msg=await message.channel.send(embed=tool[1])
											elif tool[0]=="say=":
												try:
													msg=await message.channel.send(tool[1].replace("#msgID",str(msg.id)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix))
												except:
													msg=await message.channel.send(tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#message",give_msg()))
											break
									elif cd.startswith("wait"):
										_time = cd[5:-1]
										if _time[-1] == "s":
											await asyncio.sleep(int(_time.replace( _time[-1], "")))
										elif _time[-1] == "m":
											await asyncio.sleep(int(_time.replace( _time[-1], ""))*60)
										elif _time[-1] == "h":
											await asyncio.sleep(int(_time.replace( _time[-1], ""))*60*60)
										elif _time[-1] == "d":
											await asyncio.sleep(int(_time.replace( _time[-1], ""))*60*60*24)
										else:
											await asyncio.sleep(int(_time))
									elif cd.startswith("reply"):
										tool=getAllVars(cd[6:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=tool.split(";")
										try:
											mesg=await message.channel.fetch_message(int(tool[0].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor))))
										except:
											mesg=await message.channel.fetch_message(int(tool[0].replace("#waitForInfo",str(cmd.waitfor))))
										try:
											msg=await message.channel.send("> "+str(mesg.content).replace('\n','\n> ')+"\n"+tool[1].replace("#msgID",str(msg.id)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix))
										except:
											msg=await message.channel.send("> "+str(mesg.content).replace('\n','\n> ')+"\n"+tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#message",give_msg()))
									elif cd.startswith("say"):
										tool=getAllVars(cd[4:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=getEmbed(tool)
										if tool[0]=="embed=":
											msg=await message.channel.send(embed=tool[1])
										elif tool[0]=="say=":
											try:
												msg=await message.channel.send(tool[1].replace("#msgID",str(msg.id)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix))
											except:
												msg=await message.channel.send(tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#message",give_msg()))
									elif cd.startswith("role"):
										tool=getAllVars(cd[5:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=tool.split(";")
										role = discord.utils.get(message.guild.roles, id=int(tool[2]))
										user=discord.utils.get(message.guild.members, id=int(tool[1]))
										if tool[0]=="give":
											await user.add_roles(role)
										elif tool[0]=="take":
											await user.remove_roles(role)
									elif cd.startswith("if"):
										v=cd[3:-1]
										v=getAllVars(v)
										v=math(v)
										tool=v.split(";")
										if "==" in tool[1]:
											t=tool[1].split("==")
											if t[0]==t[1]:
												t=True
											else:
												t=False
										elif "!=" in tool[1]:
											t=tool[1].split("!=")
											if t[0]!=t[1]:
												t=True
											else:
												t=False
										elif ">=" in tool[1]:
											t=tool[1].split(">=")
											if int(t[0])>=int(t[1]):
												t=True
											else:
												t=False
										elif "<=" in tool[1]:
											t=tool[1].split("<=")
											if int(t[0])<=int(t[1]):
												t=True
											else:
												t=False
										elif ">" in tool[1]:
											t=tool[1].split(">")
											if int(t[0])>int(t[1]):
												t=True
											else:
												t=False
										elif "<" in tool[1]:
											t=tool[1].split("<")
											if int(t[0])<int(t[1]):
												t=True
											else:
												t=False
										if t==False:
											p+=int(tool[0])
									elif cd.startswith("react"):
										reacts=str(cd[6:-1])
										reacts=getAllVars(reacts)
										reacts=math(reacts)
										reacts=reacts.split(";")
										try:
											mes=await message.channel.fetch_message(int(reacts[0].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor))))
										except:
											mes=await message.channel.fetch_message(int(reacts[0]))
										for react in reacts:
											if react!=reacts[0]:
												try:
													await mes.add_reaction(react)
												except:
													await message.channel.send(f"Не удалось добавить реакцию `{react}`!")
									elif cd.startswith("botquit"):
										await client.logout()
									elif cd.startswith("dm"):
										tool=cd[3:-1].split(";")
										user=discord.utils.get(message.guild.members, id=int(tool[0]))
										tool=getAllVars(cd[3:-1].replace(tool[0]+";",""))
										tool=math(tool)
										tool=getEmbed(tool)
										if tool[0]=="embed=":
											msg=await user.send(embed=tool[1])
										elif tool[0]=="say=":
											try:
												msg=await user.send(tool[1].replace("#msgID",str(msg.id)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix))
											except:
												msg=await user.send(tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#message",give_msg()))
									elif cd.startswith("addEmoji"):
										tool=cd[9:-1].split(";")
										nm=tool[0]
										img=cd[9:-1].replace(nm,"")
										await client.create_custom_emoji(message.guild, name=nm, image=img)
									elif cd.startswith("delChannel"):
										tool=cd[11:-1]
										tool=getAllVars(tool)
										tool=math(tool)
										ch=discord.utils.get(message.guild.channels, id=int(tool))
										await ch.delete()
									elif cd.startswith("split"):
										tool=cd[6:-1]
										tool=getAllVars(tool)
										tool=math(tool)
										try:
											tool=tool.replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",cmd.waitfor)
										except:
											tool=tool.replace("#waitForInfo",cmd.waitfor)
										tool=tool.split(";")
										cmd.split=tool[0].split(tool[1])
									elif cd.startswith("unreact"):
										unreacts=str(cd[8:-1]).split(";")
										mes=await message.channel.fetch_message(int(unreacts[0]))
										user=discord.utils.get(message.guild.members, id=int(unreacts[1]))
										for unreact in unreacts:
											if unreact!=unreacts[0] and unreact!=unreacts[1]:
												try:
													await mes.remove_reaction(unreact,user)
												except:
													await message.channel.send(f"Не удалось удалить реакцию  `{react}`!")
									elif cd.startswith("clear"):
										await message.channel.purge(limit=int(cd[6:-1])+1)
									elif cd.startswith("error"):
										tool=cd[6:-1].split(";")
										n=tool[0]
										tool=cd[6:-1].replace(f"{n};","")
										tool=getAllVars(tool)
										g=getEmbed(tool)
										if g[0]=="embed=":
											cmd.error=[int(n),tool]
										elif g[0]=="say=":
											try:
												cmd.error=[int(n),tool.replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix)]
											except:
												cmd.error=[int(n),tool.replace("#n","\n").replace("#hostTime",str(_codown)).replace("#message",give_msg())]
									elif cd.startswith("hasReact"):
										tool=str(cd[9:-1]).split(";")
										users=[]
										mes=await msg.channel.fetch_message(int(tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor))))
										for reaction in mes.reactions:
											if reaction.emoji == tool[3]:
												users = await reaction.users().flatten()
												users.remove(client.user)
											usrs=[]
											for user in users:
												usrs.append(str(user.id))
											if tool[2] not in usrs:
												p+=int(tool[0])
									elif cd.startswith("hasNoReact"):
										tool=str(cd[11:-1]).split(";")
										users=[]
										mes=await msg.channel.fetch_message(int(tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor))))
										for reaction in mes.reactions:
											if reaction.emoji == tool[3]:
												users = await reaction.users().flatten()
												users.remove(client.user)
											usrs=[]
											for user in users:
												usrs.append(str(user.id))
											if tool[2] in usrs:
												p+=int(tool[0])
									elif cd.startswith("needArg"):
										tool=getAllVars(cd[8:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=tool.split(";")
										t=give_msg().split(" ")
										if int(tool[1])>len(t) or int(tool[1])<0:
											p+=int(tool[0])
										else:
											if t[int(tool[1])-1]=="":
												p+=int(tool[0])
									elif cd.startswith("getReacts"):
										tool=str(cd[10:-1])
										tool=getAllVars(tool)
										tool=math(tool)
										users=[]
										mes=await message.channel.fetch_message(int(tool.replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor))))
										cmd.reactions={}
										for reaction in mes.reactions:
											users = await reaction.users().flatten()
											users.remove(client.user)
											usrs=""
											for user in users:
												if user==users[0]:
													usrs=usrs+str(user.id)
												else:
													usrs=usrs+","+str(user.id)
											if users!=[]:
												cmd.reactions[str(reaction.emoji)]=usrs
									elif cd.startswith("needNoArg"):
										tool=getAllVars(cd[10:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=tool.split(";")
										t=give_msg().split(" ")
										if int(tool[1])>len(t) or int(tool[1])<0:
											t
										else:
											if t[int(tool[1])-1]!="":
												p+=int(tool[0])
									elif cd.startswith("hasContent"):
										tool=getAllVars(cd[11:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=tool.split(";")
										if str(tool[2]) in str(tool[1]) != True:
											p+=int(tool[0])
									elif cd.startswith("hasNoContent"):
										tool=getAllVars(cd[13:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=tool.split(";")
										if tool[2] in str(tool[1]):
											p+=int(tool[0])
									elif cd.startswith("hasRole"):
										tool=getAllVars(cd[8:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=tool.split(";")
										role = discord.utils.get(message.guild.roles, id=int(tool[2]))
										user=discord.utils.get(message.guild.members, id=int(tool[1]))
										if role not in user.roles:
											p+=int(tool[0])
									elif cd.startswith("hasNoRole"):
										tool=getAllVars(cd[8:-1])
										tool=translate(tool)
										tool=math(tool)
										tool=tool.split(";")
										role = discord.utils.get(message.guild.roles, id=int(tool[2]))
										user=discord.utils.get(message.guild.members, id=int(tool[1]))
										if role in user.roles:
											p+=int(tool[0])
									elif cd.startswith("kick"):
										member=discord.utils.get(message.guild.members, id=int(cd[5:-1]))
										await member.kick(reason="")
									elif cd.startswith("quit"):
										break
									elif cd.startswith("edit"):
										tool=getAllVars(cd[5:-1])
										tool=getEmbed(tool)
										if tool[0]=="embed=":
											await msg.edit(embed=tool[1])
										elif tool[0]=="say=":
											try:
												await msg.edit(content=tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix))
											except:
												await msg.edit(content=tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#message",give_msg()))
									elif cd.startswith("loop"):
										tool=cd[5:-1].split(";")
										n=tool[0]
										func=cd[5:-1].replace(f"{n};","").replace("#fprefix#",_fprefix)
										func=func.split("&")
										done=0
										br=0
										while done!=int(n) and br==0:
											done+=1
											pl=0
											for cm in func:
												if pl!=0:
													pl-=1
												else:
													if cm.startswith("typeerror"):
														if cm[10:-1] in ["print","say"]:
															cmd.err=cm[10:-1]
														else:
															print("❌Указан несуществующий тип ошибки в `typeerror`\nТипы ошибки: print, say")
													elif cm.startswith("botedit"):
														n=cm[8:-1].split(";")
														if n[0]=="name":
															await client.user.edit(username=n[1])
														elif n[0]=="avatar":
															with open(n[1], 'rb') as f:
																image = f.read()
																await client.user.edit(avatar=image)
													elif cm.startswith("cooldown"):
														tool=cm[9:-1].split(";")
														num=tool[0]
														text=cd[9:-1].replace(num+";","")
														if num[-1] == "s":
															cmd.cooldown[str(message.author.id)]=_codown+(int(num.replace( num[-1], "")))
														elif num[-1] == "m":
															cmd.cooldown[str(message.author.id)]=_codown+(int(num.replace( num[-1], "")*60))
														elif num[-1] == "h":
															cmd.cooldown[str(message.author.id)]=_codown+(int(num.replace( num[-1], "")*60*60))
														elif num[-1] == "d":
															cmd.cooldown[str(message.author.id)]=_codown+(int(num.replace( num[-1], "")*60*60*24))
														else:
															cmd.cooldown[str(message.author.id)]=_codown+int(num)
														cmd.cderror=text
													elif cm.startswith("print"):
														tool=getAllVars(cm[6:-1])
														tool=translate(tool)
														tool=math(tool)
														try:
															print(tool.replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#fprefix#",_fprefix).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n"))
														except:
																print(tool.replace("#n","\n").replace("#hostTime",str(_codown)).replace("#hostTime",str(_codown)).replace("#message",give_msg()))
													elif cm.startswith("status"):
														st=cm[7:-1].split(";")
														if st[0] in ["play","watch","listen","stream"]:
															if st[0]=="play":
																await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,name=st[1]))
															elif st[0]=="watch":
																await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=st[1]))
															elif st[0]=="listen":
																await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=st[1]))
															elif st[0]=="stream":
																await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,name=st[1]))
														else:
															print(f"❌Ошибка\nКомманда: {cmd.name}\nФункция: `$status({cm[7:-1]})`\nПодробнее: Несуществующий тип статуса: {_stat[1]}\nСтатусы: play, watch, listen, stream")
													elif cm.startswith("deletemessage"):
														try:
															mes=await message.channel.fetch_message(int(cm[14:-1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor))))
														except:
															mes=await message.channel.fetch_message(int(cm[14:-1]))
														await mes.delete()
													elif cm.startswith("setGlobalVar"):
														v=getAllVars(cm[13:-1])
														v=math(v)
														v=v.split(";")
														_setVar(v[0],v[1],v[2],v[3])
													elif cm.startswith("setLocalVar"):
														v=getAllVars(cm[12:-1])
														v=math(v)
														v=v.split(";")
														cmd.vars[v[0]]=v[1]
													elif cm.startswith("forReactionAdd"):
														tool=cm[8:-1]
														tool=getAllVars(tool)
														tool=math(tool)
														tool=tool.split(";")
														try:
															reaction, user= await client.wait_for("reaction_add", timeout=int(tool[1]))
															cmd.waitfor=f"{reaction.emoji},{user.id}"
														except asyncio.TimeoutError:
															pl+=int(tool[0])
													elif cm.startswith("forReactionRemove"):
														tool=cm[8:-1]
														tool=getAllVars(tool)
														tool=math(tool)
														tool=tool.split(";")
														try:
															reaction, user= await client.wait_for("reaction_remove", timeout=int(tool[1]))
															cmd.waitfor=f"{reaction.emoji},{user.id}"
														except asyncio.TimeoutError:
															pl+=int(tool[0])
													elif cm.startswith("forMessage"):
														tool=cm[8:-1]
														tool=getAllVars(tool)
														tool=math(tool)
														tool=tool.split(";")
														try:
															mess = await client.wait_for("message", timeout=int(tool[1]))
															cmd.waitfor=f"{mess.content},{mess.author.id}"
														except asyncio.TimeoutError:
															pl+=int(tool[0])
													elif cm.startswith("newChannel"):
														tool=cm[11:-1]
														tool=getAllVars(tool)
														tool=math(tool)
														tool=tool.split(";")
														if tool[0]=="text":
															if len(tool)==1:
																await message.guild.create_text_channel("Текст "+random.randint(1,9)+random.randint(1,9)+random.randint(1,9)+random.randint(1,9))
															elif len(tool)==2:
																await message.guild.create_text_channel(tool[1])
															elif len(tool)==3:
																catg = discord.utils.get(message.guild.categories, id=int(tool[2]))
																await message.guild.create_text_channel(tool[1],category=catg)
														elif tool[0]=="voice":
															if len(tool)==1:
																await message.guild.create_voice_channel("Текст "+random.randint(1,9)+random.randint(1,9)+random.randint(1,9)+random.randint(1,9))
															elif len(tool)==2:
																await message.guild.create_voice_channel(tool[1])
															elif len(tool)==3:
																catg = discord.utils.get(message.guild.categories, id=int(tool[2]))
																await message.guild.create_voice_channel(tool[1],category=catg)
													elif cm.startswith("onlyAdmin"):
														if not message.author.guild_permissions.administrator:
															tool=translate(cm[10:-1])
															tool=math(tool)
															tool=getAllVars(tool)
															tool=getEmbed(tool)
															if tool[0]=="embed=":
																msg=await message.channel.send(embed=tool[1])
															elif tool[0]=="say=":
																try:
																	msg=await message.channel.send(tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)))
																except:
																	msg=await message.channel.send(tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#message",give_msg()))
															break
													elif cm.startswith("wait"):
														_time = cm[5:-1]
														if _time[-1] == "s":
															await asyncio.sleep(int(_time.replace( _time[-1], "")))
														elif _time[-1] == "m":
															await asyncio.sleep(int(_time.replace( _time[-1], ""))*60)
														elif _time[-1] == "h":
															await asyncio.sleep(int(_time.replace( _time[-1], ""))*60*60)
														elif _time[-1] == "d":
															await asyncio.sleep(int(_time.replace( _time[-1], ""))*60*60*24)
														else:
															await asyncio.sleep(int(_time))
													elif cm.startswith("reply"):
														tool=getAllVars(cm[6:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=tool.split(";")
														try:
															mesg=await message.channel.fetch_message(int(tool[0].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor))))
														except:
															mesg=await message.channel.fetch_message(int(tool[0].replace("#waitForInfo",str(cmd.waitfor))))
														try:
															msg=await message.channel.send("> "+str(mesg.content).replace('\n','\n> ')+"\n"+tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)))
														except:
															msg=await message.channel.send("> "+str(mesg.content).replace('\n','\n> ')+"\n"+tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#message",give_msg()))
													elif cm.startswith("say"):
														tool=getAllVars(cm[4:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=getEmbed(tool)
														if tool[0]=="embed=":
															msg=await message.channel.send(embed=tool[1])
														elif tool[0]=="say=":
															try:
																msg=await message.channel.send(tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)))
															except:
																msg=await message.channel.send(tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#hostTime",str(_codown)).replace("#message",give_msg()))
													elif cm.startswith("role"):
														tool=getAllVars(cm[5:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=tool.split(";")
														role = discord.utils.get(message.guild.roles, id=int(tool[2]))
														user=discord.utils.get(message.guild.members, id=int(tool[1]))
														if tool[0]=="give":
															await user.add_roles(role)
														elif tool[0]=="take":
															await user.remove_roles(role)
													elif cm.startswith("if"):
														v=cm[3:-1]
														v=getAllVars(v)
														v=math(v)
														tool=v.split(";")
														if "==" in tool[1]:
															t=tool[1].split("==")
															if t[0]==t[1]:
																t=True
															else:
																t=False
														elif "!=" in tool[1]:
															t=tool[1].split("!=")
															if t[0]!=t[1]:
																t=True
															else:
																t=False
														elif ">=" in tool[1]:
															t=tool[1].split(">=")
															if int(t[0])>=int(t[1]):
																t=True
															else:
																t=False
														elif "<=" in tool[1]:
															t=tool[1].split("<=")
															if int(t[0])<=int(t[1]):
																t=True
															else:
																t=False
														elif ">" in tool[1]:
															t=tool[1].split(">")
															if int(t[0])>int(t[1]):
																t=True
															else:
																t=False
														elif "<" in tool[1]:
															t=tool[1].split("<")
															if int(t[0])<int(t[1]):
																t=True
															else:
																t=False
														if t==False:
															pl+=int(tool[0])
													elif cm.startswith("react"):
														reacts=str(cm[6:-1])
														reacts=getAllVars(reacts)
														reacts=math(reacts)
														reacts=reacts.split(";")
														try:
															mes=await message.channel.fetch_message(int(reacts[0].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor))))
														except:
															mes=await message.channel.fetch_message(int(reacts[0]))
														for react in reacts:
															if react!=reacts[0]:
																try:
																	await mes.add_reaction(react)
																except:
																	await message.channel.send(f"Не удалось добавить реакцию `{react}`!")
													elif cm.startswith("botquit"):
														await client.logout()
													elif cm.startswith("dm"):
														tool=cm[3:-1].split(";")
														user=discord.utils.get(message.guild.members, id=int(tool[0]))
														tool=getAllVars(cm[3:-1].replace(tool[0]+";",""))
														tool=math(tool)
														tool=getEmbed(tool)
														if tool[0]=="embed=":
															msg=await user.send(embed=tool[1])
														elif tool[0]=="say=":
															try:
																msg=await user.send(tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)))
															except:
																msg=await user.send(tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#message",give_msg()))
													elif cm.startswith("addEmoji"):
														tool=cm[9:-1].split(";")
														nm=tool[0]
														img=cm[9:-1].replace(nm,"")
														await client.create_custom_emoji(message.guild, name=nm, image=img)
													elif cm.startswith("delChannel"):
														tool=cm[11:-1]
														tool=getAllVars(tool)
														tool=math(tool)
														ch=discord.utils.get(message.guild.channels, id=int(tool))
														await ch.delete()
													elif cm.startswith("split"):
														tool=cm[6:-1]
														tool=getAllVars(tool)
														tool=math(tool)
														try:
															tool=tool.replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",cmd.waitfor)
														except:
															tool=tool.replace("#waitForInfo",cmd.waitfor)
														tool=tool.split(";")
														cmd.split=tool[0].split(tool[1])
													elif cm.startswith("ban"):
														member=discord.utils.get(message.guild.members, id=int(cm[4:-1]))
														await member.ban(reason = "ban")
													elif cm.startswith("unban"):
														banned_users = await message.guild.bans()
														for ban_entry in banned_users:
															user = ban_entry.user
															if user.id==int(cm[6:-1]):
																await message.guild.unban(user)
													elif cm.startswith("unreact"):
														unreacts=str(cm[8:-1]).split(";")
														mes=await message.channel.fetch_message(int(unreacts[0]))
														user=discord.utils.get(message.guild.members, id=int(unreacts[1]))
														for unreact in unreacts:
															if unreact!=unreacts[0] and unreact!=unreacts[1]:
																try:
																	await mes.remove_reaction(unreact,user)
																except:
																	await message.channel.send(f"Не удалось удалить реакцию  `{react}`!")
													elif cm.startswith("clear"):
														await message.channel.purge(limit=int(cm[6:-1])+1)
													elif cm.startswith("error"):
														tool=cm[6:-1].split(";")
														n=tool[0]
														tool=cm[6:-1].replace(f"{n};","")
														tool=getAllVars(tool)
														g=getEmbed(tool)
														if g[0]=="embed=":
															cmd.error=[int(n),tool]
														elif g[0]=="say=":
															try:
																cmd.error=[int(n),tool.replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown))]
															except:
																cmd.error=[int(n),tool.replace("#n","\n").replace("#hostTime",str(_codown)).replace("#message",give_msg())]
													elif cm.startswith("hasReact"):
														tool=str(cm[9:-1]).split(";")
														users=[]
														mes=await msg.channel.fetch_message(int(tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor))))
														for reaction in mes.reactions:
															if reaction.emoji == tool[3]:
																users = await reaction.users().flatten()
																users.remove(client.user)
															usrs=[]
															for user in users:
																usrs.append(str(user.id))
															if tool[2] not in usrs:
																pl+=int(tool[0])
													elif cm.startswith("hasNoReact"):
														tool=str(cm[11:-1]).split(";")
														users=[]
														mes=await msg.channel.fetch_message(int(tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor))))
														for reaction in mes.reactions:
															if reaction.emoji == tool[3]:
																users = await reaction.users().flatten()
																users.remove(client.user)
															usrs=[]
															for user in users:
																usrs.append(str(user.id))
															if tool[2] in usrs:
																pl+=int(tool[0])
													elif cm.startswith("needArg"):
														tool=getAllVars(cm[8:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=tool.split(";")
														t=give_msg().split(" ")
														if int(tool[1])>len(t) or int(tool[1])<0:
															pl+=int(tool[0])
														else:
															if t[int(tool[1])-1]=="":
																pl+=int(tool[0])
													elif cm.startswith("getReacts"):
														tool=str(cm[10:-1])
														tool=getAllVars(tool)
														tool=math(tool)
														users=[]
														mes=await message.channel.fetch_message(int(tool.replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor))))
														cmd.reactions={}
														for reaction in mes.reactions:
															users = await reaction.users().flatten()
															users.remove(client.user)
															usrs=""
															for user in users:
																if user==users[0]:
																	usrs=usrs+str(user.id)
																else:
																	usrs=usrs+","+str(user.id)
															if users!=[]:
																cmd.reactions[str(reaction.emoji)]=usrs
													elif cm.startswith("needNoArg"):
														tool=getAllVars(cm[10:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=tool.split(";")
														t=give_msg().split(" ")
														if int(tool[1])>len(t) or int(tool[1])<0:
															t
														else:
															if t[int(tool[1])-1]!="":
																pl+=int(tool[0])
													elif cm.startswith("hasContent"):
														tool=getAllVars(cm[11:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=tool.split(";")
														if str(tool[2]) in str(tool[1]) != True:
															pl+=int(tool[0])
													elif cm.startswith("hasNoContent"):
														tool=getAllVars(cm[13:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=tool.split(";")
														if tool[2] in str(tool[1]):
															pl+=int(tool[0])
													elif cm.startswith("hasRole"):
														tool=getAllVars(cm[8:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=tool.split(";")
														role = discord.utils.get(message.guild.roles, id=int(tool[2]))
														user=discord.utils.get(message.guild.members, id=int(tool[1]))
														if role not in user.roles:
															pl+=int(tool[0])
													elif cm.startswith("hasNoRole"):
														tool=getAllVars(cm[8:-1])
														tool=translate(tool)
														tool=math(tool)
														tool=tool.split(";")
														role = discord.utils.get(message.guild.roles, id=int(tool[2]))
														user=discord.utils.get(message.guild.members, id=int(tool[1]))
														if role in user.roles:
															pl+=int(tool[0])
													elif cm.startswith("kick"):
														member=discord.utils.get(message.guild.members, id=int(cm[5:-1]))
														await member.kick(reason="")
													elif cm.startswith("quit"):
														break
													elif cm.startswith("edit"):
														tool=getAllVars(cm[5:-1])
														tool=getEmbed(tool)
														if tool[0]=="embed=":
															await msg.edit(embed=tool[1])
														elif tool[0]=="say=":
															try:
																await msg.edit(content=tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)))
															except:
																await msg.edit(content=tool[1].replace("#n","\n").replace("#hostTime",str(_codown)).replace("#message",give_msg()))
													else:
														print(f"❌Ошибка\nКомманда: {cmd.name}\nФункции `${cd}` не существует".replace("#msgID","#messageID"))
									else:
										print(f"❌Ошибка\nКомманда: {cmd.name}\nФункции `${cd}` не существует".replace("#msgID","#messageID"))
								_Vars.save()
							except Exception as e:
								if not cd.startswith("forReactionAdd") or cd.startswith("forReactionRemove") or cd.startswith("forMessage"):
									if cmd.err=="print":
										print(f"❌Ошибка\nКомманда: {cmd.name}\nФункция: `${cd}`\nПодробнее: {e}".replace("#msgID","#messageID"))
									elif cmd.err=="say":
										await message.channel.send(embed=discord.Embed(title="❌Ошибка",description="Комманда: {cmd.name}\nФункция: `${cd}`\nПодробнее: {e}",color=Color("FF0000")))
									try:
										cmd.error[0]
										cmd.error[1]
									except:
										cmd.error=None
									if cmd.error is not None:
										if cmd.error[1]!="":
											if cmd.error[0]!=0:
												tool=getAllVars(cmd.error[1])
												tool=getEmbed(tool)
												if tool[0]=="embed=":
													await message.channel.send(embed=tool[1])
												elif tool[0]=="say=":
													try:
														await message.channel.send(tool[1].replace("#msgID",str(msg.id)).replace("#hostTime",str(_codown)).replace("#waitForInfo",str(cmd.waitfor)).replace("#message",give_msg()).replace("#n","\n").replace("#hostTime",str(_codown)))
													except:
														await message.channel.send(tool[1].replace("#n#","\n").replace("#message#",give_msg()))
												cmd.error[0]-=1
				htr=help_trigger
				if htr is None:
					htr="<@"+str(client.user.id)+">"
				if message.content.startswith(str(htr)):
					if help_type!="no" and help_type!="ultra":
						if _commdprefix=="":
							await message.channel.send(embed=discord.Embed(title="CSDBE.PY HELP",description=f"Комманды:\n{cmms}",color=discord.Color.blurple()))
						else:
							await message.channel.send(embed=discord.Embed(title="CSDBE.PY HELP",description=f"Префикс: {_commdprefix}\nКомманды:\n{cmms}",color=discord.Color.blurple()))
					elif help_type=="ultra" and help_type!="no":
						userid = str(message.author.id)
						previuspage = '◀️'
						nextpage = '▶️'
						page = 0
						descript=[]
						for cos in command.comms:
							r = lambda: random.randint(0,255)
							h='%02X%02X%02X' % (r(),r(),r())
							rgb=list(int(h[i:i+2], 16) for i in (0, 2, 4))
							col=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
							d=f"Код: ```{cos.code}```"
							while len(d)>1024:
								d=d[:1021]
								d+="..."
							t=f"Комманда: `{cos.name.replace('#cmdprefix#',_commdprefix)}`"
							while len(t)>1024:
								t=t[:1021]
								t+="..."
							descript.append(discord.Embed(title=t,description=d,color=col))
						embed=descript[page]
						mesg = await message.channel.send(embed=embed)
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
								embed=descript[page]
								await mesg.remove_reaction(r,message.author)
								await mesg.edit(embed=embed)
							except asyncio.TimeoutError:
								try:
									await mesg.remove_reaction(previuspage,client.user)
								except:
									pass
								try:
									await mesg.remove_reaction(nextpage,client.user)
								except:
									pass
								embed.set_footer(text="Время вышло")
								await mesg.edit(embed=embed)
								loopclose = 1
		client.run(token)