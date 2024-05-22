from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io

# Init the flask app, Start a server file for my app
app = Flask('__name__')

# Enable CORS
CORS(app)

# Define our Global Variable to store all our File Data in an empty dictionary
geojson_data = {}

# Function that will convert DataFrame to our GEOjson
def df_to_geojson(df):
    print(request.files) # debug  
    features = []
    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',  
                'coordinates': [row['LongStart'], row['LatStart']]
            },
            'properties': {
                'CruiseIDstr': row['CruiseIDstr'],
                'SampleLabel': row['SampleLabel'],
                'WatchIDStr': row['WatchIDStr'],
                'StartTime': row['StartTime'],
                'Alpha': row['Alpha'],
                'Distance': row['Distance'],
                'FlySwim': row['FlySwim'],
                'Count': row['Count'],
                'Observer': row['Observer'],
                'PlatformSpeed': row['PlatformSpeed'],
                'Windspd': row['Windspd']
            }
        }
        features.append(feature)

    return {
        'type': 'FeatureCollection',
        'features': features
    }

# Define our endpoints
@app.route('/', methods=['GET'])
def home():
  return 'Welcome to the Seabird Survey App API.'

# Set the route for uploading files
# Define a function that will hold all the logic for our file analysis
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file is in request
    if 'file' not in request.files: 
        # return json error
        return jsonify({'error': 'No file part'}), 400
    
    # Get the file requested
    file = request.files['file']
    # Check the file has a valid name
    if file.filename == '':
        # return error
        return jsonify({'error': 'No selected file uploaded'}), 400

    try:
        # Read the file into a pandas DataFrame
        df = pd.read_csv(io.StringIO(file.stream.read().decode('UTF8')), header=0)
        
        # Convert our DataFrame into geoJSON
        global geojson_data
        geojson_data = df_to_geojson(df)

        # Return the geoJSON data
        return jsonify({"message": "File processed successfully", "geojson": geojson_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define our geojson endpoint that has our stored data
@app.route('/get-geojson', methods=['GET'])
def get_geojson():
    return jsonify(geojson_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
