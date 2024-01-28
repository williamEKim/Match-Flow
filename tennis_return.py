import pandas as pd
from scipy.optimize import minimize
from fuzzywuzzy import process
import numpy as np
import sys
import json

# Load your tennis dataset
# Replace 'tennis_data.csv' with the actual file path


def get_player_names_list():
    # Load your CSV file into a pandas DataFrame
    df = pd.read_csv('./data/name_rank.csv')  

    df_2 = pd.read_csv('./data/tennis_data.csv')

    # Rename columns for consistency
    df_2.rename(columns={'Win%': 'Actual Winning Percentage', 'TPW': 'Total Points Won', 'Rank': 'Rank'}, inplace=True)
    df_2.rename(columns={'Player': 'Name', 'Rank': 'Rank'}, inplace=True)

    # Create a list to store dictionaries of player names
    player_names_list = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        player_rank = row['Rank']
        player_name = row['Name']
        
        # Check if there are rows in df_2 that match the condition
        if not df_2[df_2['Rank'] == player_rank].empty:
            player_winrate = df_2[df_2['Rank'] == player_rank]['Actual Winning Percentage'].values[0]
            player_names_list.append({ "rank":player_rank, "name": player_name, "win rate": player_winrate })
        else:
            player_names_list.append({ "rank":player_rank, "name": player_name, "win rate": "N/A" })  # Or handle the case when no match is found differently

    return player_names_list



# sending back the json structure
player_list_json = json.dumps(get_player_names_list())
print(player_list_json)
sys.stdout.flush()
