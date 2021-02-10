#!/usr/bin/python
# Author: https://vk.com/id181265169
# https://github.com/fgRuslan/vk-spammer

import vk, urllib.request, urllib.error, urllib.parse, json, random, time
import threading
import sys

import os
import platform
import json

HOME_PATH = os.path.expanduser("~")
SPAMMER_PATH = os.path.join(HOME_PATH + "/" + ".vk-spammer/")

if not os.path.exists(SPAMMER_PATH):
	os.mkdir(SPAMMER_PATH)

API_VERSION = 5.73

DELAY = 4 # Количество секунд задержки

auth_data = {}

# -------------------------------------------
# Сообщения, которые будет отправлять спаммер
messages = []

if os.path.exists(SPAMMER_PATH + "messages.txt"):
	with open(SPAMMER_PATH + "messages.txt") as f:
		for line in f:
			messages.append(line)
else:
	messages = [
	    "hi",
	    "2",
	    "3",
	    "fuck",
	    "5"
	]
# -------------------------------------------

def do_save_auth_data():
	with open(SPAMMER_PATH + "auth.dat", "w+") as f:
		json.dump(auth_data, f)
	f.close()

def load_auth_data():
	global auth_data
	if os.path.exists(SPAMMER_PATH + "auth.dat"):
		f = open(SPAMMER_PATH + "auth.dat", 'r')
		obj = json.load(f)
		auth_data = obj
		f.close()
		return True
	else:
		return False
	
class MainThread(threading.Thread):
	def run(self):
		print("-" * 4)
		print("Delay: ", args.delay)
		print("-" * 4)
		DELAY = args.delay
		while(True):
			try:
				msg = random.choice(messages)
				r = vk.messages.send(peer_id = victim, message = msg, v = API_VERSION)
				print("Sent ", msg)
				time.sleep(DELAY)
			except Exception as e:
				print(e)
				pass

def main():
	try:
		thread = MainThread()
		thread.daemon = True
		thread.start()

		while thread.is_alive():
			thread.join(1)
	except KeyboardInterrupt:
		print("Ctrl+C pressed...")
		sys.exit(1)

import argparse
parser = argparse.ArgumentParser(description='Spam settings:')
parser.add_argument(
    '-d',
    '--delay',
    type=int,
    default=4,
    help='Delay (default: 4)'
)
parser.add_argument('-e', '--editmessages', action='store_true', help='Use this argument to edit the message list')
parser.add_argument('-r', '--removedata', action='store_true', help='Use this argument to delete auth data (login, password)')
args = parser.parse_args()

if(args.editmessages):
	if platform.system() == "Windows":
		os.system("notepad.exe " + SPAMMER_PATH + "messages.txt")
	if platform.system() == "Linux":
		os.system("nano " + SPAMMER_PATH + "messages.txt")
	print("Please restart vk-spammer to reload the message list")
	exit(0)

if(args.removedata):
	print("Removing existing auth data...")
	os.remove(SPAMMER_PATH + "auth.dat")

load_result = load_auth_data()
if(load_result == False):
	username = input("Login: ")
	password = input("Password: ")
	save_auth_data = input("Save this auth data? (Y/n): ")

	if(save_auth_data == "Y" or save_auth_data == "y" or save_auth_data == ""):
		auth_data['username'] = username
		auth_data['password'] = password
		do_save_auth_data()
else:
	print("Got auth data from settings")
	username = auth_data['username']
	password = auth_data['password']
url = "https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqyrnABp8ncuU&username=%s&password=%s" % (username, password)

try:
    r = urllib.request.urlopen(url)
except urllib.error.HTTPError:
    print("Не удалось залогиниться, возможно вы ввели неправильный пароль")
    quit(1)

r = r.read()
token = json.loads(r)["access_token"]
session = vk.Session(access_token = token)
vk = vk.API(session)

victim = input("User id: ")

victim = victim.split("/")
victim = victim[len(victim) - 1]

if victim.isdigit():
	victim = victim
else:
	print("Resolving screen name...")
	r = vk.utils.resolveScreenName(screen_name = victim, v = API_VERSION)
	victim = r["object_id"]
	print("It is: " + str(victim))

r = vk.users.get(user_id = victim, fields = "id", v = API_VERSION)
r = r[0]["id"]

victim = r

main()
