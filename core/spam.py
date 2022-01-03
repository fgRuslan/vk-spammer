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

# Данные из Kate mobile
API_ID = "2685278"
tmp = "hHbJug59sKJie78wjrH8"

ANTICAPTCHA_KEY = ''

username = None
password = None

# Если директории с настройками спамера нет, создать её
if not os.path.exists(SPAMMER_PATH):
	os.mkdir(SPAMMER_PATH)

API_VERSION = 5.131

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
	return False
def remove_auth_data():
	print("Удаляю текущие данные авторизации...")
	os.remove(SPAMMER_PATH + "auth.dat")
# -------------------------------------------

class MainThread(threading.Thread):
	def run(self):
		if(len(messages) == 0):
			print("Список сообщений пуст. Запустите спамер с параметром -e (vk-spammer -e) чтобы ввести список сообщений.")
			sys.exit(0)
		print("-" * 4)
		print("Задержка: ", args.delay)
		print("-" * 4)
		print("Нажмите Ctrl+C чтобы остановить")
		
		DELAY = args.delay
		if SPAMMING_ONLINE_USERS:
			friend_list = vk_session.method('friends.search', {"is_closed": "false",
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
		elif SPAMMING_FRIENDS:
			friend_list = vk_session.method('friends.search', {"is_closed": "false",
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
		else:
			while(True):
				try:
					msg = random.choice(messages)
					print(victim)
					r = vk.messages.send(peer_id = victim, message = msg, v = API_VERSION, random_id = random.randint(0,10000))
					print("Sent ", msg)
					time.sleep(DELAY)
				except vk_api.exceptions.ApiError as e:
					print("ОШИБКА!")
					print(e)
				except Exception as e:
					print(e)

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
	remove_auth_data()


# Пытаемся загрузить данные авторизации из файла
# Если не удалось, просим их ввести
load_result = load_auth_data()
if(load_result == False):
	username = input("Login (или токен): ")
	if len(username) == 85:
		USE_TOKEN = True
	if not USE_TOKEN:
		password = input("Пароль: ")
	else:
		password = ''
	save_auth_data = input("Сохранить эти данные авторизации? (Y/n): ")

	if(save_auth_data == "Y" or save_auth_data == "y" or save_auth_data == ""):
		auth_data['username'] = username
		auth_data['password'] = password
		do_save_auth_data()
else:
	print("Данные авторизации получены из настроек")
	username = auth_data['username']
	password = auth_data['password']
	if len(username) == 85:
		USE_TOKEN = True

def captcha_handler(captcha):
	if ANTICAPTCHA_KEY == '':
		solution = input("Решите капчу ({0}): ".format(captcha.get_url()))
		return captcha.try_again(solution)
	key = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY, save_format='const').captcha_handler(captcha_link=captcha.get_url())
	return captcha.try_again(key['solution']['text'])

def auth_handler():
	key = input("Введите код подтверждения: ")
	remember_device = True
	return key, remember_device


# -------------------------------------------
# Логинимся и получаем токен
vk_session = None

anticaptcha_api_key = input("API ключ от anti-captcha.com (оставьте пустым если он не нужен): ")
if anticaptcha_api_key == '':
	if USE_TOKEN:
		vk_session = vk_api.VkApi(token=username, auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
	else:
		vk_session = vk_api.VkApi(username, password, auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
else:
	ANTICAPTCHA_KEY = anticaptcha_api_key
	if USE_TOKEN:
		vk_session = vk_api.VkApi(token=username, captcha_handler=captcha_handler, auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
	else:
		vk_session = vk_api.VkApi(username, password, captcha_handler=captcha_handler, auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)

try:
	vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()


# -------------------------------------------
# Преобразовываем введённый id пользователя в цифровой формат

print()
print("Укажите id жертвы.")
print("Чтобы спамить своим друзьям, укажите #friends.")
print("Чтобы спамить друзьям, которые сейчас в сети, укажите #online.")
print("Чтобы спамить в беседу, укажите её id как в примере: #c375")
print("375 - это id беседы")
print()
victim = input("id жертвы: ")

if victim == "#online":
	SPAMMING_ONLINE_USERS = True
elif victim == "#friends":
	SPAMMING_FRIENDS = True
elif victim.startswith("#c"):
	victim = victim.replace("#c", "")
	victim = int(victim) + 2000000000
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
