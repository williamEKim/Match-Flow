import pandas as pd
import statsmodels.api as sm

# Load your actual data from a CSV file
df = pd.read_csv('tennis_data.csv')

# Select only the relevant columns for the analysis
selected_columns = ['A%', 'DF%', '1stIn', '1st%', '2nd%', 'Win%','Rank']
df = df[selected_columns]

# Drop rows with missing values
df = df.dropna()

# Create the modified terms in the equation
df['first_term'] = (df['1stIn'] - df['A%']) * (2 * df['1st%'] - 1)
df['second_term'] = (1 - df['1stIn'] - df['DF%']) * (2 * df['2nd%'] - 1)

# Add a constant term for the intercept in the regression model
X = sm.add_constant(df[['A%', 'DF%', 'first_term', 'second_term']])

# Dependent variable (target)
y = 2 * df['Win%'] - 1  # Adjust the dependent variable according to the new equation

# Fit the multiple linear regression model
model = sm.OLS(y, X).fit()

# Extract coefficients
coefficients = model.params

# Calculate GP for each player
df['GP'] = coefficients[1] * df['A%'] + coefficients[2] * (df['1stIn'] - df['A%']) * (2 * df['1st%'] - 1) + coefficients[3] * (1 - df['1stIn'] - df['DF%']) * (2 * df['2nd%'] - 1)

# Assign grades based on GP
df['Grade'] = pd.cut(df['GP'], bins=[-float('inf'), df['GP'].quantile(0.3), df['GP'].quantile(0.6), df['GP'].quantile(0.9), float('inf')],
                     labels=['D', 'C', 'B', 'A'], right=False)

# Function to get player's GP and Grade by Rank
def get_player_grade_by_rank(rank):
    player_data = df[df['Rank'] == rank].iloc[0]
    return player_data['GP'], player_data['Grade']

# Example: Get GP and Grade for the user-input rank
try:
    player_rank = int(input("Enter the player's rank: "))
    player_GP, player_grade = get_player_grade_by_rank(player_rank)
    print(f"\nPlayer with Rank {player_rank}: GP = {player_GP}, Grade = {player_grade}")
except ValueError:
    print("Invalid input. Please enter a valid rank (integer).")
