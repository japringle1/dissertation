import scraper
import myconstants
import forecast
import squad_selection
import simulation
import evaluation

# Scrape data
# players = scraper.scrape_player_data(1)

# Populate database
# myconstants.PLAYER_COLLECTION.remove()
# new_players = scraper.populate_collection(myconstants.PLAYER_COLLECTION, players)

# Run forecasts
# myconstants.FORECASTS_COLLECTION.remove()
# forecast.run_forecasts()

# # Run simulation of season
myconstants.SQUADS_COLLECTION.remove()
simulation.run_simulation()