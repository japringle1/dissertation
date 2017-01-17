import myconstants
from copy import deepcopy
import itertools

def get_combinations(collection, gameweek_no, budget, forecast_type):
	points_limits = get_points_limits(collection, gameweek_no, forecast_type)

	combinations = []
	previous_fetched = {}
	previous_candidates = []

	while not combinations:
		
		fetched_players = fetch_players(collection, gameweek_no, forecast_type, points_limits)

		if not fetched_players == previous_fetched:
			combinations = generate_combinations(fetched_players, budget)
			previous_fetched = fetched_players
		
		counts = {}
		for position, players in fetched_players.iteritems():
			counts[position] = len(fetched_players[position])

		if not combinations:
			positions = sorted(counts, key=counts.get)
			pos_to_reduce = positions[0]
			if (pos_to_reduce == "GOALKEEPERS") & (counts["GOALKEEPERS"] > 4):
				pos_to_reduce = positions[1]
			points_limits[pos_to_reduce] -= 0.50

	analyse_combinations(combinations, gameweek_no)

	combinations.sort(key=lambda c : (c["forecasted_points"], -c["total_cost"]))

	return combinations

def get_points_limits(collection, gameweek_no, forecast_type):
	points_limits = {}

	for key, value in myconstants.ELEMENT_TYPES.iteritems():
		top_player = list(collection.find({ "$and" : [{"element_type_id" : value["TYPE_ID"]} , {"fixture_history" : {"$exists" : True}}]}, {"_id" : 0, "id" : 1, "fixture_history" : 1, "web_name" : 1} ).sort([("fixture_history.%i.%s" % (gameweek_no, forecast_type) , -1)]).limit(1))
		points_limits[key] = top_player[0]["fixture_history"][str(gameweek_no)][forecast_type]

	return points_limits

def fetch_players(collection, gameweek_no, forecast_type, points_limits):
	all_players = {}
	points_limits = deepcopy(points_limits)

	for key, value in myconstants.ELEMENT_TYPES.iteritems():
		point_limit = points_limits[key]

		enough_players = False

		while not enough_players:
			all_players[key] = list(collection.find({ "$and" : [ {"element_type_id" : value['TYPE_ID']}, {"fixture_history.%i.opposition" % (gameweek_no) : {'$ne':'-'}},  {"fixture_history.%i.%s" % (gameweek_no, forecast_type) : {'$gte' : point_limit}}, {"fixture_history.%i.%s" % (gameweek_no, forecast_type) : {'$exists' : True}}, {"fixture_history.%i.net_transfers" % gameweek_no : {"$gte" : 0}} ]}, {"_id" : 0, "id" : 1, "fixture_history.%i.%s" % (gameweek_no, forecast_type) : 1, "fixture_history.%i.value" % gameweek_no : 1, "web_name" : 1, "team_name" : 1, "element_type_id" : 1}))
			if (len(all_players[key]) >= value['NO_REQUIRED']):
				enough_players = True
			else:
				point_limit -= 0.50

	formatted_players = {}

	for key, value in all_players.iteritems():
		holder = []
		for p in value:
			holder.append([p['id'], p['element_type_id'], p['web_name'], p['team_name'], p['fixture_history'][str(gameweek_no)]['value'], p['fixture_history'][str(gameweek_no)][forecast_type]])
		formatted_players[key] = holder

	return formatted_players

def generate_combinations(players, budget):
	combinations = []
	combinations_count = 0
	highest_total_points = 0
	for g in list(itertools.combinations(players["GOALKEEPERS"], 2)):
		for d in list(itertools.combinations(players["DEFENDERS"], 5)):
			for m in list(itertools.combinations(players["MIDFIELDERS"], 5)):
				for f in list(itertools.combinations(players["FORWARDS"], 3)):
					all_players = list([g+d+m+f][0])
					combinations_count += 1
					total_cost = 0
					total_points = 0
					teams = {}
					team_rule = False
					for player in all_players:
						total_cost += player[4]
						total_points += player[5]
						team = player[3]
						if team not in teams:
							teams[team] = 0
						teams[team] += 1
					for value in teams.values():
						if (value > 3):
							team_rule = True

					squad = {}
					if (total_points >= highest_total_points) & (total_cost <= budget) & (team_rule == False):
						highest_total_points = total_points
						squad["players"] = all_players
						squad["total_points"] = total_points
						squad["total_cost"] = total_cost
						combinations.append(squad)
	return combinations

def analyse_combinations(combinations, gameweek_no):

	for c in combinations:
		first_team = []
		contest = []
		subs = []

		# Compare goalkeepers
		goalkeepers = sorted(c["players"][:2], key=lambda p : -p[5])
		first_team.append(goalkeepers[0])
		subs.append(goalkeepers[1])

		# Compare defenders
		defenders = sorted(c["players"][2:7], key=lambda p : -p[5])
		[first_team.append(defender) for defender in defenders[:3]]
		[contest.append(defender) for defender in defenders[3:]]

		# Compare midfielders
		midfielders = sorted(c["players"][7:12], key=lambda p : -p[5])
		[first_team.append(midfielder) for midfielder in midfielders[:2]]
		[contest.append(midfielder) for midfielder in midfielders[2:]]

		# Compare forwards
		forwards = sorted(c["players"][12:], key=lambda p : -p[5])
		first_team.append(forwards[0])
		[contest.append(forward) for forward in forwards[1:]]

		# Compare players competing for first team
		contest.sort(key=lambda p : -p[5])
		[first_team.append(contestant) for contestant in contest[:4]]
		[subs.append(contestant) for contestant in contest[4:]]

		# Sort first team by element type
		first_team.sort(key=lambda p : p[1])

		# Captain
		top_scorers = sorted(first_team, key=lambda p : -p[5])[:2]
		c["captain"] = top_scorers[0]
		c["vice_captain"] = top_scorers[1]

		# Get formation
		formation = []
		[formation.append(p[1]) for p in first_team]
		formation = [formation.count(2), formation.count(3), formation.count(4)]

		del c["players"]
		c["first_team"] = first_team
		c["subs"] = subs
		c["formation"] = formation
		forecasted_points = 0.0
		for p in first_team:
			forecasted_points += p[5]
		# Add captain double score
		c["forecasted_points"] = int(round(forecasted_points + c["captain"][5],0))

	return combinations














