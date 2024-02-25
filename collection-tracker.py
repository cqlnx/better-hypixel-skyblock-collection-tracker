import time
from dhooks import Webhook, Embed
import requests

# SETTINGS CHANGE TO MATCH YOURS
key = "cdd06887-8801-4a66-8815-8f8fdd858366"  # replace with your API key
username = "popiiumaa"  # replace with your username
profile = "Pineapple"  # replace with the profile you want to track
collection = "SUGAR_CANE"  # replace with the collection you want
skill = "farming"  # replace with the skill you want to track
webhook_url = 'https://discord.com/api/webhooks/1183243149569699910/94LL-uSuRRCn2pzb-uzadWA5WhEtO_kqx0w2Eg5HS3Bfy2sVUf-4iRIrveeZEG5Cx46k'  # replace with your Discord webhook URL
# END OF SETTINGS

print(f"Your username is: {username}")
print(f"You are tracking the '{skill}' skill")
print(f"You are using the '{profile}' profile and tracking the '{collection}' collection.")
print("")

def get_uuid(username):
    url = 'https://api.mojang.com/users/profiles/minecraft/' + username
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['id']
    else:
        return None

def get_collection(user, key, profile, collection):
    # Send a request to the Hypixel API
    request_url = f"https://api.hypixel.net/skyblock/profiles?key={key}&uuid={get_uuid(user)}"
    api_response = requests.get(request_url)
    response_json = api_response.json()

    if "profiles" in response_json:
        for profile_data in response_json["profiles"]:
            if profile_data.get("cute_name") == profile:
                if "members" in profile_data:
                    member_data = profile_data["members"].get(get_uuid(user))
                    if member_data and "collection" in member_data:
                        return member_data["collection"].get(collection, 0)
    return 0

def get_skill_experience(user, key, profile, skill):
    # Send a request to the Hypixel API
    request_url = f"https://api.hypixel.net/skyblock/profiles?key={key}&uuid={get_uuid(user)}"
    api_response = requests.get(request_url)
    response_json = api_response.json()
 
    if "profiles" in response_json:
        for profile_data in response_json["profiles"]:
            if profile_data.get("cute_name") == profile:
                if "members" in profile_data:
                    member_data = profile_data["members"].get(get_uuid(user))
                    if member_data and f"experience_skill_{skill}" in member_data:
                        return int(member_data[f"experience_skill_{skill}"])
    return 0

print(f"Getting your {collection} collection stats")

start_time = time.time()
start_collection_amount = get_collection(username, key, profile, collection)
start_skill_experience = get_skill_experience(username, key, profile, skill)

while True:
    current_collection = get_collection(username, key, profile, collection)
    current_skill_experience = get_skill_experience(username, key, profile, skill)

    if isinstance(current_skill_experience, int) and isinstance(start_skill_experience, int):
        skill_experience_session = current_skill_experience - start_skill_experience
    else:
        skill_experience_session = 0
    collection_session = current_collection - start_collection_amount
    elapsed_time = time.time() - start_time

    collection_hourly_average = int(collection_session / (elapsed_time / 3600))
    skill_experience_hourly_average = int(skill_experience_session / (elapsed_time / 3600))
    
    # Create an Embed
    embed = Embed(
        title=f"Stats for {username} on {profile}",
        description=f"Stats tracker made by popiiumaa :weary:",
        color=0x3498db  # You can set a custom color here
    )

    embed.add_field(name=f"Total {collection} collected :astonished:", value=current_collection, inline=False)
    embed.add_field(name=f"Total {collection} this session", value=collection_session, inline=False)
    embed.add_field(name=f"Hourly Average {collection} collected", value=collection_hourly_average, inline=False)
    
    embed.add_field(name=f"Total {skill} Skill Experience :astonished:", value=current_skill_experience, inline=False)
    embed.add_field(name=f"{skill} Skill Experience this session", value=skill_experience_session, inline=False)
    embed.add_field(name=f"Hourly Average {skill} Skill Experience", value=skill_experience_hourly_average, inline=False)
    skin_url = f'https://minotar.net/body/{username}/300.png'
    embed.set_thumbnail(url=skin_url)

    hook = Webhook(webhook_url)
    hook.send(embed=embed)

    start_time = time.time()
    start_collection_amount = current_collection
    start_skill_experience = current_skill_experience
    print("Stats have been sent to Discord.")
    print("-------------------------------")
    time.sleep(180)
