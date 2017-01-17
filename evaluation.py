import myconstants
import pylab
import matplotlib.pyplot as plt
import numpy

human_average = [44,42,52,36,38,51,49 ,38,46,51,44,39,49,33,47,47,61 ,37,42,52,52,46,38,40,42,34,58,38,58,52,46,38]
global_leader = [64,58,67,51,47,56,104,54,63,77,67,52,74,34,72,66,108,44,40,75,61,80,66,58,68,52,90,23,87,86,55,55]

def print_forecasting_average(collection):
	GWS = range(2, myconstants.GW_COUNT+1)
	LG = []
	WA = []
	ES = []
	for i in GWS:
		squads = collection.find( {"gw" : i} )
		for squad in squads:
			if squad["forecast_type"] == "LG":
				LG.append(abs(squad["forecasted_points"] - squad["actual_points"]))
			elif squad["forecast_type"] == "WA":
				WA.append(abs(squad["forecasted_points"] - squad["actual_points"]))
			elif squad["forecast_type"] == "ES":
				ES.append(abs(squad["forecasted_points"] - squad["actual_points"]))

	LG_average = numpy.mean(LG)
	WA_average = numpy.mean(WA)
	ES_average = numpy.mean(ES)
	averages = (ES_average, WA_average, LG_average)
	ind = numpy.arange(len(averages))
	width = 0.35
	labels = ("Exponential Smoothing", "Weighted Average", "Last Game")

	fig = plt.figure()
	ax = fig.add_subplot(111)
	barlist = ax.bar(ind, averages, width)
	barlist[0].set_color('r')
	barlist[1].set_color('g')
	barlist[2].set_color('b')
	fig.suptitle("Average Difference between Forecasted Points and Actual Points")
	plt.xlabel("Forecasting Model")
	plt.ylabel("Average Difference")
	ax.set_xticks(ind+width)
	xTickNames = ax.set_xticklabels(labels)
	plt.setp(xTickNames, rotation=-15, fontsize=10)
	plt.show()

def print_forecasting_difference(collection):
	GWS = range(2, myconstants.GW_COUNT+1)
	LG = []
	WA = []
	ES = []
	for i in GWS:
		squads = collection.find( {"gw" : i} )
		for squad in squads:
			if squad["forecast_type"] == "LG":
				LG.append(abs(squad["forecasted_points"] - squad["actual_points"]))
			elif squad["forecast_type"] == "WA":
				WA.append(abs(squad["forecasted_points"] - squad["actual_points"]))
			elif squad["forecast_type"] == "ES":
				ES.append(abs(squad["forecasted_points"] - squad["actual_points"]))

	pylab.plot(GWS, LG, label="Last Game")
	pylab.plot(GWS, WA, label="Weighted Average")
	pylab.plot(GWS, ES, label="Exponential Smoothing")
	pylab.legend(loc="upper left")
	pylab.xlabel("Gameweek Number")
	pylab.ylabel("Points Difference")
	pylab.title("Weekly difference between Forecasted Points and Actual Points")
	pylab.show()

def print_forecasting_actual_comparison(collection):
	GWS = range(2, myconstants.GW_COUNT+1)
	LG_forecast = []
	LG_actual = []
	WA_forecast = []
	WA_actual = []
	ES_forecast = []
	ES_actual = []
	for i in GWS:
		squads = collection.find( {"gw" : i} )
		for squad in squads:
			if squad["forecast_type"] == "LG":
				LG_forecast.append(squad["forecasted_points"])
				LG_actual.append(squad["actual_points"])
			elif squad["forecast_type"] == "WA":
				WA_forecast.append(squad["forecasted_points"])
				WA_actual.append(squad["actual_points"])
			elif squad["forecast_type"] == "ES":
				ES_forecast.append(squad["forecasted_points"])
				ES_actual.append(squad["actual_points"])

	pylab.subplot(311)
	pylab.plot(GWS, LG_forecast, label="Forecasted")
	pylab.plot(GWS, LG_actual, label="Actual")
	pylab.legend(loc="upper left")
	pylab.title("Last Game Forecasted & Actual Points", fontsize=10)
	pylab.ylabel("Points")
	pylab.subplot(312)
	pylab.plot(GWS, WA_forecast)
	pylab.plot(GWS, WA_actual)
	pylab.title("Weighted Average Forecasted & Actual Points", fontsize=10)
	pylab.ylabel("Points")
	pylab.subplot(313)
	pylab.plot(GWS, ES_forecast)
	pylab.plot(GWS, ES_actual)
	pylab.title("Exponential Smoothing Forecasted & Actual Points", fontsize=10)
	pylab.ylabel("Points")
	pylab.xlabel("Gameweek Number")
	pylab.show()

