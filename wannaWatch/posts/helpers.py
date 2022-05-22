import requests

KEY = "k_aaaaaaaa"  # IMDB API KEY

def getMovie(imdbid):
    r = requests.get(f"https://imdb-api.com/en/API/Title/{KEY}/{imdbid}")
    content = r.json()
    result = {"title": content["fullTitle"],
              "plot": content["plot"],
              "genres": content["genres"],
              "cast": content["stars"],
              "content_rating": content["contentRating"],
              "user_rating": content["imDbRating"],
              "image": content["image"]}
    return result


def searchTitle(title):
    r = requests.get(f"https://imdb-api.com/en/API/SearchTitle/{KEY}/{title}")
    results = r.json()["results"]
    titles = []
    for content in results:
        titles.append(content['id'])
    movies = {}
    for imdbid in titles:
        movies[imdbid] = getMovie(imdbid)
    return movies
