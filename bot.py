import requests
import os
from dotenv import load_dotenv
import sys
import json

def send_telegram_message(chat_id, message):
    telegram_url = f"https://api.telegram.org/bot{os.getenv('BOT_API_TOKEN')}/sendMessage"
    telegram_payload = {"chat_id": chat_id, "text": message}
    response = requests.post(telegram_url, json=telegram_payload)
    
    if response.status_code != 200:
        print(f"Ошибка при отправке сообщения в Телеграм: {response.text}")

def get_players_to_notify(data, telegram_users):
    players_to_notify = []
    
    for member in data:
        playerName = member["playerName"]
        currentValue = int([x["currentValue"] for x in member["memberContribution"] if x["type"] == 2][0])
        
        if currentValue < 600 and playerName in telegram_users:
            telegramName = telegram_users[playerName]
            players_to_notify.append(f"{playerName} ({currentValue} / 600) {telegramName}")
    
    return players_to_notify

def main():
    load_dotenv(dotenv_path=sys.argv[1])
    
    guild_id = os.getenv("GUILD_ID")
    chat_id = os.getenv("CHAT_ID")
    comlink_url = os.getenv("COMLINK_URL")
    telegram_users_str = os.getenv("TELEGRAM_USERS")
    telegram_users = json.loads(telegram_users_str)
    url = f"{comlink_url}/guild"

    payload = {
        "payload": {
            "guildId": guild_id,
            "includeRecentGuildActivityInfo": True
        },
        "enums": False
    }

    response = requests.post(url, json=payload)
    data = response.json()["guild"]["member"]

    players_to_notify = get_players_to_notify(data, telegram_users)
    
    if players_to_notify:
        message = "Не все сдали энку!\nСписок тунеядцев-бездельников:\n\n" + "\n".join(players_to_notify)
    else:
        message = "Ай молодцы, энка сдана!"

    send_telegram_message(chat_id, message)

if __name__ == "__main__":
    main()
