import json
from requests_oauthlib import OAuth1Session
import tweepy

CONSUMER_KEY = "o6I0uL7UD7tN913ZxcrnjvAEu"
CONSUMER_SECRET = "42tF9eW5VIrIA07XF2kNeHnf7FurueWOnn6lLZC72rmkem1Mv6"
ACCESSS_TOKEN = "1393462885976731650-IoMXeqrjawOHknTApc5D9CAZbgZ7qI"
ACCESSS_TOKEN_SECRET = "K46tPixDhvQJtbIaqs8HRRw7Ub5dHKCAtEZQYC2L8VsiQ"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHQUQEAAAAAxHvXFYWp6g3YmLSOpzlPmHTaZbs%3D4tbCYth0K7WIUAcF9s7UEbMy7Mk5kiqtNGg9Ovt2OrZJVrDag0"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESSS_TOKEN, ACCESSS_TOKEN_SECRET)


api = tweepy.API(auth)
tweets = api.search(q=['python'],conut = 10)
for tweet in tweets:
  print('-------------------')
  print(tweet.text)
