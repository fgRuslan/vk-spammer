#!/usr/bin/python
# -*- coding: cp1251 -*-
#-*- coding utf8 -*-
# Author: https://vk.com/id181265169

import vk, urllib.request, urllib.error, urllib.parse, json, random, time

config = {}

try:
	exec(compile(open("config.py", "rb").read(), "config.py", 'exec'), config)
except IOError:
	print("Нету файла конйфигурации, чтобы его создать, запустите файл auth.py")
	quit(1)

url = "https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqyrnABp8ncuU&username=%s&password=%s" % (config['username'], config['password'])

try:
    r = urllib.request.urlopen(url)
except urllib.error.HTTPError:
    print("Не получилось авторизоваться (возможно неправильно указаны логин или пароль)")
    quit(1)

r = r.read()
token = json.loads(r)["access_token"] 
session = vk.Session(access_token = token)
api = vk.API(session)

foo = ["1", "2", "3", "4", "5"]

victim = input("Victim id: ")
r = api.users.get(user_ids = victim, fields = "id", v = 5.38)
r = r[0]["uid"]
victim = r

def mainloop():
    while(1):
        time.sleep(2)
        r = api.messages.send(peer_id = victim, message = random.choice(foo), v = 5.38)
        pass

mainloop()
