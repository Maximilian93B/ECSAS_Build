import unittest
import io
import sys
import os
from flask_testing import TestCase
from app import app  

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  

from flask_testing import TestCase

class TestSeabirdSurveyApp(TestCase):

    # Bind the app to the current context
    def create_app(self):
        app.config['TESTING'] = True
        return app

    # Test the home route
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Seabird Survey App API.', response.data)
        print('API Running : Test 1 Pass ')

    # Test the file upload route
    def test_upload_file(self):
        data = {
            'file': (io.BytesIO(b"LatStart,LongStart,CruiseIDstr,SampleLabel,WatchIDStr,StartTime,Alpha,Distance,FlySwim,Count,Observer,PlatformSpeed,Windspd\n45.0103,44.9872,Cruise123,SampleA,Watch1,08:00,Alpha1,100,Flying,5,Observer1,10,15"), 'test.csv')
        }
        response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File processed successfully', response.data)
        print('File processed successfully: Test 2 Pass')

    # Test the get-geojson route
    def test_get_geojson(self):
        data = {
            'file': (io.BytesIO(b"LatStart,LongStart,CruiseIDstr,SampleLabel,WatchIDStr,StartTime,Alpha,Distance,FlySwim,Count,Observer,PlatformSpeed,Windspd\n45.0103,44.9872,Cruise123,SampleA,Watch1,08:00,Alpha1,100,Flying,5,Observer1,10,15"), 'test.csv')
        }
        self.client.post('/upload', content_type='multipart/form-data', data=data)

        response = self.client.get('/get-geojson')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FeatureCollection', response.data)
        print('get-geojson successfull: Test 3 Pass')

# Run Test 
if __name__ == '__main__':
    unittest.main()
