from flask import Flask, render_template
from main import CF
import pandas as pd

app = Flask(__name__, template_folder='template')

# Load data
columns = ['User_id', 'Movie_id', 'Rating', 'timestamp']
test_data = pd.read_csv('./15/ml-100k/u.data', sep='\t', names=columns, encoding='latin-1')
testing_data = test_data.pivot(index='Movie_id', columns='User_id', values='Rating').values

cf = CF(testing_data)
cf.fit()

@app.route('/')
def index():
    recommended_items = cf.recommend(100)
    return render_template('index.html', recommended_items=recommended_items)

if __name__ == '__main__':
    app.run(debug=True)