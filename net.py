from bs4 import BeautifulSoup
import os, json, requests

NET_RANKINGS_URL = "https://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings"
CACHE = "cache.json"

SOUP = BeautifulSoup(requests.get(NET_RANKINGS_URL).content, "html.parser")
RANKINGS_TABLE = SOUP.find("table")

def _fetch_new_rankings():
    rankings_last_updated = SOUP.find(class_="rankings-last-updated")
    response = [{ "last_updated" : rankings_last_updated.get_text() }]
    for record in RANKINGS_TABLE.find_all("tr")[1:]:
        elements = record.find_all("td")
        response.append({
            "rank" : int(elements[0].get_text()),
            "previous" : int(elements[1].get_text()),
            "school" : elements[2].get_text(),
            "conference" : elements[3].get_text(),
            "record" : elements[4].get_text(),
            "road" : elements[5].get_text(),
            "neutral" : elements[6].get_text(),
            "home" : elements[7].get_text(),
            "quad 1" : elements[8].get_text(),
            "quad 2" : elements[9].get_text(),
            "quad 3" : elements[10].get_text(),
            "quad 4" : elements[11].get_text()
        })
    with open(CACHE, "w+") as file:
        json.dump(response, file)
    return response

def get_rankings():
    data = None
    # if cache doesn't exist, fetch new data
    if not os.path.exists(CACHE):
        data = _fetch_new_rankings()
    else:
        data = json.load(open(CACHE, "r"))

    # if cache is out of date, fetch new data
    if data[0]["last_updated"] != SOUP.find(class_="rankings-last-updated").get_text():
        data = _fetch_new_rankings()
        
    return data[1:]

def get_top_n_rankings(n):
    data = get_rankings()[1:n+1]
    return data

def get_conference_rankings(conf):
    conference_rank = 1
    data = get_rankings()[1:]
    response = []
    for entry in data:
        if entry['conference'] == conf:
            entry['conference_rank'] = conference_rank
            response.append(entry)
            conference_rank += 1
    return response

def get_school(school):
    data = get_rankings()[1:]
    for entry in data:
        if entry['school'] == school:
            return entry
    return None

if __name__ == "__main__":
    print(get_top_n_rankings(20))
    print()
    print(get_conference_rankings('Mountain West'))
    print()
    print(get_school("Pittsburgh"))