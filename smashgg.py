import os
import requests
import codecs

ENTRANT_POINTS = 1
TOP_FIVE_POINTS = 3
TOP_TEN_TO_SIX_POINTS = 1

def notable_players_from_file(filename):
    file = codecs.open(filename, "r", "utf-8")
    notable_IDs = {} # ID: [tag,country,PR#]
    for line in file:
        line = line[:-1]
        data = line.split("\t")
        notable_IDs[data[4]]=[data[0],data[1],data[3]]
    return notable_IDs

def tournament_tier(points):
    if points >= 200:
        return "S"
    elif points >= 120:
        return "A"
    elif points >= 80:
        return "B"
    elif points >= 50:
        return "C"
    else:
        return "Not ranked"

def url_to_api(url):
    slug = url[28:url.find("/events/")]
    event = url[url.find("/events/")+8:url.find("/overview")]
    return ("https://api.smash.gg/tournament/"+slug+"/event/"+event)

def get_players(api_url):
    players = {}
    api_url += "?expand[]=entrants&mutations[]=playerData"
    json = requests.get(api_url).json()
    for entrant in json["entities"]["entrants"]:
        #print(list(entrant["playerIds"].items())[0][1])
        players[list(entrant["playerIds"].values())[0]] = entrant["name"]
    return players

def count_ooc(api_url,original_country):
    api_url += "?expand[]=entrants&mutations[]=playerData"
    json = requests.get(api_url).json()
    countries = {}
    total_ooc = 0
    for entrant in json["entities"]["entrants"]:
        player_country = list(entrant["mutations"]["players"].values())[0]["country"]
        if player_country == None:
            player_country = "Not registered"
        if player_country not in countries:
            countries[player_country] = 0
        countries[player_country] += 1
        if player_country != original_country and player_country != "Not registered":
            total_ooc += 1
    countries["total_ooc"]=total_ooc
    return countries

def count_notable(api_url,notable_players):
    api_url += "?expand[]=entrants&mutations[]=playerData"
    json = requests.get(api_url).json()
    number_notable_players = 0
    top5 = 0
    number_of_entrants = len(json["entities"]["entrants"])
    for entrant in json["entities"]["entrants"]:
        player_id = list(entrant["mutations"]["players"].keys())[0]
        if player_id in notable_players:
            number_notable_players += 1
            if int(notable_players[player_id][2])<=5:
                top5+=1

    return [number_of_entrants,number_notable_players,top5]

def get_eventInfo(url):
    tournament_handle = url[url.find("/tournament/")+12:]
    tournament_handle = tournament_handle[:tournament_handle.find("/")]
    #event = url[url.find("/events/")+8:]
    #event = event[:event.find("/")]
    api_url = "https://api.smash.gg/tournament/"+tournament_handle
    json = requests.get(api_url).json()
    event_name = json["entities"]["tournament"]["name"]
    notable_players = count_notable(url_to_api("https://smash.gg/tournament/"+tournament_handle+"/events/wii-u-singles/overview"),nps)
    event_points = ENTRANT_POINTS*notable_players[0] + TOP_TEN_TO_SIX_POINTS*(notable_players[2]-notable_players[1])+ TOP_FIVE_POINTS*notable_players[2]
    output = ("**"+event_name+"**\n"+   "Number of entrants: **" + str(notable_players[0]) + "**\n" +   "Notable top 5 players: **" + str(notable_players[2]) + "**\n" +   "Notable 6-10 players: **" + str(notable_players[1]) + "**\n" + "Event rank: **" + str(event_points) + " - " + tournament_tier(event_points) + "**")
    return output

nps = notable_players_from_file("notables.txt")
#print(count_ooc(url_to_api("https://smash.gg/tournament/smash-valley-ft-dabuz-mkleo/events/wii-u-singles/overview"),"Germany"))
#print(count_notable(url_to_api("https://smash.gg/tournament/dat-blastzone-20/events/wii-u-singles/overview"),nps))

get_eventInfo("https://smash.gg/tournament/eclipse-2/events/wii-u-singles/overview")
