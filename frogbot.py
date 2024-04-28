# @frogbott - A twitter bot that posts frogs
import tweepy
import requests
import os

# Unsplash API
# https://unsplash.com/documentation#public-authentication
access_key = ":)"
public_auth = "Client-ID " + access_key

# Twitter API
consumer_key = ":)"
consumer_secret = ":)"
access_token =":)"
access_token_secret = ":)"
#bearer_token = ":)"
#client_id = ":)"
#client_secret = ":)"

# Download an image from unsplash
def download_random_frog():
    r = requests.get(
        "https://api.unsplash.com/photos/random?query=frog", 
        headers={'Authorization': public_auth}
    )
    photo = r.json()

    # Unsplash want to know where link clicks are coming from
    # https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines
    utm = "utm_source=frogbot&utm_medium=referral"
    unsplash_url = "https://unsplash.com/?" + utm
    download_location = photo["links"]["download_location"]
    name = photo["user"]["name"]
    user_profile = photo["user"]["links"]["html"] + "?" + utm
    # And Unsplash wants you to credit appropriatesly
    credit = "(credit)\n" + name + ": " + user_profile + "\nunsplash: " + unsplash_url
    
    # This GET returns a "url":"<link>"
    r2 = requests.get(
        download_location, 
        headers={'Authorization': public_auth}
    ).json()
    
    # Download image
    r3 = requests.get(
        r2["url"],
        headers={'Authorization': public_auth}
    )
    
    filename = "frog." + r3.headers['Content-Type'].split("/", 1)[1]
    with open(filename, 'wb') as f:
        f.write(r3.content)
    
    return filename, credit

def get_frog_counter():
    with open("count.txt", 'rb') as f:
        num = int(f.read())
    
    return num

def update_frog_counter(value):
    with open("count.txt", 'w+') as f:
        f.write(str(value))

    return value

def upload_tweet(filename, credit):
    # Auth
    # As of 28th April 2024, Twitter API v2 can't upload media and Twitter API V1 is retstricted and can't post tweets.... So we need both.
    apiv1_auth = tweepy.OAuth1UserHandler(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    apiv1 = tweepy.API(apiv1_auth)
    apiv2_client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Frog counter
    frog_counter = get_frog_counter()
    
    # Upload
    text = "frog #" + str(frog_counter) + " ribbit\n" + credit
    media = apiv1.media_upload(filename)
    response = apiv2_client.create_tweet(text=text, media_ids=[media.media_id])
    print(f"https://twitter.com/user/status/{response.data['id']}")

    update_frog_counter(frog_counter)

def main():
    filename, credit = download_random_frog()
    upload_tweet(filename, credit)
    os.remove(filename)

main()

