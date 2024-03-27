from flask import Flask, render_template, request
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
app = Flask(__name__)


# Load the medical data from CSV file
data = pd.read_csv('medicine.csv')

# Function to find medicine information based on introduction
def find_medicine(input_word):
    matching_rows = []

    # Define a function to search for the keyword in each row
    def search_in_row(row_index):
        row = data.iloc[row_index]
        if input_word.lower() in row['Uses'].lower():
            matching_rows.append(row[['Medicine Name', 'Uses']])

    # Create a ThreadPoolExecutor with max_workers equal to the number of CPU cores
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the executor for parallel execution
        executor.map(search_in_row, range(len(data)))

    if matching_rows:
            return pd.concat(matching_rows[:1])  # Concatenate and return top 1 matching medicine
    else:
        return "No medicine found for the given keyword."

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None  # Initialize result variable to None
    if request.method == 'POST':
        user_input = request.form['keyword']
        result = find_medicine(user_input)
        if isinstance(result, pd.Series):
            result = result.to_frame().T  # Convert Series to DataFrame with single row

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
