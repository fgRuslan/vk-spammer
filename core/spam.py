#!/usr/bin/python
# Author: https://vk.com/id181265169
# https://github.com/fgRuslan/vk-spammer

import vk, urllib.request, urllib.error, urllib.parse, json, random, time
import threading
import sys

API_VERSION = 5.73

DELAY = 4 # Количество секунд задержки


# -------------------------------------------
# Сообщения, которые будет отправлять спаммер
messages = [
	"hi",
	"2",
	"3",
	"fuck",
	"5"
]
# -------------------------------------------


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
    '--delay',
    type=int,
    default=4,
    help='Delay (default: 4)'
)
args = parser.parse_args()

username = input("Login: ")
password = input("Password: ")

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

try:
	temp = int(victim)
except Exception as e:
	print("Resolving screen name...")
	r = vk.utils.resolveScreenName(screen_name = victim, v = API_VERSION)
	victim = r["object_id"]
	print("It is: " + victim)

r = vk.users.get(user_id = victim, fields = "id", v = API_VERSION)
r = r[0]["id"]

victim = r

main()
