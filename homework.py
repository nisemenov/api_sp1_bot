import os
import requests
import telegram
import asyncio
import time
from datetime import datetime as dt
from datetime import timedelta as td
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

GIT_TOKEN = os.getenv('GIT_TOKEN')
GIT_USER = os.getenv('GIT_USER')


def timediff(current_datetime, date_time):
    date_format = '%Y-%m-%dT%H:%M:%SZ'
    parsed_date = dt.strptime(date_time, date_format) + td(hours=3)
    time_diff = current_datetime - parsed_date
    time_diff_minutes = time_diff.total_seconds() / 60
    return int(time_diff_minutes)


def get_event_statuses(current_time):
    url = f'https://api.github.com/users/{GIT_USER}/events'
    headers = {
        'Authorization': f'Bearer {GIT_TOKEN}',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    response = requests.get(url, headers=headers)
    datetime_str = response.json()[0]['created_at']
    time_diff = timediff(current_time, datetime_str)

    if time_diff < 20:
        if response.status_code == 200:
            return response.json()[0]
        else:
            return f'Error has occurred: {response.status_code}'


def parse_event_status(event, current_time):
    date_created = event['created_at']
    time_diff = timediff(current_time, date_created)

    repo = event['repo']
    repo_name = repo['name'].split('/')[1]
    type_event = event['type']
    if type_event == 'PushEvent':
        commit = event['payload']['commits']
        committer = commit[0]['author']['name']
        message = commit[0]['message']
        return f"{committer} made new {type_event} with message '{message}' " \
               f"{time_diff} minutes ago!\nRepo's name is '{repo_name}'."
    return f"{GIT_USER} made new {type_event} {time_diff} minutes ago!\n" \
           f"Repo's name is {repo_name}."


async def send_message(message):
    async with telegram.Bot(TELEGRAM_TOKEN) as bot:
        await bot.sendMessage(chat_id=CHAT_ID, text=message)


def main():
    current_time = dt.now()
    while True:
        try:
            new_event = get_event_statuses(current_time)
            if new_event.get('id'):
                asyncio.run(send_message(parse_event_status(new_event, current_time)))
            current_time = dt.now()
            time.sleep(600)
        except Exception as e:
            print(f'Error has occurred: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