def weekly_average_bar(collection):
	GWS = range(2, myconstants.GW_COUNT+1)
	WA = []
	ES = []
	for i in GWS:
		squads = collection.find( {"gw" : i})
		for squad in squads:
			if squad["forecast_type"] == "WA":
				WA.append(squad["actual_points"])
			elif squad["forecast_type"] == "ES":
				ES.append(squad["actual_points"])

	WA_average = numpy.mean(WA)
	ES_average = numpy.mean(ES)
	HA_average = numpy.mean(human_average)
	GL_average = numpy.mean(global_leader)
	averages = (GL_average, ES_average, WA_average, HA_average)
	ind = numpy.arange(len(averages))
	width = 0.35
	labels = ("Global Leader", "Exponential Smoothing", "Weighted Average", "Human Average")

	fig = plt.figure()
	ax = fig.add_subplot(111)
	barlist = ax.bar(ind, averages, width)
	barlist[0].set_color('b')
	barlist[1].set_color('r')
	barlist[2].set_color('g')
	barlist[3].set_color('y')
	fig.suptitle("Average Points per Gameweek without Fixture Difficulty")
	plt.xlabel("Forecasting Model")
	plt.ylabel("Average Points")
	ax.set_xticks(ind+width)
	xTickNames = ax.set_xticklabels(labels)
	plt.setp(xTickNames, rotation=-15, fontsize=10)
	plt.show()

def weekly_ranking_bar(collection):
	GWS = range(2, myconstants.GW_COUNT+1)
	WA = []
	ES = []
	for i in GWS:
		squads = collection.find( {"gw" : i})
		for squad in squads:
			if squad["forecast_type"] == "WA":
				WA.append(squad["actual_points"])
			elif squad["forecast_type"] == "ES":
				ES.append(squad["actual_points"])

	rankings = {"WA" : [0,0,0,0],
				"ES" : [0,0,0,0],
				"HA" : [0,0,0,0],
				"GL" : [0,0,0,0]
				}
	for i in range(0,len(GWS)):
		contest = []
		contest.append(["WA", WA[i]])
		contest.append(["ES", ES[i]])
		contest.append(["HA", human_average[i]])
		contest.append(["GL", global_leader[i]])
		contest.sort(key=lambda x : x[1])
		rankings[contest[3][0]][0] += 1
		rankings[contest[2][0]][1] += 1
		rankings[contest[1][0]][2] += 1
		rankings[contest[0][0]][3] += 1
		print contest
	print rankings

	labels = (1,2,3,4)
	ind = numpy.arange(len(labels))
	width = 0.2

	fig = plt.figure()
	ax = fig.add_subplot(111)
	GL_bars = ax.bar(ind, rankings["GL"], width, color='b', label='Global Leader')
	ES_bars = ax.bar(ind+width, rankings["ES"], width, color='r', label='Exponential Smoothing')
	WA_bars = ax.bar(ind+width+width, rankings["WA"], width, color='g', label='Weighted Average')
	HA_bars = ax.bar(ind+width+width+width, rankings["HA"], width, color='y', label='Human Average')
	fig.suptitle("Ranking of Players on Weekly Performance")
	plt.xlabel("Ranking")
	plt.ylabel("Frequency")
	ax.set_xticks(ind+width*2)
	xTickNames = ax.set_xticklabels(labels)

	plt.legend(loc="upper center")
	plt.show()

def cumulative_performance(collection):
	GWS = range(2, myconstants.GW_COUNT+1)
	WA = []
	ES = []
	for i in GWS:
		squads = collection.find( {"gw" : i})
		for squad in squads:
			if squad["forecast_type"] == "WA":
				WA.append(squad["actual_points"])
			elif squad["forecast_type"] == "ES":
				ES.append(squad["actual_points"])

	WA_cumulative = [WA[0]]
	ES_cumulative = [ES[0]]
	HA_cumulative = [human_average[0]]
	GL_cumulative = [global_leader[0]]

	for i in range(1,len(GWS)):
		WA_cumulative.append(WA_cumulative[i-1]+WA[i])
		ES_cumulative.append(ES_cumulative[i-1]+ES[i])
		HA_cumulative.append(HA_cumulative[i-1]+human_average[i])
		GL_cumulative.append(GL_cumulative[i-1]+global_leader[i])

	pylab.plot(GWS, WA_cumulative, label="Weighted Average", color='g')
	pylab.plot(GWS, ES_cumulative, label="Exponential Smoothing", color='r')
	pylab.plot(GWS, HA_cumulative, label="Human Average", color='y')
	pylab.plot(GWS, GL_cumulative, label="Global Leader", color='b')
	pylab.legend(loc="upper left")
	pylab.xlabel("Gameweek Number")
	pylab.ylabel("Cumulative Points")
	pylab.title("Cumulative Performance without Transfer Restrictions")
	pylab.show()

