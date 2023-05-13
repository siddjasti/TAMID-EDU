import requests, sys, os
import tkinter as tk
from tkinter import simpledialog, messagebox

#function to search articles
def search_articles(type):
    keyword = simpledialog.askstring("Enter Keyword", "Please enter a keyword:" if type == "search" else " Please enter a keyword\n\n Options are: arts, automobiles, books, business, fashion, food, health, home, insider,\n magazine, movies, nyregion, obituaries, opinion, politics, realestate, science, sports,\n sundayreview, technology, theater, t-magazine, travel, upshot, us, and world") 
    if keyword:
        if(type == "top"):
            articles = top_stories(keyword)
        if(type == "search"):
            articles = get_searched_articles(keyword)
        display_results(articles, type)
    else:
        messagebox.showerror("Error", "You must enter a keyword to search for articles.")

#command to look up top 10 articls on keyword
def get_searched_articles(keyword):
    API_KEY = open("APICode/api_key.txt", "r").read()
    link_article_search = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    url_article_search = link_article_search + "?q=" + keyword +  "&api-key=" + API_KEY

    response = requests.get(url_article_search).json()
    headlines = [article["headline"]["main"] for article in response["response"]["docs"]]
    return headlines

#command to look up top articles under a specfic section
def top_stories(keyword):
    API_KEY = open("APICode/api_key.txt", "r").read()
    #(Options are: arts, automobiles, books, business, fashion, food, health, home, insider, magazine, movies, nyregion, obituaries, opinion, politics, realestate, science, sports, sundayreview, technology, theater, t-magazine, travel, upshot, us, and world): "
    url_top_stories = f"https://api.nytimes.com/svc/topstories/v2/{keyword}.json?api-key={API_KEY}"

    response = requests.get(url_top_stories)
    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 404:
        return ["Incorrect input, please enter a correct input!"]
    elif response.status_code == 429:
        return ["Limit of requests sent, please try again later"]

    headlines = [article["title"] for article in data["results"]]
    return headlines

def display_results(articles, type):
    results_window = tk.Toplevel(root)
    results_window.configure(bg="black")
    results_window.title("Search Results")

    #display the heading
    title = "Top 10 Articles for The Keyword You Entered:" if type == "search" else "Top Articles for the Topic You Entered:"
    heading = title
    tk.Label(
        results_window,
        text=heading,
        font=("Helvetica", 14, "bold"),
        fg="#21618C",
        bg="black",
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

    #display the articles
    for i, article in enumerate(articles, start=1):
        tk.Label(
            results_window,
            text=article,
            font=("Helvetica", 12),
            fg="white",
            bg="black",
            wraplength=600,
            justify="left",
        ).grid(row=i, column=0, padx=10, pady=5, sticky="w")

#main application window
root = tk.Tk()
root.title("Article Finder")
root.configure(bg="black")
root.geometry("500x200") # Width x Height

#button for search
search_button = tk.Button(
    root,
    text="Search Articles",
    font=("Helvetica", 14),
    width = 20,
    height = 3,
    bg="black",
    fg="#21618C",
    command=lambda: search_articles("search"),
)
search_button.pack(pady=18)

#button for top
top_button = tk.Button(
    root,
    text="Top Stories",
    font=("Helvetica", 14),
    width = 20,
    height = 3,
    bg="black",
    fg="#21618C",
    command=lambda: search_articles("top"),
)
top_button.pack(pady=18)

root.mainloop()