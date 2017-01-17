import myconstants
from copy import deepcopy

def make_subs(squad):
	first_team = deepcopy(squad["first_team"])

	# Players in first team that played 0 mins
	sub_candidates = [player for player in first_team if player[7] == 0]
	candidate_count = len(sub_candidates)

	# Players on bench that played more than 0 mins
	subs = deepcopy(squad["subs"])
	non_viable_subs = [player for player in subs if player[7] == 0]
	viable_subs = [player for player in subs if player[7] > 0]
	viable_subs_count = len(viable_subs)

	# If subs need to be made and can be made
	if (candidate_count > 0) & (viable_subs_count > candidate_count):

		# Remove players from first team that played 0 mins
		remaining_first_team = deepcopy(first_team)
		[remaining_first_team.remove(p) for p in sub_candidates]
		remaining_players_count = len(remaining_first_team)

		# Get formation of remaining first team
		formation = get_formation(remaining_first_team)
		
		# Number of certain element type required to satisfy minimum lineup rules
		requirements = meet_min_requirements(formation)

		# Meet minimum formation requirements
		for r in requirements:
			for n in range(0, r[1]):
				for sub in viable_subs:
					if sub[1] == r[0]:
						remaining_first_team.append(sub)
						viable_subs.remove(sub)

		# If requirements still aren't fulfilled add 0 mins players back
		new_requirements = meet_min_requirements(formation)
		for r in new_requirements:
			for n in range(0, r[1]):
				for sub in sub_candidates:
					if sub[1] == r[0]:
						remaining_first_team.append(sub)
						sub_candidates.remove(sub)

		# Check if goalkeeper exists in first team
		goalkeeper_flag = False
		for p in remaining_first_team:
			if p[1] == 1:
				goalkeeper_flag = True

		# If no keeper in first team, sub the other one in
		if not goalkeeper_flag:
			for sub in viable_subs:
				if sub[1] == 1:
					remaining_first_team.append(sub)
					viable_subs.remove(sub)

		# Get formation of remaining team after min requirements
		formation = get_formation(remaining_first_team)

		# Perform all subs unless they are a keeper
		subs_needed = 11 - len(remaining_first_team)
		
		unused_subs = []
		for sub in viable_subs:
			if not sub[1] == 1:
				remaining_first_team.append(sub)
			else:
				unused_subs.append(sub)

		# Get formation of new team
		formation_after_subs = get_formation(remaining_first_team)

		# If formation isn't viable, pop players until it is
		while formation_after_subs not in myconstants.VIABLE_FORMATIONS:
			unused_subs.append(remaining_first_team.pop())
			formation_after_subs = get_formation(remaining_first_team)

		# Sort new team
		remaining_first_team.sort(key=lambda p : p[1])

		# Final formation
		final_formation = get_formation(remaining_first_team)

		# Final subs 
		final_subs = unused_subs + sub_candidates + non_viable_subs
		final_subs.sort(key=lambda p : p[1])

		# Change squad to contain correct data after subs
		if squad["captain"] in final_subs:
			squad["captain"] = squad["vice_captain"]

		squad["first_team"] = remaining_first_team
		squad["subs"] = final_subs
		squad["formation"] = final_formation

		forecasted_points = 0
		for player in squad["first_team"]:
			forecasted_points += p[5]
		squad["forecasted_points"] = int(round(forecasted_points + squad["captain"][5],0))

	return squad

def get_formation(team):
	formation = []
	[formation.append(p[1]) for p in team]
	return [formation.count(2), formation.count(3), formation.count(4)]

def meet_min_requirements(formation):
	positions = myconstants.ELEMENT_TYPES
	subs_required = []
	if (formation[0] < positions["DEFENDERS"]["MIN_IN_LINEUP"]):
		subs_required.append([positions["DEFENDERS"]["TYPE_ID"], positions["DEFENDERS"]["MIN_IN_LINEUP"] - formation[0]])
	if (formation[1] < positions["MIDFIELDERS"]["MIN_IN_LINEUP"]):
		subs_required.append([positions["MIDFIELDERS"]["TYPE_ID"], positions["MIDFIELDERS"]["MIN_IN_LINEUP"] - formation[1]])
	if (formation[2] < positions["FORWARDS"]["MIN_IN_LINEUP"]):
		subs_required.append([positions["FORWARDS"]["TYPE_ID"], positions["FORWARDS"]["MIN_IN_LINEUP"] - formation[2]])
	return subs_required
	