import myconstants
from numpy import mean
from copy import deepcopy
import natsort


def run_forecasts():
    print "Running forecasts."

    players = list(myconstants.PLAYER_COLLECTION.find())

    maps = get_maps(players)
    print maps
    team_map = myconstants.DEFAULT_TEAM_MAP
    home_away_map = myconstants.HOME_AWAY_MAP

    for player in players:

        actual_keys = []
        values = []
        mins_played = []
        net_transfers = []
        oppositions = []
        home_away = []
        points = []

        fh = player["fixture_history"]

        for fixture in natsort.natsorted(fh):
            points.append(fh[fixture]["points"])
            actual_keys.append(str(fh[fixture]["gw"]))
            values.append(fh[fixture]["value"])
            mins_played.append(fh[fixture]["mins_played"])
            net_transfers.append(fh[fixture]["net_transfers"])
            if "fixtures" in fh[fixture]:
                oppositions.append([f["opponent_result"][:3] for f in fh[fixture]["fixtures"]])
                home_away.append([f["opponent_result"][4:5] for f in fh[fixture]["fixtures"]])
            else:
                oppositions.append([fh[fixture]["opponent_result"][:3]])
                home_away.append([fh[fixture]["opponent_result"][4:5]])

        points = points[1:]
        points.append(0)

        values = values[1:]
        values.append(player["now_cost"])

        net_transfers = net_transfers[1:]
        net_transfers.append(player["transfers_in_event"] - player["transfers_out_event"])

        oppositions = oppositions[1:]

        home_away = home_away[1:]

        oppositions_this_week = []
        home_away_this_week = []
        for fixture in player["fixtures"]["summary"]:
            if fixture[0] == myconstants.GW_COUNT + 1:
                oppositions_this_week.append(fixture[1][:3])
                home_away_this_week.append(fixture[1][5:6])
        oppositions.append(oppositions_this_week)
        home_away.append(home_away_this_week)

        mins_played.append(0)

        forecast_keys = deepcopy(actual_keys)
        forecast_keys = forecast_keys[1:]
        forecast_keys.append(str(player["fixtures"]["summary"][0][0]))

        es_results = exponential_smoothing(actual_keys, forecast_keys, myconstants.SMOOTHING_FACTOR, player,
                                           oppositions, team_map, home_away, home_away_map)
        wa_results = weighted_average(actual_keys, forecast_keys, player, oppositions, team_map, home_away,
                                      home_away_map)
        lg_results = last_game(actual_keys, forecast_keys, player, oppositions, team_map, home_away, home_away_map)

        compiled_forecasts = {}

        if (es_results.keys() == wa_results.keys() == lg_results.keys()):
            for idx, key in enumerate(natsort.natsorted(es_results.keys())):
                compiled_forecasts[key] = {"WA": round(wa_results[key], 2),
                                           "ES": round(es_results[key], 2),
                                           "LG": round(lg_results[key], 2),
                                           "value": values[idx],
                                           "last_mins_played": mins_played[idx],
                                           "net_transfers": net_transfers[idx],
                                           "opposition": oppositions[idx],
                                           "home_away": home_away[idx],
                                           "points": points[idx]
                                           }

        if player["id"] == 393:
            print player["web_name"]
            print actual_keys
            print forecast_keys
            for key in natsort.natsorted(compiled_forecasts.keys()):
                print str(key) + ": " + str(compiled_forecasts[key])
            print

        json_data = {
            "id": player['id'],
            "web_name": player['web_name'],
            "element_type_id": player['element_type'],
            "team_name": player['team_name'],
            "fixture_history": compiled_forecasts
        }

        myconstants.FORECASTS_COLLECTION.insert(json_data)

    print "Forecasting finished!\n"


def last_game(actual_gws, forecast_gws, player, oppositions, team_map, home_away, home_away_map):
    forecasts = {}
    for idx, key in enumerate(actual_gws):
        idx += 1
        fixtures = actual_gws[0:idx]
        points = []
        for fixture in fixtures:
            points.append(player["fixture_history"][fixture]["points"])
        forecast = 0
        for fixture in range(0, len(oppositions[idx - 1])):
            forecast += (
            points[-1] * team_map[oppositions[idx - 1][fixture]] * home_away_map[home_away[idx - 1][fixture]])
        forecasts[forecast_gws[idx - 1]] = forecast
    return forecasts


def weighted_average(actual_gws, forecast_gws, player, oppositions, team_map, home_away, home_away_map):
    forecasts = {}
    for idx, key in enumerate(actual_gws):
        idx += 1
        fixtures = actual_gws[0:idx]
        points = []
        for fixture in fixtures:
            points.append(player["fixture_history"][fixture]["points"])
        last_game = points[-1]
        last_3_mean = mean(points[-3:])
        last_6_mean = mean(points[-6:])
        forecast = 0
        for fixture in range(0, len(oppositions[idx - 1])):
            forecast += (
            mean([last_game, last_3_mean, last_6_mean]) * team_map[oppositions[idx - 1][fixture]] * home_away_map[
                home_away[idx - 1][fixture]])
        forecasts[forecast_gws[idx - 1]] = forecast
    return forecasts


def exponential_smoothing(actual_gws, forecast_gws, smoothing_factor, player, oppositions, team_map, home_away,
                          home_away_map):
    forecasts = {}
    for idx, key in enumerate(actual_gws):
        forecast = 0
        for fixture in range(0, len(oppositions[idx])):
            if idx == 0:
                nforecast = player["fixture_history"][key]["points"] * team_map[oppositions[idx][fixture]] * \
                            home_away_map[home_away[idx][fixture]]
            else:
                nforecast = forecasts[forecast_gws[idx - 1]] + (smoothing_factor * (
                player['fixture_history'][forecast_gws[idx - 1]]['points'] - forecasts[forecast_gws[idx - 1]]))
                nforecast *= (team_map[oppositions[idx][fixture]] * home_away_map[home_away[idx][fixture]])
            forecast += nforecast
        forecasts[forecast_gws[idx]] = forecast
    if player["id"] == 393:
        print forecasts
    return forecasts


def get_maps(players):
    team_map = {}
    home_away_map = {
        "H": 0,
        "A": 0
    }

    for player in players:
        fh = player["fixture_history"]
        for fixture in fh:
            if fh[fixture]["minutes"] > 0:
                continue

            opponent = fh[fixture]["opponent_team"]
            if opponent not in team_map:
                team_map[opponent] = 0
            team_map[opponent] += fh[fixture]["total_points"]

            home_away = "H" if fh[fixture]["was_home"] else "A"
            home_away_map[home_away] += fh[fixture]["total_points"]

    mean_points = mean(team_map.values())
    for team in team_map:
        team_map[team] /= mean_points
    # team_map["-"] = 1.0

    mean_points_ha = mean(home_away_map.values())
    for value in home_away_map:
        home_away_map[value] /= mean_points_ha
    # home_away_map[""] = 1.0

    return {
        "teams": team_map,
        "home_away": home_away_map
    }
