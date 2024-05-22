import unittest
import io
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import your Flask app

from flask_testing import TestCase

class TestSeabirdSurveyApp(TestCase):

    def create_app(self):
        # Bind the app to the current context
        app.config['TESTING'] = True
        return app

    def test_home(self):
        # Test the home route
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Seabird Survey App API.', response.data)
        print('Test 2 : API Running')

    def test_upload_file(self):
        # Test the file upload route
        data = {
            'file': (io.BytesIO(b"LatStart,LongStart,CruiseIDstr,SampleLabel,WatchIDStr,StartTime,Alpha,Distance,FlySwim,Count,Observer,PlatformSpeed,Windspd\n45.0103,44.9872,Cruise123,SampleA,Watch1,08:00,Alpha1,100,Flying,5,Observer1,10,15"), 'test.csv')
        }
        response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File processed successfully', response.data)
        print('Test 3: File processed successfully')

    def test_get_geojson(self):
        # Test the get-geojson route
        data = {
            'file': (io.BytesIO(b"LatStart,LongStart,CruiseIDstr,SampleLabel,WatchIDStr,StartTime,Alpha,Distance,FlySwim,Count,Observer,PlatformSpeed,Windspd\n45.0103,44.9872,Cruise123,SampleA,Watch1,08:00,Alpha1,100,Flying,5,Observer1,10,15"), 'test.csv')
        }
        self.client.post('/upload', content_type='multipart/form-data', data=data)

        # test the get-geojson route
        response = self.client.get('/get-geojson')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FeatureCollection', response.data)
        print('Test 1: get-geojson successfull')

if __name__ == '__main__':
    unittest.main()
