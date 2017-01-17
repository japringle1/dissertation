import urllib2, json, myconstants

def populate_collection(collection, players):
    for player in players:
        collection.insert(player)

def format_player(player_data):
    # Add last season's points
    if (len(player_data["history_past"]) > 0):
        player_data["last_season_point"] = player_data["history_past"][-1]["total_points"]
    else:
        player_data["last_season_point"] = 0

    # Change fixture key names
    all_fixtures = {}
    for index, fixture in enumerate(player_data["history"]):
        all_fixtures[str(index + 1)] = fixture

    player_data["fixture_history"] = all_fixtures

    return player_data


def get_player_info():
    resource = urllib2.urlopen('https://fantasy.premierleague.com/drf/bootstrap-static')
    player_data = json.load(resource)
    return player_data["elements"]

def scrape_player_data(start_url):
    player_info = get_player_info()
    players = []
    i = start_url
    errorflag = False
    print "Scraping...\n"

    while (errorflag == False):
        try:
            if (i % 50 == 0):
                print str(i) + " players scraped."
            resource = urllib2.urlopen('https://fantasy.premierleague.com/drf/element-summary/%d' % (i))
            player_data = json.load(resource)
            player_data["info"] = player_info[i-1]
            players.append(format_player(player_data))
            i += 1
        except ValueError:
            print str(i) + " wasn't a valid JSON."
        except urllib2.URLError:
            errorflag = True
    print str(len(players)) + " players scraped.\n"
    return players