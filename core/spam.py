#!/usr/bin/python
# Author: https://vk.com/id181265169
# https://github.com/fgRuslan/vk-spammer

import urllib.request, urllib.error, urllib.parse, json, random, time
from requests.utils import requote_uri
from python3_anticaptcha import ImageToTextTask, errors
import threading
import sys

import os
import platform
import json
import vk_api

HOME_PATH = os.path.expanduser("~")
SPAMMER_PATH = os.path.join(HOME_PATH + "/" + ".vk-spammer/")

SPAMMING_ONLINE_USERS = False
SPAMMING_FRIENDS = False
USE_TOKEN = False

ANTICAPTCHA_KEY = ''

username = None
password = None

# Если директории с настройками спамера нет, создать её
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
			messages.append(line.encode('cp1251').decode('utf-8'))
else:
	messages = [
		"hi",
		"2",
		"3",
		"fuck",
		"5"
	]
	# Создаём пустой файл messages.txt
	open(SPAMMER_PATH + "messages.txt", 'a').close()
# -------------------------------------------
# Сохраняем введённые данные авторизации в файл auth.dat
def do_save_auth_data():
	with open(SPAMMER_PATH + "auth.dat", "w+") as f:
		json.dump(auth_data, f)
	f.close()

# Загружаем данные авторизации из файла auth.dat
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
# -------------------------------------------

class MainThread(threading.Thread):
	def run(self):
		print("-" * 4)
		print("Delay: ", args.delay)
		print("-" * 4)
		print("Press Ctrl+C to stop")
		DELAY = args.delay
		if SPAMMING_ONLINE_USERS:
			friend_list = vk_session.method('friends.search', {'user_id': MyID, "is_closed": "false",
			"can_access_closed": "true", 'can_write_private_message': 1, 'count': 1000,
			'fields': 'online'})['items']
			while(True):
				try:
					msg = random.choice(messages)
					for friend in friend_list:
						if friend['online'] == 0:
							continue
						victim_id = int(friend['id'])
						r = vk.messages.send(user_id = victim_id, message = msg, v = API_VERSION, random_id = random.randint(0,10000))
						print("Sent ", msg, " to ", victim_id)
					time.sleep(DELAY)
				except vk_api.exceptions.ApiError as e:
					print("ОШИБКА!")
					print(e)
				except Exception as e:
					print(e)
					pass
		elif SPAMMING_FRIENDS:
			friend_list = vk_session.method('friends.search', {'user_id': MyID, "is_closed": "false",
			"can_access_closed": "true", 'can_write_private_message': 1, 'count': 1000,
			'fields': 'online'})['items']
			while(True):
				try:
					msg = random.choice(messages)
					for friend in friend_list:
						victim_id = int(friend['id'])
						if(hasattr(friend, 'deactivated')):
							continue
						r = vk.messages.send(user_id = victim_id, message = msg, v = API_VERSION, random_id = random.randint(0,10000))
						print("Sent ", msg, " to ", victim_id)
					time.sleep(DELAY)
				except vk_api.exceptions.ApiError as e:
					print("ОШИБКА!")
					print(e)
				except Exception as e:
					print(e)
					pass
		else:
			while(True):
				try:
					msg = random.choice(messages)
					r = vk.messages.send(user_id = victim, message = msg, v = API_VERSION, random_id = random.randint(0,10000))
					print("Sent ", msg)
					time.sleep(DELAY)
				except vk_api.exceptions.ApiError as e:
					print("ОШИБКА!")
					print(e)
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

# -------------------------------------------
# Парсер аргументов
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
# -------------------------------------------

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


# Пытаемся загрузить данные авторизации из файла
# Если не удалось, просим их ввести
load_result = load_auth_data()
if(load_result == False):
	username = input("Login (или токен): ")
	if len(username) == 85:
		USE_TOKEN = True
	if not USE_TOKEN:
		password = input("Password: ")
	else:
		password = ''
	save_auth_data = input("Save this auth data? (Y/n): ")

	if(save_auth_data == "Y" or save_auth_data == "y" or save_auth_data == ""):
		auth_data['username'] = username
		auth_data['password'] = password
		do_save_auth_data()
else:
	print("Got auth data from settings")
	if len(username) == 85:
		USE_TOKEN = True
	username = auth_data['username']
	password = auth_data['password']

def captha_handler(captcha):
	if ANTICAPTCHA_KEY == '':
		url = captcha.get_url()
		solution = input("Решите капчу ({0}): ".format(captcha.get_url))
		return captcha.try_again(solution)
	key = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY, save_format='const').captcha_handler(captcha_link=captcha.get_url())
	return captcha.try_again(key['solution']['text'])

# -------------------------------------------
# Логинимся и получаем токен
vk_session = None

anticaptcha_api_key = input("API ключ от anti-captcha.com (оставьте пустым если он не нужен): ")
if anticaptcha_api_key == '':
	if USE_TOKEN:
		vk_session = vk_api.VkApi(token=username)
	else:
		vk_session = vk_api.VkApi(login=username, password=password)
else:
	ANTICAPTCHA_KEY = anticaptcha_api_key
	if USE_TOKEN:
		vk_session = vk_api.VkApi(token=username, captcha_handler=captha_handler)
	else:
		vk_session = vk_api.VkApi(login=username, password=password, captcha_handler=captha_handler)

try:
	vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()


# -------------------------------------------
# Преобразовываем введённый id пользователя в цифровой формат

victim = input("User id: ")

if victim == "#online":
	SPAMMING_ONLINE_USERS = True
elif victim == "#friends":
	SPAMMING_FRIENDS = True
else:

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
# -------------------------------------------
# Запускатор главного потока
main()
