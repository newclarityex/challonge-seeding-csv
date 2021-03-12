import requests
import csv
import operator
reader = csv.DictReader(open("input.csv","rt",encoding = "utf-8"))
csvdata = []
for line in reader:
    csvdata.append(line)
reader = csv.DictReader(open("seeded.csv","rt",encoding = "utf-8"))
for line in reader:
    for player in csvdata:
        if player["Username"] == line["Name"]:
            player["Seed"] = line["Seed"]
api = "API_KEY"
r = requests.get("https://api.challonge.com/v1/tournaments.json?api_key="+api)
print(r.json())
tournaments = r.json()
url = input("Please enter a URL")
tournament_id = -1
for tournament in tournaments:
    print(tournament["tournament"]["url"])
    if url == tournament["tournament"]["url"]:
        tournament_id = tournament["tournament"]["id"]
if tournament_id == -1:
    print("tournament not found")
else:
    print(tournament_id)
    r = requests.get("https://api.challonge.com/v1/tournaments/"+str(tournament_id)+"/participants.json?api_key="+api)
    print(r.json())
    participants = r.json()
    checked_in = []
    for participant in participants:
        print(participant["participant"]["name"])
        for csvplayer in csvdata:
            if csvplayer["Participant Username"] == participant["participant"]["name"] and participant["participant"]["checked_in"]:
                print("Found")
                checked_in.append({"seed":csvplayer["Seed"],"id":participant["participant"]["id"]})
                print(csvplayer)
# requests.put("https://api.challonge.com/v1/tournaments/"+str(tournament_id)+"/participants/"+str(participant["participant"]["id"])+".json?api_key="+api,data={"participant[seed]":csvplayer["Seed"]})
    checked_in.sort(key=operator.itemgetter("seed"))
    i = 0
    for player in checked_in: 
        i += 1
        requests.put("https://api.challonge.com/v1/tournaments/"+str(tournament_id)+"/participants/"+str(player["id"])+".json?api_key="+api,data={"participant[seed]":i})
        
