# Vk-spammer
Просто спамер...
Установка спамера:

```
pip install vk-spammer
```

Если вы на Windows, то можно скачать спамер без установки python.
Для этого перейдите в раздел [Actions](https://github.com/fgRuslan/vk-spammer/actions/workflows/pyinstaller.yml) этого репозитория, выберите самый свежий билд и скачайте vk-spammer из раздела Artifacts.

### Запуск

```
vk-spammer
```

В скрипте укажите свой логин и пароль от ВК. Далее, Вас спросят, хотите ли вы сохранить свои данные для входа, чтобы в будущем не вводить их снова.
Также, вас попросят ввести ключ от API антикапчи (anti-captcha.com). Если вы не знаете, что это такое, то оставьте его пустым.
После всего этого вас спросят id пользователя, которого вы хотите заспамить. Атака началась.
Также, можно указать, чтобы скрипт писал сообщения всем друзьям, либо только тем друзьям, которые сейчас в сети. Для этого, вместо id жертвы, укажите #friends или #online.

Чтобы удалить данные авторизации, запустите спамер с параметром -r.

```
vk-spammer -r
```

### Изменение сообщений

Чтобы изменить сообщения, которые спамер будет отправлять, запустите спамер с аргументом -e (--editmessages)

```
vk-spammer -e
```

Это запустит текстовый редактор (На Windows это будет блокнот, на Linux это будет nano).
Каждая строчка текста будет отдельным сообщением.
P.S. Чтобы выйти из nano, нажмите Ctrl+O.

### Изменение задержки

По умолчанию, задержка между сообщениями равна 4 секундам. Чтобы поменять этот параметр, при запуске спамера, укажите количество секунд задержки через параметр -d (--delay)

```
vk-spammer -d 4
```

Удачи.

По всем вопросам обращаться сюда: [Мой VK](https://vk.com/id181265169). Пожалуйста, пишите только после прочтения README.
