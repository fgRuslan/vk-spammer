REM =====================================
REM =      Скрипт сборки спамера        =
REM = Запускать из Windows, результат   =
REM = cборки будет находиться в папке   =
REM =          dist/spam.exe            =
REM =====================================
@echo off
pip install setuptools pyinstaller
pip install -r requirements.txt
pyinstaller --exclude-module _bootlocale --onefile core/spam.py --hidden-import=vk_api --hidden-import=python3-anticaptcha --hidden-import=requests