# Telegram bot
## Описание:
Telegram bot работает с API сервиса GitHub.

Даёт возможность:
- делать запросы к базе данных конкретного пользователя;
- получать оповещение об обновлении статуса событий в профиле

Конфиденциальные данные хранятся в пространстве переменных окружения.

## Основные технологии:
- Python 3.11
- Telegram Bot API
- Requests

## Запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/nisemenov/api_sp1_bot.git
cd api_sp1_bot
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate (Mac OS, Linux) или source venv/Scripts/activate (Win10)
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Создать файл виртуального окружения .env в корневой директории проекта:
```
touch .env
```
В нём указать свои ключи:
```
TELEGRAM_TOKEN=
CHAT_ID=
GIT_TOKEN=
GIT_USER=
```
Запустить проект на локальной машине:
```
python homework.py
```
