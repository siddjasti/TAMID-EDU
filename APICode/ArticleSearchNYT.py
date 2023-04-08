import requests

API_KEY = open("APICode/api_key.txt", "r").read()

link_article_search = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
q_article_search = str(input("Please enter keyword you would like to look up: "))
url_article_search = link_article_search + "?q=" + q_article_search +  "&api-key=" + API_KEY

response = requests.get(url_article_search).json()
headlines = [article["headline"]["main"] for article in response["response"]["docs"]]
print("")
print("Top 10 Articless for The Keyword You Entered: ")
for h in headlines:
    print(h)