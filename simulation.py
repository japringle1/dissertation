import myconstants
import squad_selection
import substitutions

def run_simulation(forecast_type):
	print "Simulating season so far with forecast type: " + forecast_type

	total_points = 0

	highest = 0

	startGW = 2

	for gw in range(startGW, myconstants.GW_COUNT+1):

		# Get budget for this week
		if (gw == startGW):
			budget = 1000
			highest = budget
		else:
			squad = list(myconstants.SQUADS_COLLECTION.find({"$and" : [{ "gw" : gw-1 }, {"forecast_type" : forecast_type}]}, {"_id" : 0, "gw" : 1, "next_week_cost" : 1}))
			if (squad[0]["next_week_cost"] > highest):
				highest = squad[0]["next_week_cost"]
				budget = highest
			else:
				budget = highest

		print "GW: " + str(gw) + " Budget: " + str(budget/10.0)

		# Get squads
		results = squad_selection.get_combinations(myconstants.FORECASTS_COLLECTION, gw, budget, forecast_type)

		ids = []
		for squad in results:
			holder = []
			team = squad["first_team"] + squad["subs"]
			for player in team:
				holder.append(player[0])
			ids.append(holder)

		actuals = {}
		actual_points = 0
		next_week_cost = 0

		players = myconstants.PLAYER_COLLECTION.find({ "$and": [{"id": {'$in': ids[-1]}}, {"fixture_history.%i.points" % gw : {'$exists': True}}]}, {"_id": 0, "id": 1, "web_name": 1, "fixture_history": 1})

		for p in players:
			actual_gws = p["fixture_history"].keys()
			next_gw = actual_gws.index(str(gw)) + 1
			
			if next_gw in actual_gws:
				next_week_cost += p["fixture_history"][str(actual_gws[next_gw])]["value"]
			else:
				next_week_cost += p["fixture_history"][str(actual_gws[next_gw-1])]["value"]

			points = 0
			# If there's a double gameweek the player scored double points
			if ("fixtures" in p["fixture_history"][str(gw)]):
				points += p["fixture_history"][str(gw)]["points"]
			points += p["fixture_history"][str(gw)]["points"]

			actual_points += int(points)
			actuals[p["id"]] = {"actual_points" : int(points),
								"mins_played" : p["fixture_history"][str(gw)]["mins_played"]
								}

		#Top Team
		top_team = results[-1]

		# Add actual points scored and round forecasts to 0 dp
		for player in top_team["first_team"]:
			player.append(actuals[player[0]]["actual_points"])
			player.append(actuals[player[0]]["mins_played"])

		for player in top_team["subs"]:
			player.append(actuals[player[0]]["actual_points"])
			player.append(actuals[player[0]]["mins_played"])

		# Make any subs
		top_team = substitutions.make_subs(top_team)
		subs_points = 0
		for player in top_team["subs"]:
			subs_points += player[6]

		top_team["subs_points"] = subs_points
		top_team["next_week_cost"] = next_week_cost
		top_team["actual_points"] = (actual_points - subs_points) + top_team["captain"][6]
		top_team["budget"] = budget
		top_team["bank"] = budget - top_team["total_cost"]
		top_team["gw"] = gw
		top_team["forecast_type"] = forecast_type

		# Add points for this week to total points
		total_points += top_team["actual_points"]

		myconstants.SQUADS_COLLECTION.insert(top_team)

		print_team(top_team)

	# Print total points over season!
	print "Total points for season: " + str(total_points)
	print

	# Print team for upcoming week...

	if (myconstants.GW_COUNT+1 < 39):
		print "Getting squad for upcoming gameweek..."
		results = squad_selection.get_combinations(myconstants.FORECASTS_COLLECTION, myconstants.GW_COUNT+1, 1000, forecast_type)
		team = results[-1]
		team["actual_points"] = "N/A"
		print_team(team)

def print_team(team):

	# Print the team you've picked
	print "Formation:"
	print team["formation"]
	print "First team: "
	for player in team["first_team"]:
		print player
	print "Subs: "
	for player in team["subs"]:
		print player
	print "Captain: \n" + str(team["captain"])
	print "Vice Captain: \n" + str(team["vice_captain"])
	print "Total Cost: \n" + str(int(team["total_cost"])/10.0)
	print "Forecasted Points: \n" + str(team["forecasted_points"])
	print "Actual points: \n" + str(team["actual_points"])
	print