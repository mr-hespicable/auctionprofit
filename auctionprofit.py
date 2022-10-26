from distutils.log import debug
import gzip
import profile
import time
import io
import requests
import json
import nbt
import base64


def getInfo(call):
    r = requests.get(call)
    return r.json
def decode_inventory_data(raw_data):
    data = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw_data)))
    extra = data.tags[0].tags[0]['tag']['ExtraAttributes']
    id = extra['id']
    
#thanks to ShadowMobX#0220 for refining this function. give him an internship                                                                                                                                        #d4688752-9597-473e-818a-1dba30f81e91
debugMode = 0       
USERNAME = 'websafe'#input('paste username here\n')
API_KEY = 'd4688752-9597-473e-818a-1dba30f81e91'#input('paste api key here\n')
PREFERRED_PROFILE = 'Pineapple'#input('paste name of active profile here. case matters\n')
mojangURL = f"https://api.mojang.com/users/profiles/minecraft/{USERNAME}?"
mojangResponse = requests.get(mojangURL)
UUID = mojangResponse.json()['id']
profileURL = f'https://api.hypixel.net/player?key={API_KEY}&uuid={UUID}'
if debugMode == 1:
    print(f'profileURL = {profileURL}')
profileResponse = requests.get(profileURL)
profileList = profileResponse.json()['player']['stats']['SkyBlock']['profiles']
for profile in profileList:
    profileName = profileResponse.json()['player']['stats']['SkyBlock']['profiles'][profile]['cute_name']
    if profileName == PREFERRED_PROFILE:
        pref_profile_id = profileResponse.json()['player']['stats']['SkyBlock']['profiles'][profile]['profile_id']
    else:
        continue
        


auctionsUp = f"https://api.hypixel.net/skyblock/auction?key={API_KEY}&profile={pref_profile_id}"
if debugMode == 1:
    print(f'auctionsUP = {auctionsUp}')
auctionResponse = requests.get(auctionsUp)
data = auctionResponse.text

parse_json = json.loads(data)

auctionList = parse_json['auctions']

while True:
    for auctionItem in auctionList:
        sold = auctionItem['highest_bid_amount']
        if sold == 0:
            starting_bid = auctionItem['starting_bid'] 
            item_bytes = auctionItem['item_bytes']['data']
            decode_inventory_data(item_bytes)
            print(f'itemid costs {starting_bid}. Claimed: {sold}\n')
        continue

    auctionsSold = f"https://api.hypixel.net/skyblock/auctions_ended?key-{API_KEY}"
    if debugMode == 1:
        print(auctionsSold)
    soldauctionResponse = requests.get(auctionsSold)
    soldData = soldauctionResponse.text
    parse_json = json.loads(soldData)
    soldauctionList = parse_json['auctions']
    exit()
    
        
    for soldItem in soldauctionList:
        uuid = soldItem['buyer']
        if uuid == '2e82ec5b72354497adfde07170979a72':
            continue
        gzipped_data = soldItem['item_bytes']
        decode_inventory_data(gzipped_data)
        price = soldItem['price']
        if id == skyblockID:
            print(price - starting_bid)
        continue
    
    print('delaying')       
    time.sleep(30)
    time.sleep(30)
    print('looping')