from flask import Flask, render_template
import csv

app = Flask(__name__)

def read_csv(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            csv_data_raw = list(csv.DictReader(csv_file))
        return csv_data_raw
    except FileNotFoundError:
        return []

def process_csv_data(csv_data_raw):
    csv_data = []
    for record in csv_data_raw:
        # Check if both 'O/U Win Ratio' and 'ML Win Ratio' have values before adding the record
        if record.get('O/U Win Ratio') and record.get('ML Win Ratio'):
            # Convert values to percentages
            record['O/U Win Ratio'] = "{:.0%}".format(float(record['O/U Win Ratio']))
            record['ML Win Ratio'] = "{:.0%}".format(float(record['ML Win Ratio']))
            csv_data.append(record)
    return csv_data

def process_monte_carlo_csv_data(csv_data_raw):
    csv_data = []
    for record in csv_data_raw:
        # Check if values are not empty before converting
        if record.get('team_1_win_percentage') and record.get('team_2_win_percentage') and record.get('total_adj_points'):
            record['team_1_win_percentage'] = "{:.2%}".format(float(record['team_1_win_percentage']))
            record['team_2_win_percentage'] = "{:.2%}".format(float(record['team_2_win_percentage']))
            record['total_adj_points'] = "{:.2f}".format(float(record['total_adj_points']))
            csv_data.append(record)
    return csv_data

@app.route('/')
def home():
    csv_data = process_csv_data(read_csv('web_app/nfl_performance.csv'))
    csv_data_2 = process_csv_data(read_csv('web_app/nba_performance.csv'))
    csv_data_3 = process_csv_data(read_csv('web_app/nhl_performance.csv'))

    return render_template('home.html', 
                           csv_data=csv_data, 
                           csv_data_2=csv_data_2, 
                           csv_data_3=csv_data_3)

@app.route('/nfl') 
def nfl():
    csv_data = process_monte_carlo_csv_data(read_csv('web_app/nfl_monte_carlo.csv'))
    return render_template('nfl.html', csv_data=csv_data)

@app.route('/nba')
def nba():
    csv_data = process_monte_carlo_csv_data(read_csv('web_app/nba_monte_carlo.csv'))
    return render_template('nba.html', csv_data=csv_data)

@app.route('/nhl')
def nhl():
    csv_data = process_monte_carlo_csv_data(read_csv('web_app/nhl_monte_carlo.csv'))
    return render_template('nhl.html', csv_data=csv_data)

if __name__ == '__main__':
    app.run(debug=True)
