import unittest
from unittest import mock
from ..clients.hawes import Hawes
from ..clients.hounslow import Hounslow
from ..clients.barnsley import Barnsley
import pandas as pd
from pandas.util.testing import assert_frame_equal

class TestHawesClientWithMock(unittest.TestCase):
    
    hawes_mock_api_response = pd.DataFrame([
        {"start": 1592172000, "end": 1592172900, "power": 731},
        {"start": 1592172900, "end": 1592173800, "power": 779},
        {"start": 1592173800, "end": 1592174700, "power": 664},
    ])
    

    def _do_get(*args, **kwargs):
        
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
            
        return MockResponse([
        {"start": 1592172000, "end": 1592172900, "power": 731},
        {"start": 1592172900, "end": 1592173800, "power": 779},
        {"start": 1592173800, "end": 1592174700, "power": 664},
        ], 200)
    
    @mock.patch('requests.get', side_effect=_do_get)    
    def test_call(self, mock_get):
        hawesClient = Hawes("16-06-2021", "17-06-2021")
        response = hawesClient.call()
        assert_frame_equal(response, self.hawes_mock_api_response)
        
class TestBarnsleyClientWithMock(unittest.TestCase):  
    
    barnsley_mock_api_response = pd.DataFrame([
        {"start": 1592172000, "end": 1592172900, "power": 557},
        {"start": 1592172900, "end": 1592173800, "power": 672},
        {"start": 1592173800, "end": 1592174700, "power": 502},
    ])
    
    def _do_get(*args, **kwargs):
        
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
            
        return MockResponse([
        {"start_time": 1592172000, "end_time": 1592172900, "value": 557},
        {"start_time": 1592172900, "end_time": 1592173800, "value": 672},
        {"start_time": 1592173800, "end_time": 1592174700, "value": 502},
        ], 200)
    
    @mock.patch('requests.get', side_effect=_do_get)    
    def test_call(self, mock_get):
        barnsleyClient = Barnsley("16-06-2021", "17-06-2021")
        response = barnsleyClient.call()
        print (response)
        print(self.barnsley_mock_api_response)
        assert_frame_equal(response, self.barnsley_mock_api_response)