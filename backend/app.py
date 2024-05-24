from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
import logging

# Initialize the Flask app
app = Flask('__name__')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Global variable to store GeoJSON data
geojson_data = {}

# Function to convert DataFrame to GeoJSON
def df_to_geojson(df):
    features = []
    for _, row in df.iterrows():
        try:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [row['LongStart'], row['LatStart']]
                },
                'properties': {
                    'CruiseIDstr': row['CruiseIDOrig'],
                    'SampleLabel': row['SampleLabel'],
                    'WatchIDStr': row['WatchIDOrig'],
                    'StartTime': row['StartTime'],
                    'Alpha': row['Alpha'],
                    'Distance': row['Distance'],
                    'FlySwim': row['FlySwim'],
                    'Count': row['Count'],
                    'Observer': row['Observer'],
                    'PlatformSpeed': row['PlatformSpeed'],
                    'Windspd': row['WindSpeed']
                }
            }
            features.append(feature)
        except KeyError as e:
            logger.error(f"KeyError: {e}")
            raise
    return {
        'type': 'FeatureCollection',
        'features': features
    }

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the Seabird Survey App API.'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error('No file part in request')
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        logger.error('No selected file uploaded')
        return jsonify({'error': 'No selected file uploaded'}), 400

    try:
        # Read the Excel file
        excel_data = pd.ExcelFile(io.BytesIO(file.read()))
        logger.debug(f"Sheet names in the uploaded file: {excel_data.sheet_names}")

        # Check for required columns in each sheet
        required_columns = {'LongStart', 'LatStart', 'CruiseIDOrig', 'SampleLabel', 'WatchIDOrig', 
                            'StartTime', 'Alpha', 'Distance', 'FlySwim', 'Count', 'Observer', 
                            'PlatformSpeed', 'WindSpeed'}
        
        logger.debug(f"Required columns: {required_columns}")

        sheet_name = None
        for sheet in excel_data.sheet_names:
            df = pd.read_excel(excel_data, sheet_name=sheet)
            logger.debug(f"Columns in sheet '{sheet}': {set(df.columns)}")
            if required_columns.issubset(set(df.columns)):
                sheet_name = sheet
                break

        if sheet_name is None:
            logger.error('No sheet contains the required columns')
            return jsonify({'error': 'No sheet contains the required columns.'}), 400

        df = pd.read_excel(excel_data, sheet_name=sheet_name)
        logger.debug(f"DataFrame loaded from sheet '{sheet_name}'")

        global geojson_data
        geojson_data = df_to_geojson(df)
        logger.debug(f"GeoJSON data prepared: {geojson_data}")

        return jsonify({"message": "File processed successfully", "geojson": geojson_data}), 200
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get-geojson', methods=['GET'])
def get_geojson():
    return jsonify(geojson_data)

if __name__ == '__main__':
    app.run(debug=True)
