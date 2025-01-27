import os
from pymongo import MongoClient

# MongoDB connection string (replace with your own secure credentials)
client = MongoClient(os.environ.get("MONGO_URI"))

# Specify the database name
db = client["3Wins_db"]

# User collection
usersCol = db["users"]

# Goals collections (one for each win)
spiritualGoalsCol = db["spiritual_goals"]
mentalGoalsCol = db["mental_goals"]
physicalGoalsCol = db["physical_goals"]

# Daily completions (optional) to track which goals were done each day
completionsCol = db["completions"]
