import myconstants
from statistics import mean
from copy import deepcopy
import natsort

from myconstants import TEAM_CODES

def run_forecasts():
    print("Running forecasts.")

    players = list(myconstants.PLAYER_COLLECTION.find())

    maps = get_maps(players)
    team_map = maps["teams"]
    home_away_map = maps["home_away"]

    for player in players:

        mins_played = []
        net_transfers = []
        oppositions = []
        home_away = []
        points = []
        values = []

        fh = player["fixture_history"]

        for fixture in natsort.natsorted(fh):
            fixture = fh[fixture]
            points.append(fixture["total_points"])
            mins_played.append(fixture["minutes"])
            net_transfers.append(fixture["transfers_balance"])
            values.append(fixture["value"])
            oppositions.append([TEAM_CODES[fixture["opponent_team"]]])
            home_away.append(["H" if fixture["was_home"] else "A"])

        points = points[1:]
        points.append(0)

        net_transfers = net_transfers[1:]
        net_transfers.append(player["info"]["transfers_in_event"] - player["info"]["transfers_out_event"])

        values = values[1:]
        values.append(player["info"]["now_cost"])

        oppositions = oppositions[1:]
        home_away = home_away[1:]

        oppositions_this_week = []
        home_away_this_week = []
        for fixture in player["fixtures_summary"]:
            if int(fixture["event_name"][-2:]) == myconstants.GW_COUNT + 1:
                oppositions_this_week.append(fixture["opponent_short_name"])
                home_away_this_week.append("H" if fixture["is_home"] else "A")
        oppositions.append(oppositions_this_week)
        home_away.append(home_away_this_week)

        mins_played.append(0)

        actual_keys = deepcopy(natsort.natsorted(player["fixture_history"].keys()))
        forecast_keys = actual_keys[1:]
        forecast_keys.append(player["fixtures_summary"][0]["event_name"][-2:])

        es_results = exponential_smoothing(actual_keys, forecast_keys, myconstants.SMOOTHING_FACTOR, player,
                                           oppositions, team_map, home_away, home_away_map)

        compiled_forecasts = {}

        for idx, key in enumerate(natsort.natsorted(es_results.keys())):
            compiled_forecasts[key] = {"forecast": round(es_results[key], 2),
                                       "last_mins_played": mins_played[idx],
                                       "net_transfers": net_transfers[idx],
                                       "opposition": oppositions[idx],
                                       "home_away": home_away[idx],
                                       "points": points[idx],
                                       "value": values[idx]
                                       }

        if player["info"]["web_name"] == "Kane":
            print(player["info"]["web_name"])
            for key in natsort.natsorted(compiled_forecasts.keys()):
                print(str(key) + ": " + str(compiled_forecasts[key]))
            print

        json_data = {
            "id": player['info']['id'],
            "web_name": player['info']['web_name'],
            "element_type_id": player['info']['element_type'],
            "team_name": TEAM_CODES[player['info']['team']],
            "fixture_history": compiled_forecasts
        }

        myconstants.FORECASTS_COLLECTION.insert(json_data)

    print("Forecasting finished!\n")


def exponential_smoothing(actual_gws, forecast_gws, smoothing_factor, player, oppositions, team_map, home_away, home_away_map):
    forecasts = {}
    for idx, key in enumerate(actual_gws):
        forecast = 0
        for gw_fixture in range(0, len(oppositions[idx])):
            if idx == 0:
                nforecast = player["fixture_history"][key]["total_points"]
            else:
                nforecast = forecasts[forecast_gws[idx - 1]] + (smoothing_factor * (player['fixture_history'][forecast_gws[idx - 1]]['total_points'] - forecasts[forecast_gws[idx - 1]]))
                # nforecast = (nforecast * team_map[oppositions[idx][gw_fixture]] * home_away_map[home_away[idx][gw_fixture]])
            forecast += nforecast
        forecasts[forecast_gws[idx]] = forecast
    return forecasts


def get_maps(players):
    team_map = {}
    home_away_map = {
        "H": 0,
        "A": 0
    }

    for player in players:
        fh = player["fixture_history"]
        for gw in fh:
            fixture = fh[gw]
            if fixture["minutes"] < 45:
                continue

            opponent = TEAM_CODES[fixture["opponent_team"]]
            if opponent not in team_map:
                team_map[opponent] = 0
            team_map[opponent] += fixture["total_points"]

            home_away = "H" if fixture["was_home"] else "A"
            home_away_map[home_away] += fixture["total_points"]

    mean_points = mean(team_map.values())
    for team in team_map:
        team_multiplier = round(team_map[team] / mean_points, 2)
        team_map[team] = team_multiplier
    team_map["-"] = 1.0

    mean_points_ha = mean(home_away_map.values())
    for value in home_away_map:
        home_away_multiplier = home_away_map[value] / mean_points_ha
        home_away_map[value] = home_away_multiplier
    home_away_map[""] = 1.0

    return {
        "teams": team_map,
        "home_away": home_away_map
    }
