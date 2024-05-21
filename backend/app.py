from flask import Flask, request , jsonify
from flask_cors import CORS
import pandas as pd 
import io 

# Init the flask app , Start a server file for my app 
app = Flask('__name__')

# Enable CORS 
CORS (app)

# Set the route for uploading files 
@app.route('/upload', methods=['POST'])
# Define a function that wil hold all the logic for our file analysis 
def upload_file():
    # Check if file is in request 
  if 'file ' not in request.files:
        # return json error 
    return jsonify({'error: Error uploading file'}), 400 
   
   # Get the file requested 
  file = request.files['file']
    # Check the file has a valid name 
  if file.filename == '':
      # return errror 
    return jsonify ({'error': 'No selected file uploaded'}), 400 

  try:
        # Read the file into a pandas DataFrame
        df = pd.read_csv(io.StringIO(file.stream.read().decode('UTF8')), header=0)
        
        # Extract LatStart and LongStart columns
        if 'LatStart' in df.columns and 'LongStart' in df.columns:
            # Convert the list of columns into a list of dictionaries 
            # We do this so we can it can easily be sent to our FrontEnd as a JSON Response
            locations = df[['LatStart', 'LongStart']].to_dict(orient='records')
        else:
            return jsonify({"error": "LatStart and LongStart columns not found"}), 400
        
        # Perform some basic analysis
        analysis = {
            "num_records": len(df),
            "columns": list(df.columns),
            "summary_statistics": df.describe().to_dict(),
            "locations": locations
        }
        
        # Return the analysis results as JSON response 
        return jsonify({"message": "File processed successfully", "analysis": analysis}), 200
  except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)





