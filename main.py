import requests
import time
import sys
from loguru import logger
# Set up the logger with custom formatting and color
logger.remove()  # Remove default handler
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")

# The URL for the API endpoint
url = 'https://api-clicker.pixelverse.xyz/api/'
secret = ''
tgId = ''

logger.info("Starting the clicker bot... with telegramUserId:"+tgId)

# The HTTP headers to send with the request
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,id-ID;q=0.9,id;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://web.telegram.org',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://web.telegram.org/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'secret': secret,
    'tg-id': tgId,
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
# Infinite loop with a 1-second interval
try:
    while True:
        #send request get
        response = requests.get(url+'users', headers=headers)
        if(response.status_code != 200):
            #sprint status code and response http
            logger.error(f"Error: {response.status_code} - {response.text}")
            continue;
        else:
            logger.success(f"Success: {response.status_code}")
        
        #convert response.text to json
        response = response.json()
        energy = response['pet']['energy']
        balance = response['clicksCount']
        pointPerClick = response['pointPerClick']
        levelUpPrice = response['pet']['levelUpPrice']
        petId = response['pet']['id']
        petLevel = response['pet']['level']

        logger.info(f"Energy: {energy} - Balance: {balance} -  PointPerClick: {pointPerClick} - LevelUpPrice: {levelUpPrice} - PetId: {petId} - PetLevel: {petLevel}")

        if(balance > levelUpPrice):
            response = requests.post(f"{url}pets/user-pets/{petId}/level-up", headers=headers)
            response = response.json()
            logger.info(f"Level up pet - current level : {response['level']}")
            time.sleep(1)
            continue;

        if(energy == 0):
            #print sleep 200 sec
            logger.info("Sleeping for 10 minute")
            time.sleep(600)
            continue;
        
        # The data to send with the POST request
        data = {
            "clicksAmount": energy,
            "PointPerClick": 100,
        }

        response = requests.post(url+'users', headers=headers, json=data)

        if(response.status_code == 201):
            response = response.json()
            logger.success(f"clicked! current balance: {response['clicksCount']}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Loop interrupted. Stopping...")

