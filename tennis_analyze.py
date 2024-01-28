import pandas as pd
import statsmodels.api as sm

# Load the overall tennis data
df = pd.read_csv('tennis_data.csv')

# Select only the relevant columns for the analysis
selected_columns = ['A%', 'DF%', '1stIn', '1st%', '2nd%', 'Win%']
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

# Print the coefficients
print("Coefficients:")
for variable, coefficient in zip(X.columns, coefficients):
    print(f"{variable}: {coefficient}")

# Load player data for Novak Djokovic and Alexander Zverev
player1 = pd.read_csv('novak_djokovic.csv')
player2 = pd.read_csv('Alexander_Zverev.csv')  # Corrected file extension

# Replace missing values with 0
player1.fillna(0, inplace=True)
player2.fillna(0, inplace=True)

# Calculate Win% for each player using the predicted coefficients
def calculate_win_percentage(data, coefficients):
    return (1 + coefficients[1] * data['A%'] - coefficients[2] * data['DF%']
            + coefficients[3] * (data['1stIn'] - data['A%']) * (2 * data['1st%'] - 1)
            + coefficients[4] * (1 - data['1stIn'] - data['DF%']) * (2 * data['2nd%'] - 1)) / 2

# Calculate Win% for each player
player1['Win%'] = calculate_win_percentage(player1, coefficients)
player2['Win%'] = calculate_win_percentage(player2, coefficients)

# Print the calculated Win%
print("\nWin% for Novak Djokovic:")
print(player1['Win%'])

print("\nWin% for Alexander Zverev:")
print(player2['Win%'])
