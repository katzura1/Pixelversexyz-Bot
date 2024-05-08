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
        currentPetId = ""
        #get user data
        logger.info("Getting user data...")
        response = requests.get(url + 'users', headers=headers)
        if(response.status_code == 200):
            response = response.json()
            currentPetId = response['pet']['id']
        #get pet
        logger.info("Getting pets...")
        response = requests.get(url + 'pets', headers=headers)
        if(response.status_code == 200):
            response = response.json()
            listPet = response['data']
            logger.info("found "+str(len(listPet))+" pets")
            #looping through pets
            for pet in listPet:
                userPet = pet['userPet']
                idPet = userPet['id']

                #select pet
                logger.info("Selecting pet with id: "+str(idPet))
                response = requests.post(url + 'pets/user-pets/'+idPet+'/select',  headers=headers)
                if(response.status_code == 201 or idPet == currentPetId):
                    logger.info("Pet selected")
                    currentPetId = idPet
                    #get user data with current pet
                    response = requests.get(url + 'users', headers=headers)
                    if(response.status_code == 200):
                        response = response.json()
                        pointPerClick = response['pointPerClick']
                        clicksCount = response['clicksCount']
                        pet = response['pet']
                        petName = pet['pet']['name']
                        petEnergy = pet['energy']
                        level = pet['level']
                        levelUpPrice = pet['levelUpPrice']

                        logger.info("Pet name: "+petName+" - Energy: "+str(petEnergy)+" - Level: "+str(level)+" - Level up price: "+str(levelUpPrice))
                        
                        if(petEnergy > 0):
                            #click pet
                            dataClick = {
                                "clicksAmount": petEnergy
                            }
                            logger.info("Clicking pet with "+str(petEnergy)+" energy")
                            response = requests.post(url + 'users', headers=headers, json=dataClick)
                            if(response.status_code == 201):
                                response = response.json()
                                clicksCount = response['clicksCount']
                                logger.success("Pet clicked, current point: "+str(round(clicksCount, 2)))
                        
                        while(clicksCount > levelUpPrice):
                            #level up pet
                            logger.info("Level up pet with price: "+str(levelUpPrice))
                            response = requests.post(url + 'pets/user-pets/'+idPet+'/level-up', headers=headers)
                            if(response.status_code == 201):
                                response = response.json()
                                level = response['level']
                                levelUpPrice = response['levelUpPrice']
                                clicksCount = response['clicksCount']
                                logger.success("Pet level up to "+str(level)+", next level price: "+str(levelUpPrice))
                            else:
                                break;
                    else:
                        logger.error("Error getting user data")
                        time.sleep(1)
                else:
                    logger.error("Error selecting pet : "+str(response.status_code)+" - "+response.text)
                    time.sleep(1)
            logger.info("Sleeping for 10 minutes")
            time.sleep(600)
        else:
            logger.error("Error getting pets")
            time.sleep(1)


except KeyboardInterrupt:
    print("Loop interrupted. Stopping...")
