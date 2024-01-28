import pandas as pd
from scipy.optimize import minimize
import numpy as np

# Load your tennis dataset
# Replace 'tennis_data.csv' with the actual file path
df = pd.read_csv('tennis_data.csv')

# Rename columns for consistency
df.rename(columns={'Win%': 'Actual Winning Percentage', 'TPW': 'Total Points Won', 'Rank': 'Rank'}, inplace=True)

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

# Initial guess for the exponent 'n'
initial_guess = 2.0

# Perform optimization to find the value of 'n'
result = minimize(objective_function, initial_guess, args=(df,), method='Nelder-Mead')

# Extract the optimal value of 'n'
optimal_n = result.x[0]

# Display the optimal value of 'n'
print(f"The optimal value of 'n' is: {optimal_n:.3f}")

# Function to predict winning percentage based on Pythagorean winning percentage
def predict_winning_percentage(tpw):
    return pythagorean_winning_percentage(tpw, optimal_n)

# Input player ranks
player1_rank = int(input("Enter the rank of Player 1 (1 to 50): "))
player2_rank = int(input("Enter the rank of Player 2 (1 to 50): "))

# Extract Pythagorean Win% for Player 1 and Player 2
player1_pythagorean_win_percentage = predict_winning_percentage(df[df['Rank'] == player1_rank]['Total Points Won'].values[0])
player2_pythagorean_win_percentage = predict_winning_percentage(df[df['Rank'] == player2_rank]['Total Points Won'].values[0])

# Calculate k using Pythagorean Win%
k = player2_pythagorean_win_percentage - player1_pythagorean_win_percentage

# Calculate player1's winning rate against player2 using the logistic function
winning_rate_player1_vs_player2 = logistic_function(-3*k)

# Display Pythagorean Win% for Player 1 and Player 2
print(f"Player {player1_rank}'s Pythagorean Win%: {player1_pythagorean_win_percentage:.2%}")
print(f"Player {player2_rank}'s Pythagorean Win%: {player2_pythagorean_win_percentage:.2%}")

# Display the winning rate of Player 1 against Player 2
print(f"Player {player1_rank}'s winning rate against Player {player2_rank}: {winning_rate_player1_vs_player2:.2%}")
