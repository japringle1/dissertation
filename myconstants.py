from pymongo import MongoClient

MONGO_CLIENT = MongoClient("localhost")
DB = MONGO_CLIENT.test_fantasy_manager
PLAYER_COLLECTION = DB.player_collection
FORECASTS_COLLECTION = DB.forecasts_collection
SQUADS_COLLECTION = DB.squads_collection

FIXTURE_KEY_MAP = {
    0 : "date", 
    1 : "gw",
    2 : "opponent_result", 
    3 : "mins_played", 
    4 : "goals",
    5 : "assists",
    6 : "clean_sheet",
    7 : "goals_conceded",
    8 : "own_goals",
    9 : "pens_saved",
    10 : "pens_missed",
    11 : "yellows",
    12 : "reds",
    13 : "saves",
    14 : "bonus",
    15 : "ppi",
    16 : "bps",
    17 : "net_transfers",
    18 : "value",
    19 : "points"
}

TEAM_MAP = {
    "ARS" : 0.86, 
    "AVL" : 1.08, 
    "BUR" : 1.16,
    "CHE" : 0.84, 
    "CRY" : 1.0,
    "EVE" : 0.88,
    "HUL" : 1.10,
    "LEI" : 1.14,
    "LIV" : 0.82,
    "MCI" : 0.8,
    "MUN" : 0.92,
    "NEW" : 0.98,
    "QPR" : 1.18,
    "SOU" : 0.94,
    "STK" : 0.96,
    "SUN" : 1.06,
    "SWA" : 1.02,
    "TOT" : 0.9,
    "WBA" : 1.12,
    "WHU" : 1.04,
    "-" : 1.0
}

HOME_AWAY_MAP = {
    "H" : 1.09,
    "A" : 0.91,
    "" : 1.0
}

DEFAULT_TEAM_MAP = {
    "ARS" : 1.0, 
    "AVL" : 1.0, 
    "BUR" : 1.0,
    "CHE" : 1.0, 
    "CRY" : 1.0,
    "EVE" : 1.0,
    "HUL" : 1.0,
    "LEI" : 1.0,
    "LIV" : 1.0,
    "MCI" : 1.0,
    "MUN" : 1.0,
    "NEW" : 1.0,
    "QPR" : 1.0,
    "SOU" : 1.0,
    "STK" : 1.0,
    "SUN" : 1.0,
    "SWA" : 1.0,
    "TOT" : 1.0,
    "WBA" : 1.0,
    "WHU" : 1.0,
    "-" : 1.0
}

DEFAULT_HOME_AWAY_MAP = {
    "H" : 1.0,
    "A" : 1.0,
    "" : 1.0
}

SMOOTHING_FACTOR = 0.1

ELEMENT_TYPES = {
    "GOALKEEPERS" : {"TYPE_ID" : 1, "NO_REQUIRED" : 2, "MIN_IN_LINEUP" : 1}, 
    "DEFENDERS" :   {"TYPE_ID" : 2, "NO_REQUIRED" : 5, "MIN_IN_LINEUP" : 3}, 
    "MIDFIELDERS" : {"TYPE_ID" : 3, "NO_REQUIRED" : 5, "MIN_IN_LINEUP" : 2},
    "FORWARDS" :    {"TYPE_ID" : 4, "NO_REQUIRED" : 3, "MIN_IN_LINEUP" : 1}
}

VIABLE_FORMATIONS = [[3,4,3],[3,5,2],[4,3,3],[4,4,2],[4,5,1],[5,3,2],[5,4,1],[5,2,3]]

GW_COUNT = 33