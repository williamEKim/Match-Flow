import pandas as pd
from scipy.optimize import minimize
from fuzzywuzzy import process
import numpy as np
import sys
import json

# Load your tennis dataset
# Replace 'tennis_data.csv' with the actual file path
df = pd.read_csv('./data/tennis_data.csv')

# Rename columns for consistency
df.rename(columns={'Win%': 'Actual Winning Percentage', 'TPW': 'Total Points Won', 'Rank': 'Rank'}, inplace=True)
df.rename(columns={'Player': 'Name', 'Rank': 'Rank'}, inplace=True)

# Define the Pythagorean winning percentage function with TPW
def pythagorean_winning_percentage(tpw, n):
    return tpw**n / (tpw**n + (1 - tpw)**n)

# Define the logistic function to calculate player1's winning rate against player2
def logistic_function(k):
    return 1 / (1 + np.exp(-k))

# Define the objective function to minimize the sum of squared differences
def objective_function(n, df):
    predicted_winning_percentage = pythagorean_winning_percentage(df['Total Points Won'], n)
    observed_winning_percentage = df['Actual Winning Percentage']
    return ((predicted_winning_percentage - observed_winning_percentage)**2).sum()

def get_player_name(rank):
    # Load your CSV file into a pandas DataFrame
    df = pd.read_csv('./data/name_rank.csv')  # Replace 'your_file.csv' with the actual file path

    # Check if the input is a valid rank
    if rank not in df['Rank'].values:
        return "Rank not found"

    # Get the name of the player with the given rank
    player_name = df[df['Rank'] == rank]['Name'].values[0]
    return player_name

def get_player_rank(name):
    # Load your CSV file into a pandas DataFrame
    df = pd.read_csv('./data/name_rank.csv')  # Replace 'your_file.csv' with the actual file path

    # Check if the input is a valid rank
    player_names = df['Name'].tolist()
    closest_match = process.extractOne(name, player_names)
    
    # Get the name of the player with the closest match
    closest_name = closest_match[0]
    closest_score = closest_match[1]

    # Get the rank of the closest match
    player_rank = df[df['Name'] == closest_name]['Rank'].values[0]
    
    if closest_score < 90:  # Adjust the threshold as needed
        return "No close match found"
    
    return player_rank

# Initial guess for the exponent 'n'
initial_guess = 2.0

# Perform optimization to find the value of 'n'
result = minimize(objective_function, initial_guess, args=(df,), method='Nelder-Mead')

# Extract the optimal value of 'n'
optimal_n = result.x[0]

# Display the optimal value of 'n'
# print(f"The optimal value of 'n' is: {optimal_n:.3f}")

# Function to predict winning percentage based on Pythagorean winning percentage
def predict_winning_percentage(tpw):
    return pythagorean_winning_percentage(tpw, optimal_n)


player1_rank = player2_rank = int(0)
player1_name = player2_name = ""

if sys.argv[1] == "rank":
    # Input player ranks
    player1_rank = int(sys.argv[2])
    player2_rank = int(sys.argv[3])

    player1_name = get_player_name(player1_rank)
    player2_name = get_player_name(player2_rank)

elif sys.argv[1] == "name":
    player1_name = sys.argv[2]
    player2_name = sys.argv[3]

    player1_rank = int(get_player_rank(player1_name))
    player2_rank = int(get_player_rank(player2_name))

    player1_name = get_player_name(player1_rank)
    player2_name = get_player_name(player2_rank)

# Extract Pythagorean Win% for Player 1 and Player 2
player1_pythagorean_win_percentage = predict_winning_percentage(df[df['Rank'] == player1_rank]['Total Points Won'].values[0])
player2_pythagorean_win_percentage = predict_winning_percentage(df[df['Rank'] == player2_rank]['Total Points Won'].values[0])


# Calculate k using Pythagorean Win%
k = player2_pythagorean_win_percentage - player1_pythagorean_win_percentage

# Calculate player1's winning rate against player2 using the logistic function
winning_rate_player1_vs_player2 = logistic_function(-3*k)

# Display Pythagorean Win% for Player 1 and Player 2
# print(f"Player {player1_rank}'s Pythagorean Win%: {player1_pythagorean_win_percentage:.2%}")
# print(f"Player {player2_rank}'s Pythagorean Win%: {player2_pythagorean_win_percentage:.2%}")

# Display the winning rate of Player 1 against Player 2
# print(f"Player {player1_rank}'s winning rate against Player {player2_rank}: {winning_rate_player1_vs_player2:.2%}")


# sending back the json structure
winrate = [{"player1":player1_name, "player2":player2_name, "player1_vs_player2_winrate":f"{winning_rate_player1_vs_player2:.2%}"}]
winrate_json = json.dumps(winrate)
print(winrate_json)
sys.stdout.flush()