def cumulative_performance_with_restrictions(collection):
	GWS = range(2, myconstants.GW_COUNT+1)
	WA = []
	WA_actual = []
	WA_transfers = []
	WA_reductions = []
	ES = []
	ES_actual = []
	ES_transfers = []
	ES_reductions = []
	for i in GWS:
		squads = collection.find( {"gw" : i})
		for squad in squads:
			if squad["forecast_type"] == "WA":
				if i == 2:
					WA.append(squad["actual_points"])
					WA_actual.append(squad["actual_points"])
				elif i > 2:
					old_squad = list(collection.find( {"gw" : i-1, "forecast_type" : "WA"}))[0]
					old_ids = []
					for p in (old_squad["first_team"]+old_squad["subs"]):
						old_ids.append(p[0])

					ids = []
					for p in (squad["first_team"]+squad["subs"]):
						ids.append(p[0])

					transfers = list(set(ids)-set(old_ids))
					total_transfers = len(transfers)-1
					total_reduction = total_transfers * 4
					final_points = squad["actual_points"]-total_reduction

					WA.append(final_points)
					WA_actual.append(squad["actual_points"])
					WA_transfers.append(total_transfers)
					WA_reductions.append(total_reduction)
			elif squad["forecast_type"] == "ES":
				if i == 2:
					ES.append(squad["actual_points"])
					ES_actual.append(squad["actual_points"])
				elif i > 2:
					old_squad = list(collection.find( {"gw" : i-1, "forecast_type" : "ES"}))[0]
					old_ids = []
					for p in (old_squad["first_team"]+old_squad["subs"]):
						old_ids.append(p[0])

					ids = []
					for p in (squad["first_team"]+squad["subs"]):
						ids.append(p[0])

					transfers = list(set(ids)-set(old_ids))
					total_transfers = len(transfers)-1
					total_reduction = total_transfers * 4
					final_points = squad["actual_points"]-total_reduction

					ES.append(final_points)
					ES_actual.append(squad["actual_points"])
					ES_transfers.append(total_transfers)
					ES_reductions.append(total_reduction)

	print "GL"
	print "Total: " + str(sum(global_leader))
	print
	print "HA"
	print "Total: " + str(sum(human_average))
	print
	print "WA"
	print "Before: " + str(sum(WA_actual))
	print "Transfers: " + str(sum(WA_transfers))
	print "Avg per week: " + str(numpy.mean(WA_transfers))
	print "Reductions: " + str(sum(WA_reductions))
	print "After: " + str(sum(WA))
	print
	print "ES"
	print "Before: " + str(sum(ES_actual))
	print "Transfers: " + str(sum(ES_transfers))
	print "Avg per week: " + str(numpy.mean(ES_transfers))
	print "Reductions: " + str(sum(ES_reductions))
	print "After: " + str(sum(ES))

	WA_cumulative = [WA[0]]
	ES_cumulative = [ES[0]]
	HA_cumulative = [human_average[0]]
	GL_cumulative = [global_leader[0]]

	for i in range(1,len(GWS)):
		WA_cumulative.append(WA_cumulative[i-1]+WA[i])
		ES_cumulative.append(ES_cumulative[i-1]+ES[i])
		HA_cumulative.append(HA_cumulative[i-1]+human_average[i])
		GL_cumulative.append(GL_cumulative[i-1]+global_leader[i])

	pylab.plot(GWS, WA_cumulative, label="Weighted Average", color='g')
	pylab.plot(GWS, ES_cumulative, label="Exponential Smoothing", color='r')
	pylab.plot(GWS, HA_cumulative, label="Human Average", color='y')
	pylab.plot(GWS, GL_cumulative, label="Global Leader", color='b')
	pylab.legend(loc="upper left")
	pylab.xlabel("Gameweek Number")
	pylab.ylabel("Cumulative Points")
	pylab.title("Cumulative Performance with Transfer Restrictions & without Fixture Difficulty")
	pylab.show()

def print_squad_scores(collection):
	GWS = range(2, myconstants.GW_COUNT+1)
	LG_actual = []
	WA_actual = []
	ES_actual = []
	for i in GWS:
		squads = collection.find( {"gw" : i} )
		for squad in squads:
			if squad["forecast_type"] == "LG":
				LG_actual.append(squad["actual_points"])
			elif squad["forecast_type"] == "WA":
				WA_actual.append(squad["actual_points"])
			elif squad["forecast_type"] == "ES":
				ES_actual.append(squad["actual_points"])

	print "LG"
	print "Total: " + str(sum(LG_actual))
	print "Average: " + str(numpy.mean(LG_actual))
	print
	print "WA"
	print "Total: " + str(sum(WA_actual))
	print "Average: " + str(numpy.mean(WA_actual))
	print
	print "ES"
	for score in ES_actual:
		print score
	print "Total: " + str(sum(ES_actual))
	print "Average: " + str(numpy.mean(ES_actual))





