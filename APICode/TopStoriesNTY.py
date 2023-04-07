import requests, sys, os

API_KEY = open("APICode/api_key.txt", "r").read()
print(API_KEY)

section =  str(input("Please enter topic you would like to look up (Options are: arts, automobiles, books, business, fashion,"
                              + "food, health, home, insider, magazine, movies, nyregion, obituaries, opinion, politics, realestate,"
                              + "science, sports, sundayreview, technology, theater, t-magazine, travel, upshot, us, and world): "))
url_top_stories = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={API_KEY}"

response = requests.get(url_top_stories)
if response.status_code == 200:
    data = response.json()
elif response.status_code == 404:
    print("Incorrect input, please enter a correct input!")
    sys.exit()
elif response.status_code == 429:
    print("Limit of requests sent, please try again later")
    sys.exit()

headlines = [article["title"] for article in data["results"]]
print("\n" + f"Top Articles Relating to {section}:")
for h in headlines:
    print(h)
