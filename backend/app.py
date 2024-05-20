from flask import Flask, request , jsonify
from flask_cors import CORS
import pandas as pd 
import io 

# Init the flask app , Start a server file for my app 
app = Flask('__name__')

# Enable CORS 
CORS (app)

# Set the route for uploading files 
@app.route('/upload', method=['POST'])
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
    # Read file in to panda DataFrame 
        df = pd.read_csv(io.StringIO(file.stream.read().decode('UTF8')), header=0)
      
      # Perform PD analysis 
        analysis = {
        # some basic analysis 
        "num_records" : len(df), 
        "columns": list(df.columns),
        "summary_statistics": df.describe().to_dict()
        }
    
        # return success and give 200 OK 
        return jsonify({'message':'File successfully read and analyzed', 'analysis': analysis}), 200 
        # If error return error code 
    except Exception as e:
        return jsonify({'Error': str(e)}), 500 


if __name__ == '__main__':

    # Run the app in debug for dev 
    app.run(debug=True)





