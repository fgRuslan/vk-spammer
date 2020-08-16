#!/usr/bin/python
# Author: https://vk.com/id181265169

import vk, urllib.request, urllib.error, urllib.parse, json, random, time

config = {}

try:
	exec(compile(open("config.py", "rb").read(), "config.py", 'exec'), config)
except IOError:
	print("���� ����� �������������, ����� ��� �������, ��������� ���� auth.py")
	quit(1)

url = "https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqyrnABp8ncuU&username=%s&password=%s" % (config['username'], config['password'])

try:
    r = urllib.request.urlopen(url)
except urllib.error.HTTPError:
    print("�� ���������� �������������� (�������� ����������� ������� ����� ��� ������)")
    quit(1)

r = r.read()
token = json.loads(r)["access_token"] 
session = vk.Session(access_token = token)
vk = vk.API(session)

foo = ["hi", "2", "3", "fuck", "5"]

# print (foo)

victim = input("Victim id: ")

r = vk.users.get(user_id = victim, fields = "id", v = 5.73)
r = r[0]["id"]

victim = r

def mainloop():
	try:
		while(1):
			time.sleep(7)
			r = vk.messages.send(peer_id = victim, message = random.choice(foo), v = 5.73)
			print()
			print("wait...")
			time.sleep(3)
			print("done  ",random.choice(foo))
			pass
	except:
		mainloop()

mainloop()
